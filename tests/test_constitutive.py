from __future__ import annotations

import numpy as np
import pytest

from tensyl import LinearABDWall


def _wall() -> LinearABDWall:
    A = np.diag([10.0, 12.0, 3.0])
    B = np.diag([1.0, 2.0, 0.5])
    D = np.diag([5.0, 6.0, 1.5])
    As = np.diag([4.0, 4.5])
    return LinearABDWall(A=A, B=B, D=D, As=As)


def test_linear_abd_wall_assembles_expected_tangent() -> None:
    wall = _wall()

    assert wall.C8.shape == (8, 8)
    np.testing.assert_allclose(wall.C8[0:3, 0:3], wall.A)
    np.testing.assert_allclose(wall.C8[0:3, 3:6], wall.B)
    np.testing.assert_allclose(wall.C8[3:6, 0:3], wall.B)
    np.testing.assert_allclose(wall.C8[6:8, 6:8], wall.As)
    np.testing.assert_allclose(wall.C8, wall.C8.T)


def test_linear_abd_wall_energy_resultants_and_tangent_are_consistent() -> None:
    wall = _wall()
    eta = np.array([0.01, -0.02, 0.03, 0.004, -0.003, 0.002, 0.05, -0.04])

    resultants = wall.resultants(eta)

    np.testing.assert_allclose(resultants, wall.tangent() @ eta)
    assert wall.energy(eta) == pytest.approx(0.5 * float(eta @ resultants))


def test_linear_abd_wall_rejects_bad_shapes_and_nonsymmetric_blocks() -> None:
    with pytest.raises(ValueError, match="A must have shape"):
        LinearABDWall(
            A=np.zeros((2, 2)),
            B=np.zeros((3, 3)),
            D=np.zeros((3, 3)),
            As=np.zeros((2, 2)),
        )

    with pytest.raises(ValueError, match="B must be symmetric"):
        LinearABDWall(
            A=np.eye(3),
            B=np.array([[1.0, 2.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]),
            D=np.eye(3),
            As=np.eye(2),
        )


def test_linear_abd_wall_rejects_bad_eta_shape() -> None:
    wall = _wall()

    with pytest.raises(ValueError, match="eta must have shape"):
        wall.energy(np.zeros(7))
