"""Beam-section stiffness value objects for Level 1 homogenization."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

import numpy as np


def _positive(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be finite and positive."
        raise ValueError(msg)
    return checked


def _optional_positive(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    return _positive(value, name=name)


def _finite(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{name} must be finite."
        raise ValueError(msg)
    return checked


@dataclass(frozen=True, slots=True)
class BeamSection:
    """Centroidal beam-section stiffnesses for a Level 1 stiffener member.

    ``EA`` is the axial stiffness, ``EIy`` is the out-of-plane bending stiffness,
    ``EIz`` is the in-plane bending stiffness retained for provenance, and
    ``GJ`` is the torsional stiffness. ``kGAy`` and ``kGAz`` are optional shear
    stiffnesses in the member-local in-plane transverse and normal directions.
    """

    EA: float
    EIy: float
    EIz: float
    GJ: float
    kGAy: float | None = None
    kGAz: float | None = None
    EIyz: float = 0.0
    metadata: dict[str, Any] | MappingProxyType[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "EA", _positive(self.EA, name="EA"))
        object.__setattr__(self, "EIy", _positive(self.EIy, name="EIy"))
        object.__setattr__(self, "EIz", _positive(self.EIz, name="EIz"))
        object.__setattr__(self, "GJ", _positive(self.GJ, name="GJ"))
        object.__setattr__(self, "kGAy", _optional_positive(self.kGAy, name="kGAy"))
        object.__setattr__(self, "kGAz", _optional_positive(self.kGAz, name="kGAz"))
        EIyz = _finite(self.EIyz, name="EIyz")
        if self.EIy * self.EIz - EIyz**2 <= 0.0:
            msg = "section bending stiffness block must be positive definite."
            raise ValueError(msg)
        object.__setattr__(self, "EIyz", EIyz)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


__all__ = ["BeamSection"]
