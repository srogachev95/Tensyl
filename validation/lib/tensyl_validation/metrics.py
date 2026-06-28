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
