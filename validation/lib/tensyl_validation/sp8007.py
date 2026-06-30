"""SP-8007 reconciliation helpers for validation reports.

The formulas in this module are audit comparators, not package oracles. They
encode the SP-8007 Section 4.1.2.6 ring/stringer and isogrid equations as
written, and also expose the isogrid parallel-axis correction discussed in the
validation report. That lets the report separate a printed formula omission from
the remaining model-content differences.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Literal

import numpy as np

from tensyl import (
    ABDStiffness,
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    equilateral_isogrid_cell,
    isotropic_plate,
    orthogrid_cell,
)

CoefficientName = Literal[
    "Ebar_x",
    "Ebar_y",
    "Ebar_xy",
    "Gbar_xy",
    "Cbar_x",
    "Cbar_y",
    "Cbar_xy",
    "Kbar_xy",
    "Dbar_x",
    "Dbar_y",
    "Dbar_xy",
]

COEFFICIENTS: tuple[CoefficientName, ...] = (
    "Ebar_x",
    "Ebar_y",
    "Ebar_xy",
    "Gbar_xy",
    "Cbar_x",
    "Cbar_y",
    "Cbar_xy",
    "Kbar_xy",
    "Dbar_x",
    "Dbar_y",
    "Dbar_xy",
)

BENDING_COEFFICIENTS: tuple[CoefficientName, ...] = ("Dbar_x", "Dbar_y", "Dbar_xy")

SP8007_ORTHOGRID_EQUATIONS = "NASA/SP-8007-2020/REV 2, Eqs. 82-91"
SP8007_ISOGRID_EQUATIONS = "NASA/SP-8007-2020/REV 2, Eqs. 92-98"
SP8007_ISOGRID_CORRECTION = (
    "Eqs. 97-98 corrected with explicit stiffener parallel-axis EA*z^2 terms"
)


@dataclass(frozen=True, slots=True)
class SP8007ComparisonCase:
    """Synthetic case used by the SP-8007 reconciliation report."""

    name: str
    model: Literal["orthogrid", "isogrid"]
    material_E: float = 10.6e6
    material_nu: float = 0.33
    skin_thickness: float = 0.080
    stiffener_area: float = 0.030
    out_of_plane_inertia: float = 1.20e-3
    in_plane_inertia: float = 1.20e-3
    torsion_constant: float = 2.50e-4
    eccentricity: float = 0.32
    stringer_spacing: float = 6.0
    rib_spacing: float = 8.0
    pitch: float = 6.0
    note: str = ""

    def material(self) -> IsotropicMaterial:
        """Return the isotropic material used by this case."""

        return IsotropicMaterial(E=self.material_E, nu=self.material_nu)

    def section(self) -> BeamSection:
        """Return Tensyl's centroidal beam section for this case."""

        material = self.material()
        return BeamSection(
            EA=material.E * self.stiffener_area,
            EIy=material.E * self.out_of_plane_inertia,
            EIz=material.E * self.in_plane_inertia,
            GJ=material.G * self.torsion_constant,
            metadata={"source": "sp8007_reconciliation_case", "case": self.name},
        )

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable description of the case."""

        return {
            "name": self.name,
            "model": self.model,
            "material_E": self.material_E,
            "material_nu": self.material_nu,
            "skin_thickness": self.skin_thickness,
            "stiffener_area": self.stiffener_area,
            "out_of_plane_inertia": self.out_of_plane_inertia,
            "in_plane_inertia": self.in_plane_inertia,
            "torsion_constant": self.torsion_constant,
            "eccentricity": self.eccentricity,
            "stringer_spacing": self.stringer_spacing,
            "rib_spacing": self.rib_spacing,
            "pitch": self.pitch,
            "note": self.note,
        }


def default_reconciliation_cases() -> tuple[SP8007ComparisonCase, ...]:
    """Return public synthetic cases for the committed reconciliation artifact."""

    low_in_plane = 1.20e-6
    return (
        SP8007ComparisonCase(
            name="orthogrid_full_section_eccentric",
            model="orthogrid",
            note=(
                "Orthogrid with in-plane beam bending retained in Tensyl but absent "
                "from SP-8007 Eqs. 89-91 as written."
            ),
        ),
        SP8007ComparisonCase(
            name="orthogrid_suppressed_inplane_bending",
            model="orthogrid",
            in_plane_inertia=low_in_plane,
            note="Orthogrid limit that nearly removes Tensyl's cross-family in-plane bending.",
        ),
        SP8007ComparisonCase(
            name="isogrid_full_section_eccentric",
            model="isogrid",
            note=(
                "Isogrid with full in-plane beam bending and eccentric axial stiffness "
                "retained in Tensyl."
            ),
        ),
        SP8007ComparisonCase(
            name="isogrid_suppressed_inplane_bending_zero_eccentricity",
            model="isogrid",
            in_plane_inertia=low_in_plane,
            eccentricity=0.0,
            note="Isogrid limit where the printed and corrected Eqs. 97-98 coincide.",
        ),
        SP8007ComparisonCase(
            name="isogrid_suppressed_inplane_bending_eccentric",
            model="isogrid",
            in_plane_inertia=low_in_plane,
            note=(
                "Isogrid case isolating the missing eccentric axial-stiffness "
                "terms in SP-8007 Eqs. 97-98."
            ),
        ),
    )


def sp8007_coefficients_from_abd(
    stiffness: ABDStiffness,
    *,
    tolerance: float = 1.0e-9,
) -> dict[CoefficientName, float]:
    """Extract SP-8007 barred coefficients from Tensyl local ABD stiffness."""

    unsupported = {
        "A16": stiffness.A[0, 2],
        "A26": stiffness.A[1, 2],
        "B16": stiffness.B[0, 2],
        "B26": stiffness.B[1, 2],
        "B61": stiffness.B[2, 0],
        "B62": stiffness.B[2, 1],
        "D16": stiffness.D[0, 2],
        "D26": stiffness.D[1, 2],
    }
    nonzero = {name: float(value) for name, value in unsupported.items() if abs(value) > tolerance}
    if nonzero:
        msg = (
            "SP-8007 orthotropic-cylinder coefficients assume axial/circumferential "
            f"orthotropy; unsupported coupling terms are nonzero: {nonzero}"
        )
        raise ValueError(msg)
    return {
        "Ebar_x": float(stiffness.A[0, 0]),
        "Ebar_y": float(stiffness.A[1, 1]),
        "Ebar_xy": float(stiffness.A[0, 1]),
        "Gbar_xy": float(stiffness.A[2, 2]),
        "Dbar_x": float(stiffness.D[0, 0]),
        "Dbar_y": float(stiffness.D[1, 1]),
        "Dbar_xy": float(2.0 * stiffness.D[0, 1] + 4.0 * stiffness.D[2, 2]),
        "Cbar_x": float(stiffness.B[0, 0]),
        "Cbar_y": float(stiffness.B[1, 1]),
        "Cbar_xy": float(stiffness.B[0, 1]),
        "Kbar_xy": float(stiffness.B[2, 2]),
    }


def tensyl_coefficients(case: SP8007ComparisonCase) -> dict[CoefficientName, float]:
    """Compute Tensyl ABD coefficients for a reconciliation case."""

    skin = isotropic_plate(
        case.material(),
        thickness=case.skin_thickness,
        metadata={"validation_case": case.name, "validation_model": case.model},
    )
    section = case.section()
    if case.model == "orthogrid":
        cell = orthogrid_cell(
            skin=skin,
            stringer_section=section,
            rib_section=section,
            stringer_spacing=case.stringer_spacing,
            rib_spacing=case.rib_spacing,
            stringer_eccentricity=case.eccentricity,
            rib_eccentricity=case.eccentricity,
        )
    else:
        cell = equilateral_isogrid_cell(
            skin=skin,
            member_section=section,
            pitch=case.pitch,
            eccentricity=case.eccentricity,
        )
    stiffness = EnergyHomogenizer().compute(cell).stiffness
    return sp8007_coefficients_from_abd(stiffness)


def sp8007_reference_coefficients(case: SP8007ComparisonCase) -> dict[CoefficientName, float]:
    """Compute SP-8007 coefficients as written for a reconciliation case."""

    if case.model == "orthogrid":
        return _sp8007_orthogrid_coefficients(case)
    return _sp8007_isogrid_coefficients(case)


def sp8007_corrected_coefficients(case: SP8007ComparisonCase) -> dict[CoefficientName, float]:
    """Compute SP-8007 coefficients with the isogrid ``EA*z^2`` omission corrected."""

    coefficients = sp8007_reference_coefficients(case)
    if case.model != "isogrid" or case.eccentricity == 0.0:
        return coefficients

    d_correction, dxy_correction = isogrid_parallel_axis_correction(case)
    corrected = dict(coefficients)
    corrected["Dbar_x"] += d_correction
    corrected["Dbar_y"] += d_correction
    corrected["Dbar_xy"] += dxy_correction
    return corrected


def isogrid_parallel_axis_correction(case: SP8007ComparisonCase) -> tuple[float, float]:
    """Return the missing isogrid ``(D_x, D_xy)`` parallel-axis corrections."""

    if case.model != "isogrid":
        msg = "isogrid parallel-axis correction is only defined for isogrid cases."
        raise ValueError(msg)
    material = case.material()
    ea = material.E * case.stiffener_area
    root3 = float(np.sqrt(3.0))
    d_correction = 3.0 * root3 * ea * case.eccentricity**2 / (4.0 * case.pitch)
    dxy_correction = 3.0 * root3 * ea * case.eccentricity**2 / (2.0 * case.pitch)
    return d_correction, dxy_correction


def _skin_terms(case: SP8007ComparisonCase) -> dict[str, float]:
    material = case.material()
    e = material.E
    nu = material.nu
    t = case.skin_thickness
    return {
        "Ebar": e * t / (1.0 - nu**2),
        "Ebar_xy": nu * e * t / (1.0 - nu**2),
        "Gbar_xy": e * t / (2.0 * (1.0 + nu)),
        "Dbar": e * t**3 / (12.0 * (1.0 - nu**2)),
        "Dbar_xy": nu * e * t**3 / (6.0 * (1.0 - nu**2)) + e * t**3 / (6.0 * (1.0 + nu)),
    }


def _sp8007_orthogrid_coefficients(case: SP8007ComparisonCase) -> dict[CoefficientName, float]:
    skin = _skin_terms(case)
    material = case.material()
    ea = material.E * case.stiffener_area
    ei = material.E * case.out_of_plane_inertia
    gj = material.G * case.torsion_constant
    bs = case.stringer_spacing
    br = case.rib_spacing
    z = case.eccentricity
    return {
        "Ebar_x": skin["Ebar"] + ea / bs,
        "Ebar_y": skin["Ebar"] + ea / br,
        "Ebar_xy": skin["Ebar_xy"],
        "Gbar_xy": skin["Gbar_xy"],
        "Cbar_x": z * ea / bs,
        "Cbar_y": z * ea / br,
        "Cbar_xy": 0.0,
        "Kbar_xy": 0.0,
        "Dbar_x": skin["Dbar"] + ei / bs + z**2 * ea / bs,
        "Dbar_y": skin["Dbar"] + ei / br + z**2 * ea / br,
        "Dbar_xy": skin["Dbar_xy"] + gj / bs + gj / br,
    }


def _sp8007_isogrid_coefficients(case: SP8007ComparisonCase) -> dict[CoefficientName, float]:
    skin = _skin_terms(case)
    material = case.material()
    ea = material.E * case.stiffener_area
    ei = material.E * case.out_of_plane_inertia
    gj = material.G * case.torsion_constant
    a = case.pitch
    z = case.eccentricity
    root3 = float(np.sqrt(3.0))
    ext = root3 * ea / (4.0 * a)
    bend = root3 * ei / (4.0 * a)
    twist = root3 * gj / (4.0 * a)
    return {
        "Ebar_x": skin["Ebar"] + 3.0 * ext,
        "Ebar_y": skin["Ebar"] + 3.0 * ext,
        "Ebar_xy": skin["Ebar_xy"] + ext,
        "Gbar_xy": skin["Gbar_xy"] + ext,
        "Cbar_x": z * 3.0 * ext,
        "Cbar_y": z * 3.0 * ext,
        "Cbar_xy": z * ext,
        "Kbar_xy": z * ext,
        "Dbar_x": skin["Dbar"] + 3.0 * bend + twist,
        "Dbar_y": skin["Dbar"] + 3.0 * bend + twist,
        "Dbar_xy": skin["Dbar_xy"] + 6.0 * bend + 2.0 * twist,
    }


def comparison_rows(
    cases: tuple[SP8007ComparisonCase, ...] | None = None,
) -> list[dict[str, Any]]:
    """Return coefficient-by-coefficient Tensyl/SP-8007 comparison rows."""

    rows: list[dict[str, Any]] = []
    for case in default_reconciliation_cases() if cases is None else cases:
        tensyl = tensyl_coefficients(case)
        sp8007_as_written = sp8007_reference_coefficients(case)
        sp8007_corrected = sp8007_corrected_coefficients(case)
        for coefficient in COEFFICIENTS:
            actual = tensyl[coefficient]
            printed = sp8007_as_written[coefficient]
            corrected = sp8007_corrected[coefficient]
            delta_as_written = actual - printed
            delta_corrected = actual - corrected
            printed_scale = max(abs(printed), 1.0)
            corrected_scale = max(abs(corrected), 1.0)
            corrected_relative_delta = delta_corrected / corrected_scale
            rows.append(
                {
                    "case_name": case.name,
                    "model": case.model,
                    "coefficient": coefficient,
                    "tensyl": actual,
                    "sp8007_as_written": printed,
                    "sp8007_corrected": corrected,
                    "delta_as_written": delta_as_written,
                    "relative_delta_as_written": delta_as_written / printed_scale,
                    "abs_relative_delta_as_written": abs(delta_as_written) / printed_scale,
                    "delta_corrected": delta_corrected,
                    "relative_delta_corrected": corrected_relative_delta,
                    "abs_relative_delta_corrected": abs(corrected_relative_delta),
                    "interpretation": _row_interpretation(
                        case=case,
                        coefficient=coefficient,
                        abs_relative_delta_corrected=abs(corrected_relative_delta),
                    ),
                    "case_note": case.note,
                }
            )
    return rows


def _row_interpretation(
    *,
    case: SP8007ComparisonCase,
    coefficient: CoefficientName,
    abs_relative_delta_corrected: float,
) -> str:
    if abs_relative_delta_corrected < 1.0e-9:
        return "agreement"
    if (
        case.model == "orthogrid"
        and coefficient in {"Dbar_x", "Dbar_y"}
        and case.in_plane_inertia > 0.0
    ):
        return "cross_family_inplane_bending"
    if case.model == "isogrid" and coefficient in BENDING_COEFFICIENTS:
        return "retained_member_bending_residual"
    return "model_difference"


def sweep_rows(
    *,
    ratios: tuple[float, ...] = (1.0e-4, 1.0e-3, 1.0e-2, 1.0e-1, 1.0),
) -> list[dict[str, Any]]:
    """Return sweep rows showing sensitivity to retained in-plane beam bending."""

    base_cases = (
        SP8007ComparisonCase(
            name="orthogrid_inplane_bending_sweep",
            model="orthogrid",
            eccentricity=0.32,
        ),
        SP8007ComparisonCase(
            name="isogrid_inplane_bending_sweep_zero_eccentricity",
            model="isogrid",
            eccentricity=0.0,
        ),
    )
    rows: list[dict[str, Any]] = []
    for base in base_cases:
        for ratio in ratios:
            case = replace(
                base,
                in_plane_inertia=base.out_of_plane_inertia * ratio,
                note=f"in_plane_inertia/out_of_plane_inertia = {ratio:g}",
            )
            comparison = comparison_rows((case,))
            max_bending_error = max(
                row["abs_relative_delta_corrected"]
                for row in comparison
                if row["coefficient"] in BENDING_COEFFICIENTS
            )
            rows.append(
                {
                    "case_name": case.name,
                    "model": case.model,
                    "in_plane_inertia_ratio": ratio,
                    "max_bending_abs_relative_delta": max_bending_error,
                }
            )
    return rows


def torsion_sweep_rows(
    *,
    multipliers: tuple[float, ...] = (0.01, 0.1, 1.0, 10.0, 100.0),
) -> list[dict[str, Any]]:
    """Return rows showing sensitivity to the supplied member torsion constant."""

    base_cases = (
        SP8007ComparisonCase(
            name="orthogrid_torsion_sweep",
            model="orthogrid",
            in_plane_inertia=1.20e-6,
        ),
        SP8007ComparisonCase(
            name="isogrid_torsion_sweep",
            model="isogrid",
            in_plane_inertia=1.20e-6,
        ),
    )
    rows: list[dict[str, Any]] = []
    for base in base_cases:
        baseline_case = replace(base, torsion_constant=base.torsion_constant)
        baseline = tensyl_coefficients(baseline_case)
        for multiplier in multipliers:
            case = replace(base, torsion_constant=base.torsion_constant * multiplier)
            tensyl = tensyl_coefficients(case)
            corrected = sp8007_corrected_coefficients(case)
            rows.append(
                {
                    "case_name": case.name,
                    "model": case.model,
                    "torsion_multiplier": multiplier,
                    "torsion_constant": case.torsion_constant,
                    "tensyl_Dbar_xy": tensyl["Dbar_xy"],
                    "sp8007_corrected_Dbar_xy": corrected["Dbar_xy"],
                    "tensyl_Dbar_xy_over_baseline": (
                        tensyl["Dbar_xy"] / baseline["Dbar_xy"]
                        if baseline["Dbar_xy"] != 0.0
                        else 0.0
                    ),
                    "corrected_relative_delta": (
                        (tensyl["Dbar_xy"] - corrected["Dbar_xy"])
                        / max(abs(corrected["Dbar_xy"]), 1.0)
                    ),
                }
            )
    return rows


def summary_payload(
    rows: list[dict[str, Any]],
    sweep: list[dict[str, Any]],
    torsion_sweep: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return a compact report summary from comparison rows."""

    worst_by_case: list[dict[str, Any]] = []
    for case_name in sorted({str(row["case_name"]) for row in rows}):
        case_rows = [row for row in rows if row["case_name"] == case_name]
        worst = max(case_rows, key=lambda row: float(row["abs_relative_delta_corrected"]))
        worst_by_case.append(
            {
                "case_name": case_name,
                "model": worst["model"],
                "worst_coefficient": worst["coefficient"],
                "worst_abs_relative_delta_corrected": worst["abs_relative_delta_corrected"],
                "interpretation": worst["interpretation"],
            }
        )
    return {
        "schema_version": "tensyl.validation.sp8007-reconciliation-summary.v2",
        "title": "SP-8007 reconciliation summary",
        "source_equations": {
            "orthogrid": SP8007_ORTHOGRID_EQUATIONS,
            "isogrid": SP8007_ISOGRID_EQUATIONS,
            "isogrid_correction": SP8007_ISOGRID_CORRECTION,
        },
        "interpretation": [
            "SP-8007 is treated as an independent comparator, not as an oracle.",
            (
                "SP-8007 isogrid Eqs. 97-98 as printed omit explicit stiffener "
                "parallel-axis EA*z^2 bending terms."
            ),
            ("Correcting that omission removes the large eccentric-isogrid bending discrepancy."),
            (
                "The remaining orthogrid bending differences track Tensyl's retained "
                "cross-family in-plane member bending."
            ),
            (
                "The supplied member torsion constant J is a model input, not a "
                "universal section truth."
            ),
        ],
        "worst_by_case": worst_by_case,
        "sweep": sweep,
        "torsion_sweep": torsion_sweep,
    }
