from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_run_matrix_runs_multiple_cases(tmp_path: Path) -> None:
    smoke = ROOT / "validation" / "cases" / "smoke" / "skin_only.yml"
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
