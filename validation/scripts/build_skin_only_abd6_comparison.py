#!/usr/bin/env python
"""Build detailed skin-only ABD6 comparison artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["svg.hashsalt"] = "tensyl-validation-skin-only-abd6"
from matplotlib import colors as mpl_colors  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.artifacts import write_json  # noqa: E402

CASE_DIR = ROOT / "validation" / "artifacts" / "committed" / "local_abd" / "skin_only"
RESULTANT_ORDER = ("N11", "N22", "N12", "M11", "M22", "M12")
STRAIN_ORDER = ("epsilon_11", "epsilon_22", "gamma_12", "kappa_11", "kappa_22", "kappa_12")


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"{path} must contain a JSON object."
        raise ValueError(msg)
    return data


def _matrix(data: object, *, path: Path, key: str) -> list[list[float]]:
    if not isinstance(data, list) or len(data) != 6:
        msg = f"{path}:{key} must be a 6 x 6 matrix."
        raise ValueError(msg)
    matrix: list[list[float]] = []
    for row in data:
        if not isinstance(row, list) or len(row) != 6:
            msg = f"{path}:{key} must be a 6 x 6 matrix."
            raise ValueError(msg)
        matrix.append([float(value) for value in row])
    return matrix


def _target_abd6(path: Path) -> list[list[float]]:
    target = _read_json(path)
    blocks = target.get("blocks")
    if not isinstance(blocks, dict):
        msg = f"{path}:blocks must be a JSON object."
        raise ValueError(msg)
    c8 = blocks.get("C8")
    if not isinstance(c8, list) or len(c8) < 6:
        msg = f"{path}:blocks.C8 must contain at least the leading ABD6 rows."
        raise ValueError(msg)
    return _matrix([row[:6] for row in c8[:6]], path=path, key="blocks.C8[:6,:6]")


def _extracted_abd6(path: Path) -> list[list[float]]:
    extracted = _read_json(path)
    blocks = extracted.get("blocks")
    if not isinstance(blocks, dict):
        msg = f"{path}:blocks must be a JSON object."
        raise ValueError(msg)
    return _matrix(blocks.get("ABD6"), path=path, key="blocks.ABD6")


def _block_name(row: int, column: int) -> str:
    if row < 3 and column < 3:
        return "A"
    if row < 3 and column >= 3:
        return "B"
    if row >= 3 and column < 3:
        return "B_transpose"
    return "D"


def build_comparison_table(target_path: Path, extracted_path: Path) -> dict[str, Any]:
    """Return detailed entrywise comparison rows for the promoted ABD6 slice."""

    target = _target_abd6(target_path)
    extracted = _extracted_abd6(extracted_path)
    rows: list[dict[str, Any]] = []
    sum_square = 0.0
    target_sum_square = 0.0
    max_abs_error = 0.0
    max_entry_relative_error = 0.0
    for row_index, row_name in enumerate(RESULTANT_ORDER):
        for column_index, column_name in enumerate(STRAIN_ORDER):
            target_value = target[row_index][column_index]
            extracted_value = extracted[row_index][column_index]
            absolute_error = extracted_value - target_value
            relative_error = absolute_error / max(abs(target_value), 1.0)
            sum_square += absolute_error * absolute_error
            target_sum_square += target_value * target_value
            max_abs_error = max(max_abs_error, abs(absolute_error))
            max_entry_relative_error = max(max_entry_relative_error, abs(relative_error))
            rows.append(
                {
                    "row_index": row_index,
                    "column_index": column_index,
                    "resultant": row_name,
                    "strain": column_name,
                    "block": _block_name(row_index, column_index),
                    "target": target_value,
                    "extracted": extracted_value,
                    "absolute_error": absolute_error,
                    "relative_error": relative_error,
                }
            )
    return {
        "schema_version": "tensyl.validation.skin-only-abd6-comparison-table.v1",
        "case_name": "local_abd_skin_only",
        "source_files": {
            "target": str(target_path.relative_to(ROOT)),
            "extracted": str(extracted_path.relative_to(ROOT)),
        },
        "resultant_order": list(RESULTANT_ORDER),
        "strain_order": list(STRAIN_ORDER),
        "relative_error_denominator": "max(abs(target), 1.0)",
        "checks": {
            "frobenius_relative_error": math.sqrt(sum_square) / math.sqrt(target_sum_square),
            "max_abs_entry_error": max_abs_error,
            "max_entry_relative_error": max_entry_relative_error,
        },
        "rows": rows,
    }


def write_csv(path: Path, comparison: dict[str, Any]) -> None:
    """Write the comparison rows as a compact CSV table."""

    fieldnames = (
        "resultant",
        "strain",
        "block",
        "target",
        "extracted",
        "absolute_error",
        "relative_error",
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in comparison["rows"]:
            writer.writerow({field: row[field] for field in fieldnames})


def write_error_heatmap(comparison: dict[str, Any], output: Path) -> None:
    """Write an SVG heatmap of signed entrywise relative errors."""

    values = [[0.0 for _ in STRAIN_ORDER] for _ in RESULTANT_ORDER]
    for row in comparison["rows"]:
        values[row["row_index"]][row["column_index"]] = row["relative_error"]

    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.4), layout="constrained")
    norm = mpl_colors.SymLogNorm(linthresh=1.0e-11, linscale=1.0, vmin=-1.0e-7, vmax=1.0e-7)
    image = ax.imshow(values, cmap="coolwarm", norm=norm)
    ax.set_xticks(range(len(STRAIN_ORDER)), labels=STRAIN_ORDER, rotation=35, ha="right")
    ax.set_yticks(range(len(RESULTANT_ORDER)), labels=RESULTANT_ORDER)
    ax.set_title("Skin-only ABD6 entrywise relative error")
    ax.set_xlabel("generalized strain input")
    ax.set_ylabel("generalized resultant output")
    colorbar = fig.colorbar(image, ax=ax, shrink=0.86)
    colorbar.set_label("signed relative error")
    for row_index in range(len(RESULTANT_ORDER)):
        for column_index in range(len(STRAIN_ORDER)):
            value = values[row_index][column_index]
            ax.text(
                column_index,
                row_index,
                f"{value:.1e}",
                ha="center",
                va="center",
                fontsize=7,
            )
    fig.savefig(output, format="svg", metadata={"Date": None})
    plt.close(fig)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        type=Path,
        default=CASE_DIR / "target_abd.json",
        help="Tensyl target ABD artifact.",
    )
    parser.add_argument(
        "--extracted",
        type=Path,
        default=CASE_DIR / "extracted_abd.json",
        help="Solver-extracted ABD artifact.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        default=CASE_DIR / "abd6_comparison_table.json",
        help="Output JSON table path.",
    )
    parser.add_argument(
        "--csv-output",
        type=Path,
        default=CASE_DIR / "abd6_comparison_table.csv",
        help="Output CSV table path.",
    )
    parser.add_argument(
        "--plot-output",
        type=Path,
        default=ROOT / "docs" / "assets" / "validation" / "skin-only-abd6-relative-error.svg",
        help="Output SVG heatmap path.",
    )
    args = parser.parse_args(argv)

    comparison = build_comparison_table(args.target, args.extracted)
    write_json(args.json_output, comparison)
    write_csv(args.csv_output, comparison)
    write_error_heatmap(comparison, args.plot_output)
    print(f"json: {args.json_output}")
    print(f"csv: {args.csv_output}")
    print(f"plot: {args.plot_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
