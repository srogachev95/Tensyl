"""Shared typing aliases and public generalized-vector wrappers."""

from __future__ import annotations

from typing import Any, NewType

import numpy as np
from numpy.typing import NDArray

from tensyl.core._validation import readonly_array

FloatArray = NDArray[np.float64]
GeneralizedStrain = NewType("GeneralizedStrain", np.ndarray[Any, np.dtype[np.float64]])
GeneralizedResultant = NewType("GeneralizedResultant", np.ndarray[Any, np.dtype[np.float64]])


def _readonly_generalized_vector(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(values, shape=(8,), name=name)


def generalized_strain(values: Any) -> GeneralizedStrain:
    """Return a read-only generalized strain vector.

    The runtime value is still a NumPy array, but the public type is distinct
    from resultants for static checkers.

    Args:
        values: Array-like generalized strain values with shape ``(8,)``.

    Returns:
        Read-only generalized strain vector.

    Raises:
        ValueError: If ``values`` cannot be read as a finite vector with shape
            ``(8,)``.
    """

    return GeneralizedStrain(_readonly_generalized_vector(values, name="eta"))


def generalized_resultant(values: Any) -> GeneralizedResultant:
    """Return a read-only generalized resultant vector.

    Args:
        values: Array-like generalized resultant values with shape ``(8,)``.

    Returns:
        Read-only generalized resultant vector.

    Raises:
        ValueError: If ``values`` cannot be read as a finite vector with shape
            ``(8,)``.
    """

    return GeneralizedResultant(_readonly_generalized_vector(values, name="resultant"))


__all__ = [
    "FloatArray",
    "GeneralizedResultant",
    "GeneralizedStrain",
    "generalized_resultant",
    "generalized_strain",
]
