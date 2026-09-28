from __future__ import annotations

import sys
from pathlib import Path

import pytest

from tensyl import IsotropicMaterial, isotropic_plate

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.sp8007 import (  # noqa: E402
    SP8007ComparisonCase,
    comparison_rows,
    isogrid_parallel_axis_correction,
    sp8007_coefficients_from_abd,
    sp8007_corrected_coefficients,
    sp8007_reference_coefficients,
    tensyl_coefficients,
)


def test_sp8007_extraction_uses_modified_twisting_stiffness() -> None:
    material = IsotropicMaterial(E=10.0e6, nu=0.30)
    thickness = 0.1
    stiffness = isotropic_plate(material, thickness=thickness)

    coefficients = sp8007_coefficients_from_abd(stiffness)

    assert coefficients["Dbar_xy"] == pytest.approx(
        2.0 * stiffness.D[0, 1] + 4.0 * stiffness.D[2, 2]
    )
    assert coefficients["Dbar_xy"] != pytest.approx(stiffness.D[2, 2])


def test_orthogrid_matches_sp8007_as_written_for_every_coefficient() -> None:
    case = SP8007ComparisonCase(name="orthogrid_eccentric", model="orthogrid")

    tensyl = tensyl_coefficients(case)
    sp8007 = sp8007_reference_coefficients(case)

    for coefficient, value in sp8007.items():
        assert tensyl[coefficient] == pytest.approx(value, rel=1.0e-12, abs=1.0e-9)


def test_isogrid_zero_eccentricity_matches_sp8007_as_written() -> None:
    case = SP8007ComparisonCase(
        name="isogrid_zero_eccentricity",
        model="isogrid",
        eccentricity=0.0,
    )
    rows = comparison_rows((case,))

    assert max(row["abs_relative_delta_as_written"] for row in rows) < 1.0e-12


def test_isogrid_parallel_axis_correction_closes_eccentric_gap() -> None:
    case = SP8007ComparisonCase(name="isogrid_eccentric", model="isogrid", eccentricity=0.32)
    rows = comparison_rows((case,))
    as_written_bending_error = max(
        row["abs_relative_delta_as_written"]
        for row in rows
        if row["coefficient"] in {"Dbar_x", "Dbar_y", "Dbar_xy"}
    )
    corrected_error = max(row["abs_relative_delta_corrected"] for row in rows)

    assert as_written_bending_error > 1.0
    assert corrected_error < 1.0e-12


def test_every_report_case_agrees_with_corrected_sp8007() -> None:
    rows = comparison_rows()

    assert {row["case_name"] for row in rows} == {
        "orthogrid_eccentric",
        "isogrid_zero_eccentricity",
        "isogrid_eccentric",
    }
    assert max(row["abs_relative_delta_corrected"] for row in rows) < 1.0e-12
    assert {row["interpretation"] for row in rows} == {"agreement"}


def test_isogrid_parallel_axis_correction_matches_expected_terms() -> None:
    case = SP8007ComparisonCase(name="isogrid_eccentric", model="isogrid", eccentricity=0.32)
    material = case.material()
    d_correction, dxy_correction = isogrid_parallel_axis_correction(case)
    expected_d = 3.0 * 3.0**0.5 * material.E * case.stiffener_area * case.eccentricity**2
    expected_d /= 4.0 * case.pitch

    assert d_correction == pytest.approx(expected_d)
    assert dxy_correction == pytest.approx(2.0 * expected_d)

    as_written = sp8007_reference_coefficients(case)
    corrected = sp8007_corrected_coefficients(case)
    assert corrected["Dbar_x"] - as_written["Dbar_x"] == pytest.approx(d_correction)
    assert corrected["Dbar_y"] - as_written["Dbar_y"] == pytest.approx(d_correction)
    assert corrected["Dbar_xy"] - as_written["Dbar_xy"] == pytest.approx(dxy_correction)
