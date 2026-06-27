from __future__ import annotations

import numpy as np

from tensyl import IsotropicMaterial, OrthotropicPlyMaterial, Ply, isotropic_plate, laminate_plate


def test_isotropic_plate_matches_closed_form_abd_and_shear() -> None:
    material = IsotropicMaterial(E=70.0e9, nu=0.33, density=2700.0)
    h = 0.004
    kappa = 5.0 / 6.0

    wall = isotropic_plate(material, h, shear_correction=kappa)
    Q = material.plane_stress_stiffness()

    np.testing.assert_allclose(wall.A, Q * h)
    np.testing.assert_allclose(wall.B, np.zeros((3, 3)), atol=0.0)
    np.testing.assert_allclose(wall.D, Q * h**3 / 12.0)
    np.testing.assert_allclose(wall.As, np.diag([kappa * material.G * h] * 2))
    assert wall.areal_mass == 2700.0 * h


def test_single_isotropic_laminate_equals_isotropic_plate() -> None:
    material = IsotropicMaterial(E=10.0e6, nu=0.25)
    h = 0.25

    direct = isotropic_plate(material, h)
    laminate = laminate_plate([Ply(material=material, thickness=h, angle_rad=np.pi / 7.0)])

    np.testing.assert_allclose(laminate.A, direct.A)
    np.testing.assert_allclose(laminate.B, direct.B, atol=1.0e-12)
    np.testing.assert_allclose(laminate.D, direct.D)
    np.testing.assert_allclose(laminate.As, direct.As)


def test_symmetric_laminate_has_zero_membrane_bending_coupling() -> None:
    material = OrthotropicPlyMaterial(
        E1=140.0e9,
        E2=9.0e9,
        G12=5.0e9,
        nu12=0.28,
        G13=4.0e9,
        G23=3.0e9,
    )
    plies = [
        Ply(material=material, thickness=0.001, angle_rad=0.0),
        Ply(material=material, thickness=0.001, angle_rad=np.pi / 2.0),
        Ply(material=material, thickness=0.001, angle_rad=np.pi / 2.0),
        Ply(material=material, thickness=0.001, angle_rad=0.0),
    ]

    wall = laminate_plate(plies)

    np.testing.assert_allclose(wall.B, np.zeros((3, 3)), atol=1.0e-8)
    np.testing.assert_allclose(wall.C8, wall.C8.T, atol=1.0e-8)
