from __future__ import annotations

import numpy as np

from tensyl import BeamSection, EnergyHomogenizer, LinearABDWall
from tensyl.homogenizers import member_energy


def zero_skin() -> LinearABDWall:
    return LinearABDWall(
        A=np.zeros((3, 3)),
        B=np.zeros((3, 3)),
        D=np.zeros((3, 3)),
        As=np.zeros((2, 2)),
    )


def membrane_skin(stiffness: float = 10.0) -> LinearABDWall:
    return LinearABDWall(
        A=stiffness * np.eye(3),
        B=np.zeros((3, 3)),
        D=np.zeros((3, 3)),
        As=np.zeros((2, 2)),
    )


def beam_section(*, shear: bool = True) -> BeamSection:
    return BeamSection(
        EA=1200.0,
        EIy=50.0,
        EIz=30.0,
        GJ=20.0,
        kGAy=400.0 if shear else None,
        kGAz=300.0 if shear else None,
    )


def assert_energy_consistent(cell) -> None:
    eta = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])
    result = EnergyHomogenizer().compute(cell)
    wall_energy = 0.5 * cell.area * float(eta @ result.law.C8 @ eta)
    explicit_energy = cell.area * cell.skin.energy(eta) + sum(
        member_energy(member, eta) for member in cell.members
    )
    np.testing.assert_allclose(wall_energy, explicit_energy, rtol=1.0e-12, atol=1.0e-10)
    assert result.diagnostics["symmetric"] is True
    assert result.diagnostics["positive_semidefinite"] is True
