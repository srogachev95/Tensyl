"""Skin-only plate and laminate ABD builders."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

import numpy as np

from tensyl.core._validation import positive_number
from tensyl.core.constitutive import ABDStiffness
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.typing import FloatArray
from tensyl.materials.base import IsotropicMaterial, OrthotropicPlyMaterial

PlyMaterial = IsotropicMaterial | OrthotropicPlyMaterial


def _metadata(mapping: dict[str, Any] | None, *, source: str) -> dict[str, Any]:
    data = {} if mapping is None else dict(mapping)
    data.setdefault("source", source)
    return data


def _isotropic_shear(material: IsotropicMaterial) -> FloatArray:
    shear = np.diag([material.G, material.G]).astype(np.float64)
    shear.setflags(write=False)
    return shear


def _transformed_q(material: PlyMaterial, angle_rad: float) -> FloatArray:
    # Isotropic plies are already invariant under in-plane rotation; avoiding a
    # transform here also avoids accumulating roundoff in symmetric layups.
    if isinstance(material, IsotropicMaterial):
        return material.plane_stress_stiffness()
    return material.transformed_reduced_stiffness(angle_rad)


def _transformed_shear(material: PlyMaterial, angle_rad: float) -> FloatArray:
    if isinstance(material, IsotropicMaterial):
        return _isotropic_shear(material)
    return material.transformed_shear_stiffness(angle_rad)


@dataclass(frozen=True, slots=True)
class Ply:
    """One laminate ply, ordered bottom-to-top in ``laminate_plate``."""

    material: PlyMaterial
    thickness: float
    angle_rad: float = 0.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "thickness", positive_number(self.thickness, name="thickness"))
        angle = float(self.angle_rad)
        if not np.isfinite(angle):
            msg = "angle_rad must be finite."
            raise ValueError(msg)
        object.__setattr__(self, "angle_rad", angle)


def isotropic_plate(
    material: IsotropicMaterial,
    thickness: float,
    *,
    shear_correction: float = 5.0 / 6.0,
    frame: Frame2D = DEFAULT_FRAME,
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
    metadata: dict[str, Any] | None = None,
) -> ABDStiffness:
    """Build a skin-only isotropic plate stiffness about its mid-surface."""

    h = positive_number(thickness, name="thickness")
    kappa = positive_number(shear_correction, name="shear_correction")
    Q = material.plane_stress_stiffness()
    A = Q * h
    B = np.zeros((3, 3), dtype=np.float64)
    D = Q * h**3 / 12.0
    As = _isotropic_shear(material) * (kappa * h)
    areal_mass = None if material.density is None else material.density * h
    return ABDStiffness(
        A=A,
        B=B,
        D=D,
        As=As,
        frame=frame,
        convention=convention,
        areal_mass=areal_mass,
        metadata=_metadata(metadata, source="isotropic_plate"),
    )


def laminate_plate(
    plies: Iterable[Ply],
    *,
    shear_correction: float = 5.0 / 6.0,
    frame: Frame2D = DEFAULT_FRAME,
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
    metadata: dict[str, Any] | None = None,
) -> ABDStiffness:
    """Build a laminate plate stiffness using bottom-to-top ply order."""

    ply_tuple = tuple(plies)
    if not ply_tuple:
        msg = "laminate_plate requires at least one ply."
        raise ValueError(msg)
    kappa = positive_number(shear_correction, name="shear_correction")
    total_thickness = sum(ply.thickness for ply in ply_tuple)
    z_bottom = -0.5 * total_thickness

    # Plies are integrated about the laminate mid-surface. Unsymmetric stacks
    # therefore produce B coupling naturally through the z and z^2 moments.
    A = np.zeros((3, 3), dtype=np.float64)
    B = np.zeros((3, 3), dtype=np.float64)
    D = np.zeros((3, 3), dtype=np.float64)
    As = np.zeros((2, 2), dtype=np.float64)
    mass = 0.0
    has_complete_density = True

    z0 = z_bottom
    for ply in ply_tuple:
        z1 = z0 + ply.thickness
        Qbar = _transformed_q(ply.material, ply.angle_rad)
        shear = _transformed_shear(ply.material, ply.angle_rad)
        # Classical laminate ABD integration: A, B, and D are the zeroth,
        # first, and second through-thickness moments of transformed Q.
        A += Qbar * (z1 - z0)
        B += 0.5 * Qbar * (z1**2 - z0**2)
        D += (1.0 / 3.0) * Qbar * (z1**3 - z0**3)
        As += kappa * shear * (z1 - z0)
        if ply.material.density is None:
            has_complete_density = False
        else:
            # Areal mass is only meaningful when every ply supplied density.
            mass += ply.material.density * ply.thickness
        z0 = z1

    areal_mass = mass if has_complete_density else None
    data = _metadata(metadata, source="laminate_plate")
    data.setdefault("ply_count", len(ply_tuple))
    data.setdefault("total_thickness", total_thickness)
    return ABDStiffness(
        A=A,
        B=B,
        D=D,
        As=As,
        frame=frame,
        convention=convention,
        areal_mass=areal_mass,
        metadata=MappingProxyType(data),
    )


__all__ = ["Ply", "PlyMaterial", "isotropic_plate", "laminate_plate"]
