from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    BeamMember,
    CanonicalUnitCell,
    EnergyHomogenizer,
    IsotropicMaterial,
    isotropic_plate,
    member_loads,
)
from tests._helpers import beam_section, zero_skin


def test_strains_recovers_a_coupled_generalized_load_case() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70e9, nu=0.3), 0.002)
    cell = CanonicalUnitCell(
        area=2.0, skin=skin, members=(BeamMember(beam_section(), 1.0, 0.37, 0.2),)
    )
    stiffness = EnergyHomogenizer().compute(cell).stiffness
    eta = np.array([0.002, -0.001, 0.003, 0.04, -0.02, 0.05, 0.006, -0.007])
    recovered = stiffness.strains(stiffness.resultants(eta))
    np.testing.assert_allclose(recovered, eta, rtol=1e-12, atol=1e-15)
    assert not recovered.flags.writeable


def test_strains_rejects_singular_stiffness() -> None:
    with pytest.raises(ValueError, match="singular"):
        zero_skin().strains(np.zeros(8))


@pytest.mark.parametrize("loads", [np.zeros(7), np.full(8, np.nan)])
def test_strains_validates_resultants(loads) -> None:
    with pytest.raises(ValueError):
        ABDStiffness.from_tangent(np.eye(8)).strains(loads)


@pytest.mark.parametrize("angle", [0.0, 0.37, np.pi / 2])
def test_member_loads_match_independent_member_strains(angle: float) -> None:
    section = beam_section()
    assert section.kGAy is not None and section.kGAz is not None
    member = BeamMember(
        section, 3.0, angle, 0.2, shear_eccentricity=-0.1, multiplicity=2.0, label="rib"
    )
    cell = CanonicalUnitCell(area=4.0, skin=zero_skin(), members=(member,))
    eta = np.array([0.002, -0.001, 0.003, 0.04, -0.02, 0.05, 0.006, -0.007])
    c, s = np.cos(angle), np.sin(angle)
    extension = c * c * eta[0] + s * s * eta[1] + c * s * eta[2]
    curvature = c * c * eta[3] + s * s * eta[4] + c * s * eta[5]
    shear = -2 * c * s * eta[0] + 2 * c * s * eta[1] + (c * c - s * s) * eta[2]
    twist = -2 * c * s * eta[3] + 2 * c * s * eta[4] + (c * c - s * s) * eta[5]
    transverse = c * eta[6] + s * eta[7]
    (load,) = member_loads(cell, eta)
    assert load.member_index == 0 and load.label == "rib"
    assert load.axial_force == pytest.approx(section.EA * (extension + 0.2 * curvature))
    assert load.in_plane_shear_force == pytest.approx(section.kGAy * 0.5 * (shear - 0.1 * twist))
    assert load.transverse_shear_force == pytest.approx(section.kGAz * transverse)
    assert load.bending_moment == pytest.approx(section.EIy * curvature)
    assert load.torque == pytest.approx(-0.5 * section.GJ * twist)
    # Per-member forces do not grow with how much of the rib a cell represents.
    different_density = replace(cell, members=(replace(member, length=7.0, multiplicity=4.0),))
    assert member_loads(different_density, eta) == (load,)


def test_member_loads_report_omitted_shear_as_zero_and_keep_order() -> None:
    section = beam_section(shear=False)
    cell = CanonicalUnitCell(
        area=1.0,
        skin=zero_skin(),
        members=(
            BeamMember(section, 1.0, 0.0, 0.0, label="first"),
            BeamMember(section, 1.0, np.pi / 2, 0.0, label="second"),
        ),
    )
    loads = member_loads(cell, np.ones(8))
    assert [load.label for load in loads] == ["first", "second"]
    assert [load.member_index for load in loads] == [0, 1]
    assert all(load.in_plane_shear_force == load.transverse_shear_force == 0.0 for load in loads)
    with pytest.raises(ValueError, match="finite"):
        member_loads(cell, np.full(8, np.inf))
