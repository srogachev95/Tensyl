from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_run_matrix_runs_multiple_cases(tmp_path: Path) -> None:
    smoke = ROOT / "validation" / "cases" / "smoke" / "skin_only.yml"
    flat_panel = ROOT / "validation" / "cases" / "flat_panels" / "orthogrid_axial_smeared.yml"
    barrel = ROOT / "validation" / "cases" / "barrels" / "orthogrid_axial_smeared.yml"
    local = tmp_path / "local.yml"
    local.write_text(
        """
schema_version: tensyl.validation.case.v1
case_type: local_abd
name: script_skin_only
model: skin_only
material:
  E: 10600000.0
  nu: 0.33
skin_thickness: 0.08
geometry: {}
""",
        encoding="utf-8",
    )

    completed = subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(ROOT / "validation" / "scripts" / "run_matrix.py"),
            str(local),
            str(smoke),
            str(flat_panel),
            str(barrel),
            "--artifacts",
            str(tmp_path / "artifacts"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert "ok:" in completed.stdout
    assert (tmp_path / "artifacts" / "smoke" / "skin_only" / "metrics.json").exists()
    assert (tmp_path / "artifacts" / tmp_path.name / "local" / "target_abd.json").exists()
    assert (
        tmp_path / "artifacts" / "flat_panels" / "orthogrid_axial_smeared" / "smeared_response.json"
    ).exists()
    assert (
        tmp_path / "artifacts" / "barrels" / "orthogrid_axial_smeared" / "smeared_response.json"
    ).exists()


def test_build_gallery_summary_writes_json_and_plot(tmp_path: Path) -> None:
    summary = tmp_path / "gallery_summary.json"
    plot = tmp_path / "gallery_solver_errors.svg"

    completed = subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(ROOT / "validation" / "scripts" / "build_gallery_summary.py"),
            "--output",
            str(summary),
            "--plot-output",
            str(plot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert data["case_count"] >= 1
    assert data["promoted_solver_case_count"] == 1
    assert plot.read_text(encoding="utf-8").startswith("<?xml")


def test_build_skin_only_abd6_comparison_writes_table_and_plot(tmp_path: Path) -> None:
    table = tmp_path / "abd6_comparison_table.json"
    csv_table = tmp_path / "abd6_comparison_table.csv"
    plot = tmp_path / "skin_only_abd6_relative_error.svg"

    completed = subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(ROOT / "validation" / "scripts" / "build_skin_only_abd6_comparison.py"),
            "--json-output",
            str(table),
            "--csv-output",
            str(csv_table),
            "--plot-output",
            str(plot),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    data = json.loads(table.read_text(encoding="utf-8"))
    assert data["schema_version"] == "tensyl.validation.skin-only-abd6-comparison-table.v1"
    assert data["case_name"] == "local_abd_skin_only"
    assert len(data["rows"]) == 36
    assert math.isclose(
        data["checks"]["frobenius_relative_error"],
        3.787943382534907e-08,
        rel_tol=1.0e-12,
    )
    assert csv_table.read_text(encoding="utf-8").splitlines()[0].startswith("resultant,strain")
    assert plot.read_text(encoding="utf-8").startswith("<?xml")


def test_build_sp8007_reconciliation_writes_artifacts_and_plots(tmp_path: Path) -> None:
    artifact_dir = tmp_path / "sp8007"
    plot_dir = tmp_path / "plots"

    completed = subprocess.run(
        [
            "uv",
            "run",
            "python",
            str(ROOT / "validation" / "scripts" / "build_sp8007_reconciliation.py"),
            "--artifact-dir",
            str(artifact_dir),
            "--plot-dir",
            str(plot_dir),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    table = json.loads((artifact_dir / "comparison_table.json").read_text(encoding="utf-8"))
    summary = json.loads((artifact_dir / "summary.json").read_text(encoding="utf-8"))
    sweep = json.loads((artifact_dir / "inplane_bending_sweep.json").read_text(encoding="utf-8"))
    torsion_sweep = json.loads((artifact_dir / "torsion_sweep.json").read_text(encoding="utf-8"))

    assert table["schema_version"] == "tensyl.validation.sp8007-reconciliation-table.v2"
    assert len(table["cases"]) == 5
    assert len(table["rows"]) == 55
    assert summary["source_equations"]["orthogrid"].endswith("Eqs. 82-91")
    assert summary["source_equations"]["isogrid"].endswith("Eqs. 92-98")
    assert "parallel-axis" in summary["source_equations"]["isogrid_correction"]
    assert any(
        item["case_name"] == "isogrid_suppressed_inplane_bending_eccentric"
        and item["worst_abs_relative_delta_corrected"] < 1.0e-3
        for item in summary["worst_by_case"]
    )
    assert len(sweep["rows"]) == 10
    assert torsion_sweep["schema_version"] == "tensyl.validation.sp8007-torsion-sweep.v1"
    assert len(torsion_sweep["rows"]) == 10
    assert (
        (artifact_dir / "comparison_table.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
        .startswith("case_name,model,coefficient,tensyl,sp8007_as_written,sp8007_corrected")
    )
    assert (plot_dir / "sp8007-term-errors.svg").read_text(encoding="utf-8").startswith("<?xml")
    assert (
        (plot_dir / "sp8007-isogrid-correction.svg").read_text(encoding="utf-8").startswith("<?xml")
    )
    assert (plot_dir / "sp8007-bending-ratio.svg").read_text(encoding="utf-8").startswith("<?xml")
    assert (
        (plot_dir / "sp8007-inplane-bending-sweep.svg")
        .read_text(encoding="utf-8")
        .startswith("<?xml")
    )
    assert (plot_dir / "sp8007-torsion-sweep.svg").read_text(encoding="utf-8").startswith("<?xml")
