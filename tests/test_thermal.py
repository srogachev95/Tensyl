from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from tensyl import (
    BeamMember,
    BeamSection,
    CanonicalUnitCell,
    IsotropicMaterial,
    OrthotropicPlyMaterial,
    Ply,
    ThermalResultants,
    blade_section,
    cell_thermal_resultants,
    laminate_plate,
    laminate_thermal_resultants,
)
from tensyl.core.rotations import generalized_strain_transform


def test_isotropic_free_expansion_and_restrained_force() -> None:
    plies = (Ply(IsotropicMaterial(E=70e9, nu=0.3, alpha=23e-6), 0.002),)
    stiffness = laminate_plate(plies)
    thermal = laminate_thermal_resultants(plies)
    np.testing.assert_allclose(thermal.N_T, [70e9 * 23e-6 * 0.002 / 0.7] * 2 + [0])
    np.testing.assert_array_equal(thermal.M_T, np.zeros(3))
    strain = stiffness.strains(thermal.equivalent_load(50))
    np.testing.assert_allclose(strain, [23e-6 * 50, 23e-6 * 50, 0, 0, 0, 0, 0, 0], atol=1e-18)


def test_two_layer_thermal_moment_has_positive_top_layer_sign() -> None:
    bottom = IsotropicMaterial(E=100, nu=0, alpha=1e-3)
    top = IsotropicMaterial(E=200, nu=0, alpha=3e-3)
    thermal = laminate_thermal_resultants((Ply(bottom, 1), Ply(top, 1)))
    np.testing.assert_allclose(thermal.N_T, [0.7, 0.7, 0])
    np.testing.assert_allclose(thermal.M_T, [0.25, 0.25, 0])


def test_off_axis_thermal_strain_uses_engineering_shear() -> None:
    material = OrthotropicPlyMaterial(
        E1=140, E2=10, G12=5, nu12=0.3, G13=5, G23=3, alpha1=1e-6, alpha2=20e-6
    )
    plies = (Ply.from_degrees(material, 0.1, 45),)
    thermal = laminate_thermal_resultants(plies)
    strain = laminate_plate(plies).strains(thermal.equivalent_load(1))
    np.testing.assert_allclose(strain[:3], [10.5e-6, 10.5e-6, -19e-6], rtol=1e-12)


def test_thermal_rotation_shift_and_value_semantics() -> None:
    thermal = ThermalResultants(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0]))
    clone = ThermalResultants(thermal.N_T.copy(), thermal.M_T.copy())
    assert thermal == clone and hash(thermal) == hash(clone)
    assert not thermal.N_T.flags.writeable
    np.testing.assert_allclose(thermal.shift_reference_surface(2).M_T, [2, 1, 0])
    strain = np.arange(8.0)
    rotated = thermal.rotate(0.37)
    assert rotated.equivalent_load(1) @ (
        generalized_strain_transform(0.37) @ strain
    ) == pytest.approx(thermal.equivalent_load(1) @ strain)


@pytest.mark.parametrize("angle", [0.0, 0.4, np.pi / 2])
def test_eccentric_member_thermal_force_and_moment(angle: float) -> None:
    material = IsotropicMaterial(E=100, nu=0, alpha=0)
    skin = laminate_plate((Ply(material, 0.1),))
    section = BeamSection(EA=100, EIy=1, EIz=1, GJ=1, thermal_expansion=0.01)
    member = BeamMember(
        section=section, length=3, angle_rad=angle, axial_eccentricity=2, multiplicity=2
    )
    cell = CanonicalUnitCell(area=4, skin=skin, members=(member,))
    thermal = cell_thermal_resultants(cell, skin=laminate_thermal_resultants((Ply(material, 0.1),)))
    direction = np.array([np.cos(angle) ** 2, np.sin(angle) ** 2, np.cos(angle) * np.sin(angle)])
    np.testing.assert_allclose(thermal.N_T, 1.5 * direction)
    np.testing.assert_allclose(thermal.M_T, 3 * direction)
    missing = replace(
        cell, members=(replace(member, section=replace(section, thermal_expansion=None)),)
    )
    with pytest.raises(ValueError, match="thermal_expansion"):
        cell_thermal_resultants(missing, skin=ThermalResultants(np.zeros(3), np.zeros(3)))
    with pytest.raises(ValueError, match="frame"):
        cell_thermal_resultants(cell, skin=thermal.rotate(0.2))


def test_missing_and_nonfinite_expansion_are_refused() -> None:
    with pytest.raises(ValueError, match="alpha"):
        laminate_thermal_resultants((Ply(IsotropicMaterial(E=100, nu=0), 0.1),))
    with pytest.raises(ValueError, match="alpha"):
        IsotropicMaterial(E=100, nu=0, alpha=np.nan)
    with pytest.raises(ValueError, match="finite"):
        ThermalResultants(np.zeros(3), np.zeros(3)).equivalent_load(np.inf)
    material = IsotropicMaterial(E=100, nu=0, alpha=-1e-5)
    assert (
        blade_section(material=material, height=1, thickness=0.1).section.thermal_expansion == -1e-5
    )


def test_thermal_arrays_are_copied_and_invalid_shapes_refused() -> None:
    force = np.ones(3)
    thermal = ThermalResultants(force, np.zeros(3))
    force[:] = 0
    np.testing.assert_array_equal(thermal.N_T, np.ones(3))
    with pytest.raises(ValueError, match="shape"):
        ThermalResultants(np.zeros(2), np.zeros(3))
    with pytest.raises(ValueError, match="finite"):
        ThermalResultants(np.array([0, 0, np.nan]), np.zeros(3))
