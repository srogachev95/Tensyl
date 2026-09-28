"""Parametric shell midsurfaces for geometry embedding."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from tensyl.core._validation import (
    finite_number,
    frozen_value,
    normalized_vector3,
    positive_number,
    readonly_array,
    readonly_mapping,
)
from tensyl.core.conventions import Frame2D
from tensyl.core.typing import FloatArray

_TOLERANCE = 1.0e-12


def _unit_vector(values: FloatArray, *, name: str) -> FloatArray:
    return normalized_vector3(values, name=name, tolerance=_TOLERANCE)


def _readonly_vector(values: FloatArray, *, name: str) -> FloatArray:
    return readonly_array(values, shape=(3,), name=name)


def _readonly_matrix(values: FloatArray, *, shape: tuple[int, int], name: str) -> FloatArray:
    return readonly_array(values, shape=shape, name=name)


def _principal_curvatures(metric: FloatArray, curvature: FloatArray) -> tuple[float, float]:
    # Principal curvatures are eigenvalues of the shape operator I^-1 II. The
    # metric solve avoids explicitly forming a fragile inverse.
    values = np.linalg.eigvals(np.linalg.solve(metric, curvature))
    real_values = np.real_if_close(values, tol=1000)
    if np.iscomplexobj(real_values):
        msg = "principal curvature calculation produced complex values."
        raise ValueError(msg)
    ordered = tuple(sorted(float(value) for value in real_values))
    return (ordered[0], ordered[1])


def _min_radius(principal_curvatures: tuple[float, float]) -> float:
    # Flat directions have infinite radius; they should not dominate the
    # minimum-radius validity check for cylinders, cones, or plates.
    radii = [
        np.inf if abs(curvature) <= _TOLERANCE else 1.0 / abs(curvature)
        for curvature in principal_curvatures
    ]
    return float(min(radii))


@dataclass(frozen=True, slots=True)
class SurfacePoint:
    """Differential geometry data at a parametric surface point.

    Attributes:
        u: First parametric coordinate after validation.
        v: Second parametric coordinate after validation.
        position: Three-dimensional point on the midsurface.
        tangent_u: Physical tangent vector for increasing ``u``.
        tangent_v: Physical tangent vector for increasing ``v``.
        metric: First fundamental form in the ``(u, v)`` chart.
        curvature: Second fundamental form in the ``(u, v)`` chart.
        frame: Right-handed local tangent frame used by stiffness values.
        jacobian: Positive surface area scale for the parameterization.
        principal_curvatures: The two signed principal curvatures.
        min_radius: Smallest positive curvature radius, or infinity for flat
            directions.
        metadata: Read-only provenance for the surface and coordinate names.
    """

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
        object.__setattr__(self, "u", finite_number(self.u, name="u"))
        object.__setattr__(self, "v", finite_number(self.v, name="v"))
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
        jacobian = finite_number(self.jacobian, name="jacobian")
        if jacobian <= 0.0:
            msg = "jacobian must be positive."
            raise ValueError(msg)
        object.__setattr__(self, "jacobian", jacobian)
        principal = tuple(
            finite_number(value, name="principal_curvature") for value in self.principal_curvatures
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

    def _key(self) -> tuple[Any, ...]:
        return (
            self.u,
            self.v,
            frozen_value(self.position),
            frozen_value(self.tangent_u),
            frozen_value(self.tangent_v),
            frozen_value(self.metric),
            frozen_value(self.curvature),
            self.frame,
            self.jacobian,
            self.principal_curvatures,
            self.min_radius,
            frozen_value(self.metadata),
        )

    def __eq__(self, other: object) -> bool:
        # Array fields make the generated dataclass __eq__ raise; compare the
        # frozen payload instead.
        if not isinstance(other, SurfacePoint):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())


class Surface(Protocol):
    """Protocol for parametric shell midsurfaces.

    Attributes:
        point_at: Method that evaluates the surface chart at ``(u, v)``.
    """

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return differential geometry data at parametric coordinates.

        Args:
            u: First coordinate in the surface's parameterization.
            v: Second coordinate in the surface's parameterization.

        Returns:
            The surface point, local frame, metric, curvature, and metadata
            needed to embed an ABD stiffness on the shell midsurface.

        Raises:
            ValueError: If the coordinates are non-finite or land on a
                singular point of the parameterization.
        """


@dataclass(frozen=True, slots=True)
class FlatPlate:
    """Flat plate parameterized by Cartesian coordinates ``(u, v)``.

    Attributes:
        origin: Three-dimensional point where ``u = v = 0``.
        e1: Unit direction for increasing ``u``.
        e2: Unit direction for increasing ``v``.
        label: Frame and metadata label attached to sampled points.
    """

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
        # Frame2D re-orthonormalizes e2 against e1 and n, so downstream code
        # sees a right-handed local basis even when the input axes are only
        # approximately orthogonal.
        frame = Frame2D(e1=e1, e2=e2, n=normal, label=self.label)
        object.__setattr__(self, "origin", _readonly_vector(self.origin, name="origin"))
        object.__setattr__(self, "e1", frame.e1)
        object.__setattr__(self, "e2", frame.e2)

    def _key(self) -> tuple[Any, ...]:
        return (
            frozen_value(self.origin),
            frozen_value(self.e1),
            frozen_value(self.e2),
            self.label,
        )

    def __eq__(self, other: object) -> bool:
        # Fields compare surfaces by value, so equal plates must not raise on
        # array truth values.
        if not isinstance(other, FlatPlate):
            return NotImplemented
        return self._key() == other._key()

    def __hash__(self) -> int:
        return hash(self._key())

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return the flat-plate geometry at Cartesian coordinates.

        Args:
            u: Distance along ``e1``.
            v: Distance along ``e2``.

        Returns:
            A ``SurfacePoint`` with identity metric, zero curvature, and
            infinite minimum curvature radius.

        Raises:
            ValueError: If either coordinate is not finite.
        """

        u_checked = finite_number(u, name="u")
        v_checked = finite_number(v, name="v")
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

    Attributes:
        radius: Positive cylinder radius.
        length: Optional positive axial length used as model metadata by
            callers. The parameterization itself does not clip ``u``.
        label: Frame and metadata label attached to sampled points.
    """

    radius: float
    length: float | None = None
    label: str = "cylinder"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "radius",
            positive_number(self.radius, name="radius", finite_and_positive_message=False),
        )
        if self.length is not None:
            object.__setattr__(
                self,
                "length",
                positive_number(self.length, name="length", finite_and_positive_message=False),
            )

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return cylinder geometry at axial station and angle.

        Args:
            u: Axial coordinate ``x``.
            v: Circumferential angle ``theta`` in radians.

        Returns:
            A ``SurfacePoint`` with outward normal and signed curvature
            ``-1 / radius`` in the circumferential direction.

        Raises:
            ValueError: If either coordinate is not finite.
        """

        x = finite_number(u, name="u")
        theta = finite_number(v, name="v")
        radius = self.radius
        c = float(np.cos(theta))
        s = float(np.sin(theta))
        # e2 is chosen opposite the raw theta tangent so e1, e2, n form the
        # same right-handed convention used by the shell stiffness frame.
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
class Sphere:
    """Spherical surface parameterized by polar angle and azimuth ``(phi, theta)``.

    The single chart excludes both poles. Use ``SphericalCap`` when a partial
    spherical domain is a better model for the physical shell.

    Attributes:
        radius: Positive sphere radius.
        label: Frame and metadata label attached to sampled points.
    """

    radius: float
    label: str = "sphere"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "radius",
            positive_number(self.radius, name="radius", finite_and_positive_message=False),
        )

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return spherical geometry away from the poles.

        Args:
            u: Polar angle ``phi`` in radians.
            v: Azimuth angle ``theta`` in radians.

        Returns:
            A ``SurfacePoint`` with equal signed principal curvatures
            ``-1 / radius``.

        Raises:
            ValueError: If either coordinate is non-finite or ``u`` is at a
                polar singularity.
        """

        phi = finite_number(u, name="u")
        theta = finite_number(v, name="v")
        if phi <= _TOLERANCE or phi >= np.pi - _TOLERANCE:
            # The polar chart has no unique azimuth direction at either pole.
            msg = "spherical coordinates are singular at the poles."
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
class SphericalCap:
    """Spherical surface parameterized by polar angle and azimuth ``(phi, theta)``.

    The pole and cap boundary are singular for the current coordinate chart and
    are rejected by ``point_at``.

    Attributes:
        radius: Positive spherical radius.
        half_angle_rad: Positive polar half-angle of the cap, no larger than
            ``pi``.
        label: Frame and metadata label attached to sampled points.
    """

    radius: float
    half_angle_rad: float = np.pi
    label: str = "spherical_cap"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "radius",
            positive_number(self.radius, name="radius", finite_and_positive_message=False),
        )
        half_angle = positive_number(
            self.half_angle_rad, name="half_angle_rad", finite_and_positive_message=False
        )
        if half_angle > np.pi:
            msg = "half_angle_rad must be less than or equal to pi."
            raise ValueError(msg)
        object.__setattr__(self, "half_angle_rad", half_angle)

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return spherical-cap geometry inside the open cap.

        Args:
            u: Polar angle ``phi`` in radians.
            v: Azimuth angle ``theta`` in radians.

        Returns:
            A ``SurfacePoint`` with outward normal and spherical curvature.

        Raises:
            ValueError: If either coordinate is non-finite, at the pole, or at
                the cap boundary.
        """

        phi = finite_number(u, name="u")
        theta = finite_number(v, name="v")
        if phi <= _TOLERANCE or phi >= self.half_angle_rad - _TOLERANCE:
            # Rejecting the cap boundary keeps the single chart smooth and
            # avoids pretending boundary conditions are part of geometry data.
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
class ConicalFrustum:
    """Circular conical frustum parameterized by axial coordinate and angle.

    Coordinates are ``(x, theta)``. The local frame uses ``e1`` along increasing
    axial station/generator direction, ``e2`` opposite the positive ``theta``
    tangent, and ``n`` outward. The apex is not part of the supported smooth
    midsurface domain.

    Attributes:
        radius_start: Positive radius at ``u = 0``.
        radius_end: Positive radius at ``u = length``.
        length: Positive axial length.
        label: Frame and metadata label attached to sampled points.
    """

    radius_start: float
    radius_end: float
    length: float
    label: str = "conical_frustum"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "radius_start",
            positive_number(
                self.radius_start, name="radius_start", finite_and_positive_message=False
            ),
        )
        object.__setattr__(
            self,
            "radius_end",
            positive_number(self.radius_end, name="radius_end", finite_and_positive_message=False),
        )
        object.__setattr__(
            self,
            "length",
            positive_number(self.length, name="length", finite_and_positive_message=False),
        )

    @property
    def slope(self) -> float:
        """Return ``dr/dx`` for the linear radius law.

        Returns:
            The signed radius change per unit axial distance.
        """

        return (self.radius_end - self.radius_start) / self.length

    def radius_at(self, u: float) -> float:
        """Return the local radius at an axial coordinate.

        Args:
            u: Axial coordinate measured from ``radius_start``.

        Returns:
            The positive interpolated radius.

        Raises:
            ValueError: If ``u`` is non-finite or the interpolated radius is
                nonpositive, which would put the point at or beyond the cone
                apex.
        """

        x = finite_number(u, name="u")
        radius = self.radius_start + self.slope * x
        if radius <= _TOLERANCE:
            # A cone apex is not a smooth shell midsurface point for the local
            # tangent-plane constitutive embedding used here.
            msg = "conical frustum radius is singular or nonpositive at this point."
            raise ValueError(msg)
        return float(radius)

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return conical-frustum geometry at axial station and angle.

        Args:
            u: Axial coordinate ``x``.
            v: Circumferential angle ``theta`` in radians.

        Returns:
            A ``SurfacePoint`` with the generator-aligned local frame and
            signed circumferential curvature.

        Raises:
            ValueError: If either coordinate is non-finite or the local radius
                is singular.
        """

        x = finite_number(u, name="u")
        theta = finite_number(v, name="v")
        radius = self.radius_at(x)
        slope = self.slope
        q = float(np.sqrt(1.0 + slope * slope))
        c = float(np.cos(theta))
        s = float(np.sin(theta))
        e1 = np.array([1.0, slope * c, slope * s]) / q
        e2 = np.array([0.0, s, -c])
        normal = np.array([-slope, c, s]) / q
        tangent_u = np.array([1.0, slope * c, slope * s])
        tangent_v = np.array([0.0, -radius * s, radius * c])
        return SurfacePoint(
            u=x,
            v=theta,
            position=np.array([x, radius * c, radius * s]),
            tangent_u=tangent_u,
            tangent_v=tangent_v,
            metric=np.array([[q * q, 0.0], [0.0, radius * radius]]),
            curvature=np.array([[0.0, 0.0], [0.0, -radius / q]]),
            frame=Frame2D(e1=e1, e2=e2, n=normal, label=self.label),
            jacobian=radius * q,
            principal_curvatures=(-1.0 / (radius * q), 0.0),
            min_radius=radius * q,
            metadata={
                "surface": self.label,
                "coordinate_v": "theta_rad",
            },
        )


@dataclass(frozen=True, slots=True)
class Ellipsoid:
    """Triaxial ellipsoid parameterized by polar angle and azimuth.

    Attributes:
        a: Positive semi-axis along global ``x``.
        b: Positive semi-axis along global ``y``.
        c: Positive semi-axis along global ``z``.
        label: Frame and metadata label attached to sampled points.
    """

    a: float
    b: float
    c: float
    label: str = "ellipsoid"

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "a", positive_number(self.a, name="a", finite_and_positive_message=False)
        )
        object.__setattr__(
            self, "b", positive_number(self.b, name="b", finite_and_positive_message=False)
        )
        object.__setattr__(
            self, "c", positive_number(self.c, name="c", finite_and_positive_message=False)
        )

    def point_at(self, u: float, v: float) -> SurfacePoint:
        """Return ellipsoid geometry away from the poles.

        Args:
            u: Polar angle ``phi`` in radians, strictly between ``0`` and
                ``pi``.
            v: Azimuth angle ``theta`` in radians.

        Returns:
            A ``SurfacePoint`` with outward normal, metric, curvature, and
            principal curvatures computed from the local ellipsoid chart.

        Raises:
            ValueError: If either coordinate is non-finite, ``phi`` is outside
                ``(0, pi)``, or the chart is singular at the requested point.
        """

        phi = finite_number(u, name="u")
        theta = finite_number(v, name="v")
        if phi <= _TOLERANCE or phi >= np.pi - _TOLERANCE:
            # Outside (0, pi) the chart folds back on itself and the cross
            # product of the tangents points inward, which would silently flip
            # every eccentricity sign. The poles themselves are singular.
            msg = "ellipsoid coordinates are singular at the poles; phi must lie in (0, pi)."
            raise ValueError(msg)
        sp = float(np.sin(phi))
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

        # Unlike the sphere, the ellipsoid curvature is not constant. Compute
        # the first and second fundamental forms at the sample point.
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
    "ConicalFrustum",
    "Cylinder",
    "Ellipsoid",
    "FlatPlate",
    "Sphere",
    "SphericalCap",
    "Surface",
    "SurfacePoint",
]
