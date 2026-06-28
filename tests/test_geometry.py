from __future__ import annotations

import numpy as np
import pytest

from tensyl import ConicalFrustum, Cylinder, Ellipsoid, FlatPlate, Sphere, SphericalCap


def _assert_right_handed(point) -> None:
    np.testing.assert_allclose(np.cross(point.frame.e1, point.frame.e2), point.frame.n)


def test_flat_plate_has_cartesian_geometry() -> None:
    plate = FlatPlate()
    point = plate.point_at(2.0, 3.0)

    np.testing.assert_allclose(point.position, np.array([2.0, 3.0, 0.0]))
    np.testing.assert_allclose(point.metric, np.eye(2))
    np.testing.assert_allclose(point.curvature, np.zeros((2, 2)))
    assert point.jacobian == pytest.approx(1.0)
    assert point.principal_curvatures == (0.0, 0.0)
    assert point.min_radius == np.inf
    assert point.position.flags.writeable is False
    _assert_right_handed(point)


def test_cylinder_uses_outward_normal_and_signed_curvature() -> None:
    cylinder = Cylinder(radius=2.0, length=5.0)
    point = cylinder.point_at(1.0, np.pi / 2.0)

    np.testing.assert_allclose(point.position, np.array([1.0, 0.0, 2.0]), atol=1.0e-12)
    np.testing.assert_allclose(point.metric, np.array([[1.0, 0.0], [0.0, 4.0]]))
    np.testing.assert_allclose(point.curvature, np.array([[0.0, 0.0], [0.0, -2.0]]))
    assert point.jacobian == pytest.approx(2.0)
    assert point.principal_curvatures == pytest.approx((-0.5, 0.0))
    assert point.min_radius == pytest.approx(2.0)
    np.testing.assert_allclose(point.frame.n, np.array([0.0, 0.0, 1.0]), atol=1.0e-12)
    _assert_right_handed(point)


def test_spherical_cap_has_outward_negative_curvatures_and_rejects_singularity() -> None:
    cap = SphericalCap(radius=3.0, half_angle_rad=1.2)
    point = cap.point_at(0.7, 0.3)

    assert point.principal_curvatures == pytest.approx((-1.0 / 3.0, -1.0 / 3.0))
    assert point.min_radius == pytest.approx(3.0)
    assert point.jacobian == pytest.approx(9.0 * np.sin(0.7))
    _assert_right_handed(point)

    with pytest.raises(ValueError, match="singular"):
        cap.point_at(0.0, 0.3)


def test_sphere_has_constant_curvature_and_rejects_poles() -> None:
    sphere = Sphere(radius=4.0)
    point = sphere.point_at(0.8, 0.4)

    assert point.principal_curvatures == pytest.approx((-0.25, -0.25))
    assert point.min_radius == pytest.approx(4.0)
    assert point.jacobian == pytest.approx(16.0 * np.sin(0.8))
    assert point.frame.label == "sphere"
    _assert_right_handed(point)

    with pytest.raises(ValueError, match="poles"):
        sphere.point_at(0.0, 0.4)

    with pytest.raises(ValueError, match="poles"):
        sphere.point_at(np.pi, 0.4)


def test_ellipsoid_computes_finite_geometry_and_sphere_special_case() -> None:
    ellipsoid = Ellipsoid(a=2.0, b=3.0, c=4.0)
    point = ellipsoid.point_at(0.8, 0.4)

    assert np.all(np.isfinite(point.metric))
    assert np.all(np.isfinite(point.curvature))
    assert point.jacobian > 0.0
    assert point.min_radius > 0.0
    _assert_right_handed(point)

    sphere = Ellipsoid(a=4.0, b=4.0, c=4.0)
    sphere_point = sphere.point_at(0.8, 0.4)
    assert sphere_point.principal_curvatures == pytest.approx((-0.25, -0.25))
    assert sphere_point.min_radius == pytest.approx(4.0)

    with pytest.raises(ValueError, match="singular"):
        ellipsoid.point_at(0.0, 0.0)


def test_sphere_matches_ellipsoid_sphere_special_case() -> None:
    sphere = Sphere(radius=4.0)
    ellipsoid = Ellipsoid(a=4.0, b=4.0, c=4.0)

    sphere_point = sphere.point_at(0.8, 0.4)
    ellipsoid_point = ellipsoid.point_at(0.8, 0.4)

    np.testing.assert_allclose(sphere_point.position, ellipsoid_point.position)
    np.testing.assert_allclose(sphere_point.metric, ellipsoid_point.metric, atol=1.0e-12)
    np.testing.assert_allclose(sphere_point.curvature, ellipsoid_point.curvature, atol=1.0e-12)
    np.testing.assert_allclose(sphere_point.frame.e1, ellipsoid_point.frame.e1, atol=1.0e-12)
    np.testing.assert_allclose(sphere_point.frame.e2, ellipsoid_point.frame.e2, atol=1.0e-12)
    np.testing.assert_allclose(sphere_point.frame.n, ellipsoid_point.frame.n, atol=1.0e-12)
    assert sphere_point.principal_curvatures == pytest.approx(ellipsoid_point.principal_curvatures)
    assert sphere_point.min_radius == pytest.approx(ellipsoid_point.min_radius)


def test_conical_frustum_has_outward_frame_and_signed_curvature() -> None:
    cone = ConicalFrustum(radius_start=2.0, radius_end=3.0, length=5.0)
    point = cone.point_at(2.5, np.pi / 2.0)
    slope = 0.2
    radius = 2.5
    q = np.sqrt(1.0 + slope * slope)

    np.testing.assert_allclose(point.position, np.array([2.5, 0.0, 2.5]), atol=1.0e-12)
    np.testing.assert_allclose(point.metric, np.array([[q * q, 0.0], [0.0, radius * radius]]))
    np.testing.assert_allclose(point.curvature, np.array([[0.0, 0.0], [0.0, -radius / q]]))
    assert point.jacobian == pytest.approx(radius * q)
    assert point.principal_curvatures == pytest.approx((-1.0 / (radius * q), 0.0))
    assert point.min_radius == pytest.approx(radius * q)
    np.testing.assert_allclose(
        point.frame.n,
        np.array([-slope, 0.0, 1.0]) / q,
        atol=1.0e-12,
    )
    _assert_right_handed(point)


def test_conical_frustum_reduces_to_cylinder_when_slope_is_zero() -> None:
    cone = ConicalFrustum(radius_start=2.0, radius_end=2.0, length=5.0)
    cylinder = Cylinder(radius=2.0, length=5.0)

    cone_point = cone.point_at(1.0, 0.7)
    cylinder_point = cylinder.point_at(1.0, 0.7)

    np.testing.assert_allclose(cone_point.position, cylinder_point.position)
    np.testing.assert_allclose(cone_point.metric, cylinder_point.metric)
    np.testing.assert_allclose(cone_point.curvature, cylinder_point.curvature)
    np.testing.assert_allclose(cone_point.frame.e1, cylinder_point.frame.e1)
    np.testing.assert_allclose(cone_point.frame.e2, cylinder_point.frame.e2)
    np.testing.assert_allclose(cone_point.frame.n, cylinder_point.frame.n)
    assert cone_point.jacobian == pytest.approx(cylinder_point.jacobian)
    assert cone_point.principal_curvatures == pytest.approx(cylinder_point.principal_curvatures)
    assert cone_point.min_radius == pytest.approx(cylinder_point.min_radius)


def test_conical_frustum_rejects_invalid_inputs_and_apex_points() -> None:
    with pytest.raises(ValueError, match="radius_start"):
        ConicalFrustum(radius_start=0.0, radius_end=2.0, length=5.0)

    with pytest.raises(ValueError, match="length"):
        ConicalFrustum(radius_start=1.0, radius_end=2.0, length=0.0)

    cone = ConicalFrustum(radius_start=1.0, radius_end=2.0, length=5.0)
    with pytest.raises(ValueError, match="singular"):
        cone.radius_at(-5.0)
