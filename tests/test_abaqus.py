from __future__ import annotations

import numpy as np
import pytest

from tensyl import ABDStiffness
from tensyl.adapters import abaqus_shell_general_section


def _stiffness(*, mass: float | None = 3.5) -> ABDStiffness:
    return ABDStiffness(
        A=np.array([[101, 12, 16], [12, 202, 26], [16, 26, 66]]),
        B=np.array([[11, 2, 6], [2, 22, -7], [6, -7, 9]]),
        D=np.array([[301, 32, 36], [32, 402, 46], [36, 46, 96]]),
        As=np.array([[501, -56], [-56, 602]]),
        areal_mass=mass,
    )


def test_full_abaqus_packing_preserves_coupling_and_shear_signs() -> None:
    stiffness = _stiffness()
    text = abaqus_shell_general_section(stiffness, elset="panel", orientation="axes")
    lines = [line for line in text.splitlines() if not line.startswith("**")]
    assert lines[0] == "*SHELL GENERAL SECTION, ELSET=panel, ORIENTATION=axes, DENSITY=3.5"
    assert [[float(x) for x in line.split(",")] for line in lines[1:4]] == [
        [101, 12, 202, 16, 26, 66, 11, 2],
        [6, 301, 2, 22, -7, 32, 402, 6],
        [-7, 9, 36, 46, 96],
    ]
    assert lines[4] == "*TRANSVERSE SHEAR STIFFNESS"
    assert [float(x) for x in lines[5].split(",")] == [501, 602, -56]
    packed = [float(x) for line in lines[1:4] for x in line.split(",")]
    restored = np.zeros((6, 6))
    for value, (row, col) in zip(packed, zip(*np.tril_indices(6), strict=True), strict=True):
        restored[row, col] = restored[col, row] = value
    np.testing.assert_array_equal(restored, stiffness.C8[:6, :6])


def test_missing_mass_is_omitted_for_standard_and_refused_for_explicit() -> None:
    stiffness = _stiffness(mass=None)
    assert "DENSITY=" not in abaqus_shell_general_section(stiffness, elset="panel")
    with pytest.raises(ValueError, match="areal_mass"):
        abaqus_shell_general_section(stiffness, elset="panel", explicit=True)
    assert "DENSITY=3.5" in abaqus_shell_general_section(_stiffness(), elset="p", explicit=True)


@pytest.mark.parametrize("shear", [np.diag([0, 1]), np.zeros((2, 2)), np.array([[1, 2], [2, 1]])])
def test_nonpositive_shear_is_refused(shear: np.ndarray) -> None:
    stiffness = _stiffness()
    stiffness = ABDStiffness(A=stiffness.A, B=stiffness.B, D=stiffness.D, As=shear)
    with pytest.raises(ValueError, match="positive definite"):
        abaqus_shell_general_section(stiffness, elset="panel")


@pytest.mark.parametrize("name", ["", "p, MATERIAL=x", "p\n*STEP", "two words", "a" * 81])
def test_keyword_names_are_validated(name: str) -> None:
    with pytest.raises(ValueError, match="name"):
        abaqus_shell_general_section(_stiffness(), elset=name)
    with pytest.raises(ValueError, match="name"):
        abaqus_shell_general_section(_stiffness(), elset="panel", orientation=name)
