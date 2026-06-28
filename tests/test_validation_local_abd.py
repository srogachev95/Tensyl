from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import load_case, run_case  # noqa: E402
from tensyl_validation.local_abd import LocalABDCase, target_stiffness  # noqa: E402


def _base_spec(model: str) -> str:
    section = """
section:
  EA: 1200.0
  EIy: 50.0
  EIz: 30.0
  GJ: 20.0
  kGAy: 400.0
  kGAz: 300.0
"""
    geometry = {
        "skin_only": "geometry: {}\n",
        "unidirectional": "geometry:\n  spacing: 2.0\n  eccentricity: 0.0\n",
        "orthogrid": (
            "geometry:\n"
            "  stringer_spacing: 2.0\n"
            "  rib_spacing: 3.0\n"
            "  stringer_eccentricity: 0.1\n"
            "  rib_eccentricity: 0.0\n"
        ),
        "equilateral_isogrid": "geometry:\n  pitch: 2.0\n  eccentricity: 0.0\n",
    }[model]
    section_text = "" if model == "skin_only" else section
    return f"""
schema_version: tensyl.validation.case.v1
case_type: local_abd
name: {model}_target
model: {model}
material:
  E: 10600000.0
  nu: 0.33
  density: 0.1
skin_thickness: 0.08
units:
  length: in
  force: lbf
  stress: psi
{section_text}{geometry}
"""


def test_local_abd_case_loads_and_computes_target(tmp_path: Path) -> None:
    spec = tmp_path / "case.yml"
    spec.write_text(_base_spec("orthogrid"), encoding="utf-8")

    case = load_case(spec)
    assert isinstance(case, LocalABDCase)

    stiffness = target_stiffness(case)

    assert stiffness.A[0, 0] > 0.0
    assert stiffness.B[0, 0] > 0.0
    assert np.allclose(stiffness.C8, stiffness.C8.T)


def test_run_case_writes_local_abd_target_artifacts(tmp_path: Path) -> None:
    spec = tmp_path / "case.yml"
    spec.write_text(_base_spec("skin_only"), encoding="utf-8")

    outputs = run_case(spec, artifact_dir=tmp_path / "artifacts", command=["run_case.py"])

    target = json.loads(outputs["target"].read_text(encoding="utf-8"))
    metrics = json.loads(outputs["metrics"].read_text(encoding="utf-8"))
    manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))

    assert target["schema_version"] == "tensyl.validation.local-abd-target.v1"
    assert target["blocks"]["A"][0][0] > 0.0
    assert metrics["case_type"] == "local_abd"
    assert metrics["checks"]["symmetric_C8"] is True
    assert manifest["metadata"]["artifact_role"] == "tensyl_target"
