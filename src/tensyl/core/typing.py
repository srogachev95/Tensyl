"""Shared typing aliases and public generalized-vector wrappers."""

from __future__ import annotations

from typing import Any, NewType

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]
GeneralizedStrain = NewType("GeneralizedStrain", np.ndarray[Any, np.dtype[np.float64]])
GeneralizedResultant = NewType("GeneralizedResultant", np.ndarray[Any, np.dtype[np.float64]])


def _readonly_generalized_vector(values: FloatArray, *, name: str) -> FloatArray:
    vector = np.array(values, dtype=np.float64, copy=True)
    if vector.shape != (8,):
        msg = f"{name} must have shape (8,), got {vector.shape}."
        raise ValueError(msg)
    if not np.all(np.isfinite(vector)):
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    vector.setflags(write=False)
    return vector


def generalized_strain(values: Any) -> GeneralizedStrain:
    """Return a read-only generalized strain vector.

    The runtime value is still a NumPy array, but the public type is distinct
    from resultants for static checkers.
    """

    return GeneralizedStrain(_readonly_generalized_vector(values, name="eta"))


def generalized_resultant(values: Any) -> GeneralizedResultant:
    """Return a read-only generalized resultant vector."""

    return GeneralizedResultant(_readonly_generalized_vector(values, name="resultant"))


__all__ = [
    "FloatArray",
    "GeneralizedResultant",
    "GeneralizedStrain",
    "generalized_resultant",
    "generalized_strain",
]
