"""Constitutive wall-law operators."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import numpy as np

from tensyl.core._validation import (
    finite_number,
    nonnegative_number,
    readonly_array,
    readonly_mapping,
)
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.typing import (
    FloatArray,
    GeneralizedResultant,
    GeneralizedStrain,
    generalized_resultant,
    generalized_strain,
)

_SYMMETRY_TOLERANCE = 1.0e-10
GeneralizedStrainInput = GeneralizedStrain | FloatArray


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(
        values,
        shape=shape,
        name=name,
        symmetric=True,
        symmetry_tolerance=_SYMMETRY_TOLERANCE,
    )


def _build_tangent(A: FloatArray, B: FloatArray, D: FloatArray, As: FloatArray) -> FloatArray:
    tangent = np.zeros((8, 8), dtype=np.float64)
    tangent[0:3, 0:3] = A
    tangent[0:3, 3:6] = B
    tangent[3:6, 0:3] = B
    tangent[3:6, 3:6] = D
    tangent[6:8, 6:8] = As
    tangent.setflags(write=False)
    return tangent


def _readonly_tangent(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(
        values,
        shape=(8, 8),
        name=name,
        symmetric=True,
        symmetry_tolerance=_SYMMETRY_TOLERANCE,
    )


def _hash_array(values: FloatArray) -> int:
    array = np.ascontiguousarray(values)
    return hash((array.shape, array.dtype.str, array.tobytes()))


def _freeze_for_hash(value: Any) -> Any:
    if isinstance(value, Mapping):
        return tuple(sorted((key, _freeze_for_hash(item)) for key, item in value.items()))
    if isinstance(value, np.ndarray):
        return ("ndarray", value.shape, value.dtype.str, value.tobytes())
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_for_hash(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return tuple(sorted(_freeze_for_hash(item) for item in value))
    try:
        hash(value)
    except TypeError:
        return repr(value)
    return value


@runtime_checkable
class HyperelasticLaw(Protocol):
    """Public mechanics contract for a generalized hyperelastic wall law."""

    frame: Frame2D
    convention: StrainConvention
    metadata: Mapping[str, Any]
    validity: Any

    def energy(self, eta: GeneralizedStrain) -> float:
        """Return strain energy density for generalized strain ``eta``."""

    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant:
        """Return generalized resultants for generalized strain ``eta``."""

    def tangent(self, eta: GeneralizedStrain) -> FloatArray:
        """Return the constitutive tangent at generalized strain ``eta``."""

    def rotate(self, angle_rad: float) -> HyperelasticLaw:
        """Return an equivalent law expressed in a rotated local frame."""


@runtime_checkable
class LinearLaw(HyperelasticLaw, Protocol):
    """Refinement for wall laws whose tangent is independent of strain."""

    @property
    def constant_tangent(self) -> FloatArray:
        """Return the strain-independent tangent."""


ConstitutiveLaw = HyperelasticLaw


@dataclass(frozen=True, slots=True)
class LinearABDWall:
    """Linear equivalent-wall law in ABD plus transverse-shear form.

    Args:
        A: ``3x3`` extensional stiffness block in the active unit system.
        B: ``3x3`` membrane-bending coupling block about the reference surface.
        D: ``3x3`` bending and twisting stiffness block.
        As: ``2x2`` transverse-shear stiffness block.
        frame: Local right-handed wall frame for the matrix components.
        convention: Generalized strain ordering and shear convention.
        areal_mass: Optional mass per unit reference-surface area.
        metadata: Provenance metadata preserved by serialization.
        validity: Optional validity report attached by homogenization.
    """

    A: FloatArray
    B: FloatArray
    D: FloatArray
    As: FloatArray
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION
    areal_mass: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    validity: Any = None
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
            object.__setattr__(
                self,
                "areal_mass",
                nonnegative_number(self.areal_mass, name="areal_mass"),
            )

        object.__setattr__(self, "_c8", c8)
        object.__setattr__(self, "A", c8[0:3, 0:3])
        object.__setattr__(self, "B", c8[0:3, 3:6])
        object.__setattr__(self, "D", c8[3:6, 3:6])
        object.__setattr__(self, "As", c8[6:8, 6:8])
        object.__setattr__(self, "metadata", readonly_mapping(self.metadata))

    @classmethod
    def from_tangent(
        cls,
        tangent: FloatArray,
        *,
        frame: Frame2D = DEFAULT_FRAME,
        convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
        areal_mass: float | None = None,
        metadata: Mapping[str, Any] | None = None,
        validity: Any = None,
    ) -> LinearABDWall:
        """Build a linear wall law from the canonical ``8x8`` tangent.

        The tangent order is ``[N11, N22, N12, M11, M22, M12, Q13, Q23]`` by
        ``[eps11, eps22, gamma12, kappa11, kappa22, kappa12, gamma13,
        gamma23]``.
        """

        c8 = _readonly_tangent(tangent, name="tangent")
        return cls(
            A=c8[0:3, 0:3],
            B=c8[0:3, 3:6],
            D=c8[3:6, 3:6],
            As=c8[6:8, 6:8],
            frame=frame,
            convention=convention,
            areal_mass=areal_mass,
            metadata={} if metadata is None else metadata,
            validity=validity,
        )

    def with_validity(self, validity: Any) -> LinearABDWall:
        """Return an equivalent wall law with attached validity diagnostics."""

        return LinearABDWall.from_tangent(
            self.C8,
            frame=self.frame,
            convention=self.convention,
            areal_mass=self.areal_mass,
            metadata=self.metadata,
            validity=validity,
        )

    def __hash__(self) -> int:
        return hash(
            (
                _hash_array(self.C8),
                self.frame,
                self.convention,
                self.areal_mass,
                _freeze_for_hash(self.metadata),
                _freeze_for_hash(self.validity),
            )
        )

    @property
    def C8(self) -> FloatArray:
        """The canonical 8x8 wall tangent."""

        return self._c8

    @property
    def constant_tangent(self) -> FloatArray:
        """Return the strain-independent wall tangent."""

        return self.C8

    def tangent(self, eta: GeneralizedStrainInput) -> FloatArray:
        """Return the constant wall tangent after validating ``eta``."""

        generalized_strain(eta)
        return self.constant_tangent

    def resultants(self, eta: GeneralizedStrainInput) -> GeneralizedResultant:
        """Return generalized resultants ``[N11, N22, N12, M11, M22, M12, Q13, Q23]``."""

        vector = np.asarray(generalized_strain(eta), dtype=np.float64)
        result = self.C8 @ vector
        result.setflags(write=False)
        return generalized_resultant(result)

    def energy(self, eta: GeneralizedStrainInput) -> float:
        """Return ``0.5 * eta @ C8 @ eta``."""

        vector = np.asarray(generalized_strain(eta), dtype=np.float64)
        return 0.5 * float(vector @ self.C8 @ vector)

    def rotate(self, angle_rad: float) -> LinearABDWall:
        """Return this wall law expressed in a frame rotated about ``n``."""

        from tensyl.core.rotations import rotate_linear_abd_wall

        return rotate_linear_abd_wall(self, angle_rad)


def shift_reference_surface(wall: LinearABDWall, offset: float) -> LinearABDWall:
    """Return ``wall`` expressed about a reference surface shifted by ``offset``.

    ``offset`` is the signed distance from the wall's current reference surface
    to the new reference surface along ``+n``. Curvatures and transverse-shear
    strains are unchanged.
    """

    checked_offset = finite_number(offset, name="offset")

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
    return LinearABDWall.from_tangent(
        shifted,
        frame=wall.frame,
        convention=wall.convention,
        areal_mass=wall.areal_mass,
        metadata=metadata,
        validity=wall.validity,
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
    return LinearABDWall.from_tangent(
        sum((wall.C8 for wall in walls), start=np.zeros((8, 8))),
        frame=first.frame,
        convention=first.convention,
        areal_mass=areal_mass,
        metadata=combined_metadata,
        validity=first.validity if all(wall.validity == first.validity for wall in walls) else None,
    )


__all__ = [
    "ConstitutiveLaw",
    "HyperelasticLaw",
    "LinearABDWall",
    "LinearLaw",
    "shift_reference_surface",
    "superpose_linear_abd_walls",
]
