"""Rotation utilities for Phase 1 generalized stiffness operators."""

from __future__ import annotations

import numpy as np

from tensyl.core._validation import finite_number, readonly_array
from tensyl.core.constitutive import ABDStiffness
from tensyl.core.typing import FloatArray


def _finite_angle(angle_rad: float) -> float:
    return finite_number(angle_rad, name="angle_rad")


def engineering_strain_transform(angle_rad: float) -> FloatArray:
    """Transform ``[e11, e22, g12]`` into a frame rotated by ``angle_rad``."""

    angle = _finite_angle(angle_rad)
    # This matrix is for engineering shear gamma12, not tensor shear e12.
    # The factors of two are the convention choice that every rotated ABD block
    # depends on.
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    c2 = c * c
    s2 = s * s
    cs = c * s
    transform = np.array(
        [
            [c2, s2, cs],
            [s2, c2, -cs],
            [-2.0 * cs, 2.0 * cs, c2 - s2],
        ],
        dtype=np.float64,
    )
    transform.setflags(write=False)
    return transform


def resultant_transform(angle_rad: float) -> FloatArray:
    """Transform ``[N11, N22, N12]`` into a frame rotated by ``angle_rad``."""

    # Resultants use the energy-conjugate dual of the strain transform so that
    # r.dot(eta) is invariant under a change of local in-plane frame.
    transform = np.linalg.inv(engineering_strain_transform(angle_rad)).T
    transform.setflags(write=False)
    return transform


def transverse_shear_transform(angle_rad: float) -> FloatArray:
    """Transform ``[g13, g23]`` or ``[Q13, Q23]`` into a rotated frame."""

    angle = _finite_angle(angle_rad)
    c = float(np.cos(angle))
    s = float(np.sin(angle))
    transform = np.array([[c, s], [-s, c]], dtype=np.float64)
    transform.setflags(write=False)
    return transform


def generalized_strain_transform(angle_rad: float) -> FloatArray:
    """Return the 8x8 generalized strain transform for ``eta``."""

    membrane = engineering_strain_transform(angle_rad)
    shear = transverse_shear_transform(angle_rad)
    transform = np.zeros((8, 8), dtype=np.float64)
    transform[0:3, 0:3] = membrane
    transform[3:6, 3:6] = membrane
    transform[6:8, 6:8] = shear
    transform.setflags(write=False)
    return transform


def generalized_resultant_transform(angle_rad: float) -> FloatArray:
    """Return the 8x8 generalized resultant transform."""

    in_plane = resultant_transform(angle_rad)
    shear = transverse_shear_transform(angle_rad)
    transform = np.zeros((8, 8), dtype=np.float64)
    transform[0:3, 0:3] = in_plane
    transform[3:6, 3:6] = in_plane
    transform[6:8, 6:8] = shear
    transform.setflags(write=False)
    return transform


def rotate_tangent(tangent: FloatArray, angle_rad: float) -> FloatArray:
    """Rotate an 8x8 stiffness tangent into a rotated local frame."""

    matrix = readonly_array(tangent, shape=(8, 8), name="tangent")
    strain_transform = generalized_strain_transform(angle_rad)
    resultant = generalized_resultant_transform(angle_rad)
    # C maps strain to resultants. Rotate the input strain into the source
    # frame, apply C, then express the resultants in the target frame.
    rotated = resultant @ matrix @ np.linalg.inv(strain_transform)
    rotated = 0.5 * (rotated + rotated.T)
    rotated.setflags(write=False)
    return rotated


def rotate_abd_stiffness(stiffness: ABDStiffness, angle_rad: float) -> ABDStiffness:
    """Rotate an ``ABDStiffness`` into a new local frame."""

    tangent = rotate_tangent(stiffness.C8, angle_rad)
    return ABDStiffness(
        A=tangent[0:3, 0:3],
        B=tangent[0:3, 3:6],
        D=tangent[3:6, 3:6],
        As=tangent[6:8, 6:8],
        frame=stiffness.frame.rotate(angle_rad),
        convention=stiffness.convention,
        areal_mass=stiffness.areal_mass,
        metadata=dict(stiffness.metadata),
    )


__all__ = [
    "engineering_strain_transform",
    "generalized_resultant_transform",
    "generalized_strain_transform",
    "resultant_transform",
    "rotate_abd_stiffness",
    "rotate_tangent",
    "transverse_shear_transform",
]
