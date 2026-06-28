"""Constitutive stiffness operators."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import numpy as np

from tensyl.core._validation import (
    finite_number,
    nonnegative_number,
    positive_number,
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
_REDUCTION_WARNING_B = "membrane_bending_coupling_discarded"
_REDUCTION_WARNING_A16_A26 = "off_axis_membrane_coupling_discarded"
_REDUCTION_WARNING_D16_D26 = "off_axis_bending_coupling_discarded"
_REDUCTION_WARNING_VALIDITY_B = "validity_membrane_bending_coupling_exceeds_threshold"


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(
        values,
        shape=shape,
        name=name,
        symmetric=True,
        symmetry_tolerance=_SYMMETRY_TOLERANCE,
    )


def _build_tangent(A: FloatArray, B: FloatArray, D: FloatArray, As: FloatArray) -> FloatArray:
    # C8 is the canonical payload because it keeps membrane, bending, and
    # transverse shear in one operator. The ABD blocks remain public views.
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
    # Metadata can contain nested NumPy arrays from verification or import
    # paths. Hash the semantic payload instead of falling back to object ids.
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
class HyperelasticModel(Protocol):
    """Public mechanics contract for a generalized hyperelastic stiffness model."""

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

    def rotate(self, angle_rad: float) -> HyperelasticModel:
        """Return an equivalent stiffness expressed in a rotated local frame."""


@runtime_checkable
class LinearModel(HyperelasticModel, Protocol):
    """Refinement for stiffness models whose tangent is independent of strain."""

    @property
    def constant_tangent(self) -> FloatArray:
        """Return the strain-independent tangent."""


ConstitutiveModel = HyperelasticModel


@dataclass(frozen=True, slots=True)
class ReducedOrthotropicProperties:
    """Membrane-equivalent orthotropic plane-stress constants.

    Args:
        t_eff: Effective shell thickness used for the membrane reduction.
        E1: Young's modulus in local direction 1.
        E2: Young's modulus in local direction 2.
        G12: In-plane shear modulus.
        nu12: Major Poisson ratio.
        nu21: Minor Poisson ratio.
        warnings: Machine-readable notices for stiffness terms not represented
            by the reduction.
        metadata: Provenance metadata for the reduced values.
    """

    t_eff: float
    E1: float
    E2: float
    G12: float
    nu12: float
    nu21: float
    warnings: tuple[str, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "t_eff", positive_number(self.t_eff, name="t_eff"))
        for name in ("E1", "E2", "G12"):
            object.__setattr__(self, name, positive_number(getattr(self, name), name=name))
        for name in ("nu12", "nu21"):
            object.__setattr__(self, name, finite_number(getattr(self, name), name=name))
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "metadata", readonly_mapping(self.metadata))


@dataclass(frozen=True, slots=True)
class ABDStiffness:
    """Linear ABD stiffness in ABD plus transverse-shear form.

    Args:
        A: ``3x3`` extensional stiffness block in the active unit system.
        B: ``3x3`` membrane-bending coupling block about the reference surface.
        D: ``3x3`` bending and twisting stiffness block.
        As: ``2x2`` transverse-shear stiffness block.
        frame: Local right-handed frame for the matrix components.
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
        # Validate the user-facing blocks first, then rebuild all block
        # attributes as readonly views of one symmetric C8 matrix. That avoids
        # the familiar bug where A/B/D/As and C8 drift apart after construction.
        A = _readonly_matrix(self.A, shape=(3, 3), name="A")
        B = _readonly_matrix(self.B, shape=(3, 3), name="B")
        D = _readonly_matrix(self.D, shape=(3, 3), name="D")
        As = _readonly_matrix(self.As, shape=(2, 2), name="As")
        c8 = _build_tangent(A, B, D, As)
        if not np.allclose(c8, c8.T, atol=_SYMMETRY_TOLERANCE, rtol=0.0):
            msg = "assembled stiffness tangent must be symmetric."
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
    ) -> ABDStiffness:
        """Build a linear ABD stiffness from the canonical ``8x8`` tangent.

        The tangent order is ``[N11, N22, N12, M11, M22, M12, Q13, Q23]`` by
        ``[eps11, eps22, gamma12, kappa11, kappa22, kappa12, gamma13,
        gamma23]``.
        """

        c8 = _readonly_tangent(tangent, name="tangent")
        # Route through the block constructor so all stiffnesses, whether they
        # start as blocks or as C8, receive identical symmetry and readonly
        # treatment.
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

    def with_validity(self, validity: Any) -> ABDStiffness:
        """Return an equivalent stiffness with attached validity diagnostics."""

        return ABDStiffness.from_tangent(
            self.C8,
            frame=self.frame,
            convention=self.convention,
            areal_mass=self.areal_mass,
            metadata=self.metadata,
            validity=validity,
        )

    def __hash__(self) -> int:
        # Frozen dataclasses do not make arrays hashable. Hash the numeric
        # payload explicitly so ABDStiffness can be used in caches and atlases.
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
        """The canonical 8x8 stiffness tangent."""

        return self._c8

    @property
    def constant_tangent(self) -> FloatArray:
        """Return the strain-independent stiffness tangent."""

        return self.C8

    def tangent(self, eta: GeneralizedStrainInput) -> FloatArray:
        """Return the constant stiffness tangent after validating ``eta``."""

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

    def rotate(self, angle_rad: float) -> ABDStiffness:
        """Return this stiffness expressed in a frame rotated about ``n``."""

        from tensyl.core.rotations import rotate_abd_stiffness

        return rotate_abd_stiffness(self, angle_rad)

    def reduced_orthotropic_properties(
        self,
        t_eff: float,
        *,
        tolerance: float = 1.0e-9,
    ) -> ReducedOrthotropicProperties:
        """Return membrane-equivalent orthotropic plane-stress properties.

        ``t_eff`` is the shell thickness used by a downstream model to turn
        membrane stiffness per unit width into material stiffness. The reduction
        is based on ``A / t_eff`` and does not preserve the bending, coupling, or
        transverse-shear blocks.
        """

        checked_t_eff = positive_number(t_eff, name="t_eff")
        checked_tolerance = nonnegative_number(tolerance, name="tolerance")
        q_eff = self.A / checked_t_eff
        try:
            s_eff = np.linalg.inv(q_eff)
        except np.linalg.LinAlgError as exc:
            msg = "A block must be invertible for reduced orthotropic properties."
            raise ValueError(msg) from exc
        values = {
            "E1": 1.0 / s_eff[0, 0],
            "E2": 1.0 / s_eff[1, 1],
            "G12": 1.0 / s_eff[2, 2],
            "nu12": -s_eff[0, 1] / s_eff[0, 0],
            "nu21": -s_eff[0, 1] / s_eff[1, 1],
        }
        warnings = _reduced_orthotropic_warnings(self, tolerance=checked_tolerance)
        metadata = {
            "source": "reduced_orthotropic_properties",
            "reduction": "membrane_compliance_from_A",
            "t_eff": checked_t_eff,
            "tolerance": checked_tolerance,
        }
        return ReducedOrthotropicProperties(
            t_eff=checked_t_eff,
            warnings=warnings,
            metadata=metadata,
            **values,
        )


def _has_nonzero(values: FloatArray, *, tolerance: float) -> bool:
    return bool(np.any(np.abs(values) > tolerance))


def _reduced_orthotropic_warnings(
    stiffness: ABDStiffness,
    *,
    tolerance: float,
) -> tuple[str, ...]:
    warnings: list[str] = []
    if _has_nonzero(stiffness.B, tolerance=tolerance):
        warnings.append(_REDUCTION_WARNING_B)
    if _has_nonzero(stiffness.A[[0, 1], 2], tolerance=tolerance):
        warnings.append(_REDUCTION_WARNING_A16_A26)
    if _has_nonzero(stiffness.D[[0, 1], 2], tolerance=tolerance):
        warnings.append(_REDUCTION_WARNING_D16_D26)
    validity_warnings = tuple(getattr(stiffness.validity, "warnings", ()))
    if "membrane_bending_coupling_exceeds_threshold" in validity_warnings:
        warnings.append(_REDUCTION_WARNING_VALIDITY_B)
    return tuple(dict.fromkeys(warnings))


def shift_reference_surface(stiffness: ABDStiffness, offset: float) -> ABDStiffness:
    """Return ``stiffness`` expressed about a reference surface shifted by ``offset``.

    ``offset`` is the signed distance from the current reference surface
    to the new reference surface along ``+n``. Curvatures and transverse-shear
    strains are unchanged.
    """

    checked_offset = finite_number(offset, name="offset")

    transform = np.eye(8, dtype=np.float64)
    transform[0:3, 3:6] = -checked_offset * np.eye(3, dtype=np.float64)
    shifted = transform.T @ stiffness.C8 @ transform
    shifted = 0.5 * (shifted + shifted.T)
    metadata = dict(stiffness.metadata)
    metadata.update(
        {
            "reference_surface_shift": checked_offset,
            "source": "shift_reference_surface",
        }
    )
    return ABDStiffness.from_tangent(
        shifted,
        frame=stiffness.frame,
        convention=stiffness.convention,
        areal_mass=stiffness.areal_mass,
        metadata=metadata,
        validity=stiffness.validity,
    )


def superpose_abd_stiffnesses(
    *stiffnesses: ABDStiffness,
    metadata: dict[str, Any] | None = None,
) -> ABDStiffness:
    """Return the superposition of compatible ABD stiffnesses."""

    if not stiffnesses:
        msg = "at least one stiffness is required."
        raise ValueError(msg)
    first = stiffnesses[0]
    for stiffness in stiffnesses[1:]:
        if stiffness.frame != first.frame:
            msg = "all stiffnesses must use the same frame."
            raise ValueError(msg)
        if stiffness.convention != first.convention:
            msg = "all stiffnesses must use the same strain convention."
            raise ValueError(msg)

    areal_mass = None
    if all(stiffness.areal_mass is not None for stiffness in stiffnesses):
        areal_mass = sum(
            stiffness.areal_mass for stiffness in stiffnesses if stiffness.areal_mass is not None
        )

    combined_metadata = {
        "source": "superpose_abd_stiffnesses",
        "stiffness_count": len(stiffnesses),
    }
    if metadata is not None:
        combined_metadata.update(metadata)
    return ABDStiffness.from_tangent(
        sum((stiffness.C8 for stiffness in stiffnesses), start=np.zeros((8, 8))),
        frame=first.frame,
        convention=first.convention,
        areal_mass=areal_mass,
        metadata=combined_metadata,
        validity=(
            first.validity
            if all(stiffness.validity == first.validity for stiffness in stiffnesses)
            else None
        ),
    )


__all__ = [
    "ConstitutiveModel",
    "HyperelasticModel",
    "ABDStiffness",
    "LinearModel",
    "ReducedOrthotropicProperties",
    "shift_reference_surface",
    "superpose_abd_stiffnesses",
]
