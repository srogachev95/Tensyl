#!/usr/bin/env python
"""Create or update Tensyl's project-local validation solver environment."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.solvers import check_solver_inventory  # noqa: E402


def _run(command: list[str]) -> None:
    print(" ".join(command))
    subprocess.run(command, check=True)


def _ensure_micromamba(install_with_brew: bool) -> str:
    micromamba = shutil.which("micromamba")
    if micromamba is not None:
        return micromamba
    if not install_with_brew:
        msg = (
            "micromamba was not found. Install it with Homebrew or rerun with --install-micromamba."
        )
        raise RuntimeError(msg)
    brew = shutil.which("brew")
    if brew is None:
        msg = "Homebrew was not found, so micromamba cannot be installed automatically."
        raise RuntimeError(msg)
    _run([brew, "install", "micromamba"])
    micromamba = shutil.which("micromamba")
    if micromamba is None:
        msg = "Homebrew completed, but micromamba is still not on PATH."
        raise RuntimeError(msg)
    return micromamba


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prefix",
        type=Path,
        default=ROOT / "validation" / ".solver-env",
        help="Project-local solver environment prefix.",
    )
    parser.add_argument(
        "--environment",
        type=Path,
        default=ROOT / "validation" / "solver-environment.yml",
        help="Conda environment YAML file.",
    )
    parser.add_argument(
        "--install-micromamba",
        action="store_true",
        help="Install micromamba with Homebrew when it is missing.",
    )
    args = parser.parse_args(argv)

    micromamba = _ensure_micromamba(args.install_micromamba)
    args.prefix.parent.mkdir(parents=True, exist_ok=True)
    if (args.prefix / "conda-meta").exists():
        command = [
            micromamba,
            "env",
            "update",
            "--yes",
            "--prefix",
            str(args.prefix),
            "--file",
            str(args.environment),
        ]
    else:
        command = [
            micromamba,
            "create",
            "--yes",
            "--prefix",
            str(args.prefix),
            "--file",
            str(args.environment),
        ]
    _run(command)

    inventory = check_solver_inventory(ROOT)
    if not inventory.ok:
        print("Solver environment was created, but verification failed:", file=sys.stderr)
        for key, probe in inventory.as_dict()["solvers"].items():
            if not probe["ok"]:
                print(f"- {key}: {probe['error']}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
