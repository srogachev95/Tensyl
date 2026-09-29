"""Check the actual scripts included in the engineering handbook."""

from __future__ import annotations

import runpy
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "docs" / "examples" / "scripts"


def test_walkthrough_matches_skin_and_smeared_blade_formulas(tmp_path: Path) -> None:
    example = runpy.run_path(str(SCRIPTS / "walkthrough.py"))
    skin, result = example["skin"], example["result"]
    E, nu, t, h, web = 70e9, 0.33, 0.002, 0.025, 0.002
    area, z = h * web, (t + h) / 2
    assert skin.A[0, 0] == pytest.approx(E * t / (1 - nu**2))
    assert skin.D[0, 0] == pytest.approx(E * t**3 / (12 * (1 - nu**2)))
    assert result.stiffness.A[0, 0] - skin.A[0, 0] == pytest.approx(E * area / 0.1)
    assert result.stiffness.B[0, 0] == pytest.approx(E * area * z / 0.1)
    assert result.stiffness.D[0, 0] - skin.D[0, 0] == pytest.approx(
        E * (web * h**3 / 12 + area * z**2) / 0.1
    )
    assert result.stiffness.areal_mass == pytest.approx(2700 * (t + area / 0.1 + area / 0.15))
    np.testing.assert_allclose(
        result.stiffness.resultants(example["strain"]), example["loads"], atol=1e-10
    )
    assert example["strain"][3] < 0  # Axial load at the skin midplane bends the eccentric grid.
    saved = example["save_result"](tmp_path / "panel.json")
    assert saved.stiffness == result.stiffness


def test_printed_walkthrough_values_come_from_the_example() -> None:
    renderer = runpy.run_path(str(SCRIPTS / "render_handbook.py"))
    for filename, text in renderer["render_tables"]().items():
        assert (ROOT / "docs" / "includes" / filename).read_text() == text
