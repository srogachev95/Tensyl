#!/usr/bin/env python
"""Run solver-backed local ABD extraction for supported cases."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import load_case  # noqa: E402
from tensyl_validation.local_abd import LocalABDCase  # noqa: E402
from tensyl_validation.local_abd_solver import (  # noqa: E402
    UnsupportedSolverExtractionError,
    prepare_unidirectional_stiffened_probe_decks,
    run_skin_only_solver_extraction,
)


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
    parser.add_argument(
        "--prepare-probe-decks",
        action="store_true",
        help=(
            "Write non-promoted review/probe decks for supported stiffened cases instead "
            "of running solver extraction."
        ),
    )
    args = parser.parse_args(argv)

    loaded = load_case(args.case)
    if not isinstance(loaded, LocalABDCase):
        msg = f"{args.case} is not a local ABD validation case."
        raise TypeError(msg)
    if loaded.model == "skin_only" and not args.prepare_probe_decks:
        outputs = run_skin_only_solver_extraction(
            args.case,
            artifact_dir=args.artifacts,
            work_dir=args.work_dir,
            command=sys.argv,
            project_root=ROOT,
        )
    elif loaded.model == "unidirectional" and args.prepare_probe_decks:
        outputs = prepare_unidirectional_stiffened_probe_decks(
            args.case,
            artifact_dir=args.artifacts,
            work_dir=args.work_dir,
            command=sys.argv,
        )
    else:
        msg = (
            f"{loaded.model!r} does not have a promoted solver extraction runner. "
            "Use --prepare-probe-decks for supported stiffened preflight decks."
        )
        raise UnsupportedSolverExtractionError(msg)

    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
