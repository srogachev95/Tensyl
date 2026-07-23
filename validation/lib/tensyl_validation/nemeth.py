"""Independent Nemeth equivalent-plate reference calculations.

The routines here are validation comparators, not a second public Tensyl API.
Callers supply the beam-member attributes transcribed from Nemeth's basic-cell
tables. The comparator evaluates scalar block equations directly and never
reads ``CanonicalUnitCell.members`` or calls Tensyl's production beam transform.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from tensyl import ABDStiffness, BeamSection
from tensyl.core.typing import FloatArray

NEMETH_SOURCE = "Nemeth 2011 NASA/TP-2011-216882, Eqs. 30-39 and Tables 4-9"


@dataclass(frozen=True, slots=True)
class NemethFamily:
    """One independently specified row from a Nemeth basic-cell table."""

    section: BeamSection
    length: float
    cosine: float
    sine: float
    axial_eccentricity: float
    shear_eccentricity: float
    multiplicity: float = 1.0
    label: str = ""


def nemeth_reference_stiffness(
    *,
    skin: ABDStiffness,
    cell_area: float,
    families: tuple[NemethFamily, ...],
    cell_source: str,
) -> ABDStiffness:
    """Return an independent strict-Nemeth ABD stiffness.

    This evaluates the scalar membrane, coupling, bending, and transverse-shear
    blocks implied by Nemeth's Eqs. 30-39. In-plane member bending is omitted,
    consistent with the paper's ``chi_Z = 0`` constraint.
    """

    area = float(cell_area)
    if not np.isfinite(area) or area <= 0.0:
        msg = "cell_area must be finite and positive."
        raise ValueError(msg)
    tangent = np.array(skin.C8, dtype=np.float64, copy=True)
    for family in families:
        tangent += _family_reference_contribution(family, cell_area=area)
    tangent = 0.5 * (tangent + tangent.T)
    return ABDStiffness.from_tangent(
        tangent,
        frame=skin.frame,
        convention=skin.convention,
        areal_mass=skin.areal_mass,
        metadata={
            "source": "nemeth_reference_stiffness",
            "source_equations": (NEMETH_SOURCE,),
            "cell_source": cell_source,
        },
        validity=skin.validity,
    )


def nemeth_comparison_payload(
    *,
    reference: ABDStiffness,
    actual: ABDStiffness,
    cell_source: str,
) -> dict[str, Any]:
    """Return compact comparison metrics for a Tensyl/Nemeth stiffness pair."""

    delta = np.array(actual.C8 - reference.C8, dtype=np.float64)
    scale = max(float(np.linalg.norm(reference.C8, ord="fro")), 1.0)
    return {
        "schema_version": "tensyl.validation.nemeth-cell-comparison.v2",
        "source_equations": (NEMETH_SOURCE,),
        "cell_source": cell_source,
        "absolute_c8_error": float(np.linalg.norm(delta, ord="fro")),
        "relative_c8_error": float(np.linalg.norm(delta, ord="fro") / scale),
        "max_absolute_entry_error": float(np.max(np.abs(delta))),
    }


def _family_reference_contribution(
    family: NemethFamily,
    *,
    cell_area: float,
) -> FloatArray:
    length = float(family.length)
    multiplicity = float(family.multiplicity)
    c = float(family.cosine)
    s = float(family.sine)
    axial_z = float(family.axial_eccentricity)
    shear_z = float(family.shear_eccentricity)
    values = (length, multiplicity, c, s, axial_z, shear_z)
    if not all(np.isfinite(value) for value in values):
        msg = f"Nemeth family {family.label!r} contains a non-finite value."
        raise ValueError(msg)
    if length <= 0.0 or multiplicity <= 0.0:
        msg = f"Nemeth family {family.label!r} length and multiplicity must be positive."
        raise ValueError(msg)
    if not np.isclose(c * c + s * s, 1.0, rtol=1.0e-12, atol=1.0e-12):
        msg = f"Nemeth family {family.label!r} direction cosines must have unit norm."
        raise ValueError(msg)

    section = family.section
    in_plane_shear = 0.0 if section.kGAy is None else section.kGAy
    transverse_shear = 0.0 if section.kGAz is None else section.kGAz
    density = multiplicity * length / cell_area

    # Nemeth Eqs. 30-36 reduce to these scalar direction vectors for the
    # engineering-shear convention used by C8 = [A B 0; B D 0; 0 0 As].
    axial = np.array([c * c, s * s, c * s], dtype=np.float64)
    shear = np.array([-c * s, c * s, 0.5 * (c * c - s * s)], dtype=np.float64)
    transverse = np.array([c, s], dtype=np.float64)

    axial_outer = np.outer(axial, axial)
    shear_outer = np.outer(shear, shear)
    contribution = np.zeros((8, 8), dtype=np.float64)
    contribution[0:3, 0:3] = section.EA * axial_outer + in_plane_shear * shear_outer
    contribution[0:3, 3:6] = (
        section.EA * axial_z * axial_outer + in_plane_shear * shear_z * shear_outer
    )
    contribution[3:6, 0:3] = contribution[0:3, 3:6].T
    contribution[3:6, 3:6] = (section.EA * axial_z * axial_z + section.EIy) * axial_outer + (
        in_plane_shear * shear_z * shear_z + section.GJ
    ) * shear_outer
    contribution[6:8, 6:8] = transverse_shear * np.outer(transverse, transverse)
    return density * contribution


__all__ = [
    "NEMETH_SOURCE",
    "NemethFamily",
    "nemeth_comparison_payload",
    "nemeth_reference_stiffness",
]
