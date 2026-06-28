#!/usr/bin/env python
"""Run one validation case."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import run_case  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path, help="Path to a validation case YAML file.")
    parser.add_argument(
        "--artifacts",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "scratch" / "run",
        help="Directory for generated metrics and manifests.",
    )
    args = parser.parse_args(argv)

    outputs = run_case(args.case, artifact_dir=args.artifacts, command=sys.argv)
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
