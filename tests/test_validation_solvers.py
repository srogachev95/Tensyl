from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.solvers import check_solver_inventory, find_solver_executable  # noqa: E402


def _fake_executable(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nprintf 'fake\\n'\n", encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)


def test_solver_discovery_prefers_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    explicit = tmp_path / "explicit" / "ccx"
    project = tmp_path / "validation" / ".solver-env" / "bin" / "ccx"
    _fake_executable(explicit)
    _fake_executable(project)
    monkeypatch.setenv("TENSYL_CCX", str(explicit))

    found = find_solver_executable("ccx", env_var="TENSYL_CCX", project_root=tmp_path)

    assert found == (explicit, "TENSYL_CCX")


def test_solver_discovery_uses_project_environment_before_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    project = tmp_path / "validation" / ".solver-env" / "bin" / "gmsh"
    path_dir = tmp_path / "path-bin"
    path_tool = path_dir / "gmsh"
    _fake_executable(project)
    _fake_executable(path_tool)
    monkeypatch.delenv("TENSYL_GMSH", raising=False)
    monkeypatch.setenv("PATH", str(path_dir))

    found = find_solver_executable("gmsh", env_var="TENSYL_GMSH", project_root=tmp_path)

    assert found == (project, "validation/.solver-env")


def test_missing_solver_inventory_is_not_ok_when_required_tools_are_absent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("TENSYL_CCX", raising=False)
    monkeypatch.delenv("TENSYL_GMSH", raising=False)
    monkeypatch.setenv("PATH", os.devnull)

    inventory = check_solver_inventory(tmp_path)

    assert inventory.ok is False
    assert inventory.ccx.ok is False
    assert inventory.gmsh.ok is False
