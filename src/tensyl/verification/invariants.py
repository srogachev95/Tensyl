"""Reusable mechanics invariant checks."""

from __future__ import annotations

from typing import Any

import numpy as np

from tensyl.core.constitutive import HyperelasticModel
from tensyl.core.typing import FloatArray, generalized_strain


def finite_difference_gradient(
    stiffness: HyperelasticModel,
    eta: Any,
    *,
    step: float = 1.0e-6,
) -> FloatArray:
    """Return a central-difference approximation to ``grad(W)(eta)``.

    Args:
        stiffness: Hyperelastic model whose energy is differentiated.
        eta: Generalized strain vector at which to evaluate the gradient.
        step: Positive finite-difference step.

    Returns:
        Read-only length-8 gradient approximation.

    Raises:
        ValueError: If ``eta`` is not a valid generalized strain vector.
    """

    center = np.array(generalized_strain(eta), dtype=np.float64, copy=True)
    gradient = np.zeros(8, dtype=np.float64)
    for index in range(8):
        delta = np.zeros(8, dtype=np.float64)
        delta[index] = step
        gradient[index] = (
            stiffness.energy(generalized_strain(center + delta))
            - stiffness.energy(generalized_strain(center - delta))
        ) / (2.0 * step)
    gradient.setflags(write=False)
    return gradient


def finite_difference_hessian(
    stiffness: HyperelasticModel,
    eta: Any,
    *,
    step: float = 1.0e-5,
) -> FloatArray:
    """Return a central-difference approximation to ``hessian(W)(eta)``.

    Args:
        stiffness: Hyperelastic model whose resultants are differentiated.
        eta: Generalized strain vector at which to evaluate the Hessian.
        step: Positive finite-difference step.

    Returns:
        Read-only 8x8 Hessian approximation.

    Raises:
        ValueError: If ``eta`` is not a valid generalized strain vector.
    """

    center = np.array(generalized_strain(eta), dtype=np.float64, copy=True)
    hessian = np.zeros((8, 8), dtype=np.float64)
    for index in range(8):
        delta = np.zeros(8, dtype=np.float64)
        delta[index] = step
        plus = stiffness.resultants(generalized_strain(center + delta))
        minus = stiffness.resultants(generalized_strain(center - delta))
        hessian[:, index] = (np.asarray(plus) - np.asarray(minus)) / (2.0 * step)
    hessian = 0.5 * (hessian + hessian.T)
    hessian.setflags(write=False)
    return hessian


def assert_hyperelastic_consistency(
    stiffness: HyperelasticModel,
    eta: Any,
    *,
    gradient_rtol: float = 1.0e-5,
    gradient_atol: float = 1.0e-7,
    hessian_rtol: float = 1.0e-4,
    hessian_atol: float = 1.0e-6,
) -> None:
    """Assert that energy, resultants, and tangent form a derivative tower.

    Args:
        stiffness: Hyperelastic model to check.
        eta: Generalized strain vector at which to check consistency.
        gradient_rtol: Relative tolerance for gradient/resultant agreement.
        gradient_atol: Absolute tolerance for gradient/resultant agreement.
        hessian_rtol: Relative tolerance for Hessian/tangent agreement.
        hessian_atol: Absolute tolerance for Hessian/tangent agreement.

    Raises:
        AssertionError: If finite differences do not match the model
            resultants or tangent within tolerance.
        ValueError: If ``eta`` is not a valid generalized strain vector.
    """

    checked_eta = generalized_strain(eta)
    np.testing.assert_allclose(
        finite_difference_gradient(stiffness, checked_eta),
        np.asarray(stiffness.resultants(checked_eta)),
        rtol=gradient_rtol,
        atol=gradient_atol,
    )
    np.testing.assert_allclose(
        finite_difference_hessian(stiffness, checked_eta),
        stiffness.tangent(checked_eta),
        rtol=hessian_rtol,
        atol=hessian_atol,
    )


__all__ = [
    "assert_hyperelastic_consistency",
    "finite_difference_gradient",
    "finite_difference_hessian",
]
