"""Affine thermal member loading smeared over a canonical cell."""

from __future__ import annotations

import numpy as np

from tensyl.cells import CanonicalUnitCell
from tensyl.core.conventions import DEFAULT_STRAIN_CONVENTION
from tensyl.core.thermal import ThermalResultants
from tensyl.homogenizers.tangent_plane import _member_transform


def cell_thermal_resultants(
    cell: CanonicalUnitCell, *, skin: ThermalResultants
) -> ThermalResultants:
    """Add skin loads and density-weighted EA alpha member contributions.

    Skin thermal loads must be explicitly supplied in the cell frame and at
    its reference surface. Every member needs ``section.thermal_expansion``.
    This beam approximation represents uniform axial expansion only; it omits
    intrinsic thermal curvature of heterogeneous sections and local relaxation.
    """
    if cell.convention != DEFAULT_STRAIN_CONVENTION:
        raise ValueError("Thermal cell assembly requires the default strain convention.")
    if not skin.frame.is_close(cell.frame) or skin.convention != cell.convention:
        raise ValueError("Skin thermal frame and convention must match the cell.")
    total = np.array(skin.equivalent_load(1), copy=True)
    for member in cell.members:
        alpha = member.section.thermal_expansion
        if alpha is None:
            raise ValueError(f"Member {member.label!r} requires known thermal_expansion.")
        loads = np.array([member.section.EA * alpha, 0.0, 0.0, 0.0, 0.0])
        total += (
            member.multiplicity * member.length / cell.area * (_member_transform(member).T @ loads)
        )
    return ThermalResultants(total[:3], total[3:6], cell.frame, cell.convention)


__all__ = ["cell_thermal_resultants"]
