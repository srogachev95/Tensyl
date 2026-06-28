#!/usr/bin/env python
"""Run a matrix of validation case specs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.cases import run_case  # noqa: E402


def _artifact_dir(base: Path, spec: Path) -> Path:
    return base / spec.parent.name / spec.stem


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cases", nargs="+", type=Path, help="Validation case YAML files.")
    parser.add_argument(
        "--artifacts",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "scratch" / "matrix",
        help="Base directory for generated artifacts.",
    )
    args = parser.parse_args(argv)

    failures: list[tuple[Path, Exception]] = []
    for spec in args.cases:
        try:
            outputs = run_case(
                spec,
                artifact_dir=_artifact_dir(args.artifacts, spec),
                command=[sys.argv[0], str(spec)],
            )
        except Exception as exc:  # noqa: BLE001 - report all case failures, then exit non-zero.
            failures.append((spec, exc))
            print(f"failed: {spec}: {exc}", file=sys.stderr)
            continue
        labels = ", ".join(f"{label}={path}" for label, path in outputs.items())
        print(f"ok: {spec}: {labels}")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
