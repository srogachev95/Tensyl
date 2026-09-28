"""Coordinate frames and generalized strain conventions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tensyl.core._validation import frozen_value, readonly_array
from tensyl.core.typing import FloatArray

_DEFAULT_TOLERANCE = 1.0e-10


def _readonly_vector(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(values, shape=(3,), name=name)


@dataclass(frozen=True, slots=True)
class Frame2D:
    """Right-handed orthonormal local frame.

    Attributes:
        e1: Unit basis vector for local direction 1.
        e2: Unit basis vector for local direction 2.
        n: Unit normal vector satisfying ``cross(e1, e2) == n``.
        label: Human-readable frame label carried into metadata.
    """

    e1: FloatArray
    e2: FloatArray
    n: FloatArray
    label: str = "local_tangent"

    def __post_init__(self) -> None:
        e1 = _readonly_vector(self.e1, name="e1")
        e2 = _readonly_vector(self.e2, name="e2")
        n = _readonly_vector(self.n, name="n")

        for name, vector in (("e1", e1), ("e2", e2), ("n", n)):
            norm = float(np.linalg.norm(vector))
            if not np.isclose(norm, 1.0, atol=_DEFAULT_TOLERANCE, rtol=0.0):
                msg = f"{name} must be unit length, got norm {norm}."
                raise ValueError(msg)

        if not np.isclose(float(e1 @ e2), 0.0, atol=_DEFAULT_TOLERANCE, rtol=0.0):
            msg = "e1 and e2 must be orthogonal."
            raise ValueError(msg)
        if not np.isclose(float(e1 @ n), 0.0, atol=_DEFAULT_TOLERANCE, rtol=0.0):
            msg = "e1 and n must be orthogonal."
            raise ValueError(msg)
        if not np.isclose(float(e2 @ n), 0.0, atol=_DEFAULT_TOLERANCE, rtol=0.0):
            msg = "e2 and n must be orthogonal."
            raise ValueError(msg)
        if not np.isclose(float(np.cross(e1, e2) @ n), 1.0, atol=_DEFAULT_TOLERANCE, rtol=0.0):
            msg = "frame must be right-handed: cross(e1, e2) must align with n."
            raise ValueError(msg)

        object.__setattr__(self, "e1", e1)
        object.__setattr__(self, "e2", e2)
        object.__setattr__(self, "n", n)

    def __hash__(self) -> int:
        return hash(
            (
                frozen_value(self.e1),
                frozen_value(self.e2),
                frozen_value(self.n),
                self.label,
            )
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Frame2D):
            return NotImplemented
        return (
            np.array_equal(self.e1, other.e1)
            and np.array_equal(self.e2, other.e2)
            and np.array_equal(self.n, other.n)
            and self.label == other.label
        )

    @classmethod
    def canonical(cls, *, label: str = "local_tangent") -> Frame2D:
        """Create the canonical Cartesian local frame.

        Args:
            label: Frame label for the returned object.

        Returns:
            Frame with ``e1 = x``, ``e2 = y``, and ``n = z``.
        """

        return cls(
            e1=np.array([1.0, 0.0, 0.0]),
            e2=np.array([0.0, 1.0, 0.0]),
            n=np.array([0.0, 0.0, 1.0]),
            label=label,
        )

    def rotate(self, angle_rad: float, *, label: str | None = None) -> Frame2D:
        """Return a frame rotated counterclockwise about ``n``.

        Args:
            angle_rad: Rotation angle in radians.
            label: Optional label for the rotated frame. Defaults to the
                current label.

        Returns:
            Rotated right-handed local frame.

        Raises:
            ValueError: If ``angle_rad`` is not finite.
        """

        angle = float(angle_rad)
        if not np.isfinite(angle):
            msg = "angle_rad must be finite."
            raise ValueError(msg)
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        return Frame2D(
            e1=c * self.e1 + s * self.e2,
            e2=-s * self.e1 + c * self.e2,
            n=self.n,
            label=self.label if label is None else label,
        )


@dataclass(frozen=True, slots=True)
class StrainConvention:
    """Generalized strain/resultant ordering for ABD stiffnesses.

    Attributes:
        membrane_order: Membrane strain/resultant names. Current public support
            is ``("e11", "e22", "g12")``.
        bending_order: Curvature/moment names. Current public support is
            ``("k11", "k22", "k12")``.
        shear_order: Transverse-shear strain/resultant names. Current public
            support is ``("g13", "g23")``.
        engineering_shear: Whether shear strains are engineering shear strains.
            Current public support requires ``True``.
        reference_surface: Name of the reference surface for bending and
            coupling terms.
        normal_positive: Positive normal convention. Current public support is
            ``"+n"``.
    """

    membrane_order: tuple[str, str, str] = ("e11", "e22", "g12")
    bending_order: tuple[str, str, str] = ("k11", "k22", "k12")
    shear_order: tuple[str, str] = ("g13", "g23")
    engineering_shear: bool = True
    reference_surface: str = "mid_surface"
    normal_positive: str = "+n"

    def __post_init__(self) -> None:
        if self.membrane_order != ("e11", "e22", "g12"):
            msg = "Phase 1 supports membrane_order ('e11', 'e22', 'g12') only."
            raise ValueError(msg)
        if self.bending_order != ("k11", "k22", "k12"):
            msg = "Phase 1 supports bending_order ('k11', 'k22', 'k12') only."
            raise ValueError(msg)
        if self.shear_order != ("g13", "g23"):
            msg = "Phase 1 supports shear_order ('g13', 'g23') only."
            raise ValueError(msg)
        if not self.engineering_shear:
            msg = "Phase 1 supports engineering shear strains only."
            raise ValueError(msg)
        if not self.reference_surface:
            msg = "reference_surface must be non-empty."
            raise ValueError(msg)
        if self.normal_positive != "+n":
            msg = "Phase 1 supports normal_positive '+n' only."
            raise ValueError(msg)


DEFAULT_FRAME = Frame2D.canonical()
DEFAULT_STRAIN_CONVENTION = StrainConvention()

__all__ = ["DEFAULT_FRAME", "DEFAULT_STRAIN_CONVENTION", "Frame2D", "StrainConvention"]
