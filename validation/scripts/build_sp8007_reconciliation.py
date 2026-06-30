#!/usr/bin/env python
"""Build SP-8007 reconciliation artifacts and plots."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "tensyl-sp8007-reconciliation"
from matplotlib import pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.artifacts import ArtifactManifest, write_json  # noqa: E402
from tensyl_validation.sp8007 import (  # noqa: E402
    BENDING_COEFFICIENTS,
    COEFFICIENTS,
    comparison_rows,
    default_reconciliation_cases,
    summary_payload,
    sweep_rows,
)


def _repo_relative(path: Path) -> Path:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT)
    except ValueError:
        return path


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "case_name",
        "model",
        "coefficient",
        "tensyl",
        "sp8007_as_written",
        "delta",
        "relative_delta",
        "abs_relative_delta",
        "case_note",
    ]
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _strip_trailing_whitespace(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def _case_short_name(case_name: str) -> str:
    return (
        case_name.replace("orthogrid_", "ortho\n")
        .replace("isogrid_", "iso\n")
        .replace("_inplane_bending", "\nin-plane")
        .replace("_eccentricity", "\necc.")
        .replace("_eccentric", "\necc.")
        .replace("_zero", "\nzero")
        .replace("_section", "\nsection")
        .replace("_suppressed", "\nsuppressed")
    )


def write_term_error_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write a coefficient error plot for all report cases."""

    case_names = sorted({str(row["case_name"]) for row in rows})
    coefficients = list(COEFFICIENTS)
    values = [
        [
            max(
                float(row["abs_relative_delta"])
                for row in rows
                if row["case_name"] == case_name and row["coefficient"] == coefficient
            )
            for coefficient in coefficients
        ]
        for case_name in case_names
    ]
    floor = 1.0e-12
    x = range(len(coefficients))
    width = 0.14

    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.2, 4.6), layout="constrained")
    for idx, case_name in enumerate(case_names):
        offset = (idx - (len(case_names) - 1) / 2.0) * width
        ax.bar(
            [item + offset for item in x],
            [max(value, floor) for value in values[idx]],
            width=width,
            label=_case_short_name(case_name),
        )
    ax.set_yscale("log")
    ax.set_ylim(floor, max(max(row) for row in values) * 4.0)
    ax.set_ylabel("absolute relative delta")
    ax.set_title("Tensyl vs. SP-8007 coefficient deltas")
    ax.set_xticks(list(x), coefficients, rotation=40, ha="right")
    ax.grid(axis="y", which="both", alpha=0.25)
    ax.legend(ncols=2, fontsize=8)
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)
    _strip_trailing_whitespace(output)


def write_bending_ratio_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write a bending ratio plot for the most important coefficients."""

    case_names = sorted({str(row["case_name"]) for row in rows})
    coefficients = list(BENDING_COEFFICIENTS)
    values = []
    for case_name in case_names:
        case_values = []
        for coefficient in coefficients:
            row = next(
                row
                for row in rows
                if row["case_name"] == case_name and row["coefficient"] == coefficient
            )
            expected = float(row["sp8007_as_written"])
            case_values.append(float(row["tensyl"]) / expected if expected != 0.0 else 0.0)
        values.append(case_values)

    x = range(len(case_names))
    width = 0.22
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8.8, 4.4), layout="constrained")
    for idx, coefficient in enumerate(coefficients):
        offset = (idx - 1) * width
        ax.bar(
            [item + offset for item in x],
            [value[idx] for value in values],
            width=width,
            label=coefficient,
        )
    ax.axhline(1.0, color="#222222", linewidth=1.0)
    ax.set_ylabel("Tensyl / SP-8007 as written")
    ax.set_title("Bending coefficient ratio")
    ax.set_xticks(list(x), [_case_short_name(item) for item in case_names], rotation=0)
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)
    _strip_trailing_whitespace(output)


def write_inplane_bending_sweep_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write the in-plane beam-bending sensitivity sweep."""

    case_names = sorted({str(row["case_name"]) for row in rows})
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.2, 4.0), layout="constrained")
    for case_name in case_names:
        case_rows = [row for row in rows if row["case_name"] == case_name]
        case_rows.sort(key=lambda row: float(row["in_plane_inertia_ratio"]))
        ax.plot(
            [float(row["in_plane_inertia_ratio"]) for row in case_rows],
            [float(row["max_bending_abs_relative_delta"]) for row in case_rows],
            marker="o",
            label=_case_short_name(case_name),
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("in-plane inertia / out-of-plane inertia")
    ax.set_ylabel("max bending absolute relative delta")
    ax.set_title("Sensitivity to retained in-plane member bending")
    ax.grid(which="both", alpha=0.25)
    ax.legend()
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)
    _strip_trailing_whitespace(output)


def build_outputs(
    *,
    artifact_dir: Path,
    plot_dir: Path,
    command: list[str],
) -> dict[str, Path]:
    """Build all SP-8007 reconciliation artifacts."""

    rows = comparison_rows()
    sweep = sweep_rows()
    summary = summary_payload(rows, sweep)
    cases = [case.as_dict() for case in default_reconciliation_cases()]

    table_json = artifact_dir / "comparison_table.json"
    table_csv = artifact_dir / "comparison_table.csv"
    summary_json = artifact_dir / "summary.json"
    sweep_json = artifact_dir / "inplane_bending_sweep.json"
    manifest_path = artifact_dir / "manifest.json"
    term_plot = plot_dir / "sp8007-term-errors.svg"
    bending_plot = plot_dir / "sp8007-bending-ratio.svg"
    sweep_plot = plot_dir / "sp8007-inplane-bending-sweep.svg"

    write_json(
        table_json,
        {
            "schema_version": "tensyl.validation.sp8007-reconciliation-table.v1",
            "cases": cases,
            "rows": rows,
        },
    )
    _write_csv(table_csv, rows)
    write_json(summary_json, summary)
    write_json(
        sweep_json,
        {
            "schema_version": "tensyl.validation.sp8007-inplane-bending-sweep.v1",
            "rows": sweep,
        },
    )
    write_term_error_plot(rows, term_plot)
    write_bending_ratio_plot(rows, bending_plot)
    write_inplane_bending_sweep_plot(sweep, sweep_plot)

    manifest = ArtifactManifest(
        case_name="sp8007_reconciliation",
        command=command,
        inputs=[],
        outputs=[
            _repo_relative(table_json),
            _repo_relative(table_csv),
            _repo_relative(summary_json),
            _repo_relative(sweep_json),
            _repo_relative(term_plot),
            _repo_relative(bending_plot),
            _repo_relative(sweep_plot),
            _repo_relative(manifest_path),
        ],
        metadata={
            "case_type": "sp8007_reconciliation",
            "artifact_role": "literature_comparison",
            "solver_required": False,
            "phase": "validation",
            "reference_is_oracle": False,
        },
    )
    write_json(manifest_path, manifest.as_dict())
    return {
        "table_json": table_json,
        "table_csv": table_csv,
        "summary": summary_json,
        "sweep": sweep_json,
        "term_plot": term_plot,
        "bending_plot": bending_plot,
        "sweep_plot": sweep_plot,
        "manifest": manifest_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--artifact-dir",
        type=Path,
        default=ROOT / "validation" / "artifacts" / "committed" / "sp8007_reconciliation",
        help="Directory for JSON/CSV comparison artifacts.",
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=ROOT / "docs" / "assets" / "validation",
        help="Directory for report SVG plots.",
    )
    args = parser.parse_args(argv)

    outputs = build_outputs(
        artifact_dir=args.artifact_dir,
        plot_dir=args.plot_dir,
        command=sys.argv,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
