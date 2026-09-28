"""Uniform-temperature classical laminate thermal loading."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np

from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.rotations import engineering_strain_transform
from tensyl.core.thermal import ThermalResultants
from tensyl.materials.base import IsotropicMaterial
from tensyl.materials.laminates import Ply, _transformed_q


def laminate_thermal_resultants(
    plies: Iterable[Ply],
    *,
    frame: Frame2D = DEFAULT_FRAME,
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
) -> ThermalResultants:
    """Integrate Qbar alpha through bottom-to-top plies about the midplane.

    Returns N_T and M_T per unit uniform temperature change. Every material
    must supply expansion coefficients; unknown coefficients are refused.
    Temperature gradients and temperature-dependent properties are unsupported.
    """
    layers = tuple(plies)
    if not layers:
        raise ValueError("laminate_thermal_resultants requires at least one ply.")
    z = -sum(p.thickness for p in layers) / 2
    membrane = np.zeros(3)
    bending = np.zeros(3)
    for ply in layers:
        material = ply.material
        if isinstance(material, IsotropicMaterial):
            if material.alpha is None:
                raise ValueError("Every ply requires known alpha for thermal loading.")
            expansion = np.array([material.alpha, material.alpha, 0.0])
        else:
            if material.alpha1 is None or material.alpha2 is None:
                raise ValueError("Every orthotropic ply requires known alpha1 and alpha2.")
            expansion = engineering_strain_transform(-ply.angle_rad) @ np.array(
                [material.alpha1, material.alpha2, 0.0]
            )
        stress = _transformed_q(material, ply.angle_rad) @ expansion
        top = z + ply.thickness
        membrane += stress * ply.thickness
        bending += stress * (top**2 - z**2) / 2
        z = top
    return ThermalResultants(membrane, bending, frame, convention)


__all__ = ["laminate_thermal_resultants"]
