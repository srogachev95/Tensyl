"""Private validation and immutable-array helpers."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

import numpy as np
from numpy.typing import NDArray

Float64Array = NDArray[np.float64]


def finite_number(value: float, *, name: str) -> float:
    """Return ``value`` as a finite float."""

    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{name} must be finite."
        raise ValueError(msg)
    return checked


def positive_number(
    value: float,
    *,
    name: str,
    finite_and_positive_message: bool = True,
) -> float:
    """Return ``value`` as a positive finite float."""

    checked = float(value)
    if not np.isfinite(checked) or checked <= 0.0:
        suffix = "finite and positive" if finite_and_positive_message else "positive"
        msg = f"{name} must be {suffix}."
        raise ValueError(msg)
    return checked


def nonnegative_number(value: float, *, name: str) -> float:
    """Return ``value`` as a nonnegative finite float."""

    checked = float(value)
    if not np.isfinite(checked) or checked < 0.0:
        msg = f"{name} must be finite and nonnegative."
        raise ValueError(msg)
    return checked


def optional_positive_number(value: float | None, *, name: str) -> float | None:
    """Return ``None`` or a positive finite float."""

    if value is None:
        return None
    return positive_number(value, name=name)


def optional_nonnegative_number(value: float | None, *, name: str) -> float | None:
    """Return ``None`` or a nonnegative finite float."""

    if value is None:
        return None
    return nonnegative_number(value, name=name)


def readonly_array(
    values: Any,
    *,
    shape: tuple[int, ...],
    name: str,
) -> Float64Array:
    """Return a finite read-only float64 array with the requested shape."""

    array = np.array(values, dtype=np.float64, copy=True)
    if array.shape != shape:
        msg = f"{name} must have shape {shape}, got {array.shape}."
        raise ValueError(msg)
    if not np.all(np.isfinite(array)):
        msg = f"{name} must contain only finite values."
        raise ValueError(msg)
    array.setflags(write=False)
    return array


def normalized_vector3(values: Any, *, name: str, tolerance: float) -> Float64Array:
    """Return a finite read-only normalized 3-vector."""

    vector = readonly_array(values, shape=(3,), name=name).copy()
    norm = float(np.linalg.norm(vector))
    if norm <= tolerance:
        msg = f"{name} must have nonzero length."
        raise ValueError(msg)
    vector /= norm
    vector.setflags(write=False)
    return vector


def readonly_mapping(mapping: Mapping[str, Any]) -> MappingProxyType[str, Any]:
    """Return a shallow read-only copy of ``mapping``."""

    return MappingProxyType(dict(mapping))


def frozen_value(value: Any) -> Any:
    """Return a hashable, comparable stand-in for nested metadata values."""

    # Metadata can contain nested NumPy arrays from verification or import
    # paths. Freeze the semantic payload instead of falling back to object ids,
    # so equal values hash equally and compare without array truth-value errors.
    if isinstance(value, Mapping):
        return tuple(sorted((key, frozen_value(item)) for key, item in value.items()))
    if isinstance(value, np.ndarray):
        array = np.ascontiguousarray(value)
        if np.issubdtype(array.dtype, np.floating):
            # -0.0 == 0.0 but their bytes differ; normalize so equal values
            # always hash equally.
            array = array + 0.0
        return ("ndarray", array.shape, array.dtype.str, array.tobytes())
    if isinstance(value, (list, tuple)):
        return tuple(frozen_value(item) for item in value)
    if isinstance(value, (set, frozenset)):
        return tuple(sorted(frozen_value(item) for item in value))
    try:
        hash(value)
    except TypeError:
        return repr(value)
    return value


__all__ = [
    "finite_number",
    "frozen_value",
    "nonnegative_number",
    "normalized_vector3",
    "optional_nonnegative_number",
    "optional_positive_number",
    "positive_number",
    "readonly_array",
    "readonly_mapping",
]
