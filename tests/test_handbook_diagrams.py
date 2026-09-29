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


def test_overview_cell_is_centered_on_a_node_with_midpitch_boundaries() -> None:
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
    # Three equally spaced ribs per direction, with half-pitch margins at the crop.
    edges = [
        points(node)
        for node in root.findall(f".//{SVG}polyline")
        if node.attrib["stroke-width"] == "4"
    ][:6]
    xs = np.array(sorted(edge[0, 0] for edge in edges if edge[0, 0] == edge[1, 0]))
    ys = np.array(sorted(edge[0, 1] for edge in edges if edge[0, 1] == edge[1, 1]))
    assert len(xs) == len(ys) == 3
    np.testing.assert_allclose(np.diff(xs), np.diff(xs)[0])
    np.testing.assert_allclose(np.diff(ys), np.diff(ys)[0])
    np.testing.assert_allclose(np.diff(xs), 1.5 * np.diff(ys))
    np.testing.assert_allclose(chosen.mean(axis=0), [xs[1], ys[1]])
    np.testing.assert_allclose(chosen.min(axis=0), [(xs[0] + xs[1]) / 2, (ys[0] + ys[1]) / 2])
    np.testing.assert_allclose(chosen.max(axis=0), [(xs[1] + xs[2]) / 2, (ys[1] + ys[2]) / 2])
    dashed = [
        node for node in root.findall(f".//{SVG}polyline") if "stroke-dasharray" in node.attrib
    ]
    assert len(dashed) == 2  # Highlight in the panel and enlarged cell.
    np.testing.assert_allclose(points(dashed[0])[:-1], chosen)
    # The enlarged cell has exactly two solid ribs, each passing through its center.
    enlarged = points(dashed[1])[:-1]
    ribs = [
        points(node)
        for node in root.findall(f".//{SVG}polyline")
        if node.attrib["stroke-width"] == "4"
    ][6:]
    assert len(ribs) == 2
    for rib in ribs:
        np.testing.assert_allclose(rib.mean(axis=0), enlarged.mean(axis=0))
