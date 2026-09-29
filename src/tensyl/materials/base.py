"""Elastic materials for plate, laminate, and rib stiffness calculations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from tensyl.core._validation import finite_number, optional_nonnegative_number, positive_number
from tensyl.core.typing import FloatArray


@dataclass(frozen=True, slots=True)
class IsotropicMaterial:
    """Plane-stress isotropic material.

    Attributes:
        E: Positive Young's modulus.
        nu: Poisson ratio satisfying ``-1 < nu < 0.5``.
        density: Optional nonnegative mass per volume (kg/m³ for SI inputs). Plate
            builders use it to calculate mass per area.
        alpha: Optional thermal expansion per temperature increment; None is unknown.
    """

    E: float
    nu: float
    density: float | None = None
    alpha: float | None = None

    def __post_init__(self) -> None:
        if self.alpha is not None:
            object.__setattr__(self, "alpha", finite_number(self.alpha, name="alpha"))
        E = positive_number(self.E, name="E")
        nu = float(self.nu)
        if not np.isfinite(nu) or not -1.0 < nu < 0.5:
            msg = "nu must be finite and satisfy -1 < nu < 0.5."
            raise ValueError(msg)
        object.__setattr__(self, "E", E)
        object.__setattr__(self, "nu", nu)
        object.__setattr__(
            self,
            "density",
            optional_nonnegative_number(self.density, name="density"),
        )

    @property
    def G(self) -> float:
        """Return the isotropic shear modulus.

        Returns:
            ``E / (2 * (1 + nu))`` in the same unit system as ``E``.
        """

        return self.E / (2.0 * (1.0 + self.nu))

    def plane_stress_stiffness(self) -> FloatArray:
        """Return the reduced plane-stress stiffness matrix.

        Returns:
            Read-only 3x3 matrix in engineering shear order
            ``(e11, e22, g12)``.
        """

        factor = self.E / (1.0 - self.nu**2)
        Q = factor * np.array(
            [
                [1.0, self.nu, 0.0],
                [self.nu, 1.0, 0.0],
                [0.0, 0.0, (1.0 - self.nu) / 2.0],
            ],
            dtype=np.float64,
        )
        Q.setflags(write=False)
        return Q


@dataclass(frozen=True, slots=True)
class OrthotropicPlyMaterial:
    """Orthotropic lamina material in local ``1-2-n`` axes.

    Attributes:
        E1: Positive Young's modulus in the material 1 direction.
        E2: Positive Young's modulus in the material 2 direction.
        G12: Positive in-plane shear modulus.
        nu12: Major Poisson ratio. The reciprocal ratio is inferred from minor
            symmetry.
        G13: Positive transverse-shear modulus in the 1-n plane.
        G23: Positive transverse-shear modulus in the 2-n plane.
        density: Optional nonnegative mass per volume (kg/m³ for SI inputs).
        alpha1: Optional expansion along material direction 1, per temperature increment.
        alpha2: Optional expansion along material direction 2, per temperature increment.
    """

    E1: float
    E2: float
    G12: float
    nu12: float
    G13: float
    G23: float
    density: float | None = None
    alpha1: float | None = None
    alpha2: float | None = None

    def __post_init__(self) -> None:
        for name in ("alpha1", "alpha2"):
            value = getattr(self, name)
            if value is not None:
                object.__setattr__(self, name, finite_number(value, name=name))
        E1 = positive_number(self.E1, name="E1")
        E2 = positive_number(self.E2, name="E2")
        G12 = positive_number(self.G12, name="G12")
        G13 = positive_number(self.G13, name="G13")
        G23 = positive_number(self.G23, name="G23")
        nu12 = float(self.nu12)
        if not np.isfinite(nu12):
            msg = "nu12 must be finite."
            raise ValueError(msg)
        nu21 = nu12 * E2 / E1
        if 1.0 - nu12 * nu21 <= 0.0:
            msg = "orthotropic plane-stress stiffness must be positive definite."
            raise ValueError(msg)
        object.__setattr__(self, "E1", E1)
        object.__setattr__(self, "E2", E2)
        object.__setattr__(self, "G12", G12)
        object.__setattr__(self, "nu12", nu12)
        object.__setattr__(self, "G13", G13)
        object.__setattr__(self, "G23", G23)
        object.__setattr__(
            self,
            "density",
            optional_nonnegative_number(self.density, name="density"),
        )

    @property
    def nu21(self) -> float:
        """Return the reciprocal Poisson ratio from minor symmetry.

        Returns:
            ``nu12 * E2 / E1``.
        """

        return self.nu12 * self.E2 / self.E1

    def reduced_stiffness(self) -> FloatArray:
        """Return local lamina reduced stiffness.

        Returns:
            Read-only 3x3 plane-stress stiffness matrix in engineering shear
            order ``(e11, e22, g12)``.
        """

        denom = 1.0 - self.nu12 * self.nu21
        Q = np.array(
            [
                [self.E1 / denom, self.nu12 * self.E2 / denom, 0.0],
                [self.nu12 * self.E2 / denom, self.E2 / denom, 0.0],
                [0.0, 0.0, self.G12],
            ],
            dtype=np.float64,
        )
        Q.setflags(write=False)
        return Q

    def transformed_reduced_stiffness(self, angle_rad: float) -> FloatArray:
        """Return transformed in-plane reduced stiffness for a ply angle.

        Args:
            angle_rad: Ply angle from the local 1 direction to the laminate
                frame, in radians.

        Returns:
            Read-only transformed 3x3 reduced stiffness matrix.

        Raises:
            ValueError: If ``angle_rad`` is not finite.
        """

        angle = float(angle_rad)
        if not np.isfinite(angle):
            msg = "angle_rad must be finite."
            raise ValueError(msg)
        Q11, Q12, Q22, Q66 = (
            self.reduced_stiffness()[0, 0],
            self.reduced_stiffness()[0, 1],
            self.reduced_stiffness()[1, 1],
            self.reduced_stiffness()[2, 2],
        )
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        c2 = c * c
        s2 = s * s
        c4 = c2 * c2
        s4 = s2 * s2
        c3s = c2 * c * s
        cs3 = c * s2 * s
        c2s2 = c2 * s2
        Qbar = np.array(
            [
                [
                    Q11 * c4 + 2.0 * (Q12 + 2.0 * Q66) * c2s2 + Q22 * s4,
                    (Q11 + Q22 - 4.0 * Q66) * c2s2 + Q12 * (c4 + s4),
                    (Q11 - Q12 - 2.0 * Q66) * c3s - (Q22 - Q12 - 2.0 * Q66) * cs3,
                ],
                [
                    (Q11 + Q22 - 4.0 * Q66) * c2s2 + Q12 * (c4 + s4),
                    Q11 * s4 + 2.0 * (Q12 + 2.0 * Q66) * c2s2 + Q22 * c4,
                    (Q11 - Q12 - 2.0 * Q66) * cs3 - (Q22 - Q12 - 2.0 * Q66) * c3s,
                ],
                [
                    (Q11 - Q12 - 2.0 * Q66) * c3s - (Q22 - Q12 - 2.0 * Q66) * cs3,
                    (Q11 - Q12 - 2.0 * Q66) * cs3 - (Q22 - Q12 - 2.0 * Q66) * c3s,
                    (Q11 + Q22 - 2.0 * Q12 - 2.0 * Q66) * c2s2 + Q66 * (c4 + s4),
                ],
            ],
            dtype=np.float64,
        )
        Qbar.setflags(write=False)
        return Qbar

    def transformed_shear_stiffness(self, angle_rad: float) -> FloatArray:
        """Return transformed transverse-shear stiffness for a ply angle.

        Args:
            angle_rad: Ply angle from the local 1 direction to the laminate
                frame, in radians.

        Returns:
            Read-only transformed 2x2 transverse-shear stiffness matrix.

        Raises:
            ValueError: If ``angle_rad`` is not finite.
        """

        angle = float(angle_rad)
        if not np.isfinite(angle):
            msg = "angle_rad must be finite."
            raise ValueError(msg)
        c = float(np.cos(angle))
        s = float(np.sin(angle))
        rotation = np.array([[c, -s], [s, c]], dtype=np.float64)
        local = np.diag([self.G13, self.G23]).astype(np.float64)
        shear = rotation @ local @ rotation.T
        shear.setflags(write=False)
        return shear


__all__ = ["IsotropicMaterial", "OrthotropicPlyMaterial"]
