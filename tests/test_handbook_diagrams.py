"""Keep the checked-in engineering drawings reproducible and geometrically consistent."""

from pathlib import Path
from runpy import run_path
from xml.etree import ElementTree as ET

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = run_path(str(ROOT / "scripts/generate_handbook_diagrams.py"))
SVG = "{http://www.w3.org/2000/svg}"


def test_handbook_svg_assets_match_generator(tmp_path: Path) -> None:
    GENERATOR["render_all"](tmp_path)
    assets = ROOT / "docs/assets/diagrams"
    assert {p.name for p in assets.glob("*.svg")} == {p.name for p in tmp_path.glob("*.svg")}
    for path in tmp_path.glob("*.svg"):
        assert path.read_text() == (assets / path.name).read_text()
        root = ET.parse(path).getroot()
        assert root.find(f"{SVG}title") is not None
        assert root.find(f"{SVG}desc") is not None


def test_overview_grid_has_equal_bays_and_a_centered_highlight() -> None:
    root = ET.parse(ROOT / "docs/assets/diagrams/panel-model.svg").getroot()

    def points(node):
        return np.array(
            [[float(v) for v in pair.split(",")] for pair in node.attrib["points"].split()]
        )

    skin, highlight = root.findall(f".//{SVG}polygon")[:2]
    bounds = points(skin)
    chosen = points(highlight)
    np.testing.assert_allclose(chosen.mean(axis=0), bounds.mean(axis=0))
    np.testing.assert_allclose(np.ptp(chosen, axis=0), np.ptp(bounds, axis=0) / 3)
    # Three equal bays in each direction; their aspect ratio is 150:100.
    edges = [
        points(node)
        for node in root.findall(f".//{SVG}polyline")
        if node.attrib["stroke-width"] == "4"
    ][:24]
    coordinates = np.concatenate(edges)
    xs, ys = np.unique(coordinates[:, 0]), np.unique(coordinates[:, 1])
    assert len(xs) == len(ys) == 4
    np.testing.assert_allclose(np.diff(xs), np.diff(xs)[0])
    np.testing.assert_allclose(np.diff(ys), np.diff(ys)[0])
    np.testing.assert_allclose(np.diff(xs), 1.5 * np.diff(ys))
