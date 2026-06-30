from __future__ import annotations

import sys
from pathlib import Path
from typing import Literal

import numpy as np
import pytest

from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    braced_orthogrid_cell,
    equilateral_isogrid_cell,
    hexagonal_grid_cell,
    isosceles_triangle_grid_cell,
    isotropic_plate,
    kagome_cell,
    star_cell,
)
from tensyl.materials import IsotropicMaterial
from tests._helpers import zero_skin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.nemeth import (  # noqa: E402
    NEMETH_SOURCE,
    nemeth_comparison_payload,
    nemeth_reference_stiffness,
)


def _section(scale: float = 1.0, *, shear: bool = True) -> BeamSection:
    return BeamSection(
        EA=1200.0 * scale,
        EIy=50.0 * scale,
        EIz=30.0 * scale,
        GJ=20.0 * scale,
        kGAy=400.0 * scale if shear else None,
        kGAz=300.0 * scale if shear else None,
        EIyz=4.0 * scale,
    )


def _assert_matches_nemeth_reference(cell) -> None:
    actual = EnergyHomogenizer().compute(cell).stiffness
    reference = nemeth_reference_stiffness(cell)

    np.testing.assert_allclose(actual.C8, reference.C8, rtol=1.0e-12, atol=1.0e-10)


def test_nemeth_reference_matches_orthogrid_with_skin_and_eccentricity() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=10.0e6, nu=0.30), thickness=0.08)
    cell = braced_orthogrid_cell(
        skin=skin,
        stringer_section=_section(1.0),
        rib_section=_section(1.7),
        brace_section=_section(0.8),
        opposite_brace_section=_section(1.2),
        stringer_spacing=1.3,
        rib_spacing=1.9,
        stringer_eccentricity=0.04,
        rib_eccentricity=-0.02,
        brace_eccentricity=0.06,
        opposite_brace_eccentricity=0.01,
        brace_pattern="double",
    )

    _assert_matches_nemeth_reference(cell)


@pytest.mark.parametrize("brace_pattern", ["double", "single"])
def test_nemeth_reference_matches_braced_orthogrid_patterns(
    brace_pattern: Literal["double", "single"],
) -> None:
    cell = braced_orthogrid_cell(
        skin=zero_skin(),
        stringer_section=_section(1.0),
        rib_section=_section(1.4),
        brace_section=_section(0.7),
        opposite_brace_section=_section(1.1),
        stringer_spacing=2.1,
        rib_spacing=1.4,
        stringer_eccentricity=0.03,
        rib_eccentricity=0.05,
        brace_eccentricity=0.02,
        opposite_brace_eccentricity=-0.01,
        brace_pattern=brace_pattern,
    )

    _assert_matches_nemeth_reference(cell)


def test_nemeth_reference_matches_equilateral_isogrid_with_eccentricity() -> None:
    cell = equilateral_isogrid_cell(
        skin=zero_skin(),
        member_section=_section(1.3),
        pitch=1.6,
        eccentricity=0.025,
    )

    _assert_matches_nemeth_reference(cell)


def test_nemeth_reference_matches_isosceles_triangle_and_kagome_cells() -> None:
    triangle = isosceles_triangle_grid_cell(
        skin=zero_skin(),
        stringer_section=_section(1.0),
        diagonal_section=_section(0.9),
        opposite_diagonal_section=_section(1.2),
        base=1.7,
        height=0.8,
        stringer_eccentricity=0.02,
        diagonal_eccentricity=0.03,
        opposite_diagonal_eccentricity=-0.01,
    )
    kagome = kagome_cell(
        skin=zero_skin(),
        stringer_section=_section(1.0),
        diagonal_section=_section(0.9),
        opposite_diagonal_section=_section(1.2),
        base=1.7,
        height=0.8,
        stringer_eccentricity=0.02,
        diagonal_eccentricity=0.03,
        opposite_diagonal_eccentricity=-0.01,
    )

    _assert_matches_nemeth_reference(triangle)
    _assert_matches_nemeth_reference(kagome)


def test_nemeth_reference_matches_hexagonal_and_star_cells() -> None:
    hexagonal = hexagonal_grid_cell(
        skin=zero_skin(),
        rib_section=_section(1.4, shear=False),
        diagonal_section=_section(0.8),
        opposite_diagonal_section=_section(1.1),
        half_width=1.2,
        diagonal_rise=0.9,
        rib_length=0.7,
        rib_eccentricity=0.02,
        diagonal_eccentricity=0.03,
        opposite_diagonal_eccentricity=-0.01,
    )
    star = star_cell(
        skin=zero_skin(),
        stringer_section=_section(1.2),
        diagonal_section=_section(0.75),
        opposite_diagonal_section=_section(1.05),
        base=1.5,
        height=0.9,
        stringer_eccentricity=0.01,
        diagonal_eccentricity=0.04,
        opposite_diagonal_eccentricity=-0.02,
    )

    _assert_matches_nemeth_reference(hexagonal)
    _assert_matches_nemeth_reference(star)


def test_nemeth_comparison_payload_records_source_and_error_metrics() -> None:
    cell = equilateral_isogrid_cell(
        skin=zero_skin(),
        member_section=_section(),
        pitch=1.2,
        eccentricity=0.0,
    )
    actual = EnergyHomogenizer().compute(cell).stiffness

    payload = nemeth_comparison_payload(cell, actual)

    assert payload["schema_version"] == "tensyl.validation.nemeth-cell-comparison.v1"
    assert payload["source_equations"] == (NEMETH_SOURCE,)
    assert payload["cell_source"] == "equilateral_isogrid"
    assert payload["relative_c8_error"] == pytest.approx(0.0, abs=1.0e-14)
    assert payload["max_absolute_entry_error"] == pytest.approx(0.0, abs=1.0e-12)
