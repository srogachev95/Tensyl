"""Constitutive stiffness operators."""

from __future__ import annotations

import warnings as warnings_module
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

import numpy as np

from tensyl.core._validation import (
    finite_number,
    frozen_value,
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
from tensyl.core.validity import ValidityReport

_ROUNDOFF_RELATIVE_TOLERANCE = float(64.0 * np.finfo(np.float64).eps)
GeneralizedStrainInput = GeneralizedStrain | FloatArray
_REDUCTION_WARNING_B = "membrane_bending_coupling_discarded"
_REDUCTION_WARNING_A16_A26 = "off_axis_membrane_coupling_discarded"
_REDUCTION_WARNING_D16_D26 = "off_axis_bending_coupling_discarded"
_REDUCTION_WARNING_VALIDITY_B = "validity_membrane_bending_coupling_exceeds_threshold"
_ORTHOTROPIC_WARNING_OFF_AXIS = "orthotropic_reduction_off_axis_terms_present"


class _ABDTangentReductionError(ValueError):
    """Raised when a tangent cannot be reduced to Tensyl's ABD block form."""


class StiffnessSymmetryError(_ABDTangentReductionError):
    """Raised when stiffness asymmetry exceeds the chosen import tolerance."""


def _checked_finite_fields(obj: object, names: tuple[str, ...]) -> None:
    for name in names:
        object.__setattr__(obj, name, finite_number(getattr(obj, name), name=name))


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(values, shape=shape, name=name)


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


def _roundoff_limit(*values: FloatArray) -> float:
    scale = max((float(np.max(np.abs(value))) for value in values if value.size), default=0.0)
    return _ROUNDOFF_RELATIVE_TOLERANCE * scale


def _symmetrized_roundoff_block(values: FloatArray, *, name: str) -> FloatArray:
    residual = float(np.max(np.abs(values - values.T)))
    limit = _roundoff_limit(values)
    if residual > limit:
        msg = (
            f"{name} must be symmetric within numerical roundoff "
            f"(residual {residual:.6g}, limit {limit:.6g}). "
            "For printed-precision matrices, use ABDStiffness.from_published_blocks."
        )
        raise StiffnessSymmetryError(msg)
    return 0.5 * (values + values.T)


def _canonical_abd_tangent(values: FloatArray) -> FloatArray:
    """Project roundoff onto Tensyl's symmetric ABD-plus-shear block form."""
    A = _symmetrized_roundoff_block(values[0:3, 0:3], name="tangent A block")
    D = _symmetrized_roundoff_block(values[3:6, 3:6], name="tangent D block")
    As = _symmetrized_roundoff_block(values[6:8, 6:8], name="tangent As block")

    B_upper = values[0:3, 3:6]
    B_lower_transpose = values[3:6, 0:3].T
    cross_residual = float(np.max(np.abs(B_upper - B_lower_transpose)))
    cross_limit = _roundoff_limit(B_upper, B_lower_transpose)
    if cross_residual > cross_limit:
        msg = (
            "tangent membrane-bending cross-blocks must be transposes within "
            f"numerical roundoff (residual {cross_residual:.6g}, "
            f"limit {cross_limit:.6g})."
        )
        raise StiffnessSymmetryError(msg)
    B = _symmetrized_roundoff_block(
        0.5 * (B_upper + B_lower_transpose),
        name="tangent B block",
    )

    unsupported = np.concatenate(
        (
            values[0:6, 6:8].reshape(-1),
            values[6:8, 0:6].reshape(-1),
        )
    )
    unsupported_residual = float(np.max(np.abs(unsupported)))
    if unsupported_residual > 0.0:
        msg = (
            "tangent contains membrane/bending-to-transverse-shear coupling "
            "outside Tensyl's ABD-plus-shear representation "
            f"(maximum magnitude {unsupported_residual:.6g})."
        )
        raise _ABDTangentReductionError(msg)
    return _build_tangent(A, B, D, As)


def _readonly_tangent(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(values, shape=(8, 8), name=name)


def _hash_array(values: FloatArray) -> int:
    return hash(frozen_value(values))


@runtime_checkable
class HyperelasticModel(Protocol):
    """Public mechanics contract for a generalized hyperelastic model.

    Attributes:
        frame: Local right-handed frame for the model components.
        convention: Generalized strain/resultant ordering.
        metadata: Provenance metadata.
        validity: Optional validity report attached by builders.
    """

    @property
    def frame(self) -> Frame2D:
        """Return the local right-handed frame."""

    @property
    def convention(self) -> StrainConvention:
        """Return the generalized strain/resultant convention."""

    @property
    def metadata(self) -> Mapping[str, Any]:
        """Return provenance metadata."""

    @property
    def validity(self) -> ValidityReport | None:
        """Return the attached validity report, if any."""

    def energy(self, eta: GeneralizedStrain) -> float:
        """Return strain energy density for a generalized strain.

        Args:
            eta: Generalized strain vector in the model convention.

        Returns:
            Stored strain energy density in the active unit system.
        """

    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant:
        """Return generalized resultants for a generalized strain.

        Args:
            eta: Generalized strain vector in the model convention.

        Returns:
            Generalized force and moment resultants in the conjugate ordering.
        """

    def tangent(self, eta: GeneralizedStrain) -> FloatArray:
        """Return the constitutive tangent at a generalized strain.

        Args:
            eta: Generalized strain vector in the model convention.

        Returns:
            Tangent matrix mapping generalized strain increments to resultants.
        """

    def rotate(self, angle_rad: float) -> HyperelasticModel:
        """Return an equivalent model in a rotated local frame.

        Args:
            angle_rad: Counterclockwise rotation angle about the local normal.

        Returns:
            Model representing the same physical law in the rotated frame.
        """


@dataclass(frozen=True, slots=True)
class ReducedOrthotropicProperties:
    """Membrane-equivalent orthotropic plane-stress constants.

    Attributes:
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


_ABD_COEFFICIENT_FIELD_NAMES = (
    "A11",
    "A22",
    "A12",
    "A16",
    "A26",
    "A66",
    "B11",
    "B22",
    "B12",
    "B16",
    "B26",
    "B66",
    "D11",
    "D22",
    "D12",
    "D16",
    "D26",
    "D66",
    "As11",
    "As22",
    "As12",
)


@dataclass(frozen=True, slots=True)
class ABDStiffnessCoefficients:
    """Named scalar view of an ``ABDStiffness`` matrix.

    The fields use the conventional laminate/shell coefficient names. For
    example, ``A16`` is ``A[0, 2]``, ``D66`` is ``D[2, 2]``, and ``As12`` is
    ``As[0, 1]``.

    Attributes:
        A11: Extensional stiffness in local direction 1.
        A22: Extensional stiffness in local direction 2.
        A12: Extensional coupling stiffness.
        A16: Extensional-shear coupling stiffness.
        A26: Extensional-shear coupling stiffness.
        A66: In-plane shear stiffness.
        B11: Membrane-bending coupling in local direction 1.
        B22: Membrane-bending coupling in local direction 2.
        B12: Membrane-bending coupling cross term.
        B16: Membrane-twist coupling term.
        B26: Membrane-twist coupling term.
        B66: Membrane-shear/twist coupling term.
        D11: Bending stiffness in local direction 1.
        D22: Bending stiffness in local direction 2.
        D12: Bending coupling stiffness.
        D16: Bending-twist coupling term.
        D26: Bending-twist coupling term.
        D66: Twist stiffness coefficient.
        As11: Transverse-shear stiffness in local direction 1.
        As22: Transverse-shear stiffness in local direction 2.
        As12: Transverse-shear coupling stiffness.
    """

    A11: float
    A22: float
    A12: float
    A16: float
    A26: float
    A66: float
    B11: float
    B22: float
    B12: float
    B16: float
    B26: float
    B66: float
    D11: float
    D22: float
    D12: float
    D16: float
    D26: float
    D66: float
    As11: float
    As22: float
    As12: float

    def __post_init__(self) -> None:
        _checked_finite_fields(self, _ABD_COEFFICIENT_FIELD_NAMES)


_ORTHOTROPIC_COEFFICIENT_FIELD_NAMES = (
    "Ebar_x",
    "Ebar_y",
    "Ebar_xy",
    "Gbar_xy",
    "Dbar_x",
    "Dbar_y",
    "Dbar_xy",
    "Cbar_x",
    "Cbar_y",
    "Cbar_xy",
    "Kbar_xy",
)


@dataclass(frozen=True, slots=True)
class OrthotropicStiffnessCoefficients:
    """Barred coefficients for aligned orthotropic shell equations.

    This is a reduction of a full ABD stiffness, not another complete stiffness
    representation. ``warnings`` and ``unsupported_terms`` record off-axis terms
    that were present in the source ABD matrix but are not carried by this
    coefficient set.

    Attributes:
        Ebar_x: Effective axial membrane coefficient in the x direction.
        Ebar_y: Effective axial membrane coefficient in the y direction.
        Ebar_xy: Effective membrane coupling coefficient.
        Gbar_xy: Effective in-plane shear coefficient.
        Dbar_x: Effective bending coefficient in the x direction.
        Dbar_y: Effective bending coefficient in the y direction.
        Dbar_xy: Modified bending-twist coefficient ``2*D12 + 4*D66``.
        Cbar_x: Membrane-bending coupling coefficient in the x direction.
        Cbar_y: Membrane-bending coupling coefficient in the y direction.
        Cbar_xy: Membrane-bending coupling cross coefficient.
        Kbar_xy: Membrane-shear/twist coupling coefficient.
        warnings: Warning identifiers recorded during reduction.
        unsupported_terms: Off-axis source ABD terms not represented here.
    """

    Ebar_x: float
    Ebar_y: float
    Ebar_xy: float
    Gbar_xy: float
    Dbar_x: float
    Dbar_y: float
    Dbar_xy: float
    Cbar_x: float
    Cbar_y: float
    Cbar_xy: float
    Kbar_xy: float
    warnings: tuple[str, ...] = ()
    unsupported_terms: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _checked_finite_fields(self, _ORTHOTROPIC_COEFFICIENT_FIELD_NAMES)
        object.__setattr__(self, "warnings", tuple(self.warnings))
        object.__setattr__(self, "unsupported_terms", readonly_mapping(self.unsupported_terms))


@dataclass(frozen=True, slots=True)
class ABDStiffness:
    """Linear ABD stiffness in ABD plus transverse-shear form.

    Attributes:
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
    validity: ValidityReport | None = None
    _c8: FloatArray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Validate and project roundoff in the user-facing blocks first, then
        # rebuild every attribute as a readonly view of one exactly symmetric
        # C8 matrix. That avoids the familiar bug where A/B/D/As and C8 drift
        # apart after construction.
        A = _symmetrized_roundoff_block(
            _readonly_matrix(self.A, shape=(3, 3), name="A"),
            name="A",
        )
        B = _symmetrized_roundoff_block(
            _readonly_matrix(self.B, shape=(3, 3), name="B"),
            name="B",
        )
        D = _symmetrized_roundoff_block(
            _readonly_matrix(self.D, shape=(3, 3), name="D"),
            name="D",
        )
        As = _symmetrized_roundoff_block(
            _readonly_matrix(self.As, shape=(2, 2), name="As"),
            name="As",
        )
        c8 = _build_tangent(A, B, D, As)
        if self.validity is not None and not isinstance(self.validity, ValidityReport):
            msg = f"validity must be a ValidityReport or None, got {type(self.validity).__name__}."
            raise TypeError(msg)
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
        validity: ValidityReport | None = None,
    ) -> ABDStiffness:
        """Build a linear ABD stiffness from the canonical ``8x8`` tangent.

        The tangent order is ``[N11, N22, N12, M11, M22, M12, Q13, Q23]`` by
        ``[eps11, eps22, gamma12, kappa11, kappa22, kappa12, gamma13,
        gamma23]``.

        Args:
            tangent: Symmetric 8x8 generalized stiffness matrix.
            frame: Local frame for the matrix components.
            convention: Generalized strain/resultant ordering.
            areal_mass: Optional nonnegative mass per unit area.
            metadata: Optional provenance metadata.
            validity: Optional validity report to attach.

        Returns:
            ``ABDStiffness`` with readonly block views of the supplied tangent.

        Raises:
            ValueError: If the tangent has the wrong shape, is not finite, or
                cannot be reduced to Tensyl's symmetric
                ABD-plus-transverse-shear block form within roundoff.
        """

        c8 = _canonical_abd_tangent(_readonly_tangent(tangent, name="tangent"))
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

    @classmethod
    def from_published_blocks(
        cls,
        A: FloatArray,
        B: FloatArray,
        D: FloatArray,
        As: FloatArray,
        *,
        rtol: float = 1.0e-6,
        frame: Frame2D = DEFAULT_FRAME,
        convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
        areal_mass: float | None = None,
        metadata: Mapping[str, Any] | None = None,
        validity: ValidityReport | None = None,
    ) -> ABDStiffness:
        """Import blocks whose symmetry was rounded to printed precision.

        Each block is averaged with its transpose only when its maximum
        asymmetry is at most ``rtol`` times that block's largest absolute
        coefficient. This does not test positive energy or change units.

        Args:
            A: 3x3 membrane block.
            B: 3x3 membrane-bending block.
            D: 3x3 bending block.
            As: 2x2 transverse-shear block.
            rtol: Finite relative asymmetry limit, in [0, 1).
            frame: Local frame for the coefficients.
            convention: Generalized strain/resultant ordering.
            areal_mass: Optional nonnegative mass per unit area.
            metadata: Provenance, augmented by a ``published_blocks`` record.
            validity: Optional validity report to attach.

        Returns:
            Exactly symmetric stiffness with the maximum relative correction
            and each block's absolute correction recorded in metadata.

        Raises:
            StiffnessSymmetryError: If a block exceeds the requested tolerance.
            ValueError: If a shape, value, or tolerance is invalid.
        """

        tolerance = nonnegative_number(rtol, name="rtol")
        if tolerance >= 1.0:
            raise ValueError("rtol must be less than 1.")
        blocks: dict[str, FloatArray] = {}
        corrections: dict[str, float] = {}
        relative_correction = 0.0
        for name, values, shape in (
            ("A", A, (3, 3)),
            ("B", B, (3, 3)),
            ("D", D, (3, 3)),
            ("As", As, (2, 2)),
        ):
            block = _readonly_matrix(values, shape=shape, name=name)
            scale = float(np.max(np.abs(block)))
            residual = float(np.max(np.abs(block - block.T)))
            if residual > tolerance * scale:
                raise StiffnessSymmetryError(
                    f"{name} asymmetry {residual:.6g} exceeds rtol * block scale "
                    f"({tolerance * scale:.6g})."
                )
            blocks[name] = 0.5 * block + 0.5 * block.T
            corrections[name] = 0.5 * residual
            if scale > 0.0:
                relative_correction = max(relative_correction, 0.5 * residual / scale)
        provenance = {} if metadata is None else dict(metadata)
        provenance["published_blocks"] = {
            "rtol": tolerance,
            "max_relative_correction": relative_correction,
            "absolute_corrections": corrections,
        }
        return cls(
            **blocks,
            frame=frame,
            convention=convention,
            areal_mass=areal_mass,
            metadata=provenance,
            validity=validity,
        )

    def with_validity(self, validity: ValidityReport | None) -> ABDStiffness:
        """Return an equivalent stiffness with attached validity diagnostics.

        Args:
            validity: Validity report to attach to the copy.

        Returns:
            New ``ABDStiffness`` with the same numeric tangent and metadata.
        """

        return ABDStiffness.from_tangent(
            self.C8,
            frame=self.frame,
            convention=self.convention,
            areal_mass=self.areal_mass,
            metadata=self.metadata,
            validity=validity,
        )

    def __repr__(self) -> str:
        count = None if self.validity is None else len(self.validity.warnings)
        return (
            f"ABDStiffness(frame={self.frame.label!r}, areal_mass={self.areal_mass!r}, "
            f"A11={self.A[0, 0]:.4e}, D11={self.D[0, 0]:.4e}, warnings={count})"
        )

    def summary(self, *, units: Mapping[str, str] | None = None, precision: int = 6) -> str:
        """Return a readable engineering-notation block summary.

        Args:
            units: Optional display labels keyed by A, B, D, As, or areal_mass.
                These labels do not convert or validate the numeric units.
            precision: Decimal places in scientific notation, from 0 to 16.

        Returns:
            Text containing the local frame, ordering, block values, mass,
            and validity warnings. Use ``print(stiffness.summary())`` to print.

        Raises:
            ValueError: If precision is not an integer from 0 to 16.
        """

        if (
            isinstance(precision, bool)
            or not isinstance(precision, int)
            or not 0 <= precision <= 16
        ):
            raise ValueError("precision must be an integer from 0 to 16.")
        labels = {} if units is None else units
        lines = [
            f"ABD stiffness — frame: {self.frame.label}",
            "Engineering notation (engineering shear): 11, 22, 12; transverse: 13, 23",
            f"Reference surface: {self.convention.reference_surface}; positive normal: +n",
        ]
        for name in ("A", "B", "D", "As"):
            label = f" [{labels[name]}]" if name in labels else ""
            lines.append(name + label)
            lines.append(
                np.array2string(
                    getattr(self, name), formatter={"float_kind": lambda x: f"{x:.{precision}e}"}
                )
            )
        mass = "unknown" if self.areal_mass is None else f"{self.areal_mass:.{precision}e}"
        mass_unit = f" [{labels['areal_mass']}]" if "areal_mass" in labels else ""
        lines.append(f"Areal mass{mass_unit}: {mass}")
        if self.validity is None:
            lines.append("Validity: not evaluated")
        else:
            lines.append("Warnings: " + (", ".join(self.validity.warnings) or "none"))
        return "\n".join(lines)

    def __hash__(self) -> int:
        # Frozen dataclasses do not make arrays hashable. Hash the numeric
        # payload explicitly so ABDStiffness can be used in caches and atlases.
        return hash(
            (
                _hash_array(self.C8),
                self.frame,
                self.convention,
                self.areal_mass,
                frozen_value(self.metadata),
                frozen_value(self.validity),
            )
        )

    def __eq__(self, other: object) -> bool:
        # The generated dataclass __eq__ would compare NumPy arrays and raise.
        # Compare the same payload that __hash__ fingerprints.
        if not isinstance(other, ABDStiffness):
            return NotImplemented
        return (
            np.array_equal(self.C8, other.C8)
            and self.frame == other.frame
            and self.convention == other.convention
            and self.areal_mass == other.areal_mass
            and frozen_value(self.metadata) == frozen_value(other.metadata)
            and frozen_value(self.validity) == frozen_value(other.validity)
        )

    @property
    def C8(self) -> FloatArray:
        """Return the canonical 8x8 stiffness tangent.

        Returns:
            Read-only stiffness matrix in the active generalized ordering.
        """

        return self._c8

    @property
    def constant_tangent(self) -> FloatArray:
        """Return the strain-independent stiffness tangent.

        Returns:
            The same read-only matrix as ``C8``.
        """

        return self.C8

    def tangent(self, eta: GeneralizedStrainInput) -> FloatArray:
        """Return the constant stiffness tangent after validating strain.

        Args:
            eta: Generalized strain vector with shape ``(8,)``.

        Returns:
            The strain-independent tangent matrix.

        Raises:
            ValueError: If ``eta`` does not have shape ``(8,)`` or contains
                non-finite values.
        """

        generalized_strain(eta)
        return self.constant_tangent

    def strains(self, resultants: GeneralizedResultant | FloatArray) -> GeneralizedStrain:
        """Solve the full coupled stiffness for strains under given resultants.

        Args:
            resultants: Finite vector in order N11, N22, N12, M11, M22, M12,
                Q13, Q23, expressed in this stiffness's frame and units.

        Returns:
            Read-only strain vector in the canonical engineering ordering.

        Raises:
            ValueError: If the load vector is invalid, the tangent is singular,
                or the solve produces non-finite strains. No pseudoinverse or
                regularization is applied to a singular tangent.
        """

        loads = generalized_resultant(resultants)
        try:
            solution = np.linalg.solve(self.C8, loads)
        except np.linalg.LinAlgError as exc:
            raise ValueError(
                "stiffness tangent is singular; strains are not uniquely determined."
            ) from exc
        return generalized_strain(solution)

    def resultants(self, eta: GeneralizedStrainInput) -> GeneralizedResultant:
        """Return generalized resultants for a strain vector.

        Args:
            eta: Generalized strain vector with shape ``(8,)``.

        Returns:
            Read-only generalized resultants in order
            ``[N11, N22, N12, M11, M22, M12, Q13, Q23]``.

        Raises:
            ValueError: If ``eta`` does not have shape ``(8,)`` or contains
                non-finite values.
        """

        vector = np.asarray(generalized_strain(eta), dtype=np.float64)
        result = self.C8 @ vector
        result.setflags(write=False)
        return generalized_resultant(result)

    def energy(self, eta: GeneralizedStrainInput) -> float:
        """Return linear strain energy density.

        Args:
            eta: Generalized strain vector with shape ``(8,)``.

        Returns:
            ``0.5 * eta @ C8 @ eta``.

        Raises:
            ValueError: If ``eta`` does not have shape ``(8,)`` or contains
                non-finite values.
        """

        vector = np.asarray(generalized_strain(eta), dtype=np.float64)
        return 0.5 * float(vector @ self.C8 @ vector)

    def rotate(self, angle_rad: float) -> ABDStiffness:
        """Return this stiffness in a frame rotated about ``n``.

        Args:
            angle_rad: Counterclockwise rotation angle in radians.

        Returns:
            Equivalent ``ABDStiffness`` expressed in the rotated local frame.

        Raises:
            ValueError: If ``angle_rad`` is not finite.
        """

        from tensyl.core.rotations import rotate_abd_stiffness

        return rotate_abd_stiffness(self, angle_rad)

    @property
    def coefficients(self) -> ABDStiffnessCoefficients:
        """Return independent stiffness terms as named scalars.

        Returns:
            Named scalar view of the ABD and transverse-shear blocks.
        """

        return ABDStiffnessCoefficients(
            A11=float(self.A[0, 0]),
            A22=float(self.A[1, 1]),
            A12=float(self.A[0, 1]),
            A16=float(self.A[0, 2]),
            A26=float(self.A[1, 2]),
            A66=float(self.A[2, 2]),
            B11=float(self.B[0, 0]),
            B22=float(self.B[1, 1]),
            B12=float(self.B[0, 1]),
            B16=float(self.B[0, 2]),
            B26=float(self.B[1, 2]),
            B66=float(self.B[2, 2]),
            D11=float(self.D[0, 0]),
            D22=float(self.D[1, 1]),
            D12=float(self.D[0, 1]),
            D16=float(self.D[0, 2]),
            D26=float(self.D[1, 2]),
            D66=float(self.D[2, 2]),
            As11=float(self.As[0, 0]),
            As22=float(self.As[1, 1]),
            As12=float(self.As[0, 1]),
        )

    def orthotropic_coefficients(
        self,
        *,
        tolerance: float = 1.0e-9,
        relative_tolerance: float = _ROUNDOFF_RELATIVE_TOLERANCE,
    ) -> OrthotropicStiffnessCoefficients:
        """Return barred coefficients for aligned orthotropic shell equations.

        The returned ``Dbar_xy`` is the modified twisting coefficient used by
        classical orthotropic shell formulas, including NASA SP-8007-style hand
        equations. It is not the raw ABD ``D66`` term. Tensyl computes
        ``Dbar_xy = 2*D12 + 4*D66`` so the combined bending-twist input is
        handed off in the form those equations expect.

        Off-axis terms such as ``A16`` and ``D26`` are not represented by this
        coefficient set. A term is retained when it exceeds ``tolerance`` plus
        ``relative_tolerance`` times the scale of its parent stiffness block.
        The relative term prevents roundoff from becoming a finding merely
        because the stiffness scale is large, while ``tolerance`` preserves an
        explicit caller-controlled absolute floor. The method still returns
        the reduced coefficients, records retained terms in
        ``unsupported_terms``, and emits a warning so the caller can decide
        whether the reduction is acceptable for the downstream calculation.

        Args:
            tolerance: Nonnegative absolute tolerance for off-axis terms.
            relative_tolerance: Nonnegative dimensionless tolerance relative to
                the applicable ``A``, ``B``, or ``D`` block scale.

        Returns:
            Barred orthotropic coefficient view plus warning metadata.

        Raises:
            ValueError: If either tolerance is negative or non-finite.
        """

        checked_tolerance = nonnegative_number(tolerance, name="tolerance")
        checked_relative_tolerance = nonnegative_number(
            relative_tolerance,
            name="relative_tolerance",
        )
        coefficients = self.coefficients
        unsupported_terms = _orthotropic_unsupported_terms(
            self,
            tolerance=checked_tolerance,
            relative_tolerance=checked_relative_tolerance,
        )
        warning_codes = ()
        if unsupported_terms:
            warning_codes = (_ORTHOTROPIC_WARNING_OFF_AXIS,)
            warnings_module.warn(
                "orthotropic_coefficients() does not represent nonzero off-axis "
                f"ABD terms: {unsupported_terms}",
                UserWarning,
                stacklevel=2,
            )
        return OrthotropicStiffnessCoefficients(
            Ebar_x=coefficients.A11,
            Ebar_y=coefficients.A22,
            Ebar_xy=coefficients.A12,
            Gbar_xy=coefficients.A66,
            Dbar_x=coefficients.D11,
            Dbar_y=coefficients.D22,
            Dbar_xy=2.0 * coefficients.D12 + 4.0 * coefficients.D66,
            Cbar_x=coefficients.B11,
            Cbar_y=coefficients.B22,
            Cbar_xy=coefficients.B12,
            Kbar_xy=coefficients.B66,
            warnings=warning_codes,
            unsupported_terms=unsupported_terms,
        )

    def reduced_orthotropic_properties(
        self,
        t_eff: float,
        *,
        tolerance: float = 1.0e-9,
        relative_tolerance: float = _ROUNDOFF_RELATIVE_TOLERANCE,
    ) -> ReducedOrthotropicProperties:
        """Return membrane-equivalent orthotropic plane-stress properties.

        ``t_eff`` is the shell thickness used by a downstream model to turn
        membrane stiffness per unit width into material stiffness. The reduction
        is based on ``A / t_eff`` and does not preserve the bending, coupling, or
        transverse-shear blocks.

        Args:
            t_eff: Positive effective shell thickness.
            tolerance: Nonnegative absolute tolerance for warning about
                discarded coupling or off-axis terms.
            relative_tolerance: Nonnegative dimensionless tolerance relative to
                the applicable stiffness scale.

        Returns:
            Membrane-equivalent orthotropic plane-stress constants.

        Raises:
            ValueError: If ``t_eff`` is not positive, either tolerance is
                invalid, or the membrane stiffness block cannot be inverted.
        """

        checked_t_eff = positive_number(t_eff, name="t_eff")
        checked_tolerance = nonnegative_number(tolerance, name="tolerance")
        checked_relative_tolerance = nonnegative_number(
            relative_tolerance,
            name="relative_tolerance",
        )
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
        warnings = _reduced_orthotropic_warnings(
            self,
            tolerance=checked_tolerance,
            relative_tolerance=checked_relative_tolerance,
        )
        metadata = {
            "source": "reduced_orthotropic_properties",
            "reduction": "membrane_compliance_from_A",
            "t_eff": checked_t_eff,
            "tolerance": checked_tolerance,
            "relative_tolerance": checked_relative_tolerance,
        }
        return ReducedOrthotropicProperties(
            t_eff=checked_t_eff,
            warnings=warnings,
            metadata=metadata,
            **values,
        )


def _scaled_tolerance(
    reference: FloatArray,
    *,
    tolerance: float,
    relative_tolerance: float,
) -> float:
    scale = float(np.max(np.abs(reference)))
    return tolerance + relative_tolerance * scale


def _has_nonzero(
    values: FloatArray,
    *,
    reference: FloatArray,
    tolerance: float,
    relative_tolerance: float,
) -> bool:
    limit = _scaled_tolerance(
        reference,
        tolerance=tolerance,
        relative_tolerance=relative_tolerance,
    )
    return bool(np.any(np.abs(values) > limit))


def _orthotropic_unsupported_terms(
    stiffness: ABDStiffness,
    *,
    tolerance: float,
    relative_tolerance: float,
) -> dict[str, float]:
    coefficients = stiffness.coefficients
    grouped_terms = (
        (
            stiffness.A,
            {
                "A16": coefficients.A16,
                "A26": coefficients.A26,
            },
        ),
        (
            stiffness.B,
            {
                "B16": coefficients.B16,
                "B26": coefficients.B26,
                "B61": coefficients.B16,
                "B62": coefficients.B26,
            },
        ),
        (
            stiffness.D,
            {
                "D16": coefficients.D16,
                "D26": coefficients.D26,
            },
        ),
    )
    unsupported: dict[str, float] = {}
    for block, terms in grouped_terms:
        limit = _scaled_tolerance(
            block,
            tolerance=tolerance,
            relative_tolerance=relative_tolerance,
        )
        unsupported.update({name: value for name, value in terms.items() if abs(value) > limit})
    return unsupported


def _reduced_orthotropic_warnings(
    stiffness: ABDStiffness,
    *,
    tolerance: float,
    relative_tolerance: float,
) -> tuple[str, ...]:
    warnings: list[str] = []
    coupling_scale = np.sqrt(
        float(np.max(np.abs(stiffness.A))) * float(np.max(np.abs(stiffness.D)))
    )
    if _has_nonzero(
        stiffness.B,
        reference=np.asarray([coupling_scale]),
        tolerance=tolerance,
        relative_tolerance=relative_tolerance,
    ):
        warnings.append(_REDUCTION_WARNING_B)
    if _has_nonzero(
        stiffness.A[[0, 1], 2],
        reference=stiffness.A,
        tolerance=tolerance,
        relative_tolerance=relative_tolerance,
    ):
        warnings.append(_REDUCTION_WARNING_A16_A26)
    if _has_nonzero(
        stiffness.D[[0, 1], 2],
        reference=stiffness.D,
        tolerance=tolerance,
        relative_tolerance=relative_tolerance,
    ):
        warnings.append(_REDUCTION_WARNING_D16_D26)
    validity_warnings = () if stiffness.validity is None else stiffness.validity.warnings
    if "membrane_bending_coupling_exceeds_threshold" in validity_warnings:
        warnings.append(_REDUCTION_WARNING_VALIDITY_B)
    return tuple(dict.fromkeys(warnings))


def shift_reference_surface(stiffness: ABDStiffness, offset: float) -> ABDStiffness:
    """Return ``stiffness`` expressed about a reference surface shifted by ``offset``.

    ``offset`` is the signed distance from the current reference surface
    to the new reference surface along ``+n``. Curvatures and transverse-shear
    strains are unchanged.

    Args:
        stiffness: Source stiffness about the current reference surface.
        offset: Signed distance from the current surface to the new surface.

    Returns:
        Equivalent stiffness about the shifted reference surface.

    Raises:
        ValueError: If ``offset`` is not finite.
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
    """Return the superposition of compatible ABD stiffnesses.

    Args:
        *stiffnesses: One or more stiffnesses using the same frame and strain
            convention.
        metadata: Optional metadata to merge into the combined result.

    Returns:
        Sum of the supplied stiffness tangents. Areal mass is summed only when
        every input provides it; shared validity is preserved only when all
        inputs agree.

    Raises:
        ValueError: If no stiffnesses are supplied, or if frames/conventions do
            not match. Frames match when their axes agree within roundoff;
            labels are ignored and the result uses the first frame.
    """

    if not stiffnesses:
        msg = "at least one stiffness is required."
        raise ValueError(msg)
    first = stiffnesses[0]
    for stiffness in stiffnesses[1:]:
        if not stiffness.frame.is_close(first.frame):
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
    "StiffnessSymmetryError",
    "ABDStiffnessCoefficients",
    "HyperelasticModel",
    "ABDStiffness",
    "OrthotropicStiffnessCoefficients",
    "ReducedOrthotropicProperties",
    "shift_reference_surface",
    "superpose_abd_stiffnesses",
]
