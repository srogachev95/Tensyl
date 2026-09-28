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


__all__ = ["validity_report_for_stiffness"]
