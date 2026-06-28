#!/usr/bin/env python
"""Report validation solver availability."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.solvers import check_solver_inventory  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require",
        action="store_true",
        help="Exit non-zero when any required solver component is missing.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    inventory = check_solver_inventory(ROOT)
    data = inventory.as_dict()
    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        for key, probe in data["solvers"].items():
            status = "ok" if probe["ok"] else "missing"
            detail = probe["version"] or probe["error"] or ""
            print(f"{key}: {status} ({probe['source'] or 'not found'}) {detail}")

    if args.require and not inventory.ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
