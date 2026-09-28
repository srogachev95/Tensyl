from __future__ import annotations

from typing import TypedDict

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    IsotropicMaterial,
    OrthotropicPlyMaterial,
    Ply,
    hat_section,
    isotropic_plate,
    thin_wall_section,
)
from tensyl.sections import LaminatedThinWallSection, LaminatedWallSegment, ThinWallSegment


def test_orthotropic_wall_uses_free_contraction_modulus() -> None:
    material = OrthotropicPlyMaterial(E1=140e9, E2=10e9, G12=5e9, nu12=0.3, G13=5e9, G23=3e9)
    wall = LaminatedWallSegment(ThinWallSegment(0, 0, 0, 0.02, 0.001), (Ply(material, 0.001),))
    assert pytest.approx(material.E1) == wall.E
    assert pytest.approx(material.G12) == wall.G
    assert pytest.approx(wall.stiffness.A[0, 0] / 0.001) != wall.E


def test_laminated_strips_recover_isotropic_section_and_mass() -> None:
    material = IsotropicMaterial(E=70e9, nu=0.3, density=2700)
    geometry = (
        ThinWallSegment(0, 0, 0, 0.04, 0.002),
        ThinWallSegment(-0.01, 0.04, 0.01, 0.04, 0.002),
    )
    reference = thin_wall_section(material=material, segments=geometry)
    result = LaminatedThinWallSection(
        tuple(LaminatedWallSegment(s, isotropic_plate(material, s.thickness)) for s in geometry)
    )
    for key in ("EA", "EIy", "EIz", "EIyz", "GJ", "mass_per_length"):
        assert getattr(result.section, key) == pytest.approx(getattr(reference.section, key))
    assert result.centroid_z == pytest.approx(reference.centroid_z)


def test_elastic_centroid_and_bending_use_each_wall_modulus() -> None:
    geometry = (ThinWallSegment(-1, 0, 1, 0, 0.1), ThinWallSegment(-1, 2, 1, 2, 0.1))
    materials = (IsotropicMaterial(E=100, nu=0.25), IsotropicMaterial(E=300, nu=0.25))
    walls = tuple(
        LaminatedWallSegment(s, (Ply(m, 0.1),)) for s, m in zip(geometry, materials, strict=True)
    )
    result = LaminatedThinWallSection(walls)
    assert pytest.approx(80) == result.section.EA
    assert result.centroid_z == pytest.approx(1.5)
    assert result.section.EIy == pytest.approx(
        100 * (2 * 0.1**3 / 12 + 0.2 * 1.5**2) + 300 * (2 * 0.1**3 / 12 + 0.2 * 0.5**2)
    )
    assert result.section.mass_per_length is None


def test_laminate_wall_rejects_thickness_mismatch_and_unrepresented_coupling() -> None:
    geometry = ThinWallSegment(0, 0, 0, 1, 0.1)
    material = IsotropicMaterial(E=100, nu=0.25)
    with pytest.raises(ValueError, match="thickness"):
        LaminatedWallSegment(geometry, (Ply(material, 0.2),))
    reference = isotropic_plate(material, 0.1)
    for stiffness in (
        ABDStiffness(A=reference.A, B=np.eye(3), D=reference.D, As=reference.As),
        ABDStiffness(
            A=np.array([[10, 0, 1], [0, 10, 0], [1, 0, 10]]),
            B=np.zeros((3, 3)),
            D=reference.D,
            As=reference.As,
        ),
    ):
        with pytest.raises(ValueError, match="coupling"):
            LaminatedWallSegment(geometry, stiffness)
    with pytest.raises(ValueError, match="at least one"):
        LaminatedThinWallSection(())


class _HatInputs(TypedDict):
    material: IsotropicMaterial
    web_height: float
    web_thickness: float
    crown_width: float
    crown_thickness: float
    flange_width: float
    flange_thickness: float


def test_hat_closure_uses_median_area_without_adding_skin_mass_or_axial_stiffness() -> None:
    material = IsotropicMaterial(E=70e9, nu=0.3, density=2700)
    arguments: _HatInputs = dict(
        material=material,
        web_height=0.04,
        web_thickness=0.002,
        crown_width=0.03,
        crown_thickness=0.003,
        flange_width=0.01,
        flange_thickness=0.002,
    )
    open_hat = hat_section(**arguments)
    closed_hat = hat_section(**arguments, closure_thickness=0.004)
    height = 0.04 + 0.002 + (0.003 + 0.004) / 2
    expected = 4 * (0.03 * height) ** 2 / (2 * height / 0.002 + 0.03 / 0.003 + 0.03 / 0.004)
    assert pytest.approx(expected) == closed_hat.properties.J
    assert pytest.approx(material.G * expected) == closed_hat.section.GJ
    assert closed_hat.section.EA == open_hat.section.EA
    assert closed_hat.section.mass_per_length == open_hat.section.mass_per_length
    assert closed_hat.centroid_z == open_hat.centroid_z
    assert closed_hat.properties.J > 10 * open_hat.properties.J
    with pytest.raises(ValueError, match="closure_thickness"):
        hat_section(**arguments, closure_thickness=0)
