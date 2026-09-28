"""Checks that turn an ABD stiffness and scale data into a validity report."""

from __future__ import annotations

from types import MappingProxyType

import numpy as np

from tensyl.core.constitutive import ABDStiffness
from tensyl.core.typing import FloatArray
from tensyl.core.validity import ValidityContext, ValidityReport, ValidityThresholds

_ROUNDOFF_RELATIVE_TOLERANCE = float(64.0 * np.finfo(np.float64).eps)
_SPECTRAL_RELATIVE_TOLERANCE = _ROUNDOFF_RELATIVE_TOLERANCE


def _spectral_properties(matrix: FloatArray) -> tuple[FloatArray, float, int]:
    symmetric = 0.5 * (matrix + matrix.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
    scale = float(np.max(np.abs(eigenvalues)))
    tolerance = _SPECTRAL_RELATIVE_TOLERANCE * scale
    rank = 0 if scale == 0.0 else int(np.linalg.matrix_rank(symmetric, tol=tolerance))
    return eigenvalues, tolerance, rank


def _frobenius_norm(matrix: FloatArray) -> float:
    scale = float(np.max(np.abs(matrix)))
    return 0.0 if scale == 0.0 else scale * float(np.linalg.norm(matrix / scale))


def _normalized_coupling(A: FloatArray, B: FloatArray, D: FloatArray) -> float:
    norm_A = _frobenius_norm(A)
    norm_D = _frobenius_norm(D)
    norm_B = _frobenius_norm(B)
    if norm_A == 0.0 or norm_D == 0.0:
        return 0.0
    return float(norm_B / np.sqrt(norm_A) / np.sqrt(norm_D))


def _neutral_surface_offset(stiffness: ABDStiffness) -> float:
    weights = np.array([1.0, 1.0, np.sqrt(2.0)])
    A = weights[:, None] * stiffness.A * weights[None, :]
    B = weights[:, None] * stiffness.B * weights[None, :]
    scale = float(np.max(np.abs(A)))
    if scale == 0.0:
        # No membrane stiffness means there is no preferred neutral surface.
        return 0.0
    normalized_A = A / scale
    return float(np.sum(normalized_A * (B / scale)) / np.sum(normalized_A**2))


def _residual_coupling_ratio(stiffness: ABDStiffness) -> float:
    offset = _neutral_surface_offset(stiffness)
    residual_B = stiffness.B - offset * stiffness.A
    neutral_D = stiffness.D - offset * (stiffness.B + residual_B)
    weights = np.array([1.0, 1.0, np.sqrt(2.0)])
    # Mandel components use an orthonormal tensor basis. Engineering shear
    # components do not, so their unweighted norm changes with in-plane axes.
    return _normalized_coupling(
        weights[:, None] * stiffness.A * weights[None, :],
        weights[:, None] * residual_B * weights[None, :],
        weights[:, None] * neutral_D * weights[None, :],
    )


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

    coupling = _residual_coupling_ratio(stiffness)
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
        coupling_ratios=MappingProxyType(
            {
                "B_fro": _normalized_coupling(stiffness.A, stiffness.B, stiffness.D),
                "B_residual": coupling,
            }
        ),
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


__all__ = ["validity_report_for_stiffness"]
