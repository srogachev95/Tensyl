"""Level 1 equivalent-wall homogenizers."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Protocol

import numpy as np

from tensyl.cells.level1 import BeamMember, CanonicalUnitCell, StiffenerFamily
from tensyl.core.constitutive import LinearABDWall
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


def _positive(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be finite and positive."
        raise ValueError(msg)
    return checked


def _optional_positive(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    return _positive(value, name=name)


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    matrix = np.array(values, dtype=np.float64, copy=True)
    if matrix.shape != shape:
        msg = f"{name} must have shape {shape}, got {matrix.shape}."
        raise ValueError(msg)
    if not np.all(np.isfinite(matrix)):
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    matrix.setflags(write=False)
    return matrix


@dataclass(frozen=True, slots=True)
class ValidityContext:
    """Optional geometric scale data for Level 1 validity checks."""

    characteristic_height: float | None = None
    pitch: float | None = None
    min_radius: float | None = None
    response_length: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "characteristic_height",
            _optional_positive(self.characteristic_height, name="characteristic_height"),
        )
        object.__setattr__(self, "pitch", _optional_positive(self.pitch, name="pitch"))
        object.__setattr__(
            self,
            "min_radius",
            _optional_positive(self.min_radius, name="min_radius"),
        )
        object.__setattr__(
            self,
            "response_length",
            _optional_positive(self.response_length, name="response_length"),
        )


@dataclass(frozen=True, slots=True)
class ValidityThresholds:
    """Default warning thresholds for Level 1 scale-separation checks."""

    h_over_R: float = 0.05
    p_over_R: float = 0.05
    p_over_L_response: float = 0.05
    coupling_ratio: float = 0.10

    def __post_init__(self) -> None:
        object.__setattr__(self, "h_over_R", _positive(self.h_over_R, name="h_over_R"))
        object.__setattr__(self, "p_over_R", _positive(self.p_over_R, name="p_over_R"))
        object.__setattr__(
            self,
            "p_over_L_response",
            _positive(self.p_over_L_response, name="p_over_L_response"),
        )
        object.__setattr__(
            self,
            "coupling_ratio",
            _positive(self.coupling_ratio, name="coupling_ratio"),
        )


@dataclass(frozen=True, slots=True)
class ValidityReport:
    """Machine-readable validity diagnostics attached to a homogenized result."""

    h_over_R: float | None
    p_over_R: float | None
    p_over_L_response: float | None
    coupling_ratios: MappingProxyType[str, float]
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
    """A Level 1 homogenization result and its verification context."""

    law: LinearABDWall
    validity: ValidityReport
    diagnostics: dict[str, Any] | MappingProxyType[str, Any]
    assumptions: tuple[str, ...]
    source: Literal["energy", "direct_ec", "rve", "imported"]

    def __post_init__(self) -> None:
        law = self.law
        if getattr(law, "validity", None) != self.validity:
            law = law.with_validity(self.validity)
        object.__setattr__(self, "law", law)
        object.__setattr__(self, "diagnostics", MappingProxyType(dict(self.diagnostics)))
        object.__setattr__(self, "assumptions", tuple(self.assumptions))


class Homogenizer(Protocol):
    """Protocol for Level 1 homogenizers."""

    def compute(
        self,
        cell: CanonicalUnitCell,
        *,
        validity_context: ValidityContext | None = None,
    ) -> HomogenizationResult:
        """Compute an equivalent wall law for a canonical unit cell."""


def _beam_strain_map(eccentricity: float) -> FloatArray:
    """Map member-frame generalized wall strains into simplified beam strains."""

    z = float(eccentricity)
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
    tangent = transform.T @ stiffness @ transform
    tangent = 0.5 * (tangent + tangent.T)
    tangent.setflags(write=False)
    return tangent


def member_tangent_contribution(member: BeamMember, *, cell_area: float) -> FloatArray:
    """Return one canonical member contribution to the wall tangent."""

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
        "Level 1 local tangent-plane homogenization.",
        "Centroidal beam-section stiffnesses with member eccentricity measured along +n.",
        "Beam members use first-approximation wall kinematics.",
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


def _coupling_ratio(law: LinearABDWall) -> float:
    norm_A = float(np.linalg.norm(law.A, ord="fro"))
    norm_D = float(np.linalg.norm(law.D, ord="fro"))
    norm_B = float(np.linalg.norm(law.B, ord="fro"))
    if norm_A == 0.0 or norm_D == 0.0:
        return 0.0
    return norm_B / float(np.sqrt(norm_A * norm_D))


def _validity_report(
    law: LinearABDWall,
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

    coupling = _coupling_ratio(law)
    if coupling >= thresholds.coupling_ratio:
        warnings.append("membrane_bending_coupling_exceeds_threshold")
    matrix = law.C8
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


def _wall_from_tangent(
    tangent: FloatArray,
    *,
    skin: LinearABDWall,
    metadata: dict[str, Any],
) -> LinearABDWall:
    matrix = 0.5 * (np.array(tangent, dtype=np.float64, copy=True) + np.array(tangent).T)
    return LinearABDWall.from_tangent(
        matrix,
        frame=skin.frame,
        convention=skin.convention,
        areal_mass=skin.areal_mass,
        metadata=metadata,
    )


@dataclass(frozen=True, slots=True)
class EnergyHomogenizer:
    """Reference Level 1 energy-equivalence homogenizer."""

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
        for member in cell.members:
            tangent += member_tangent_contribution(member, cell_area=cell.area)
        metadata = dict(cell.skin.metadata)
        metadata.update({"source": "energy_homogenizer", "cell": dict(cell.metadata)})
        law = _wall_from_tangent(tangent, skin=cell.skin, metadata=metadata)
        diagnostics = _diagnostics(law.C8, member_count=len(cell.members), cell_area=cell.area)
        diagnostics["energy_consistent"] = True
        return HomogenizationResult(
            law=law,
            validity=_validity_report(law, context=validity_context, thresholds=self.thresholds),
            diagnostics=diagnostics,
            assumptions=_assumptions_for_members(cell.members),
            source="energy",
        )


@dataclass(frozen=True, slots=True)
class DirectECHomogenizer:
    """Direct equilibrium-compatibility homogenizer for straight member families."""

    thresholds: ValidityThresholds = field(default_factory=ValidityThresholds)

    def compute(
        self,
        *,
        skin: LinearABDWall,
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
        for family in family_tuple:
            tangent += (family.multiplicity / family.spacing) * member_tangent_density(family)
        metadata = dict(skin.metadata)
        metadata.update(
            {
                "source": "direct_ec_homogenizer",
                "family_count": len(family_tuple),
            }
        )
        law = _wall_from_tangent(tangent, skin=skin, metadata=metadata)
        diagnostics = _diagnostics(law.C8, member_count=len(family_tuple), cell_area=None)
        diagnostics["energy_consistent"] = True
        return HomogenizationResult(
            law=law,
            validity=_validity_report(law, context=validity_context, thresholds=self.thresholds),
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
]
