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


def test_material_and_section_examples() -> None:
    example = runpy.run_path(str(SCRIPTS / "materials_sections.py"))
    np.testing.assert_allclose(example["symmetric"].B, 0, atol=1e-10)
    assert abs(example["unsymmetric"].B[0, 0]) > 1000
    np.testing.assert_allclose(example["free_strain"][:2], 23e-6 * 50)
    np.testing.assert_allclose(example["free_strain"][2:], 0, atol=1e-14)
    open_hat, closed_hat = example["open_hat"], example["closed_hat"]
    # Independent single-cell Bredt formula, using the median enclosed area.
    width, height, wall = 0.03, 0.025 + 0.002 + 0.002, 0.002
    J = 4 * (width * height) ** 2 / (2 * height / wall + 2 * width / wall)
    assert pytest.approx(70e9 / (2 * 1.33) * J) == closed_hat.section.GJ
    assert closed_hat.section.EA == open_hat.section.EA
    assert closed_hat.section.mass_per_length == open_hat.section.mass_per_length
    # A quasi-isotropic stack's membrane compliance supplies the wall modulus.
    E_wall = 1 / (np.linalg.inv(example["symmetric"].A)[0, 0] * 0.001)
    assert pytest.approx(E_wall * 0.025 * 0.001) == example["composite_section"].EA


def test_pattern_transform_sweep_and_export_examples() -> None:
    from tensyl import EnergyHomogenizer

    example = runpy.run_path(str(SCRIPTS / "panel_workflows.py"))
    stiffness = example["stiffness"]
    custom = EnergyHomogenizer().compute(example["custom_cell"]).stiffness
    np.testing.assert_allclose(custom.C8, stiffness.C8)
    for family, density in (("e1", 10), ("e2", 1 / 0.15)):
        np.testing.assert_allclose(example["density_audit"][family], density)
    assert example["rotated"].A[0, 0] == pytest.approx(stiffness.A[1, 1])
    d = example["shift"]
    np.testing.assert_allclose(example["shifted"].B, stiffness.B - d * stiffness.A)
    np.testing.assert_allclose(
        example["shifted"].D, stiffness.D - 2 * d * stiffness.B + d**2 * stiffness.A
    )
    for row in example["rows"]:
        expected_mass = 2700 * (0.002 + 0.025 * 0.002 / row["spacing"])
        assert row["areal_mass"] == pytest.approx(expected_mass)
        assert row["A11"] == pytest.approx(
            70e9 * 0.002 / (1 - 0.33**2) + 70e9 * 0.025 * 0.002 / row["spacing"]
        )
    assert example["restored_result"].stiffness == stiffness
    np.testing.assert_allclose(
        EnergyHomogenizer().compute(example["restored_cell"]).stiffness.C8, stiffness.C8
    )
    np.testing.assert_allclose(example["net_axial_forces"], 0, atol=1e-10)
    assert "*TRANSVERSE SHEAR STIFFNESS" in example["keywords"]


def test_surface_and_atlas_examples() -> None:
    example = runpy.run_path(str(SCRIPTS / "surface_fields.py"))
    np.testing.assert_array_equal(example["local"].C8, example["skin"].C8)
    assert example["root"].A[0, 0] > example["tip"].A[0, 0]
    mid = example["varying"].stiffness_at(example["surface"], 1.5, 0)
    expected = (example["root"].A[0, 0] + mid.A[0, 0]) / 2
    assert example["interpolated"].A[0, 0] == pytest.approx(expected)
    restored = example["restored_atlas"]
    np.testing.assert_allclose(
        restored.stiffness_at(restored.surface, 0.75, np.pi / 2).C8,
        example["interpolated"].C8,
    )


def test_readme_runs_the_same_skin_example() -> None:
    readme = (ROOT / "README.md").read_text()
    displayed = readme.split("```python\n", 1)[1].split("```", 1)[0].strip()
    source = (SCRIPTS / "walkthrough.py").read_text()
    snippet = source.split("# --8<-- [start:skin]\n", 1)[1].split("# --8<-- [end:skin]", 1)[0]
    assert displayed == snippet.strip()
    example = runpy.run_path(str(SCRIPTS / "walkthrough.py"))
    assert example["skin"].areal_mass == pytest.approx(5.4)


def test_plot_and_coefficient_handoff_use_the_workflow_cell() -> None:
    from matplotlib import pyplot as plt

    example = runpy.run_path(str(SCRIPTS / "panel_workflows.py"))
    plot = runpy.run_path(str(SCRIPTS / "plot_cell.py"))["plot_cell"]
    cell = example["custom_cell"]
    axes = plot(cell)
    assert len(axes.lines) == 4 * len(cell.geometry.edges)
    plt.close(axes.figure)
    coefficients = example["orthogrid_constants"]
    D = example["stiffness"].D
    assert coefficients.Dbar_xy == pytest.approx(2 * D[0, 1] + 4 * D[2, 2])
    iso = example["isogrid_constants"]
    assert iso.Ebar_x == pytest.approx(iso.Ebar_y)
    assert iso.Cbar_x == pytest.approx(iso.Cbar_y)
