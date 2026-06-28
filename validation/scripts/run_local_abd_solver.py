#!/usr/bin/env python
"""Run solver-backed local ABD extraction for supported cases."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.local_abd_solver import run_skin_only_solver_extraction  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path, help="Path to a local ABD case YAML file.")
    parser.add_argument(
        "--artifacts",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "scratch" / "local_abd_solver",
        help="Directory for compact extracted artifacts.",
    )
    parser.add_argument(
        "--work-dir",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "scratch" / "local_abd_solver_raw",
        help="Directory for raw solver decks and outputs.",
    )
    args = parser.parse_args(argv)

    outputs = run_skin_only_solver_extraction(
        args.case,
        artifact_dir=args.artifacts,
        work_dir=args.work_dir,
        command=sys.argv,
        project_root=ROOT,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
