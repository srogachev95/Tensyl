"""Keep the gallery tied to the public builders and their repeat accounting."""

import runpy
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pytest

from tensyl import EnergyHomogenizer, check_cell_geometry

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = runpy.run_path(str(ROOT / "scripts" / "generate_pattern_diagrams.py"))
PATTERNS = GENERATOR["build_patterns"]()


@pytest.mark.parametrize("pattern", PATTERNS, ids=lambda p: p.slug)
def test_gallery_geometry_and_stiffness(pattern) -> None:
    cell = pattern.cell
    assert cell.geometry.repeat_area == pytest.approx(cell.area)
    for drawn, modeled in check_cell_geometry(cell).values():
        assert drawn == pytest.approx(modeled)
    stiffness = EnergyHomogenizer().compute(cell).stiffness
    assert np.isfinite(stiffness.C8).all()
    assert np.linalg.eigvalsh(stiffness.C8).min() > 0
    polygon = np.array(GENERATOR["repeat_polygon"](pattern))
    # Independently check the highlighted area, including oblique repeats.
    x, y = polygon.T
    area = abs(x @ np.roll(y, -1) - y @ np.roll(x, -1)) / 2
    assert area == pytest.approx(cell.area)


def test_pattern_assets_match_builders(tmp_path: Path) -> None:
    GENERATOR["render_all"](tmp_path)
    for pattern in PATTERNS:
        asset = GENERATOR["DEFAULT_OUTPUT_DIR"] / f"{pattern.slug}.svg"
        assert asset.read_text() == (tmp_path / asset.name).read_text()
        svg = ET.parse(asset).getroot()
        assert svg.attrib["viewBox"] == "0 0 960 550"
        # Text belongs in the header or footer, clear of both plot windows.
        for label in svg.iter("{http://www.w3.org/2000/svg}text"):
            assert float(label.attrib["y"]) <= 101 or float(label.attrib["y"]) >= 440


def test_orthogrid_repeat_is_centered_on_a_node() -> None:
    pattern = next(p for p in PATTERNS if p.slug == "orthogrid")
    polygon = np.array(GENERATOR["repeat_polygon"](pattern))
    center = polygon.mean(axis=0)
    assert any(np.allclose(center, (n.e1, n.e2)) for n in pattern.cell.geometry.nodes)
    np.testing.assert_allclose(np.max(polygon, axis=0) - center, [0.075, 0.05])
