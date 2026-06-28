from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.metrics import abd_comparison_metrics  # noqa: E402


def test_abd_comparison_metrics_report_block_errors() -> None:
    expected = np.eye(8)
    actual = np.eye(8)
    actual[0, 0] = 1.1
    actual[6, 6] = 0.9

    metrics = abd_comparison_metrics(actual, expected, case_name="comparison")

    assert metrics["case_name"] == "comparison"
    assert metrics["checks"]["C8_relative_frobenius_error"] > 0.0
    assert metrics["checks"]["A_relative_frobenius_error"] > 0.0
    assert metrics["checks"]["As_relative_frobenius_error"] > 0.0
    assert metrics["checks"]["D_relative_frobenius_error"] == 0.0
    assert metrics["checks"]["symmetric_actual_C8"] is True
