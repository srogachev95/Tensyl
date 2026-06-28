"""Parametric shell midsurfaces for geometry embedding."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from tensyl.core._validation import (
    finite_number,
    normalized_vector3,
    positive_number,
    readonly_array,
    readonly_mapping,
)
from tensyl.core.conventions import Frame2D
from tensyl.core.typing import FloatArray

_TOLERANCE = 1.0e-12


def _finite(value: float, *, name: str) -> float:
    return finite_number(value, name=name)


def _positive(value: float, *, name: str) -> float:
    return positive_number(value, name=name, finite_and_positive_message=False)


def _unit_vector(values: FloatArray, *, name: str) -> FloatArray:
    return normalized_vector3(values, name=name, tolerance=_TOLERANCE)


def _readonly_vector(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(values, shape=(3,), name=name)


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(values, shape=shape, name=name)


def _principal_curvatures(metric: FloatArray, curvature: FloatArray) -> tuple[float, float]:
    values = np.linalg.eigvals(np.linalg.solve(metric, curvature))
    real_values = np.real_if_close(values, tol=1000)
    if np.iscomplexobj(real_values):
        msg = "principal curvature calculation produced complex values."
        raise ValueError(msg)
    ordered = tuple(sorted(float(value) for value in real_values))
    return (ordered[0], ordered[1])


def _min_radius(principal_curvatures: tuple[float, float]) -> float:
    radii = [
        np.inf if abs(curvature) <= _TOLERANCE else 1.0 / abs(curvature)
        for curvature in principal_curvatures
    ]
    return float(min(radii))


@dataclass(frozen=True, slots=True)
class SurfacePoint:
    """Differential geometry data at a parametric surface point."""

    u: float
    v: float
    position: FloatArray
    tangent_u: FloatArray
    tangent_v: FloatArray
    metric: FloatArray
    curvature: FloatArray
    frame: Frame2D
    jacobian: float
    principal_curvatures: tuple[float, float]
    min_radius: float
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "u", _finite(self.u, name="u"))
        object.__setattr__(self, "v", _finite(self.v, name="v"))
        object.__setattr__(self, "position", _readonly_vector(self.position, name="position"))
        object.__setattr__(self, "tangent_u", _readonly_vector(self.tangent_u, name="tangent_u"))
        object.__setattr__(self, "tangent_v", _readonly_vector(self.tangent_v, name="tangent_v"))
        object.__setattr__(
            self,
            "metric",
            _readonly_matrix(self.metric, shape=(2, 2), name="metric"),
        )
        object.__setattr__(
            self,
            "curvature",
            _readonly_matrix(self.curvature, shape=(2, 2), name="curvature"),
        )
        jacobian = _finite(self.jacobian, name="jacobian")
        if jacobian <= 0.0:
            msg = "jacobian must be positive."
            raise ValueError(msg)
        object.__setattr__(self, "jacobian", jacobian)
        principal = tuple(
            _finite(value, name="principal_curvature") for value in self.principal_curvatures
        )
        if len(principal) != 2:
            msg = "principal_curvatures must contain two values."
            raise ValueError(msg)
        object.__setattr__(self, "principal_curvatures", principal)
        min_radius = float(self.min_radius)
        if min_radius < 0.0 or np.isnan(min_radius):
            msg = "min_radius must be nonnegative or infinite."
            raise ValueError(msg)
        object.__setattr__(self, "min_radius", min_radius)
        object.__setattr__(self, "metadata", readonly_mapping(self.metadata))


class Surface(Protocol):
    """Protocol for parametric shell midsurfaces."""

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return differential geometry data at parametric coordinates ``(u, v)``."""


@dataclass(frozen=True, slots=True)
class FlatPlate:
    """Flat plate parameterized by Cartesian coordinates ``(u, v)``."""

    origin: FloatArray = field(default_factory=lambda: np.array([0.0, 0.0, 0.0]))
    e1: FloatArray = field(default_factory=lambda: np.array([1.0, 0.0, 0.0]))
    e2: FloatArray = field(default_factory=lambda: np.array([0.0, 1.0, 0.0]))
    label: str = "flat_plate"

    def __post_init__(self) -> None:
        e1 = _unit_vector(self.e1, name="e1")
        e2 = _unit_vector(self.e2, name="e2")
        normal = np.cross(e1, e2)
        norm = float(np.linalg.norm(normal))
        if norm <= _TOLERANCE:
            msg = "e1 and e2 must not be parallel."
            raise ValueError(msg)
        normal /= norm
        frame = Frame2D(e1=e1, e2=e2, n=normal, label=self.label)
        object.__setattr__(self, "origin", _readonly_vector(self.origin, name="origin"))
        object.__setattr__(self, "e1", frame.e1)
        object.__setattr__(self, "e2", frame.e2)

    def point_at(self, u: float, v: float) -> SurfacePoint:
        u_checked = _finite(u, name="u")
        v_checked = _finite(v, name="v")
        frame = Frame2D(e1=self.e1, e2=self.e2, n=np.cross(self.e1, self.e2), label=self.label)
        return SurfacePoint(
            u=u_checked,
            v=v_checked,
            position=self.origin + u_checked * self.e1 + v_checked * self.e2,
            tangent_u=self.e1,
            tangent_v=self.e2,
            metric=np.eye(2),
            curvature=np.zeros((2, 2)),
            frame=frame,
            jacobian=1.0,
            principal_curvatures=(0.0, 0.0),
            min_radius=np.inf,
            metadata={"surface": self.label},
        )


@dataclass(frozen=True, slots=True)
class Cylinder:
    """Circular cylinder parameterized by axial coordinate and angle ``(x, theta)``.

    The local frame has ``e1`` in the axial direction, ``e2`` in the
    circumferential direction, and ``n`` outward.
    """

    radius: float
    length: float | None = None
    label: str = "cylinder"

    def __post_init__(self) -> None:
        object.__setattr__(self, "radius", _positive(self.radius, name="radius"))
        if self.length is not None:
            object.__setattr__(self, "length", _positive(self.length, name="length"))

    def point_at(self, u: float, v: float) -> SurfacePoint:
        x = _finite(u, name="u")
        theta = _finite(v, name="v")
        radius = self.radius
        c = float(np.cos(theta))
        s = float(np.sin(theta))
        e1 = np.array([1.0, 0.0, 0.0])
        e2 = np.array([0.0, s, -c])
        normal = np.array([0.0, c, s])
        tangent_v = np.array([0.0, -radius * s, radius * c])
        return SurfacePoint(
            u=x,
            v=theta,
            position=np.array([x, radius * c, radius * s]),
            tangent_u=e1,
            tangent_v=tangent_v,
            metric=np.array([[1.0, 0.0], [0.0, radius * radius]]),
            curvature=np.array([[0.0, 0.0], [0.0, -radius]]),
            frame=Frame2D(e1=e1, e2=e2, n=normal, label=self.label),
            jacobian=radius,
            principal_curvatures=(-1.0 / radius, 0.0),
            min_radius=radius,
            metadata={"surface": self.label, "coordinate_v": "theta_rad"},
        )


@dataclass(frozen=True, slots=True)
class SphericalCap:
    """Spherical surface parameterized by polar angle and azimuth ``(phi, theta)``.

    The pole and cap boundary are singular for the current coordinate chart and
    are rejected by ``point_at``.
    """

    radius: float
    half_angle_rad: float = np.pi
    label: str = "spherical_cap"

    def __post_init__(self) -> None:
        object.__setattr__(self, "radius", _positive(self.radius, name="radius"))
        half_angle = _positive(self.half_angle_rad, name="half_angle_rad")
        if half_angle > np.pi:
            msg = "half_angle_rad must be less than or equal to pi."
            raise ValueError(msg)
        object.__setattr__(self, "half_angle_rad", half_angle)

    def point_at(self, u: float, v: float) -> SurfacePoint:
        phi = _finite(u, name="u")
        theta = _finite(v, name="v")
        if phi <= _TOLERANCE or phi >= self.half_angle_rad - _TOLERANCE:
            msg = "spherical coordinates are singular at the cap pole or boundary."
            raise ValueError(msg)
        radius = self.radius
        sp = float(np.sin(phi))
        cp = float(np.cos(phi))
        st = float(np.sin(theta))
        ct = float(np.cos(theta))
        normal = np.array([sp * ct, sp * st, cp])
        tangent_phi = radius * np.array([cp * ct, cp * st, -sp])
        tangent_theta = radius * np.array([-sp * st, sp * ct, 0.0])
        e1 = tangent_phi / float(np.linalg.norm(tangent_phi))
        e2 = tangent_theta / float(np.linalg.norm(tangent_theta))
        return SurfacePoint(
            u=phi,
            v=theta,
            position=radius * normal,
            tangent_u=tangent_phi,
            tangent_v=tangent_theta,
            metric=np.array([[radius * radius, 0.0], [0.0, radius * radius * sp * sp]]),
            curvature=np.array([[-radius, 0.0], [0.0, -radius * sp * sp]]),
            frame=Frame2D(e1=e1, e2=e2, n=normal, label=self.label),
            jacobian=radius * radius * sp,
            principal_curvatures=(-1.0 / radius, -1.0 / radius),
            min_radius=radius,
            metadata={
                "surface": self.label,
                "coordinate_u": "phi_rad",
                "coordinate_v": "theta_rad",
            },
        )


@dataclass(frozen=True, slots=True)
class Ellipsoid:
    """Triaxial ellipsoid parameterized by polar angle and azimuth ``(phi, theta)``."""

    a: float
    b: float
    c: float
    label: str = "ellipsoid"

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", _positive(self.a, name="a"))
        object.__setattr__(self, "b", _positive(self.b, name="b"))
        object.__setattr__(self, "c", _positive(self.c, name="c"))

    def point_at(self, u: float, v: float) -> SurfacePoint:
        phi = _finite(u, name="u")
        theta = _finite(v, name="v")
        sp = float(np.sin(phi))
        if abs(sp) <= _TOLERANCE:
            msg = "ellipsoid coordinates are singular at the poles."
            raise ValueError(msg)
        cp = float(np.cos(phi))
        st = float(np.sin(theta))
        ct = float(np.cos(theta))

        position = np.array([self.a * sp * ct, self.b * sp * st, self.c * cp])
        tangent_phi = np.array([self.a * cp * ct, self.b * cp * st, -self.c * sp])
        tangent_theta = np.array([-self.a * sp * st, self.b * sp * ct, 0.0])
        normal_raw = np.cross(tangent_phi, tangent_theta)
        jacobian = float(np.linalg.norm(normal_raw))
        if jacobian <= _TOLERANCE:
            msg = "ellipsoid parameterization is singular at this point."
            raise ValueError(msg)
        normal = normal_raw / jacobian
        e1 = tangent_phi / float(np.linalg.norm(tangent_phi))
        e2 = np.cross(normal, e1)

        r_phiphi = np.array([-self.a * sp * ct, -self.b * sp * st, -self.c * cp])
        r_phitheta = np.array([-self.a * cp * st, self.b * cp * ct, 0.0])
        r_thetatheta = np.array([-self.a * sp * ct, -self.b * sp * st, 0.0])
        metric = np.array(
            [
                [float(tangent_phi @ tangent_phi), float(tangent_phi @ tangent_theta)],
                [float(tangent_theta @ tangent_phi), float(tangent_theta @ tangent_theta)],
            ]
        )
        curvature = np.array(
            [
                [float(normal @ r_phiphi), float(normal @ r_phitheta)],
                [float(normal @ r_phitheta), float(normal @ r_thetatheta)],
            ]
        )
        principal = _principal_curvatures(metric, curvature)
        return SurfacePoint(
            u=phi,
            v=theta,
            position=position,
            tangent_u=tangent_phi,
            tangent_v=tangent_theta,
            metric=metric,
            curvature=curvature,
            frame=Frame2D(e1=e1, e2=e2, n=normal, label=self.label),
            jacobian=jacobian,
            principal_curvatures=principal,
            min_radius=_min_radius(principal),
            metadata={
                "surface": self.label,
                "coordinate_u": "phi_rad",
                "coordinate_v": "theta_rad",
            },
        )


__all__ = [
    "Cylinder",
    "Ellipsoid",
    "FlatPlate",
    "SphericalCap",
    "Surface",
    "SurfacePoint",
]
