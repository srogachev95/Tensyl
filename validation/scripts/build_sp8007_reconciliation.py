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
    torsion_sweep_rows,
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
        "sp8007_corrected",
        "delta_as_written",
        "relative_delta_as_written",
        "abs_relative_delta_as_written",
        "delta_corrected",
        "relative_delta_corrected",
        "abs_relative_delta_corrected",
        "interpretation",
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
    labels = {
        "orthogrid_eccentric": "orthogrid",
        "isogrid_zero_eccentricity": "isogrid, z = 0",
        "isogrid_eccentric": "isogrid, z = 0.32 in",
        "orthogrid_torsion_sweep": "orthogrid",
        "isogrid_torsion_sweep": "isogrid",
    }
    return labels.get(case_name, case_name.replace("_", " "))


def write_term_error_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write a coefficient error plot for all report cases."""

    case_names = sorted({str(row["case_name"]) for row in rows})
    coefficients = list(COEFFICIENTS)
    values = [
        [
            max(
                float(row["abs_relative_delta_corrected"])
                for row in rows
                if row["case_name"] == case_name and row["coefficient"] == coefficient
            )
            for coefficient in coefficients
        ]
        for case_name in case_names
    ]
    floor = 1.0e-18
    agreement = 1.0e-12
    x = range(len(coefficients))
    width = 0.14

    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.8, 5.2), layout="constrained")
    for idx, case_name in enumerate(case_names):
        offset = (idx - (len(case_names) - 1) / 2.0) * width
        ax.bar(
            [item + offset for item in x],
            [max(value, floor) for value in values[idx]],
            width=width,
            label=_case_short_name(case_name),
        )
    ax.axhline(agreement, color="#222222", linewidth=1.0, linestyle="--")
    ax.annotate(
        "roundoff agreement limit",
        xy=(len(coefficients) - 0.5, agreement),
        xytext=(0, 4),
        textcoords="offset points",
        ha="right",
        fontsize=8,
    )
    ax.set_yscale("log")
    ax.set_ylim(floor, max(1.0e-6, max(max(row) for row in values) * 4.0))
    ax.set_ylabel("absolute relative delta, corrected reference")
    ax.set_title("Tensyl vs. corrected SP-8007 coefficient deltas")
    ax.set_xticks(list(x), coefficients, rotation=40, ha="right")
    ax.grid(axis="y", which="both", alpha=0.25)
    ax.legend(ncols=3, fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.23))
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)
    _strip_trailing_whitespace(output)


def write_isogrid_correction_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write a plot that isolates the SP-8007 printed isogrid omission."""

    case_name = "isogrid_eccentric"
    coefficients = list(BENDING_COEFFICIENTS)
    case_rows = {
        str(row["coefficient"]): row
        for row in rows
        if row["case_name"] == case_name and row["coefficient"] in coefficients
    }
    x = range(len(coefficients))
    width = 0.26
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.2), layout="constrained")
    ax.bar(
        [item - width for item in x],
        [float(case_rows[coefficient]["tensyl"]) for coefficient in coefficients],
        width=width,
        label="Tensyl",
        color="#3b6ea8",
    )
    ax.bar(
        list(x),
        [float(case_rows[coefficient]["sp8007_as_written"]) for coefficient in coefficients],
        width=width,
        label="SP-8007 as printed",
        color="#c95f36",
    )
    ax.bar(
        [item + width for item in x],
        [float(case_rows[coefficient]["sp8007_corrected"]) for coefficient in coefficients],
        width=width,
        label="SP-8007 corrected",
        color="#5a8f58",
    )
    ax.set_ylabel("coefficient value")
    ax.set_title("Eccentric isogrid bending terms")
    ax.set_xticks(list(x), coefficients)
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncols=3, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.14))
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)
    _strip_trailing_whitespace(output)


def write_torsion_sweep_plot(rows: list[dict[str, Any]], output: Path) -> None:
    """Write the torsion-constant sensitivity sweep."""

    case_names = sorted({str(row["case_name"]) for row in rows})
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.6, 4.4), layout="constrained")
    for case_name in case_names:
        case_rows = [row for row in rows if row["case_name"] == case_name]
        case_rows.sort(key=lambda row: float(row["torsion_multiplier"]))
        ax.plot(
            [float(row["torsion_multiplier"]) for row in case_rows],
            [float(row["tensyl_Dbar_xy_over_baseline"]) for row in case_rows],
            marker="o",
            label=_case_short_name(case_name),
        )
        last = case_rows[-1]
        ax.annotate(
            _case_short_name(case_name),
            xy=(
                float(last["torsion_multiplier"]),
                float(last["tensyl_Dbar_xy_over_baseline"]),
            ),
            xytext=(5, 0),
            textcoords="offset points",
            fontsize=8,
            va="center",
        )
    ax.set_xscale("log")
    ax.set_xlim(0.007, 180.0)
    ax.set_xlabel("member J multiplier")
    ax.set_ylabel("Tensyl Dbar_xy / baseline")
    ax.set_title("Sensitivity to supplied torsion constant")
    ax.grid(which="both", alpha=0.25)
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
    torsion_sweep = torsion_sweep_rows()
    summary = summary_payload(rows, torsion_sweep)
    cases = [case.as_dict() for case in default_reconciliation_cases()]

    table_json = artifact_dir / "comparison_table.json"
    table_csv = artifact_dir / "comparison_table.csv"
    summary_json = artifact_dir / "summary.json"
    torsion_sweep_json = artifact_dir / "torsion_sweep.json"
    manifest_path = artifact_dir / "manifest.json"
    term_plot = plot_dir / "sp8007-term-errors.svg"
    correction_plot = plot_dir / "sp8007-isogrid-correction.svg"
    torsion_plot = plot_dir / "sp8007-torsion-sweep.svg"

    write_json(
        table_json,
        {
            "schema_version": "tensyl.validation.sp8007-reconciliation-table.v3",
            "cases": cases,
            "rows": rows,
        },
    )
    _write_csv(table_csv, rows)
    write_json(summary_json, summary)
    write_json(
        torsion_sweep_json,
        {
            "schema_version": "tensyl.validation.sp8007-torsion-sweep.v1",
            "rows": torsion_sweep,
        },
    )
    write_term_error_plot(rows, term_plot)
    write_isogrid_correction_plot(rows, correction_plot)
    write_torsion_sweep_plot(torsion_sweep, torsion_plot)

    manifest = ArtifactManifest(
        case_name="sp8007_reconciliation",
        command=command,
        inputs=[],
        outputs=[
            _repo_relative(table_json),
            _repo_relative(table_csv),
            _repo_relative(summary_json),
            _repo_relative(torsion_sweep_json),
            _repo_relative(term_plot),
            _repo_relative(correction_plot),
            _repo_relative(torsion_plot),
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
        "torsion_sweep": torsion_sweep_json,
        "term_plot": term_plot,
        "correction_plot": correction_plot,
        "torsion_plot": torsion_plot,
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
