from __future__ import annotations

import numpy as np

from tensyl import IsotropicMaterial, OrthotropicPlyMaterial, Ply, isotropic_plate, laminate_plate
from tensyl.rotations import (
    generalized_resultant_transform,
    generalized_strain_transform,
    rotate_tangent,
)


def test_generalized_rotation_preserves_power_pairing() -> None:
    angle = 0.37
    eta = np.array([0.1, -0.03, 0.04, 0.02, -0.01, 0.03, 0.2, -0.1])
    resultants = np.array([1.0, 2.0, -0.5, 0.3, -0.2, 0.1, 4.0, -3.0])

    eta_rotated = generalized_strain_transform(angle) @ eta
    resultants_rotated = generalized_resultant_transform(angle) @ resultants

    np.testing.assert_allclose(resultants_rotated @ eta_rotated, resultants @ eta)


def test_isotropic_plate_rotation_is_invariant() -> None:
    stiffness = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.3), thickness=0.01)

    rotated = stiffness.rotate(np.pi / 5.0)

    np.testing.assert_allclose(rotated.C8, stiffness.C8, rtol=1.0e-12, atol=1.0e-5)


def test_rotate_then_rotate_back_recovers_tangent() -> None:
    material = OrthotropicPlyMaterial(
        E1=25.0e6,
        E2=5.0e6,
        G12=2.0e6,
        nu12=0.25,
        G13=1.5e6,
        G23=1.0e6,
    )
    stiffness = laminate_plate([Ply(material=material, thickness=0.2)])

    rotated = rotate_tangent(stiffness.C8, np.pi / 6.0)
    recovered = rotate_tangent(rotated, -np.pi / 6.0)

    np.testing.assert_allclose(recovered, stiffness.C8, rtol=1.0e-12, atol=1.0e-8)


def test_ninety_degree_orthotropic_rotation_swaps_principal_membrane_terms() -> None:
    material = OrthotropicPlyMaterial(
        E1=30.0e6,
        E2=3.0e6,
        G12=2.0e6,
        nu12=0.2,
        G13=1.7e6,
        G23=1.1e6,
    )
    stiffness = laminate_plate([Ply(material=material, thickness=0.1)])

    rotated = stiffness.rotate(np.pi / 2.0)

    np.testing.assert_allclose(rotated.A[0, 0], stiffness.A[1, 1], rtol=1.0e-12)
    np.testing.assert_allclose(rotated.A[1, 1], stiffness.A[0, 0], rtol=1.0e-12)
    np.testing.assert_allclose(rotated.As[0, 0], stiffness.As[1, 1], rtol=1.0e-12)
    np.testing.assert_allclose(rotated.As[1, 1], stiffness.As[0, 0], rtol=1.0e-12)
