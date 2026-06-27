"""Beam-section stiffness value objects for tangent-plane homogenization."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from tensyl.core._validation import (
    finite_number,
    optional_positive_number,
    positive_number,
    readonly_mapping,
)


def _positive(value: float, *, name: str) -> float:
    return positive_number(value, name=name)


def _optional_positive(value: float | None, *, name: str) -> float | None:
    return optional_positive_number(value, name=name)


def _finite(value: float, *, name: str) -> float:
    return finite_number(value, name=name)


@dataclass(frozen=True, slots=True)
class BeamSection:
    """Centroidal beam-section stiffnesses for a tangent-plane stiffener member.

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
    metadata: Mapping[str, Any] = field(default_factory=dict)

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
        object.__setattr__(self, "metadata", readonly_mapping(self.metadata))


__all__ = ["BeamSection"]
