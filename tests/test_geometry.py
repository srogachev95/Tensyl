from __future__ import annotations

import numpy as np
import pytest

from tensyl import Cylinder, Ellipsoid, FlatPlate, SphericalCap


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
