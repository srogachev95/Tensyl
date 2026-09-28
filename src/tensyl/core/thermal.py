"""Thermal section loads per uniform temperature increment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tensyl.core._validation import finite_number, frozen_value, readonly_array
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.rotations import resultant_transform
from tensyl.core.typing import FloatArray, GeneralizedResultant, generalized_resultant


@dataclass(frozen=True, slots=True, eq=False)
class ThermalResultants:
    """Membrane and bending thermal loads per unit temperature change.

    ``r = C8 eta - [N_T, M_T, 0, 0] delta_temperature``. Positive thermal
    loads produce free expansion; full restraint gives their negatives.
    Components use the same frame, engineering ordering, and reference surface
    as the mechanical stiffness supplied separately.
    """

    N_T: FloatArray
    M_T: FloatArray
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION

    def __post_init__(self) -> None:
        for name in ("N_T", "M_T"):
            object.__setattr__(
                self, name, readonly_array(getattr(self, name), shape=(3,), name=name)
            )

    def _key(self) -> tuple[object, ...]:
        return frozen_value(self.N_T), frozen_value(self.M_T), self.frame, self.convention

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ThermalResultants):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())

    def equivalent_load(self, delta_temperature: float) -> GeneralizedResultant:
        """Return the load added to mechanical loads when solving for strain."""
        delta = finite_number(delta_temperature, name="delta_temperature")
        return generalized_resultant(np.concatenate((self.N_T, self.M_T, np.zeros(2))) * delta)

    def rotate(self, angle_rad: float) -> ThermalResultants:
        """Express loads in axes rotated counterclockwise about the normal."""
        transform = resultant_transform(angle_rad)
        return ThermalResultants(
            transform @ self.N_T,
            transform @ self.M_T,
            self.frame.rotate(angle_rad),
            self.convention,
        )

    def shift_reference_surface(self, offset: float) -> ThermalResultants:
        """Move the reference by offset along +n, giving M_T - offset*N_T."""
        distance = finite_number(offset, name="offset")
        return ThermalResultants(
            self.N_T, self.M_T - distance * self.N_T, self.frame, self.convention
        )


__all__ = ["ThermalResultants"]
