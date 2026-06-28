from __future__ import annotations

import tensyl


def test_package_exposes_version() -> None:
    assert isinstance(tensyl.__version__, str)
    assert tensyl.__version__


def test_legacy_module_imports_remain_available() -> None:
    from tensyl.cells import CanonicalUnitCell
    from tensyl.constitutive import ABDStiffness
    from tensyl.homogenizers import EnergyHomogenizer
    from tensyl.laminates import isotropic_plate
    from tensyl.materials import IsotropicMaterial
    from tensyl.sections import BeamSection, ThinWallSegment, blade_section

    assert BeamSection
    assert ThinWallSegment
    assert blade_section
    assert CanonicalUnitCell
    assert EnergyHomogenizer
    assert IsotropicMaterial
    assert ABDStiffness
    assert isotropic_plate
