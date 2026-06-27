"""Constitutive wall-law operators."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol, runtime_checkable

import numpy as np

from tensyl.conventions import DEFAULT_FRAME, DEFAULT_STRAIN_CONVENTION, Frame2D, StrainConvention
from tensyl.typing import FloatArray

_SYMMETRY_TOLERANCE = 1.0e-10


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    matrix = np.array(values, dtype=np.float64, copy=True)
    if matrix.shape != shape:
        msg = f"{name} must have shape {shape}, got {matrix.shape}."
        raise ValueError(msg)
    if not np.all(np.isfinite(matrix)):
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    if not np.allclose(matrix, matrix.T, atol=_SYMMETRY_TOLERANCE, rtol=0.0):
        msg = f"{name} must be symmetric."
        raise ValueError(msg)
    matrix.setflags(write=False)
    return matrix


def _readonly_vector(values: FloatArray, *, name: str) -> FloatArray:
    vector = np.array(values, dtype=np.float64, copy=True)
    if vector.shape != (8,):
        msg = f"{name} must have shape (8,), got {vector.shape}."
        raise ValueError(msg)
    if not np.all(np.isfinite(vector)):
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    vector.setflags(write=False)
    return vector


def _build_tangent(A: FloatArray, B: FloatArray, D: FloatArray, As: FloatArray) -> FloatArray:
    tangent = np.zeros((8, 8), dtype=np.float64)
    tangent[0:3, 0:3] = A
    tangent[0:3, 3:6] = B
    tangent[3:6, 0:3] = B
    tangent[3:6, 3:6] = D
    tangent[6:8, 6:8] = As
    tangent.setflags(write=False)
    return tangent


@runtime_checkable
class ConstitutiveLaw(Protocol):
    """Public mechanics contract for a generalized wall law."""

    frame: Frame2D
    convention: StrainConvention
    metadata: MappingProxyType[str, Any]

    def energy(self, eta: FloatArray) -> float:
        """Return strain energy density for generalized strain ``eta``."""

    def resultants(self, eta: FloatArray) -> FloatArray:
        """Return generalized resultants for generalized strain ``eta``."""

    def tangent(self, eta: FloatArray | None = None) -> FloatArray:
        """Return the constitutive tangent at generalized strain ``eta``."""

    def rotate(self, angle_rad: float) -> ConstitutiveLaw:
        """Return an equivalent law expressed in a rotated local frame."""


@dataclass(frozen=True, slots=True)
class LinearABDWall:
    """Linear ABD wall law with uncoupled transverse shear block."""

    A: FloatArray
    B: FloatArray
    D: FloatArray
    As: FloatArray
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION
    areal_mass: float | None = None
    metadata: dict[str, Any] | MappingProxyType[str, Any] = field(default_factory=dict)
    _c8: FloatArray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        A = _readonly_matrix(self.A, shape=(3, 3), name="A")
        B = _readonly_matrix(self.B, shape=(3, 3), name="B")
        D = _readonly_matrix(self.D, shape=(3, 3), name="D")
        As = _readonly_matrix(self.As, shape=(2, 2), name="As")
        c8 = _build_tangent(A, B, D, As)
        if not np.allclose(c8, c8.T, atol=_SYMMETRY_TOLERANCE, rtol=0.0):
            msg = "assembled wall tangent must be symmetric."
            raise ValueError(msg)
        if self.areal_mass is not None:
            areal_mass = float(self.areal_mass)
            if not np.isfinite(areal_mass) or areal_mass < 0.0:
                msg = "areal_mass must be finite and nonnegative."
                raise ValueError(msg)
            object.__setattr__(self, "areal_mass", areal_mass)

        object.__setattr__(self, "A", A)
        object.__setattr__(self, "B", B)
        object.__setattr__(self, "D", D)
        object.__setattr__(self, "As", As)
        object.__setattr__(self, "_c8", c8)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))

    @property
    def C8(self) -> FloatArray:
        """The assembled 8x8 wall tangent."""

        return self._c8

    def tangent(self, eta: FloatArray | None = None) -> FloatArray:
        """Return the constant wall tangent."""

        if eta is not None:
            _readonly_vector(eta, name="eta")
        return self.C8

    def resultants(self, eta: FloatArray) -> FloatArray:
        """Return generalized resultants ``[N11, N22, N12, M11, M22, M12, Q13, Q23]``."""

        vector = _readonly_vector(eta, name="eta")
        result = self.C8 @ vector
        result.setflags(write=False)
        return result

    def energy(self, eta: FloatArray) -> float:
        """Return ``0.5 * eta @ C8 @ eta``."""

        vector = _readonly_vector(eta, name="eta")
        return 0.5 * float(vector @ self.C8 @ vector)

    def rotate(self, angle_rad: float) -> LinearABDWall:
        """Return this wall law expressed in a frame rotated about ``n``."""

        from tensyl.rotations import rotate_linear_abd_wall

        return rotate_linear_abd_wall(self, angle_rad)


def shift_reference_surface(wall: LinearABDWall, offset: float) -> LinearABDWall:
    """Return ``wall`` expressed about a reference surface shifted by ``offset``.

    ``offset`` is the signed distance from the wall's current reference surface
    to the new reference surface along ``+n``. Curvatures and transverse-shear
    strains are unchanged.
    """

    checked_offset = float(offset)
    if not np.isfinite(checked_offset):
        msg = "offset must be finite."
        raise ValueError(msg)

    transform = np.eye(8, dtype=np.float64)
    transform[0:3, 3:6] = -checked_offset * np.eye(3, dtype=np.float64)
    shifted = transform.T @ wall.C8 @ transform
    shifted = 0.5 * (shifted + shifted.T)
    metadata = dict(wall.metadata)
    metadata.update(
        {
            "reference_surface_shift": checked_offset,
            "source": "shift_reference_surface",
        }
    )
    return LinearABDWall(
        A=shifted[0:3, 0:3],
        B=shifted[0:3, 3:6],
        D=shifted[3:6, 3:6],
        As=shifted[6:8, 6:8],
        frame=wall.frame,
        convention=wall.convention,
        areal_mass=wall.areal_mass,
        metadata=metadata,
    )


def superpose_linear_abd_walls(
    *walls: LinearABDWall,
    metadata: dict[str, Any] | None = None,
) -> LinearABDWall:
    """Return the stiffness superposition of compatible linear wall laws."""

    if not walls:
        msg = "at least one wall is required."
        raise ValueError(msg)
    first = walls[0]
    for wall in walls[1:]:
        if wall.frame != first.frame:
            msg = "all walls must use the same frame."
            raise ValueError(msg)
        if wall.convention != first.convention:
            msg = "all walls must use the same strain convention."
            raise ValueError(msg)

    areal_mass = None
    if all(wall.areal_mass is not None for wall in walls):
        areal_mass = sum(wall.areal_mass for wall in walls if wall.areal_mass is not None)

    combined_metadata = {"source": "superpose_linear_abd_walls", "wall_count": len(walls)}
    if metadata is not None:
        combined_metadata.update(metadata)
    return LinearABDWall(
        A=sum((wall.A for wall in walls), start=np.zeros((3, 3))),
        B=sum((wall.B for wall in walls), start=np.zeros((3, 3))),
        D=sum((wall.D for wall in walls), start=np.zeros((3, 3))),
        As=sum((wall.As for wall in walls), start=np.zeros((2, 2))),
        frame=first.frame,
        convention=first.convention,
        areal_mass=areal_mass,
        metadata=combined_metadata,
    )


__all__ = [
    "ConstitutiveLaw",
    "LinearABDWall",
    "shift_reference_surface",
    "superpose_linear_abd_walls",
]
