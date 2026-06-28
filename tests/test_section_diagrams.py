from __future__ import annotations

import importlib.util
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = ROOT / "scripts" / "generate_section_diagrams.py"
SPEC = importlib.util.spec_from_file_location("generate_section_diagrams", GENERATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
generator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = generator
SPEC.loader.exec_module(generator)

DEFAULT_OUTPUT_DIR = generator.DEFAULT_OUTPUT_DIR
diagrams = generator.diagrams
render_all = generator.render_all


def test_section_diagram_assets_exist_and_parse_as_svg() -> None:
    expected = {diagram.filename for diagram in diagrams()}
    actual = {path.name for path in DEFAULT_OUTPUT_DIR.glob("*.svg")}

    assert expected <= actual
    for filename in expected:
        root = ET.parse(DEFAULT_OUTPUT_DIR / filename).getroot()
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.attrib["viewBox"] == "0 0 760 470"


def test_section_diagram_assets_match_generator(tmp_path: Path) -> None:
    render_all(tmp_path)

    for diagram in diagrams():
        generated = (tmp_path / diagram.filename).read_text(encoding="utf-8")
        committed = (DEFAULT_OUTPUT_DIR / diagram.filename).read_text(encoding="utf-8")
        assert generated == committed
