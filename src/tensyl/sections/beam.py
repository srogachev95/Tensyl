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


@dataclass(frozen=True, slots=True)
class BeamSection:
    """Centroidal beam-section stiffnesses for a tangent-plane stiffener member.

    ``EA`` is the axial stiffness, ``EIy`` is the out-of-plane bending stiffness,
    ``EIz`` is the in-plane bending stiffness retained for provenance, and
    ``GJ`` is the torsional stiffness. ``kGAy`` and ``kGAz`` are optional shear
    stiffnesses in the member-local in-plane transverse and normal directions.
    Tensyl expects stiffness products in a consistent unit system; it does not
    calculate them from cross-section dimensions.
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
        object.__setattr__(self, "EA", positive_number(self.EA, name="EA"))
        object.__setattr__(self, "EIy", positive_number(self.EIy, name="EIy"))
        object.__setattr__(self, "EIz", positive_number(self.EIz, name="EIz"))
        object.__setattr__(self, "GJ", positive_number(self.GJ, name="GJ"))
        object.__setattr__(
            self,
            "kGAy",
            optional_positive_number(self.kGAy, name="kGAy"),
        )
        object.__setattr__(
            self,
            "kGAz",
            optional_positive_number(self.kGAz, name="kGAz"),
        )
        EIyz = finite_number(self.EIyz, name="EIyz")
        if self.EIy * self.EIz - EIyz**2 <= 0.0:
            msg = "section bending stiffness block must be positive definite."
            raise ValueError(msg)
        object.__setattr__(self, "EIyz", EIyz)
        object.__setattr__(self, "metadata", readonly_mapping(self.metadata))


__all__ = ["BeamSection"]
