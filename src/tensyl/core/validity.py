"""Tangent-plane validity diagnostics attached to ABD stiffnesses.

These types live in ``core`` so an ``ABDStiffness`` can carry a typed
``ValidityReport`` without the core package depending on the homogenizers
that usually produce one.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

import numpy as np

from tensyl.core._validation import frozen_value, optional_positive_number, positive_number
from tensyl.core.typing import FloatArray

if TYPE_CHECKING:
    from tensyl.core.constitutive import ABDStiffness

_ROUNDOFF_RELATIVE_TOLERANCE = float(64.0 * np.finfo(np.float64).eps)
_SPECTRAL_RELATIVE_TOLERANCE = _ROUNDOFF_RELATIVE_TOLERANCE


def _optional_positive_or_inf(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    checked = float(value)
    if checked == np.inf:
        return checked
    return positive_number(checked, name=name)


@dataclass(frozen=True, slots=True)
class ValidityContext:
    """Optional geometric scale data for tangent-plane validity checks.

    ``characteristic_height`` is a stiffness or stiffener height scale, ``pitch`` is
    the repeated-cell spacing, ``min_radius`` is the smallest local curvature
    radius, and ``response_length`` is the intended structural response length
    such as a buckle wavelength or analysis feature size.

    Attributes:
        characteristic_height: Optional positive member or wall height scale.
        pitch: Optional positive repeated-cell pitch.
        min_radius: Optional positive curvature radius, or infinity for flat
            geometry.
        response_length: Optional positive structural response length.
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
    """Warning thresholds for tangent-plane scale-separation checks.

    Attributes:
        h_over_R: Warning threshold for height over curvature radius.
        p_over_R: Warning threshold for pitch over curvature radius.
        p_over_L_response: Warning threshold for pitch over response length.
        coupling_ratio: Warning threshold for normalized coupling terms.
    """

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
    """Machine-readable validity diagnostics attached to a result.

    Attributes:
        h_over_R: Height-to-radius ratio when both inputs were available.
        p_over_R: Pitch-to-radius ratio when both inputs were available.
        p_over_L_response: Pitch-to-response-length ratio when both inputs
            were available.
        coupling_ratios: Named normalized coupling indicators.
        warnings: Stable warning identifiers for violated checks.
    """

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

    def __hash__(self) -> int:
        # MappingProxyType is not hashable; hash the sorted ratios instead so
        # reports can sit inside hashed stiffness values.
        return hash(
            (
                self.h_over_R,
                self.p_over_R,
                self.p_over_L_response,
                frozen_value(self.coupling_ratios),
                self.warnings,
            )
        )


def _spectral_properties(matrix: FloatArray) -> tuple[FloatArray, float, int]:
    symmetric = 0.5 * (matrix + matrix.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
    scale = float(np.max(np.abs(eigenvalues)))
    tolerance = _SPECTRAL_RELATIVE_TOLERANCE * scale
    rank = 0 if scale == 0.0 else int(np.linalg.matrix_rank(symmetric, tol=tolerance))
    return eigenvalues, tolerance, rank


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
    eigenvalues, spectral_tolerance, rank = _spectral_properties(matrix)
    if rank < matrix.shape[0]:
        warnings.append("rank_deficient_tangent")
    if float(eigenvalues[0]) < -spectral_tolerance:
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
    """Return tangent-plane validity diagnostics for existing stiffness.

    Args:
        stiffness: ABD stiffness to inspect.
        context: Optional geometric and response length scales.
        thresholds: Optional warning thresholds. Defaults are used when omitted.

    Returns:
        Validity report with scale-separation ratios, coupling indicators, and
        warning identifiers.
    """

    return _validity_report(
        stiffness,
        context=context,
        thresholds=ValidityThresholds() if thresholds is None else thresholds,
    )


__all__ = [
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
    "validity_report_for_stiffness",
]
