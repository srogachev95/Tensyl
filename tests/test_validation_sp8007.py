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


def test_orthogrid_membrane_coupling_and_modified_twisting_match_sp8007() -> None:
    case = SP8007ComparisonCase(
        name="orthogrid_full_section_eccentric",
        model="orthogrid",
    )

    tensyl = tensyl_coefficients(case)
    sp8007 = sp8007_reference_coefficients(case)

    for coefficient in (
        "Ebar_x",
        "Ebar_y",
        "Ebar_xy",
        "Gbar_xy",
        "Cbar_x",
        "Cbar_y",
        "Cbar_xy",
        "Kbar_xy",
        "Dbar_xy",
    ):
        assert tensyl[coefficient] == pytest.approx(sp8007[coefficient], rel=1.0e-12, abs=1.0e-9)


def test_orthogrid_inplane_member_bending_explains_bending_gap() -> None:
    full = SP8007ComparisonCase(
        name="orthogrid_full_section_eccentric",
        model="orthogrid",
        in_plane_inertia=1.20e-3,
    )
    suppressed = SP8007ComparisonCase(
        name="orthogrid_suppressed_inplane_bending",
        model="orthogrid",
        in_plane_inertia=1.20e-6,
    )

    full_rows = comparison_rows((full,))
    suppressed_rows = comparison_rows((suppressed,))
    full_error = max(
        row["abs_relative_delta_corrected"]
        for row in full_rows
        if row["coefficient"] in {"Dbar_x", "Dbar_y"}
    )
    suppressed_error = max(
        row["abs_relative_delta_corrected"]
        for row in suppressed_rows
        if row["coefficient"] in {"Dbar_x", "Dbar_y"}
    )

    assert full_error > 0.10
    assert suppressed_error < 1.0e-3


def test_orthogrid_cross_family_eiz_terms_explain_bending_deltas() -> None:
    case = SP8007ComparisonCase(
        name="orthogrid_full_section_eccentric",
        model="orthogrid",
        in_plane_inertia=1.20e-3,
    )
    material = case.material()
    tensyl = tensyl_coefficients(case)
    sp8007 = sp8007_reference_coefficients(case)

    assert tensyl["Dbar_x"] - sp8007["Dbar_x"] == pytest.approx(
        material.E * case.in_plane_inertia / case.rib_spacing
    )
    assert tensyl["Dbar_y"] - sp8007["Dbar_y"] == pytest.approx(
        material.E * case.in_plane_inertia / case.stringer_spacing
    )


def test_isogrid_zero_eccentricity_limit_matches_sp8007_when_inplane_bending_is_small() -> None:
    case = SP8007ComparisonCase(
        name="isogrid_suppressed_inplane_bending_zero_eccentricity",
        model="isogrid",
        in_plane_inertia=1.20e-6,
        eccentricity=0.0,
    )
    rows = comparison_rows((case,))

    assert max(row["abs_relative_delta_corrected"] for row in rows) < 1.0e-3


def test_isogrid_parallel_axis_correction_closes_eccentric_gap() -> None:
    case = SP8007ComparisonCase(
        name="isogrid_suppressed_inplane_bending_eccentric",
        model="isogrid",
        in_plane_inertia=1.20e-6,
        eccentricity=0.32,
    )
    rows = comparison_rows((case,))
    as_written_bending_error = max(
        row["abs_relative_delta_as_written"]
        for row in rows
        if row["coefficient"] in {"Dbar_x", "Dbar_y", "Dbar_xy"}
    )
    corrected_bending_error = max(
        row["abs_relative_delta_corrected"]
        for row in rows
        if row["coefficient"] in {"Dbar_x", "Dbar_y", "Dbar_xy"}
    )
    membrane_error = max(
        row["abs_relative_delta_corrected"]
        for row in rows
        if row["coefficient"] in {"Ebar_x", "Ebar_y", "Ebar_xy", "Gbar_xy"}
    )

    assert membrane_error < 1.0e-12
    assert as_written_bending_error > 1.0
    assert corrected_bending_error < 1.0e-3


def test_isogrid_parallel_axis_correction_matches_expected_terms() -> None:
    case = SP8007ComparisonCase(
        name="isogrid_suppressed_inplane_bending_eccentric",
        model="isogrid",
        in_plane_inertia=1.20e-6,
        eccentricity=0.32,
    )
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
