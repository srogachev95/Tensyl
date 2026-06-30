from __future__ import annotations

import importlib.util

import tensyl


def test_package_exposes_version() -> None:
    assert isinstance(tensyl.__version__, str)
    assert tensyl.__version__


def test_public_package_imports_remain_available() -> None:
    from tensyl import (
        ABDStiffness,
        ABDStiffnessCoefficients,
        OrthotropicStiffnessCoefficients,
        ReducedOrthotropicProperties,
        isotropic_plate,
    )
    from tensyl.cells import CanonicalUnitCell
    from tensyl.homogenizers import EnergyHomogenizer
    from tensyl.materials import IsotropicMaterial
    from tensyl.sections import BeamSection, ThinWallSegment, blade_section

    assert BeamSection
    assert ThinWallSegment
    assert blade_section
    assert CanonicalUnitCell
    assert EnergyHomogenizer
    assert IsotropicMaterial
    assert ABDStiffness
    assert ABDStiffnessCoefficients
    assert OrthotropicStiffnessCoefficients
    assert ReducedOrthotropicProperties
    assert isotropic_plate


def test_top_level_compatibility_shims_are_not_packaged() -> None:
    assert importlib.util.find_spec("tensyl.constitutive") is None
    assert importlib.util.find_spec("tensyl.conventions") is None
    assert importlib.util.find_spec("tensyl.laminates") is None
    assert importlib.util.find_spec("tensyl.rotations") is None
    assert importlib.util.find_spec("tensyl.typing") is None
