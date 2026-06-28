"""Metrics for validation cases."""

from __future__ import annotations

from typing import Any

import numpy as np

from tensyl import ABDStiffness, IsotropicMaterial


def _block_summary(matrix: np.ndarray) -> dict[str, float]:
    return {
        "frobenius_norm": float(np.linalg.norm(matrix)),
        "max_abs": float(np.max(np.abs(matrix))),
        "trace": float(np.trace(matrix)),
    }


def _relative_error(actual: float, expected: float) -> float:
    scale = max(abs(expected), 1.0)
    return abs(actual - expected) / scale


def _relative_matrix_error(actual: np.ndarray, expected: np.ndarray) -> float:
    scale = max(float(np.linalg.norm(expected)), 1.0)
    return float(np.linalg.norm(actual - expected) / scale)


def abd_comparison_metrics(
    actual: np.ndarray,
    expected: np.ndarray,
    *,
    case_name: str,
) -> dict[str, Any]:
    """Compare two canonical C8 stiffness matrices."""

    actual_c8 = np.asarray(actual, dtype=np.float64)
    expected_c8 = np.asarray(expected, dtype=np.float64)
    if actual_c8.shape != (8, 8):
        msg = f"actual stiffness must have shape (8, 8), got {actual_c8.shape}."
        raise ValueError(msg)
    if expected_c8.shape != (8, 8):
        msg = f"expected stiffness must have shape (8, 8), got {expected_c8.shape}."
        raise ValueError(msg)
    delta = actual_c8 - expected_c8
    return {
        "schema_version": "tensyl.validation.abd-comparison-metrics.v1",
        "case_name": case_name,
        "checks": {
            "C8_relative_frobenius_error": _relative_matrix_error(actual_c8, expected_c8),
            "A_relative_frobenius_error": _relative_matrix_error(
                actual_c8[:3, :3],
                expected_c8[:3, :3],
            ),
            "B_relative_frobenius_error": _relative_matrix_error(
                actual_c8[:3, 3:6],
                expected_c8[:3, 3:6],
            ),
            "D_relative_frobenius_error": _relative_matrix_error(
                actual_c8[3:6, 3:6],
                expected_c8[3:6, 3:6],
            ),
            "As_relative_frobenius_error": _relative_matrix_error(
                actual_c8[6:8, 6:8],
                expected_c8[6:8, 6:8],
            ),
            "max_abs_entry_error": float(np.max(np.abs(delta))),
            "symmetric_actual_C8": bool(np.allclose(actual_c8, actual_c8.T)),
        },
    }


def abd6_comparison_metrics(
    actual: np.ndarray,
    expected: np.ndarray,
    *,
    case_name: str,
) -> dict[str, Any]:
    """Compare two membrane/bending ABD stiffness matrices."""

    actual_abd = np.asarray(actual, dtype=np.float64)
    expected_abd = np.asarray(expected, dtype=np.float64)
    if actual_abd.shape != (6, 6):
        msg = f"actual ABD stiffness must have shape (6, 6), got {actual_abd.shape}."
        raise ValueError(msg)
    if expected_abd.shape != (6, 6):
        msg = f"expected ABD stiffness must have shape (6, 6), got {expected_abd.shape}."
        raise ValueError(msg)
    delta = actual_abd - expected_abd
    return {
        "schema_version": "tensyl.validation.abd6-comparison-metrics.v1",
        "case_name": case_name,
        "checks": {
            "ABD6_relative_frobenius_error": _relative_matrix_error(actual_abd, expected_abd),
            "A_relative_frobenius_error": _relative_matrix_error(
                actual_abd[:3, :3],
                expected_abd[:3, :3],
            ),
            "B_relative_frobenius_error": _relative_matrix_error(
                actual_abd[:3, 3:6],
                expected_abd[:3, 3:6],
            ),
            "D_relative_frobenius_error": _relative_matrix_error(
                actual_abd[3:6, 3:6],
                expected_abd[3:6, 3:6],
            ),
            "max_abs_entry_error": float(np.max(np.abs(delta))),
            "symmetric_actual_ABD6": bool(np.allclose(actual_abd, actual_abd.T)),
        },
    }


def skin_only_metrics(
    stiffness: ABDStiffness,
    *,
    material: IsotropicMaterial,
    thickness: float,
) -> dict[str, Any]:
    """Return compact confirmation metrics for an isotropic skin-only plate."""

    q11 = material.E / (1.0 - material.nu**2)
    q12 = material.nu * q11
    q66 = material.E / (2.0 * (1.0 + material.nu))
    expected_a11 = q11 * thickness
    expected_a12 = q12 * thickness
    expected_a66 = q66 * thickness
    expected_d11 = q11 * thickness**3 / 12.0

    return {
        "case_type": "skin_only_isotropic",
        "blocks": {
            "A": _block_summary(stiffness.A),
            "B": _block_summary(stiffness.B),
            "D": _block_summary(stiffness.D),
            "As": _block_summary(stiffness.As),
        },
        "checks": {
            "A11_relative_error": _relative_error(float(stiffness.A[0, 0]), expected_a11),
            "A12_relative_error": _relative_error(float(stiffness.A[0, 1]), expected_a12),
            "A66_relative_error": _relative_error(float(stiffness.A[2, 2]), expected_a66),
            "D11_relative_error": _relative_error(float(stiffness.D[0, 0]), expected_d11),
            "max_abs_B": float(np.max(np.abs(stiffness.B))),
            "symmetric_ABD": bool(np.allclose(stiffness.C8[:6, :6], stiffness.C8[:6, :6].T)),
        },
        "units": {
            "A": "force/length",
            "B": "force",
            "D": "force*length",
            "As": "force/length",
        },
    }
