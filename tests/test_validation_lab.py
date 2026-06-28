from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import load_case, run_case  # noqa: E402
from tensyl_validation.flat_panels import FlatPanelSmearedResponseCase  # noqa: E402


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


def test_flat_panel_smeared_case_writes_target_artifacts(tmp_path: Path) -> None:
    spec = ROOT / "validation" / "cases" / "flat_panels" / "orthogrid_axial_smeared.yml"
    case = load_case(spec)

    assert isinstance(case, FlatPanelSmearedResponseCase)

    outputs = run_case(spec, artifact_dir=tmp_path / "artifacts", command=["run_case.py"])
    response = json.loads(outputs["response"].read_text(encoding="utf-8"))
    metrics = json.loads(outputs["metrics"].read_text(encoding="utf-8"))
    manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))

    assert response["schema_version"] == "tensyl.validation.flat-panel-smeared-response.v1"
    assert response["explicit_fe_status"] == "planned"
    assert response["units"]["resultants"]["N"] == "lbf/in"
    assert response["local_abd_reference"].endswith(
        "validation/cases/local_abd/orthogrid_zero_eccentricity.yml"
    )
    assert response["response"]["end_shortening_e1"] > 0.0
    assert metrics["checks"]["explicit_fe_comparison_available"] is False
    assert metrics["checks"]["smeared_equilibrium_relative_residual"] < 1.0e-12
    assert manifest["metadata"]["artifact_role"] == "tensyl_smeared_panel_target"
    assert manifest["metadata"]["solver_required"] is False
