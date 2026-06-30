"""Nemeth-style equivalent-plate reference calculations.

The routines here are validation comparators, not a second public Tensyl API.
They encode the member-family energy summation described by Nemeth's
basic-cell method in NASA/TP-2011-216882, Eqs. 30-39 and Appendix E. The code is
kept outside ``src/tensyl`` so the product package does not depend on the
validation laboratory.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from tensyl import ABDStiffness
from tensyl.cells.tangent_plane import BeamMember, CanonicalUnitCell
from tensyl.core.typing import FloatArray
from tensyl.sections.beam import BeamSection

NEMETH_SOURCE = "Nemeth 2011 NASA/TP-2011-216882, Eqs. 30-39 and Appendix E"


def nemeth_reference_stiffness(cell: CanonicalUnitCell) -> ABDStiffness:
    """Return an ABD stiffness from an independent Nemeth-style cell summation."""

    tangent = np.array(cell.skin.C8, dtype=np.float64, copy=True)
    for member in cell.members:
        tangent += _member_reference_contribution(member, cell_area=cell.area)
    tangent = 0.5 * (tangent + tangent.T)
    return ABDStiffness.from_tangent(
        tangent,
        frame=cell.frame,
        convention=cell.convention,
        areal_mass=cell.skin.areal_mass,
        metadata={
            "source": "nemeth_reference_stiffness",
            "source_equations": (NEMETH_SOURCE,),
            "cell": dict(cell.metadata),
        },
        validity=cell.skin.validity,
    )


def nemeth_comparison_payload(cell: CanonicalUnitCell, actual: ABDStiffness) -> dict[str, Any]:
    """Return compact comparison metrics for a Tensyl/Nemeth stiffness pair."""

    reference = nemeth_reference_stiffness(cell)
    delta = np.array(actual.C8 - reference.C8, dtype=np.float64)
    scale = max(float(np.linalg.norm(reference.C8, ord="fro")), 1.0)
    return {
        "schema_version": "tensyl.validation.nemeth-cell-comparison.v1",
        "source_equations": (NEMETH_SOURCE,),
        "cell_source": cell.metadata.get("source", "unknown"),
        "absolute_c8_error": float(np.linalg.norm(delta, ord="fro")),
        "relative_c8_error": float(np.linalg.norm(delta, ord="fro") / scale),
        "max_absolute_entry_error": float(np.max(np.abs(delta))),
    }


def _member_reference_contribution(member: BeamMember, *, cell_area: float) -> FloatArray:
    density = member.multiplicity * member.length / cell_area
    rows = _beam_strain_rows(member.angle_rad, member.eccentricity)
    stiffness = _section_stiffness_scalars(member.section)
    tangent = np.zeros((8, 8), dtype=np.float64)

    tangent += stiffness["EA"] * np.outer(rows["axial"], rows["axial"])
    tangent += stiffness["kGAy"] * np.outer(rows["inplane_shear"], rows["inplane_shear"])
    tangent += stiffness["kGAz"] * np.outer(rows["transverse_shear"], rows["transverse_shear"])
    tangent += stiffness["EIz"] * np.outer(rows["inplane_bending"], rows["inplane_bending"])
    tangent += stiffness["EIy"] * np.outer(
        rows["out_of_plane_bending"],
        rows["out_of_plane_bending"],
    )
    tangent += stiffness["GJ"] * np.outer(rows["torsion"], rows["torsion"])
    tangent += stiffness["EIyz"] * (
        np.outer(rows["inplane_bending"], rows["out_of_plane_bending"])
        + np.outer(rows["out_of_plane_bending"], rows["inplane_bending"])
    )
    return density * tangent


def _section_stiffness_scalars(section: BeamSection) -> dict[str, float]:
    return {
        "EA": section.EA,
        "EIy": section.EIy,
        "EIz": section.EIz,
        "GJ": section.GJ,
        "kGAy": 0.0 if section.kGAy is None else section.kGAy,
        "kGAz": 0.0 if section.kGAz is None else section.kGAz,
        "EIyz": section.EIyz,
    }


def _beam_strain_rows(angle_rad: float, eccentricity: float) -> dict[str, FloatArray]:
    c = float(np.cos(angle_rad))
    s = float(np.sin(angle_rad))
    c2 = c * c
    s2 = s * s
    cs = c * s
    axial = np.array([c2, s2, cs], dtype=np.float64)
    transverse = np.array([s2, c2, -cs], dtype=np.float64)
    engineering_shear = np.array([-2.0 * cs, 2.0 * cs, c2 - s2], dtype=np.float64)
    shear_normal = np.array([c, s], dtype=np.float64)
    z = float(eccentricity)

    rows = {name: np.zeros(8, dtype=np.float64) for name in _ROW_NAMES}
    rows["axial"][0:3] = axial
    rows["axial"][3:6] = z * axial
    rows["inplane_shear"][0:3] = 0.5 * engineering_shear
    rows["inplane_shear"][3:6] = -0.5 * z * engineering_shear
    rows["transverse_shear"][6:8] = shear_normal
    rows["inplane_bending"][3:6] = transverse
    rows["out_of_plane_bending"][3:6] = axial
    rows["torsion"][3:6] = -0.5 * engineering_shear
    return rows


_ROW_NAMES = (
    "axial",
    "inplane_shear",
    "transverse_shear",
    "inplane_bending",
    "out_of_plane_bending",
    "torsion",
)


__all__ = [
    "NEMETH_SOURCE",
    "nemeth_comparison_payload",
    "nemeth_reference_stiffness",
]
