"""Shared typing aliases for Tensyl arrays."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float64]

__all__ = ["FloatArray"]
