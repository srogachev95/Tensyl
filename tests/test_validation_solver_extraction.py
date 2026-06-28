from __future__ import annotations

# ruff: noqa: E402,I001

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.calculix.parsers import CalculixStressRow, CalculixStressTable  # noqa: E402
from tensyl_validation.local_abd_solver import extract_skin_only_abd6_from_stress_tables  # noqa: E402


def _table(
    *,
    sxx_bottom: float,
    sxx_top: float,
    syy_bottom: float = 0.0,
    syy_top: float = 0.0,
    sxy_bottom: float = 0.0,
    sxy_top: float = 0.0,
) -> CalculixStressTable:
    return CalculixStressTable(
        load_case=None,
        rows=(
            CalculixStressRow(1, 1, sxx_bottom, syy_bottom, 0.0, sxy_bottom, 0.0, 0.0),
            CalculixStressRow(1, 5, sxx_top, syy_top, 0.0, sxy_top, 0.0, 0.0),
        ),
    )


def test_skin_only_extraction_assembles_abd6_from_stress_tables() -> None:
    tables = {
        "epsilon_11": _table(sxx_bottom=10.0, sxx_top=10.0, syy_bottom=2.0, syy_top=2.0),
        "epsilon_22": _table(sxx_bottom=3.0, sxx_top=3.0, syy_bottom=9.0, syy_top=9.0),
        "gamma_12": _table(sxx_bottom=0.0, sxx_top=0.0, sxy_bottom=5.0, sxy_top=5.0),
        "kappa_11": _table(sxx_bottom=-12.0, sxx_top=12.0, syy_bottom=-4.0, syy_top=4.0),
        "kappa_22": _table(sxx_bottom=-1.0, sxx_top=1.0, syy_bottom=-8.0, syy_top=8.0),
        "kappa_12": _table(sxx_bottom=0.0, sxx_top=0.0, sxy_bottom=-6.0, sxy_top=6.0),
    }
    magnitudes = {component: 0.5 for component in tables}

    abd6 = extract_skin_only_abd6_from_stress_tables(
        tables,
        thickness=0.2,
        magnitudes_by_component=magnitudes,
    )

    assert abd6.shape == (6, 6)
    assert abd6[0, 0] == 4.0
    assert abd6[1, 1] == 3.6
    assert abd6[2, 2] == 2.0
    assert abd6[3, 3] == np.float64((24.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)
    assert abd6[4, 4] == np.float64((16.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)
    assert abd6[5, 5] == np.float64((12.0 * 0.2**2 * np.sqrt(3.0) / 12.0) / 0.5)
