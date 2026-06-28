"""Solver discovery for the validation laboratory."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_SOLVER_ENV = Path("validation/.solver-env")


@dataclass(frozen=True, slots=True)
class SolverProbe:
    """Discovery and version result for one external tool."""

    name: str
    ok: bool
    source: str | None = None
    path: str | None = None
    version: str | None = None
    error: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "ok": self.ok,
            "source": self.source,
            "path": self.path,
            "version": self.version,
            "error": self.error,
        }


@dataclass(frozen=True, slots=True)
class SolverInventory:
    """Current validation-solver inventory."""

    ccx: SolverProbe
    gmsh: SolverProbe
    python_gmsh: SolverProbe

    @property
    def ok(self) -> bool:
        return self.ccx.ok and self.gmsh.ok and self.python_gmsh.ok

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "solvers": {
                "ccx": self.ccx.as_dict(),
                "gmsh": self.gmsh.as_dict(),
                "python_gmsh": self.python_gmsh.as_dict(),
            },
        }


def _project_solver_env(project_root: Path) -> Path:
    return project_root / DEFAULT_SOLVER_ENV


def _candidate_from_env(env_var: str) -> tuple[Path, str] | None:
    value = os.environ.get(env_var)
    if value:
        return Path(value), env_var
    return None


def _candidate_from_project_env(project_root: Path, executable: str) -> tuple[Path, str] | None:
    path = _project_solver_env(project_root) / "bin" / executable
    if path.exists():
        return path, str(DEFAULT_SOLVER_ENV)
    return None


def _candidate_from_path(executable: str) -> tuple[Path, str] | None:
    found = shutil.which(executable)
    if found:
        return Path(found), "PATH"
    return None


def find_solver_executable(
    executable: str,
    *,
    env_var: str,
    project_root: Path,
) -> tuple[Path, str] | None:
    """Find a solver executable using Tensyl's validation discovery order."""

    for candidate in (
        _candidate_from_env(env_var),
        _candidate_from_project_env(project_root, executable),
        _candidate_from_path(executable),
    ):
        if candidate is not None:
            return candidate
    return None


def _version_from_command(
    path: Path,
    args: list[str],
    *,
    success_returncodes: tuple[int, ...] = (0,),
) -> tuple[bool, str | None, str | None]:
    try:
        completed = subprocess.run(
            [str(path), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except OSError as exc:
        return False, None, str(exc)
    output = "\n".join(part.strip() for part in (completed.stdout, completed.stderr) if part.strip())
    first_line = output.splitlines()[0] if output else None
    if completed.returncode not in success_returncodes:
        return False, None, output or f"exit code {completed.returncode}"
    return True, first_line, None


def _probe_executable(
    name: str,
    executable: str,
    version_args: list[str],
    *,
    env_var: str,
    project_root: Path,
    success_returncodes: tuple[int, ...] = (0,),
) -> SolverProbe:
    candidate = find_solver_executable(executable, env_var=env_var, project_root=project_root)
    if candidate is None:
        return SolverProbe(name=name, ok=False, error=f"{executable!r} was not found")
    path, source = candidate
    if not path.exists():
        return SolverProbe(
            name=name,
            ok=False,
            source=source,
            path=str(path),
            error="configured executable does not exist",
        )
    ok, version, error = _version_from_command(
        path,
        version_args,
        success_returncodes=success_returncodes,
    )
    return SolverProbe(name=name, ok=ok, source=source, path=str(path), version=version, error=error)


def _python_gmsh_candidate(project_root: Path) -> tuple[Path, str]:
    env_python = _project_solver_env(project_root) / "bin" / "python"
    if env_python.exists():
        return env_python, str(DEFAULT_SOLVER_ENV)
    return Path(sys.executable), "current-python"


def _probe_python_gmsh(project_root: Path) -> SolverProbe:
    python_path, source = _python_gmsh_candidate(project_root)
    ok, version, error = _version_from_command(
        python_path,
        ["-c", "import gmsh; print(gmsh.__version__)"],
    )
    return SolverProbe(
        name="python-gmsh",
        ok=ok,
        source=source,
        path=str(python_path),
        version=version,
        error=error,
    )


def check_solver_inventory(project_root: Path | None = None) -> SolverInventory:
    """Return the currently discoverable solver inventory."""

    root = Path.cwd() if project_root is None else project_root
    return SolverInventory(
        ccx=_probe_executable(
            "CalculiX/CCX",
            "ccx",
            ["-v"],
            env_var="TENSYL_CCX",
            project_root=root,
            success_returncodes=(0, 201),
        ),
        gmsh=_probe_executable(
            "Gmsh",
            "gmsh",
            ["--version"],
            env_var="TENSYL_GMSH",
            project_root=root,
        ),
        python_gmsh=_probe_python_gmsh(root),
    )
