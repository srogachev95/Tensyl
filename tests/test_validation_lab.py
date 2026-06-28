from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import load_case, run_case  # noqa: E402


def test_skin_only_smoke_case_writes_metrics_and_manifest(tmp_path: Path) -> None:
    spec = ROOT / "validation" / "cases" / "smoke" / "skin_only.yml"
    outputs = run_case(spec, artifact_dir=tmp_path / "artifacts", command=["run_case.py"])

    metrics = json.loads(outputs["metrics"].read_text(encoding="utf-8"))
    manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))

    assert metrics["case_name"] == "smoke_skin_only"
    assert metrics["checks"]["max_abs_B"] == 0.0
    assert metrics["checks"]["A11_relative_error"] < 1.0e-14
    assert metrics["checks"]["symmetric_ABD"] is True
    assert manifest["case_name"] == "smoke_skin_only"
    assert manifest["metadata"]["solver_required"] is False


def test_load_case_rejects_unknown_case_type(tmp_path: Path) -> None:
    spec = tmp_path / "bad.yml"
    spec.write_text("case_type: not_a_case\nname: bad\n", encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported validation case_type"):
        load_case(spec)
