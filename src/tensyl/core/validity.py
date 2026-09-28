"""Tangent-plane validity data attached to ABD stiffnesses.

These value types live in ``core`` so an ``ABDStiffness`` can carry a typed
``ValidityReport`` without the core package depending on the homogenizers
that usually produce one. The checks that build a report live in
``tensyl.core.validity_checks``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

import numpy as np

from tensyl.core._validation import frozen_value, optional_positive_number, positive_number


def _optional_positive_or_inf(value: float | None, *, name: str) -> float | None:
    if value is None:
        return None
    checked = float(value)
    if checked == np.inf:
        return checked
    return positive_number(checked, name=name)


@dataclass(frozen=True, slots=True)
class ValidityContext:
    """Optional geometric scale data for tangent-plane validity checks.

    ``characteristic_height`` is a stiffness or stiffener height scale, ``pitch`` is
    the repeated-cell spacing, ``min_radius`` is the smallest local curvature
    radius, and ``response_length`` is the intended structural response length
    such as a buckle wavelength or analysis feature size.

    Attributes:
        characteristic_height: Optional positive member or wall height scale.
        pitch: Optional positive repeated-cell pitch.
        min_radius: Optional positive curvature radius, or infinity for flat
            geometry.
        response_length: Optional positive structural response length.
    """

    characteristic_height: float | None = None
    pitch: float | None = None
    min_radius: float | None = None
    response_length: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "characteristic_height",
            optional_positive_number(self.characteristic_height, name="characteristic_height"),
        )
        object.__setattr__(self, "pitch", optional_positive_number(self.pitch, name="pitch"))
        object.__setattr__(
            self,
            "min_radius",
            _optional_positive_or_inf(self.min_radius, name="min_radius"),
        )
        object.__setattr__(
            self,
            "response_length",
            optional_positive_number(self.response_length, name="response_length"),
        )


@dataclass(frozen=True, slots=True)
class ValidityThresholds:
    """Warning thresholds for tangent-plane scale-separation checks.

    Attributes:
        h_over_R: Warning threshold for height over curvature radius.
        p_over_R: Warning threshold for pitch over curvature radius.
        p_over_L_response: Warning threshold for pitch over response length.
        coupling_ratio: Warning threshold for normalized coupling terms.
    """

    h_over_R: float = 0.05
    p_over_R: float = 0.05
    p_over_L_response: float = 0.05
    coupling_ratio: float = 0.10

    def __post_init__(self) -> None:
        object.__setattr__(self, "h_over_R", positive_number(self.h_over_R, name="h_over_R"))
        object.__setattr__(self, "p_over_R", positive_number(self.p_over_R, name="p_over_R"))
        object.__setattr__(
            self,
            "p_over_L_response",
            positive_number(self.p_over_L_response, name="p_over_L_response"),
        )
        object.__setattr__(
            self,
            "coupling_ratio",
            positive_number(self.coupling_ratio, name="coupling_ratio"),
        )


@dataclass(frozen=True, slots=True)
class ValidityReport:
    """Machine-readable validity diagnostics attached to a result.

    Attributes:
        h_over_R: Height-to-radius ratio when both inputs were available.
        p_over_R: Pitch-to-radius ratio when both inputs were available.
        p_over_L_response: Pitch-to-response-length ratio when both inputs
            were available.
        coupling_ratios: Named normalized coupling indicators.
        warnings: Stable warning identifiers for violated checks.
    """

    h_over_R: float | None
    p_over_R: float | None
    p_over_L_response: float | None
    coupling_ratios: Mapping[str, float]
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("h_over_R", "p_over_R", "p_over_L_response"):
            value = getattr(self, name)
            if value is not None and (not np.isfinite(value) or value < 0.0):
                msg = f"{name} must be finite and nonnegative when provided."
                raise ValueError(msg)
        object.__setattr__(self, "coupling_ratios", MappingProxyType(dict(self.coupling_ratios)))
        object.__setattr__(self, "warnings", tuple(self.warnings))

    def _key(self) -> tuple[object, ...]:
        # MappingProxyType is not hashable; compare and hash the sorted ratios
        # instead so reports can sit inside hashed stiffness values.
        return (
            self.h_over_R,
            self.p_over_R,
            self.p_over_L_response,
            frozen_value(self.coupling_ratios),
            self.warnings,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValidityReport):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())


__all__ = [
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
]
