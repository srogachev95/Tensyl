#!/usr/bin/env python
"""Build a compact validation gallery summary from committed artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "tensyl-validation-gallery"
from matplotlib import pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.artifacts import write_json  # noqa: E402


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"{path} must contain a JSON object."
        raise ValueError(msg)
    return data


def _maybe_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return _read_json(path)


def _case_entry(manifest_path: Path) -> dict[str, Any]:
    manifest = _read_json(manifest_path)
    artifact_dir = manifest_path.parent
    metadata = manifest.get("metadata", {})
    artifact_role = metadata.get("artifact_role")
    metrics = _maybe_json(artifact_dir / "metrics.json")
    comparison = (
        _maybe_json(artifact_dir / "comparison_metrics.json")
        if artifact_role != "tensyl_target"
        else None
    )
    checks = {}
    if isinstance(metrics, dict):
        checks.update(metrics.get("checks", {}))
    if isinstance(comparison, dict):
        checks.update(comparison.get("checks", {}))
    return {
        "case_name": manifest.get("case_name"),
        "artifact_dir": str(artifact_dir.relative_to(ROOT)),
        "manifest": str(manifest_path.relative_to(ROOT)),
        "artifact_role": artifact_role,
        "case_type": metadata.get("case_type"),
        "phase": metadata.get("phase"),
        "solver_required": metadata.get("solver_required"),
        "explicit_fe_status": metadata.get("explicit_fe_status"),
        "explicit_fe_comparison": metadata.get("explicit_fe_comparison"),
        "promoted_solver_metrics": _has_promoted_solver_metrics(metrics, comparison),
        "checks": checks,
    }


def _has_promoted_solver_metrics(
    metrics: dict[str, Any] | None,
    comparison: dict[str, Any] | None,
) -> bool:
    if comparison is not None:
        return True
    if metrics is None:
        return False
    comparison_status = metrics.get("comparison", {})
    return bool(
        isinstance(comparison_status, dict)
        and comparison_status.get("promoted_solver_metrics", False)
    )


def build_gallery_summary(base: Path) -> dict[str, Any]:
    """Return a deterministic summary of committed validation artifacts."""

    manifests = sorted(base.rglob("*manifest.json"))
    cases = [_case_entry(path) for path in manifests]
    promoted = [case for case in cases if case["promoted_solver_metrics"]]
    return {
        "schema_version": "tensyl.validation.gallery-summary.v1",
        "source": str(base.relative_to(ROOT)),
        "case_count": len(cases),
        "promoted_solver_case_count": len(promoted),
        "cases": cases,
        "notes": [
            "This summary is generated from committed validation artifact manifests.",
            "Target artifacts and solver-backed comparisons are deliberately distinguished.",
        ],
    }


def write_solver_error_plot(summary: dict[str, Any], output: Path) -> None:
    """Write a compact SVG plot for promoted solver-comparison errors."""

    promoted = [case for case in summary["cases"] if case["promoted_solver_metrics"]]
    labels: list[str] = []
    values: list[float] = []
    for case in promoted:
        checks = case.get("checks", {})
        for key in (
            "ABD6_relative_frobenius_error",
            "A_relative_frobenius_error",
            "B_relative_frobenius_error",
            "D_relative_frobenius_error",
        ):
            if key in checks:
                labels.append(key.replace("_relative_frobenius_error", ""))
                values.append(float(checks[key]))

    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.0, 3.2), layout="constrained")
    if values:
        floor = 1.0e-12
        ax.bar(labels, [value - floor for value in values], bottom=floor, color="#3f6f8f")
        ax.set_yscale("log")
        ax.set_ylim(floor, max(values) * 3.0)
        ax.set_ylabel("relative Frobenius error")
        ax.set_title("Promoted solver comparison errors")
        ax.grid(axis="y", which="both", alpha=0.25)
    else:
        ax.text(0.5, 0.5, "No promoted solver comparisons", ha="center", va="center")
        ax.set_axis_off()
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "committed",
        help="Committed validation artifact root to scan.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "committed" / "gallery_summary.json",
        help="Output JSON path.",
    )
    parser.add_argument(
        "--plot-output",
        type=Path,
        default=ROOT / "docs" / "assets" / "validation" / "gallery-solver-errors.svg",
        help="Output SVG path for promoted solver error plot.",
    )
    args = parser.parse_args(argv)

    summary = build_gallery_summary(args.base)
    write_json(args.output, summary)
    write_solver_error_plot(summary, args.plot_output)
    print(f"summary: {args.output}")
    print(f"plot: {args.plot_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
