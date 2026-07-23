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
    diamond_cell,
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
    NemethFamily,
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


def _family(
    section: BeamSection,
    *,
    length: float,
    angle: float,
    axial_z: float,
    shear_z: float,
    multiplicity: float = 1.0,
    label: str,
) -> NemethFamily:
    return NemethFamily(
        section=section,
        length=length,
        cosine=float(np.cos(angle)),
        sine=float(np.sin(angle)),
        axial_eccentricity=axial_z,
        shear_eccentricity=shear_z,
        multiplicity=multiplicity,
        label=label,
    )


def _assert_matches_nemeth_reference(
    cell,
    families: tuple[NemethFamily, ...],
    *,
    source_table: str,
) -> None:
    actual = EnergyHomogenizer().compute(cell).stiffness
    reference = nemeth_reference_stiffness(
        skin=cell.skin,
        cell_area=cell.area,
        families=families,
        cell_source=source_table,
    )
    np.testing.assert_allclose(actual.C8, reference.C8, rtol=1.0e-12, atol=1.0e-10)


@pytest.mark.parametrize("diagonal_pattern", ["double", "single"])
def test_nemeth_tables_4_and_5_braced_orthogrids(
    diagonal_pattern: Literal["double", "single"],
) -> None:
    skin = isotropic_plate(IsotropicMaterial(E=10.0e6, nu=0.30), thickness=0.08)
    e1 = _section(1.0)
    e2 = _section(1.7)
    positive = _section(0.8)
    negative = _section(1.2)
    e1_pitch = 1.9
    e2_pitch = 1.3
    diagonal_length = float(np.hypot(e1_pitch, e2_pitch))
    angle = float(np.arctan2(e2_pitch, e1_pitch))
    single = diagonal_pattern == "single"
    member_scale = 2.0 if single else 1.0
    orthogonal_multiplicity = 2.0 if single else 1.0
    cell = braced_orthogrid_cell(
        skin=skin,
        e1_section=e1,
        e2_section=e2,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_pitch=e1_pitch,
        e2_pitch=e2_pitch,
        e1_axial_eccentricity=0.04,
        e2_axial_eccentricity=-0.02,
        diagonal_axial_eccentricity=0.06,
        negative_diagonal_axial_eccentricity=0.01,
        e1_shear_eccentricity=0.03,
        e2_shear_eccentricity=-0.01,
        diagonal_shear_eccentricity=0.05,
        negative_diagonal_shear_eccentricity=0.02,
        diagonal_pattern=diagonal_pattern,
    )
    families = (
        _family(
            e1,
            length=member_scale * e1_pitch,
            angle=0.0,
            axial_z=0.04,
            shear_z=0.03,
            multiplicity=orthogonal_multiplicity,
            label="1-2 and 5-7" if single else "1-2",
        ),
        _family(
            e2,
            length=member_scale * e2_pitch,
            angle=np.pi / 2.0,
            axial_z=-0.02,
            shear_z=-0.01,
            multiplicity=orthogonal_multiplicity,
            label="3-4 and 5-8" if single else "3-4",
        ),
        _family(
            positive,
            length=member_scale * diagonal_length,
            angle=angle,
            axial_z=0.06,
            shear_z=0.05,
            label="5-6",
        ),
        _family(
            negative,
            length=member_scale * diagonal_length,
            angle=np.pi - angle,
            axial_z=0.01,
            shear_z=0.02,
            label="7-8",
        ),
    )
    _assert_matches_nemeth_reference(
        cell,
        families,
        source_table="Nemeth table 5" if single else "Nemeth table 4",
    )


def test_diamond_cell_is_table_4_without_the_e2_family() -> None:
    e1 = _section(1.1)
    positive = _section(0.7)
    negative = _section(1.3)
    e1_pitch = 1.8
    e2_pitch = 1.1
    length = float(np.hypot(e1_pitch, e2_pitch))
    angle = float(np.arctan2(e2_pitch, e1_pitch))
    cell = diamond_cell(
        skin=zero_skin(),
        e1_section=e1,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_pitch=e1_pitch,
        e2_pitch=e2_pitch,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.03,
        negative_diagonal_axial_eccentricity=-0.01,
    )
    families = (
        _family(e1, length=e1_pitch, angle=0.0, axial_z=0.02, shear_z=0.02, label="e1"),
        _family(
            positive,
            length=length,
            angle=angle,
            axial_z=0.03,
            shear_z=0.03,
            label="positive diagonal",
        ),
        _family(
            negative,
            length=length,
            angle=np.pi - angle,
            axial_z=-0.01,
            shear_z=-0.01,
            label="negative diagonal",
        ),
    )
    _assert_matches_nemeth_reference(cell, families, source_table="Nemeth figure 15")


def test_equilateral_isogrid_matches_table_6_limit() -> None:
    section = _section(1.3)
    side = 1.6
    height = np.sqrt(3.0) * side / 2.0
    cell = equilateral_isogrid_cell(
        skin=zero_skin(),
        member_section=section,
        side_length=side,
        axial_eccentricity=0.025,
        shear_eccentricity=0.015,
    )
    families = tuple(
        _family(
            section,
            length=side,
            angle=angle,
            axial_z=0.025,
            shear_z=0.015,
            label=label,
        )
        for angle, label in (
            (0.0, "1-2"),
            (np.pi / 3.0, "3-4"),
            (2.0 * np.pi / 3.0, "5-6"),
        )
    )
    assert cell.area == pytest.approx(side * height)
    _assert_matches_nemeth_reference(cell, families, source_table="Nemeth table 6")


def test_nemeth_tables_6_and_7_triangle_and_kagome() -> None:
    e1 = _section(1.0)
    positive = _section(0.9)
    negative = _section(1.2)
    width = 1.7
    height = 0.8
    angle = float(np.arctan2(height, 0.5 * width))
    diagonal = float(np.hypot(0.5 * width, height))
    triangle = isosceles_triangle_grid_cell(
        skin=zero_skin(),
        e1_section=e1,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_pitch=width,
        e2_pitch=height,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.03,
        negative_diagonal_axial_eccentricity=-0.01,
    )
    triangle_families = (
        _family(e1, length=width, angle=0.0, axial_z=0.02, shear_z=0.02, label="1-2"),
        _family(
            positive,
            length=diagonal,
            angle=angle,
            axial_z=0.03,
            shear_z=0.03,
            label="3-4",
        ),
        _family(
            negative,
            length=diagonal,
            angle=np.pi - angle,
            axial_z=-0.01,
            shear_z=-0.01,
            label="5-6",
        ),
    )
    _assert_matches_nemeth_reference(triangle, triangle_families, source_table="Nemeth table 6")

    kagome = kagome_cell(
        skin=zero_skin(),
        e1_section=e1,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_pitch=width,
        e2_pitch=height,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.03,
        negative_diagonal_axial_eccentricity=-0.01,
    )
    kagome_families = (
        _family(
            e1,
            length=width,
            angle=0.0,
            axial_z=0.02,
            shear_z=0.02,
            multiplicity=2.0,
            label="1-2 and 3-4",
        ),
        _family(
            positive,
            length=2.0 * diagonal,
            angle=angle,
            axial_z=0.03,
            shear_z=0.03,
            label="5-6",
        ),
        _family(
            negative,
            length=2.0 * diagonal,
            angle=np.pi - angle,
            axial_z=-0.01,
            shear_z=-0.01,
            label="7-8",
        ),
    )
    _assert_matches_nemeth_reference(kagome, kagome_families, source_table="Nemeth table 7")


def test_nemeth_table_8_hexagonal_cell() -> None:
    e2 = _section(1.4, shear=False)
    positive = _section(0.8)
    negative = _section(1.1)
    a = 1.2
    b = 0.9
    c = 0.7
    full_diagonal = float(np.hypot(a, b))
    angle = float(np.arctan2(b, a))
    cell = hexagonal_grid_cell(
        skin=zero_skin(),
        e2_section=e2,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_half_pitch=a,
        diagonal_e2_rise=b,
        e2_member_length=c,
        e2_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.03,
        negative_diagonal_axial_eccentricity=-0.01,
    )
    families = (
        _family(
            negative,
            length=0.5 * full_diagonal,
            angle=-angle,
            axial_z=-0.01,
            shear_z=-0.01,
            multiplicity=2.0,
            label="2-1 and 5-6",
        ),
        _family(
            positive,
            length=0.5 * full_diagonal,
            angle=np.pi + angle,
            axial_z=0.03,
            shear_z=0.03,
            multiplicity=2.0,
            label="2-3 and 5-4",
        ),
        _family(e2, length=c, angle=np.pi / 2.0, axial_z=0.02, shear_z=0.02, label="2-5"),
    )
    _assert_matches_nemeth_reference(cell, families, source_table="Nemeth table 8")


def test_nemeth_table_9_star_cell() -> None:
    e1 = _section(1.2)
    positive = _section(0.75)
    negative = _section(1.05)
    width = 1.5
    height = 0.9
    full_diagonal = float(np.hypot(0.5 * width, height))
    angle = float(np.arctan2(height, 0.5 * width))
    cell = star_cell(
        skin=zero_skin(),
        e1_section=e1,
        positive_diagonal_section=positive,
        negative_diagonal_section=negative,
        e1_pitch=width,
        e2_pitch=height,
        e1_axial_eccentricity=0.01,
        diagonal_axial_eccentricity=0.04,
        negative_diagonal_axial_eccentricity=-0.02,
    )
    families = (
        _family(
            e1,
            length=width / 3.0,
            angle=0.0,
            axial_z=0.01,
            shear_z=0.01,
            multiplicity=4.0,
            label="four e1 members",
        ),
        _family(
            positive,
            length=full_diagonal / 3.0,
            angle=angle,
            axial_z=0.04,
            shear_z=0.04,
            multiplicity=4.0,
            label="four positive diagonals",
        ),
        _family(
            negative,
            length=full_diagonal / 3.0,
            angle=np.pi - angle,
            axial_z=-0.02,
            shear_z=-0.02,
            multiplicity=4.0,
            label="four negative diagonals",
        ),
    )
    _assert_matches_nemeth_reference(cell, families, source_table="Nemeth table 9")


def test_nemeth_comparison_payload_records_source_and_error_metrics() -> None:
    section = _section()
    cell = equilateral_isogrid_cell(
        skin=zero_skin(),
        member_section=section,
        side_length=1.2,
        axial_eccentricity=0.0,
    )
    families = tuple(
        _family(
            section,
            length=1.2,
            angle=angle,
            axial_z=0.0,
            shear_z=0.0,
            label=label,
        )
        for angle, label in ((0.0, "e1"), (np.pi / 3.0, "+d"), (2 * np.pi / 3.0, "-d"))
    )
    actual = EnergyHomogenizer().compute(cell).stiffness
    reference = nemeth_reference_stiffness(
        skin=cell.skin,
        cell_area=cell.area,
        families=families,
        cell_source="Nemeth table 6",
    )
    payload = nemeth_comparison_payload(
        reference=reference,
        actual=actual,
        cell_source="equilateral_isogrid",
    )

    assert payload["schema_version"] == "tensyl.validation.nemeth-cell-comparison.v2"
    assert payload["source_equations"] == (NEMETH_SOURCE,)
    assert payload["cell_source"] == "equilateral_isogrid"
    assert payload["relative_c8_error"] == pytest.approx(0.0, abs=1.0e-14)
    assert payload["max_absolute_entry_error"] == pytest.approx(0.0, abs=1.0e-12)
