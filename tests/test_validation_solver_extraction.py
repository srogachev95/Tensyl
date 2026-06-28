from __future__ import annotations

# ruff: noqa: E402,I001

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import json
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.calculix.parsers import CalculixStressRow, CalculixStressTable  # noqa: E402
from tensyl_validation.local_abd_solver import (  # noqa: E402
    prepare_unidirectional_stiffened_probe_decks,
    extract_skin_only_abd6_from_stress_tables,
    run_unidirectional_stiffened_probe,
)


def _table(
    *,
    sxx_bottom: float,
    sxx_top: float,
    syy_bottom: float = 0.0,
    syy_top: float = 0.0,
    sxy_bottom: float = 0.0,
    sxy_top: float = 0.0,
) -> CalculixStressTable:
    return CalculixStressTable(
        load_case=None,
        rows=(
            CalculixStressRow(1, 1, sxx_bottom, syy_bottom, 0.0, sxy_bottom, 0.0, 0.0),
            CalculixStressRow(1, 5, sxx_top, syy_top, 0.0, sxy_top, 0.0, 0.0),
        ),
    )


def test_skin_only_extraction_assembles_abd6_from_stress_tables() -> None:
    tables = {
        "epsilon_11": _table(sxx_bottom=10.0, sxx_top=10.0, syy_bottom=2.0, syy_top=2.0),
        "epsilon_22": _table(sxx_bottom=3.0, sxx_top=3.0, syy_bottom=9.0, syy_top=9.0),
        "gamma_12": _table(sxx_bottom=0.0, sxx_top=0.0, sxy_bottom=5.0, sxy_top=5.0),
        "kappa_11": _table(sxx_bottom=-12.0, sxx_top=12.0, syy_bottom=-4.0, syy_top=4.0),
        "kappa_22": _table(sxx_bottom=-1.0, sxx_top=1.0, syy_bottom=-8.0, syy_top=8.0),
        "kappa_12": _table(sxx_bottom=0.0, sxx_top=0.0, sxy_bottom=-6.0, sxy_top=6.0),
    }
    magnitudes = {component: 0.5 for component in tables}

    abd6 = extract_skin_only_abd6_from_stress_tables(
        tables,
        thickness=0.2,
        magnitudes_by_component=magnitudes,
    )

    assert abd6.shape == (6, 6)
    assert abd6[0, 0] == 4.0
    assert abd6[1, 1] == 3.6
    assert abd6[2, 2] == 2.0
    assert abd6[3, 3] == np.float64((24.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)
    assert abd6[4, 4] == np.float64((16.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)
    assert abd6[5, 5] == np.float64((12.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)


def test_unidirectional_stiffened_probe_writes_non_promoted_manifest(tmp_path: Path) -> None:
    spec = ROOT / "validation" / "cases" / "local_abd" / "unidirectional.yml"

    outputs = prepare_unidirectional_stiffened_probe_decks(
        spec,
        artifact_dir=tmp_path / "artifacts",
        work_dir=tmp_path / "raw",
        command=["run_local_abd_solver.py", str(spec), "--prepare-probe-decks"],
    )

    summary = json.loads(outputs["summary"].read_text(encoding="utf-8"))
    manifest = json.loads(outputs["manifest"].read_text(encoding="utf-8"))

    assert summary["status"] == "review_deck_only"
    assert summary["solver_extraction_promoted"] is False
    assert summary["deck_count"] == 6
    assert manifest["metadata"]["artifact_role"] == "calculix_probe_deck"
    assert manifest["metadata"]["solver_required"] is False
    assert manifest["metadata"]["unsupported_blocks"] == ["A", "B", "D", "As"]
    assert (outputs["decks"] / "epsilon_11.inp").exists()


def test_unidirectional_stiffened_probe_run_summarizes_stress_blocks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import tensyl_validation.local_abd_solver as solver

    spec = ROOT / "validation" / "cases" / "local_abd" / "unidirectional.yml"
    ccx = SimpleNamespace(
        ok=True,
        path="/fake/ccx",
        as_dict=lambda: {"ok": True, "path": "/fake/ccx"},
    )
    monkeypatch.setattr(
        solver,
        "check_solver_inventory",
        lambda _root: SimpleNamespace(ccx=ccx),
    )

    def fake_run(
        cmd: list[str],
        *,
        cwd: Path,
        check: bool,
        capture_output: bool,
        text: bool,
        timeout: int,
    ) -> subprocess.CompletedProcess[str]:
        del check, capture_output, text, timeout
        case_id = cmd[1]
        (cwd / f"{case_id}.dat").write_text(
            """
            stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set SKIN and time 1.0
              1 1 10.0 2.0 0.0 3.0 0.0 0.0
            stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set STIFFENER and time 1.0
            101 1 20.0 0.0 0.0 0.0 0.0 0.0
            """,
            encoding="utf-8",
        )
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(solver, "subprocess", SimpleNamespace(run=fake_run))

    outputs = run_unidirectional_stiffened_probe(
        spec,
        artifact_dir=tmp_path / "artifacts",
        work_dir=tmp_path / "raw",
        command=["run_local_abd_solver.py", str(spec), "--run-probe-decks"],
        project_root=ROOT,
    )

    summary = json.loads(outputs["run_summary"].read_text(encoding="utf-8"))
    manifest = json.loads(outputs["run_manifest"].read_text(encoding="utf-8"))

    assert summary["status"] == "solver_probe_completed_not_promoted"
    assert summary["load_case_count"] == 6
    assert summary["load_cases"][0]["stress_blocks"]["SKIN"]["row_count"] == 1
    assert summary["load_cases"][0]["stress_blocks"]["STIFFENER"]["row_count"] == 1
    assert manifest["metadata"]["artifact_role"] == "calculix_probe_run"
    assert manifest["metadata"]["solver_extraction_promoted"] is False
