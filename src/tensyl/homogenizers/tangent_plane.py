"""Tangent-plane equivalent-stiffness homogenizers."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Protocol

import numpy as np

from tensyl.cells.tangent_plane import BeamMember, CanonicalUnitCell
from tensyl.core._validation import (
    frozen_value,
    readonly_array,
)
from tensyl.core.constitutive import (
    ABDStiffness,
    ABDStiffnessCoefficients,
    OrthotropicStiffnessCoefficients,
    ReducedOrthotropicProperties,
    _ABDTangentReductionError,
)
from tensyl.core.conventions import DEFAULT_STRAIN_CONVENTION
from tensyl.core.rotations import generalized_strain_transform
from tensyl.core.typing import FloatArray
from tensyl.core.validity import ValidityContext, ValidityReport, ValidityThresholds
from tensyl.core.validity_checks import (
    _spectral_properties,
    _validity_report,
    validity_report_for_stiffness,
)
from tensyl.sections.beam import BeamSection

_ROUNDOFF_RELATIVE_TOLERANCE = float(64.0 * np.finfo(np.float64).eps)


class HomogenizationFailure(Exception):
    """Base exception for homogenization failures.

    Use this when callers want to catch all Tensyl homogenization errors
    without also catching unrelated ``ValueError`` instances.
    """


class HomogenizationInputError(HomogenizationFailure, ValueError):
    """Raised when a homogenizer receives malformed or unsupported input."""


class HomogenizationNumericalError(HomogenizationFailure, ArithmeticError):
    """Raised when an assembled tangent violates the homogenizer's numeric contract."""


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(values, shape=shape, name=name)


@dataclass(frozen=True, slots=True)
class HomogenizationResult:
    """A homogenization result and its verification context.

    The stiffness is returned with ``validity`` attached so warnings remain available
    when only ``result.stiffness`` is passed to fields, exports, or downstream tools.

    Attributes:
        stiffness: Homogenized linear ABD stiffness.
        validity: Validity report attached to the stiffness.
        diagnostics: Read-only numerical diagnostics from the homogenizer.
        assumptions: Modeling assumptions made by the homogenizer.
        source: Identifier for the homogenization path that produced the result.
    """

    stiffness: ABDStiffness
    validity: ValidityReport
    diagnostics: dict[str, Any] | MappingProxyType[str, Any]
    assumptions: tuple[str, ...]
    source: Literal["energy", "direct_ec", "rve", "imported"]

    def __post_init__(self) -> None:
        stiffness = self.stiffness
        if getattr(stiffness, "validity", None) != self.validity:
            stiffness = stiffness.with_validity(self.validity)
        object.__setattr__(self, "stiffness", stiffness)
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HomogenizationResult):
            return NotImplemented
        return (
            self.stiffness == other.stiffness
            and self.validity == other.validity
            and frozen_value(self.diagnostics) == frozen_value(other.diagnostics)
            and self.assumptions == other.assumptions
            and self.source == other.source
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.stiffness,
                self.validity,
                frozen_value(self.diagnostics),
                self.assumptions,
                self.source,
            )
        )

    def reduced_orthotropic_properties(
        self,
        t_eff: float,
        *,
        tolerance: float = 1.0e-9,
        relative_tolerance: float = _ROUNDOFF_RELATIVE_TOLERANCE,
    ) -> ReducedOrthotropicProperties:
        """Return membrane-equivalent orthotropic properties.

        Args:
            t_eff: Positive effective wall thickness used to convert membrane
                stiffnesses into engineering constants.
            tolerance: Absolute tolerance for discarded off-axis or coupling terms.
            relative_tolerance: Dimensionless tolerance relative to the applicable
                stiffness block scale.

        Returns:
            Orthotropic membrane constants reduced from ``self.stiffness``.

        Raises:
            ValueError: If ``t_eff`` is not positive or the reduced compliance
                terms are not physically admissible.
        """

        return self.stiffness.reduced_orthotropic_properties(
            t_eff,
            tolerance=tolerance,
            relative_tolerance=relative_tolerance,
        )

    @property
    def coefficients(self) -> ABDStiffnessCoefficients:
        """Return the homogenized ABD stiffness terms as named scalars.

        Returns:
            Named view of the A, B, D, and transverse-shear coefficients.
        """

        return self.stiffness.coefficients

    def orthotropic_coefficients(
        self,
        *,
        tolerance: float = 1.0e-9,
        relative_tolerance: float = _ROUNDOFF_RELATIVE_TOLERANCE,
    ) -> OrthotropicStiffnessCoefficients:
        """Return aligned orthotropic shell coefficients.

        Args:
            tolerance: Absolute tolerance for terms outside the aligned
                orthotropic coefficient set.
            relative_tolerance: Dimensionless tolerance relative to the applicable
                stiffness block scale.

        Returns:
            Named orthotropic coefficient view of ``self.stiffness``.
        """

        return self.stiffness.orthotropic_coefficients(
            tolerance=tolerance,
            relative_tolerance=relative_tolerance,
        )


class Homogenizer(Protocol):
    """Protocol for tangent-plane homogenizers.

    Attributes:
        compute: Method that returns an equivalent ABD stiffness result.
    """

    def compute(
        self,
        cell: CanonicalUnitCell,
        *,
        validity_context: ValidityContext | None = None,
    ) -> HomogenizationResult:
        """Compute an equivalent ABD stiffness for a canonical unit cell.

        Args:
            cell: Canonical tangent-plane unit cell to homogenize.
            validity_context: Optional scale data used to form validity
                warnings on the result.

        Returns:
            Homogenized stiffness, diagnostics, assumptions, and validity
            report.

        Raises:
            HomogenizationInputError: If the cell is malformed or uses an
                unsupported convention.
        """


def _beam_strain_map(axial_eccentricity: float, shear_eccentricity: float) -> FloatArray:
    """Map local wall strains to Nemeth's first-approximation member strains."""

    axial_z = float(axial_eccentricity)
    shear_z = float(shear_eccentricity)
    # Rows: axial strain, in-plane shear, transverse shear, out-of-plane
    # bending curvature, and twist rate. There is no in-plane bending row:
    # under uniform wall strain and curvature a member's axis stays straight
    # in the panel plane (Nemeth's chi_Z = 0), so EIz and EIyz store no energy.
    transform = np.zeros((5, 8), dtype=np.float64)
    transform[0, 0] = 1.0
    transform[0, 3] = axial_z
    transform[1, 2] = 0.5
    # Nemeth Eqs. 10c, 12b, and 13b use gamma_xy(z) = gamma_xy^0 + z*kappa_xy.
    # The positive sign is required for a positive shear-weighted eccentricity
    # to produce positive B66 coupling under Tensyl's +n convention.
    transform[1, 5] = 0.5 * shear_z
    transform[2, 6] = 1.0
    transform[3, 3] = 1.0
    transform[4, 5] = -0.5
    transform.setflags(write=False)
    return transform


def _beam_stiffness(section: BeamSection) -> FloatArray:
    # Optional shear stiffnesses are intentionally zeroed when omitted. The
    # result assumptions report that modeling choice instead of silently
    # inventing a shear correction.
    stiffness = np.diag(
        [
            section.EA,
            0.0 if section.kGAy is None else section.kGAy,
            0.0 if section.kGAz is None else section.kGAz,
            section.EIy,
            section.GJ,
        ]
    ).astype(np.float64)
    stiffness.setflags(write=False)
    return stiffness


def _member_transform(member: BeamMember) -> FloatArray:
    if member.shear_eccentricity is None:  # normalized by the value object
        msg = "member shear_eccentricity was not normalized."
        raise HomogenizationInputError(msg)
    return _beam_strain_map(
        member.axial_eccentricity,
        member.shear_eccentricity,
    ) @ generalized_strain_transform(member.angle_rad)


def member_tangent_density(member: BeamMember) -> FloatArray:
    """Return a member tangent contribution per unit length density.

    Args:
        member: Beam member in tangent-plane coordinates.

    Returns:
        Read-only 8x8 stiffness contribution before multiplying by member
        length density.
    """

    transform = _member_transform(member)
    stiffness = _beam_stiffness(member.section)
    # The transform maps ABD generalized strain to member generalized strain,
    # so the equivalent stiffness contribution is T.T K T.
    tangent = transform.T @ stiffness @ transform
    tangent = 0.5 * (tangent + tangent.T)
    tangent.setflags(write=False)
    return tangent


def member_tangent_contribution(member: BeamMember, *, cell_area: float) -> FloatArray:
    """Return one canonical member contribution to the stiffness tangent.

    Args:
        member: Finite beam member in a canonical unit cell.
        cell_area: Positive repeated-cell area used to convert member energy
            into wall stiffness.

    Returns:
        Read-only 8x8 stiffness contribution for the member.
    """

    # Energy is accumulated over member length, then normalized by repeated cell
    # area so the result has wall-stiffness units rather than beam-stiffness
    # units.
    density = member.multiplicity * member.length / cell_area
    tangent = density * member_tangent_density(member)
    tangent.setflags(write=False)
    return tangent


def member_energy(member: BeamMember, eta: FloatArray) -> float:
    """Return explicit member strain energy for a generalized strain.

    Args:
        member: Finite beam member in a canonical unit cell.
        eta: Generalized strain vector with shape ``(8,)``.

    Returns:
        Member strain energy before division by cell area.

    Raises:
        ValueError: If ``eta`` does not have shape ``(8,)``.
    """

    vector = np.array(eta, dtype=np.float64, copy=True)
    if vector.shape != (8,):
        msg = f"eta must have shape (8,), got {vector.shape}."
        raise ValueError(msg)
    strain = _member_transform(member) @ vector
    return (
        0.5
        * member.multiplicity
        * member.length
        * float(strain @ _beam_stiffness(member.section) @ strain)
    )


def _cell_areal_mass(cell: CanonicalUnitCell) -> float | None:
    # Areal mass is only meaningful when the skin and every member know their
    # mass. Reporting skin-only mass for a stiffened panel would understate it.
    if cell.skin.areal_mass is None:
        return None
    member_mass = 0.0
    for member in cell.members:
        if member.section.mass_per_length is None:
            return None
        member_mass += member.multiplicity * member.length * member.section.mass_per_length
    return cell.skin.areal_mass + member_mass / cell.area


def _mass_assumptions(areal_mass: float | None) -> tuple[str, ...]:
    if areal_mass is not None:
        return ()
    return (
        "Areal mass is not reported because the skin or at least one member "
        "section has no mass data.",
    )


def _assumptions_for_members(members: tuple[BeamMember, ...]) -> tuple[str, ...]:
    assumptions = [
        "Local tangent-plane equivalent-stiffness homogenization.",
        "Extension- and shear-weighted member eccentricities are measured along +n.",
        "Beam members use Nemeth first-approximation generalized strain kinematics.",
    ]
    if any(member.section.kGAy is None for member in members):
        assumptions.append(
            "Omitted member kGAy values contribute no in-plane stiffener shear stiffness."
        )
    if any(member.section.kGAz is None for member in members):
        assumptions.append(
            "Omitted member kGAz values contribute no transverse stiffener shear stiffness."
        )
    return tuple(assumptions)


def _diagnostics(
    tangent: FloatArray,
    *,
    member_count: int,
    cell_area: float | None,
) -> dict[str, Any]:
    # Rank deficiency is not automatically a hard failure: some idealized cells
    # have finite but incomplete stiffness. Surface the condition as validity
    # context so callers can decide whether it is acceptable.
    matrix = _readonly_matrix(tangent, shape=(8, 8), name="tangent")
    eigenvalues, spectral_tolerance, rank = _spectral_properties(matrix)
    min_eigenvalue = float(eigenvalues[0])
    psd = bool(min_eigenvalue >= -spectral_tolerance)
    return {
        "positive_semidefinite": psd,
        "minimum_eigenvalue": min_eigenvalue,
        "rank": rank,
        "member_count": member_count,
        "cell_area": cell_area,
        "source_equations": ("Nemeth 2011 eqs. 30-39",),
    }


def _stiffness_from_tangent(
    tangent: FloatArray,
    *,
    skin: ABDStiffness,
    areal_mass: float | None,
    metadata: dict[str, Any],
) -> ABDStiffness:
    try:
        return ABDStiffness.from_tangent(
            tangent,
            frame=skin.frame,
            convention=skin.convention,
            areal_mass=areal_mass,
            metadata=metadata,
        )
    except _ABDTangentReductionError as exc:
        msg = f"assembled tangent is not reducible to ABD form: {exc}"
        raise HomogenizationNumericalError(msg) from exc


@dataclass(frozen=True, slots=True)
class EnergyHomogenizer:
    """Reference tangent-plane energy-equivalence homogenizer.

    Computes an ``ABDStiffness`` by adding skin stiffness and member energy
    contributions over a ``CanonicalUnitCell``.

    Attributes:
        thresholds: Warning thresholds used when building the result validity
            report.
    """

    thresholds: ValidityThresholds = field(default_factory=ValidityThresholds)

    def compute(
        self,
        cell: CanonicalUnitCell,
        *,
        validity_context: ValidityContext | None = None,
    ) -> HomogenizationResult:
        """Compute an equivalent ABD stiffness from a canonical cell.

        Args:
            cell: Tangent-plane unit cell containing the skin, finite members,
                frame, convention, and repeated area.
            validity_context: Optional geometric and response length scales for
                result warnings.

        Returns:
            Homogenization result with stiffness, diagnostics, assumptions, and
            validity report.

        Raises:
            HomogenizationInputError: If the cell uses a strain convention that
                the energy path does not support.
            HomogenizationNumericalError: If the assembled tangent materially
                violates Tensyl's ABD block contract.
        """

        if cell.convention != DEFAULT_STRAIN_CONVENTION:
            msg = (
                "EnergyHomogenizer currently supports Tensyl's default engineering-shear "
                "convention only."
            )
            raise HomogenizationInputError(msg)
        tangent = np.array(cell.skin.C8, dtype=np.float64, copy=True)
        # The skin is the baseline ABD stiffness; members add energy-equivalent
        # stiffness over the repeated tangent-plane cell.
        for member in cell.members:
            tangent += member_tangent_contribution(member, cell_area=cell.area)
        metadata = dict(cell.skin.metadata)
        metadata.update({"source": "energy_homogenizer", "cell": dict(cell.metadata)})
        areal_mass = _cell_areal_mass(cell)
        stiffness = _stiffness_from_tangent(
            tangent, skin=cell.skin, areal_mass=areal_mass, metadata=metadata
        )
        diagnostics = _diagnostics(
            stiffness.C8, member_count=len(cell.members), cell_area=cell.area
        )
        return HomogenizationResult(
            stiffness=stiffness,
            validity=_validity_report(
                stiffness, context=validity_context, thresholds=self.thresholds
            ),
            diagnostics=diagnostics,
            assumptions=_assumptions_for_members(cell.members) + _mass_assumptions(areal_mass),
            source="energy",
        )


__all__ = [
    "EnergyHomogenizer",
    "HomogenizationFailure",
    "HomogenizationInputError",
    "HomogenizationNumericalError",
    "HomogenizationResult",
    "Homogenizer",
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
    "member_energy",
    "member_tangent_contribution",
    "member_tangent_density",
    "validity_report_for_stiffness",
]
