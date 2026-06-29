"""Tangent-plane equivalent-stiffness homogenizers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Protocol

import numpy as np

from tensyl.cells.tangent_plane import BeamMember, CanonicalUnitCell, StiffenerFamily
from tensyl.core._validation import optional_positive_number, positive_number, readonly_array
from tensyl.core.constitutive import ABDStiffness, ReducedOrthotropicProperties
from tensyl.core.conventions import DEFAULT_STRAIN_CONVENTION, StrainConvention
from tensyl.core.rotations import generalized_strain_transform
from tensyl.core.typing import FloatArray
from tensyl.sections.beam import BeamSection

_SYMMETRY_TOLERANCE = 1.0e-9
_PSD_TOLERANCE = 1.0e-8


class HomogenizationFailure(Exception):
    """Base exception for homogenization failures."""


class HomogenizationInputError(HomogenizationFailure, ValueError):
    """Raised when a homogenizer receives malformed or unsupported input."""


def _optional_positive_or_inf(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    checked = float(value)
    if checked == np.inf:
        return checked
    return positive_number(checked, name=name)


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(values, shape=shape, name=name)


@dataclass(frozen=True, slots=True)
class ValidityContext:
    """Optional geometric scale data for tangent-plane validity checks.

    ``characteristic_height`` is a stiffness or stiffener height scale, ``pitch`` is
    the repeated-cell spacing, ``min_radius`` is the smallest local curvature
    radius, and ``response_length`` is the intended structural response length
    such as a buckle wavelength or analysis feature size.
    """

    characteristic_height: float | None = None
    pitch: float | None = None
    min_radius: float | None = None
    response_length: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "characteristic_height",
            optional_positive_number(self.characteristic_height, name="characteristic_height"),
        )
        object.__setattr__(self, "pitch", optional_positive_number(self.pitch, name="pitch"))
        object.__setattr__(
            self,
            "min_radius",
            _optional_positive_or_inf(self.min_radius, name="min_radius"),
        )
        object.__setattr__(
            self,
            "response_length",
            optional_positive_number(self.response_length, name="response_length"),
        )


@dataclass(frozen=True, slots=True)
class ValidityThresholds:
    """Default warning thresholds for tangent-plane scale-separation checks."""

    h_over_R: float = 0.05
    p_over_R: float = 0.05
    p_over_L_response: float = 0.05
    coupling_ratio: float = 0.10

    def __post_init__(self) -> None:
        object.__setattr__(self, "h_over_R", positive_number(self.h_over_R, name="h_over_R"))
        object.__setattr__(self, "p_over_R", positive_number(self.p_over_R, name="p_over_R"))
        object.__setattr__(
            self,
            "p_over_L_response",
            positive_number(self.p_over_L_response, name="p_over_L_response"),
        )
        object.__setattr__(
            self,
            "coupling_ratio",
            positive_number(self.coupling_ratio, name="coupling_ratio"),
        )


@dataclass(frozen=True, slots=True)
class ValidityReport:
    """Machine-readable validity diagnostics attached to a homogenized result."""

    h_over_R: float | None
    p_over_R: float | None
    p_over_L_response: float | None
    coupling_ratios: Mapping[str, float]
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("h_over_R", "p_over_R", "p_over_L_response"):
            value = getattr(self, name)
            if value is not None and (not np.isfinite(value) or value < 0.0):
                msg = f"{name} must be finite and nonnegative when provided."
                raise ValueError(msg)
        object.__setattr__(self, "coupling_ratios", MappingProxyType(dict(self.coupling_ratios)))
        object.__setattr__(self, "warnings", tuple(self.warnings))


@dataclass(frozen=True, slots=True)
class HomogenizationResult:
    """A homogenization result and its verification context.

    The stiffness is returned with ``validity`` attached so warnings remain available
    when only ``result.stiffness`` is passed to fields, exports, or downstream tools.
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

    def reduced_orthotropic_properties(
        self,
        t_eff: float,
        *,
        tolerance: float = 1.0e-9,
    ) -> ReducedOrthotropicProperties:
        """Return membrane-equivalent orthotropic properties for ``stiffness``."""

        return self.stiffness.reduced_orthotropic_properties(
            t_eff,
            tolerance=tolerance,
        )


class Homogenizer(Protocol):
    """Protocol for tangent-plane homogenizers."""

    def compute(
        self,
        cell: CanonicalUnitCell,
        *,
        validity_context: ValidityContext | None = None,
    ) -> HomogenizationResult:
        """Compute an equivalent ABD stiffness for a canonical unit cell."""


def _beam_strain_map(eccentricity: float) -> FloatArray:
    """Map member-frame generalized strains into simplified beam strains."""

    z = float(eccentricity)
    # This is the shared first-approximation member kinematics used by both the
    # energy and direct EC paths. Agreement between those paths checks assembly,
    # not the truth of this strain map.
    transform = np.zeros((6, 8), dtype=np.float64)
    transform[0, 0] = 1.0
    transform[0, 3] = z
    transform[1, 2] = 0.5
    transform[1, 5] = -0.5 * z
    transform[2, 6] = 1.0
    transform[3, 4] = 1.0
    transform[4, 3] = 1.0
    transform[5, 5] = -0.5
    transform.setflags(write=False)
    return transform


def _beam_stiffness(section: BeamSection) -> FloatArray:
    # Optional shear stiffnesses are intentionally zeroed when omitted. The
    # result assumptions report that modeling choice instead of silently
    # inventing a shear correction.
    stiffness = np.zeros((6, 6), dtype=np.float64)
    stiffness[0, 0] = section.EA
    if section.kGAy is not None:
        stiffness[1, 1] = section.kGAy
    if section.kGAz is not None:
        stiffness[2, 2] = section.kGAz
    stiffness[3, 3] = section.EIz
    stiffness[3, 4] = section.EIyz
    stiffness[4, 3] = section.EIyz
    stiffness[4, 4] = section.EIy
    stiffness[5, 5] = section.GJ
    stiffness.setflags(write=False)
    return stiffness


def _member_transform(member: BeamMember | StiffenerFamily) -> FloatArray:
    return _beam_strain_map(member.eccentricity) @ generalized_strain_transform(member.angle_rad)


def member_tangent_density(member: BeamMember | StiffenerFamily) -> FloatArray:
    """Return a member tangent contribution per unit member length density."""

    transform = _member_transform(member)
    stiffness = _beam_stiffness(member.section)
    # The transform maps ABD generalized strain to member generalized strain,
    # so the equivalent stiffness contribution is T.T K T.
    tangent = transform.T @ stiffness @ transform
    tangent = 0.5 * (tangent + tangent.T)
    tangent.setflags(write=False)
    return tangent


def member_tangent_contribution(member: BeamMember, *, cell_area: float) -> FloatArray:
    """Return one canonical member contribution to the stiffness tangent."""

    # Energy is accumulated over member length, then normalized by repeated cell
    # area so the result has wall-stiffness units rather than beam-stiffness
    # units.
    density = member.multiplicity * member.length / cell_area
    tangent = density * member_tangent_density(member)
    tangent.setflags(write=False)
    return tangent


def member_energy(member: BeamMember, eta: FloatArray) -> float:
    """Return explicit member strain energy for generalized strain ``eta``."""

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


def _assumptions_for_members(members: tuple[BeamMember | StiffenerFamily, ...]) -> tuple[str, ...]:
    assumptions = [
        "Local tangent-plane equivalent-stiffness homogenization.",
        "Centroidal beam-section stiffnesses with member eccentricity measured along +n.",
        "Beam members use first-approximation generalized strain kinematics.",
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
    symmetric = bool(np.allclose(matrix, matrix.T, atol=_SYMMETRY_TOLERANCE, rtol=0.0))
    eigenvalues = np.linalg.eigvalsh(0.5 * (matrix + matrix.T))
    min_eigenvalue = float(eigenvalues[0])
    psd = bool(min_eigenvalue >= -_PSD_TOLERANCE)
    rank = int(np.linalg.matrix_rank(matrix, tol=_PSD_TOLERANCE))
    return {
        "symmetric": symmetric,
        "positive_semidefinite": psd,
        "minimum_eigenvalue": min_eigenvalue,
        "rank": rank,
        "member_count": member_count,
        "cell_area": cell_area,
        "source_equations": ("Nemeth 2011 eqs. 30-39",),
    }


def _coupling_ratio(stiffness: ABDStiffness) -> float:
    # Normalize B by the geometric mean of A and D norms to produce a
    # scale-free warning metric for membrane-bending coupling.
    norm_A = float(np.linalg.norm(stiffness.A, ord="fro"))
    norm_D = float(np.linalg.norm(stiffness.D, ord="fro"))
    norm_B = float(np.linalg.norm(stiffness.B, ord="fro"))
    if norm_A == 0.0 or norm_D == 0.0:
        return 0.0
    return norm_B / float(np.sqrt(norm_A * norm_D))


def _validity_report(
    stiffness: ABDStiffness,
    *,
    context: ValidityContext | None,
    thresholds: ValidityThresholds,
) -> ValidityReport:
    warnings: list[str] = []
    h_over_R = None
    p_over_R = None
    p_over_L_response = None
    if context is None:
        warnings.append("validity_context_missing")
    else:
        # These ratios are scale-separation checks for using a flat tangent
        # cell inside a curved or spatially varying shell model.
        if context.characteristic_height is not None and context.min_radius is not None:
            h_over_R = context.characteristic_height / context.min_radius
            if h_over_R >= thresholds.h_over_R:
                warnings.append("h_over_R_exceeds_threshold")
        else:
            warnings.append("h_over_R_unavailable")
        if context.pitch is not None and context.min_radius is not None:
            p_over_R = context.pitch / context.min_radius
            if p_over_R >= thresholds.p_over_R:
                warnings.append("p_over_R_exceeds_threshold")
        else:
            warnings.append("p_over_R_unavailable")
        if context.pitch is not None and context.response_length is not None:
            p_over_L_response = context.pitch / context.response_length
            if p_over_L_response >= thresholds.p_over_L_response:
                warnings.append("p_over_L_response_exceeds_threshold")
        else:
            warnings.append("p_over_L_response_unavailable")

    coupling = _coupling_ratio(stiffness)
    if coupling >= thresholds.coupling_ratio:
        warnings.append("membrane_bending_coupling_exceeds_threshold")
    matrix = stiffness.C8
    if np.linalg.matrix_rank(matrix, tol=_PSD_TOLERANCE) < matrix.shape[0]:
        warnings.append("rank_deficient_tangent")
    if float(np.linalg.eigvalsh(0.5 * (matrix + matrix.T))[0]) < -_PSD_TOLERANCE:
        warnings.append("negative_energy_mode")
    return ValidityReport(
        h_over_R=h_over_R,
        p_over_R=p_over_R,
        p_over_L_response=p_over_L_response,
        coupling_ratios=MappingProxyType({"B_fro": coupling}),
        warnings=tuple(warnings),
    )


def validity_report_for_stiffness(
    stiffness: ABDStiffness,
    *,
    context: ValidityContext | None = None,
    thresholds: ValidityThresholds | None = None,
) -> ValidityReport:
    """Return tangent-plane validity diagnostics for an existing ABD stiffness."""

    return _validity_report(
        stiffness,
        context=context,
        thresholds=ValidityThresholds() if thresholds is None else thresholds,
    )


def _stiffness_from_tangent(
    tangent: FloatArray,
    *,
    skin: ABDStiffness,
    metadata: dict[str, Any],
) -> ABDStiffness:
    # Homogenizer assembly should already be symmetric, but symmetrizing the
    # numerical copy keeps roundoff from becoming a false mechanics failure.
    matrix = 0.5 * (np.array(tangent, dtype=np.float64, copy=True) + np.array(tangent).T)
    return ABDStiffness.from_tangent(
        matrix,
        frame=skin.frame,
        convention=skin.convention,
        areal_mass=skin.areal_mass,
        metadata=metadata,
    )


@dataclass(frozen=True, slots=True)
class EnergyHomogenizer:
    """Reference tangent-plane energy-equivalence homogenizer.

    Computes an ``ABDStiffness`` by adding skin stiffness and member energy
    contributions over a ``CanonicalUnitCell``.
    """

    thresholds: ValidityThresholds = field(default_factory=ValidityThresholds)

    def compute(
        self,
        cell: CanonicalUnitCell,
        *,
        validity_context: ValidityContext | None = None,
    ) -> HomogenizationResult:
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
        stiffness = _stiffness_from_tangent(tangent, skin=cell.skin, metadata=metadata)
        diagnostics = _diagnostics(
            stiffness.C8, member_count=len(cell.members), cell_area=cell.area
        )
        diagnostics["energy_consistent"] = True
        return HomogenizationResult(
            stiffness=stiffness,
            validity=_validity_report(
                stiffness, context=validity_context, thresholds=self.thresholds
            ),
            diagnostics=diagnostics,
            assumptions=_assumptions_for_members(cell.members),
            source="energy",
        )


@dataclass(frozen=True, slots=True)
class DirectECHomogenizer:
    """Direct equilibrium-compatibility homogenizer for straight member families.

    Use this path for supported straight-family comparisons or accelerators,
    not as a replacement for the more general energy cell path.
    """

    thresholds: ValidityThresholds = field(default_factory=ValidityThresholds)

    def compute(
        self,
        *,
        skin: ABDStiffness,
        families: tuple[StiffenerFamily, ...],
        validity_context: ValidityContext | None = None,
        convention: StrainConvention = DEFAULT_STRAIN_CONVENTION,
    ) -> HomogenizationResult:
        family_tuple = tuple(families)
        if not family_tuple:
            msg = "DirectECHomogenizer requires at least one stiffener family."
            raise HomogenizationInputError(msg)
        if skin.convention != convention or convention != DEFAULT_STRAIN_CONVENTION:
            msg = (
                "DirectECHomogenizer currently supports Tensyl's default engineering-shear "
                "convention only."
            )
            raise HomogenizationInputError(msg)
        tangent = np.array(skin.C8, dtype=np.float64, copy=True)
        # The direct family path uses length density multiplicity / spacing in
        # place of finite member length divided by finite cell area.
        for family in family_tuple:
            tangent += (family.multiplicity / family.spacing) * member_tangent_density(family)
        metadata = dict(skin.metadata)
        metadata.update(
            {
                "source": "direct_ec_homogenizer",
                "family_count": len(family_tuple),
            }
        )
        stiffness = _stiffness_from_tangent(tangent, skin=skin, metadata=metadata)
        diagnostics = _diagnostics(stiffness.C8, member_count=len(family_tuple), cell_area=None)
        diagnostics["energy_consistent"] = True
        return HomogenizationResult(
            stiffness=stiffness,
            validity=_validity_report(
                stiffness, context=validity_context, thresholds=self.thresholds
            ),
            diagnostics=diagnostics,
            assumptions=_assumptions_for_members(family_tuple)
            + ("Direct EC families use member length density multiplicity / spacing.",),
            source="direct_ec",
        )


__all__ = [
    "DirectECHomogenizer",
    "EnergyHomogenizer",
    "HomogenizationFailure",
    "HomogenizationInputError",
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
