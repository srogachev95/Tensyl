#!/usr/bin/env python
"""Compare an extracted local ABD stiffness against a Tensyl target artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.artifacts import write_json  # noqa: E402
from tensyl_validation.metrics import abd_comparison_metrics  # noqa: E402


def _load_c8(path: Path) -> np.ndarray:
    data = json.loads(path.read_text(encoding="utf-8"))
    blocks = data.get("blocks")
    if not isinstance(blocks, dict) or "C8" not in blocks:
        msg = f"{path} must contain blocks.C8."
        raise ValueError(msg)
    return np.asarray(blocks["C8"], dtype=np.float64)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-name", required=True, help="Validation case name.")
    parser.add_argument("--actual", type=Path, required=True, help="Extracted stiffness JSON.")
    parser.add_argument(
        "--expected",
        type=Path,
        required=True,
        help="Tensyl target stiffness JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Output JSON path for comparison metrics.",
    )
    args = parser.parse_args(argv)

    metrics = abd_comparison_metrics(
        _load_c8(args.actual),
        _load_c8(args.expected),
        case_name=args.case_name,
    )
    write_json(args.output, metrics)
    print(f"metrics: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
