from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from tensyl import (
    BeamSection,
    CellEdge,
    CellNode,
    EnergyHomogenizer,
    IsotropicMaterial,
    LinearABDWall,
    braced_orthogrid_cell,
    equilateral_isogrid_cell,
    equilateral_star_cell,
    graph_unit_cell,
    hexagonal_grid_cell,
    isosceles_triangle_grid_cell,
    isotropic_plate,
    kagome_cell,
    regular_hexagonal_grid_cell,
    sandwich_orthogrid_core_cell,
    shift_reference_surface,
    star_cell,
    superpose_linear_abd_walls,
)
from tensyl.homogenizers import member_energy


def _zero_skin() -> LinearABDWall:
    return LinearABDWall(
        A=np.zeros((3, 3)),
        B=np.zeros((3, 3)),
        D=np.zeros((3, 3)),
        As=np.zeros((2, 2)),
    )


def _membrane_skin(stiffness: float = 10.0) -> LinearABDWall:
    return LinearABDWall(
        A=stiffness * np.eye(3),
        B=np.zeros((3, 3)),
        D=np.zeros((3, 3)),
        As=np.zeros((2, 2)),
    )


def _section(*, shear: bool = True) -> BeamSection:
    return BeamSection(
        EA=1200.0,
        EIy=50.0,
        EIz=30.0,
        GJ=20.0,
        kGAy=400.0 if shear else None,
        kGAz=300.0 if shear else None,
    )


def _assert_energy_consistent(cell) -> None:
    eta = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])
    result = EnergyHomogenizer().compute(cell)
    wall_energy = 0.5 * cell.area * float(eta @ result.law.C8 @ eta)
    explicit_energy = cell.area * cell.skin.energy(eta) + sum(
        member_energy(member, eta) for member in cell.members
    )
    np.testing.assert_allclose(wall_energy, explicit_energy, rtol=1.0e-12, atol=1.0e-10)
    assert result.diagnostics["symmetric"] is True
    assert result.diagnostics["positive_semidefinite"] is True


def test_phase3_reference_inventory_is_present() -> None:
    path = Path(__file__).parent / "data" / "nemeth_phase3_cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))

    assert {case["id"] for case in cases} == {
        "braced_orthogrid_double",
        "braced_orthogrid_single",
        "isosceles_triangle",
        "kagome",
        "hexagonal",
        "star",
        "sandwich_cores",
    }
    assert all("Nemeth 2011" in case["source"] for case in cases)


def test_graph_unit_cell_computes_member_geometry() -> None:
    section = _section()
    cell = graph_unit_cell(
        area=2.0,
        skin=_zero_skin(),
        nodes=(CellNode(0.0, 0.0), CellNode(3.0, 4.0)),
        edges=(CellEdge(0, 1, section=section, eccentricity=0.2, label="edge"),),
    )

    assert cell.members[0].length == pytest.approx(5.0)
    assert cell.members[0].angle_rad == pytest.approx(np.arctan2(4.0, 3.0))
    assert cell.members[0].label == "edge"


def test_graph_unit_cell_rejects_invalid_edges() -> None:
    with pytest.raises(ValueError, match="out of range"):
        graph_unit_cell(
            area=1.0,
            skin=_zero_skin(),
            nodes=(CellNode(0.0, 0.0), CellNode(1.0, 0.0)),
            edges=(CellEdge(0, 2, section=_section(), eccentricity=0.0),),
        )


def test_braced_orthogrid_single_has_half_diagonal_density() -> None:
    section = _section()
    double = braced_orthogrid_cell(
        skin=_zero_skin(),
        stringer_section=section,
        rib_section=section,
        brace_section=section,
        stringer_spacing=1.3,
        rib_spacing=1.9,
        stringer_eccentricity=0.0,
        rib_eccentricity=0.0,
        brace_eccentricity=0.0,
        brace_pattern="double",
    )
    single = braced_orthogrid_cell(
        skin=_zero_skin(),
        stringer_section=section,
        rib_section=section,
        brace_section=section,
        stringer_spacing=1.3,
        rib_spacing=1.9,
        stringer_eccentricity=0.0,
        rib_eccentricity=0.0,
        brace_eccentricity=0.0,
        brace_pattern="single",
    )

    double_brace_density = sum(
        member.multiplicity * member.length / double.area
        for member in double.members
        if "brace" in member.label
    )
    single_brace_density = sum(
        member.multiplicity * member.length / single.area
        for member in single.members
        if "brace" in member.label
    )

    assert single_brace_density == pytest.approx(0.5 * double_brace_density)


def test_equilateral_triangle_constructor_matches_existing_isogrid() -> None:
    section = _section()
    pitch = 2.0
    triangle = isosceles_triangle_grid_cell(
        skin=_zero_skin(),
        stringer_section=section,
        diagonal_section=section,
        base=pitch,
        height=np.sqrt(3.0) * pitch / 2.0,
        stringer_eccentricity=0.03,
        diagonal_eccentricity=0.03,
    )
    isogrid = equilateral_isogrid_cell(
        skin=_zero_skin(),
        member_section=section,
        pitch=pitch,
        eccentricity=0.03,
    )

    np.testing.assert_allclose(
        EnergyHomogenizer().compute(triangle).law.C8,
        EnergyHomogenizer().compute(isogrid).law.C8,
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_kagome_matches_isosceles_triangle_energy_output() -> None:
    section = _section()
    triangle = isosceles_triangle_grid_cell(
        skin=_zero_skin(),
        stringer_section=section,
        diagonal_section=section,
        base=1.4,
        height=0.9,
        stringer_eccentricity=0.02,
        diagonal_eccentricity=0.04,
    )
    kagome = kagome_cell(
        skin=_zero_skin(),
        stringer_section=section,
        diagonal_section=section,
        base=1.4,
        height=0.9,
        stringer_eccentricity=0.02,
        diagonal_eccentricity=0.04,
    )

    np.testing.assert_allclose(
        EnergyHomogenizer().compute(kagome).law.C8,
        EnergyHomogenizer().compute(triangle).law.C8,
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_canonical_cell_reconstruction_is_idempotent() -> None:
    cell = kagome_cell(
        skin=_zero_skin(),
        stringer_section=_section(),
        diagonal_section=_section(),
        base=2.0,
        height=1.5,
        stringer_eccentricity=0.02,
        diagonal_eccentricity=0.03,
    )

    reconstructed = type(cell)(
        area=cell.area,
        skin=cell.skin,
        members=cell.members,
        frame=cell.frame,
        convention=cell.convention,
        metadata=cell.metadata,
    )

    assert reconstructed == cell
    np.testing.assert_allclose(
        EnergyHomogenizer().compute(reconstructed).law.C8,
        EnergyHomogenizer().compute(cell).law.C8,
    )


@pytest.mark.parametrize(
    "cell",
    [
        braced_orthogrid_cell(
            skin=_zero_skin(),
            stringer_section=_section(),
            rib_section=_section(),
            brace_section=_section(),
            stringer_spacing=1.2,
            rib_spacing=1.7,
            stringer_eccentricity=0.01,
            rib_eccentricity=0.02,
            brace_eccentricity=0.03,
        ),
        isosceles_triangle_grid_cell(
            skin=_zero_skin(),
            stringer_section=_section(),
            diagonal_section=_section(),
            base=1.5,
            height=0.8,
            stringer_eccentricity=0.01,
            diagonal_eccentricity=0.02,
        ),
        kagome_cell(
            skin=_zero_skin(),
            stringer_section=_section(),
            diagonal_section=_section(),
            base=1.5,
            height=0.8,
            stringer_eccentricity=0.01,
            diagonal_eccentricity=0.02,
        ),
        hexagonal_grid_cell(
            skin=_zero_skin(),
            rib_section=_section(),
            diagonal_section=_section(),
            half_width=1.1,
            diagonal_rise=0.7,
            rib_length=0.6,
            rib_eccentricity=0.01,
            diagonal_eccentricity=0.02,
        ),
        star_cell(
            skin=_zero_skin(),
            stringer_section=_section(),
            diagonal_section=_section(),
            base=1.2,
            height=1.0,
            stringer_eccentricity=0.01,
            diagonal_eccentricity=0.02,
        ),
    ],
)
def test_phase3_cells_are_energy_consistent(cell) -> None:
    _assert_energy_consistent(cell)


def test_regular_hexagonal_grid_has_sixty_degree_objectivity() -> None:
    cell = regular_hexagonal_grid_cell(
        skin=_zero_skin(),
        member_section=_section(shear=False),
        pitch=1.4,
        eccentricity=0.0,
    )
    law = EnergyHomogenizer().compute(cell).law

    np.testing.assert_allclose(law.rotate(-np.pi / 3.0).C8, law.C8, rtol=1.0e-12, atol=1.0e-10)


def test_equilateral_star_cell_has_sixty_degree_objectivity() -> None:
    cell = equilateral_star_cell(
        skin=_zero_skin(),
        member_section=_section(shear=False),
        pitch=1.4,
        eccentricity=0.0,
    )
    law = EnergyHomogenizer().compute(cell).law

    np.testing.assert_allclose(law.rotate(-np.pi / 3.0).C8, law.C8, rtol=1.0e-12, atol=1.0e-10)


@given(offset=st.floats(min_value=-2.0, max_value=2.0, allow_nan=False, allow_infinity=False))
def test_reference_surface_shift_preserves_energy_under_strain_transform(offset: float) -> None:
    wall = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
    shifted = shift_reference_surface(wall, offset)
    eta_new = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])
    eta_old = eta_new.copy()
    eta_old[0:3] -= offset * eta_new[3:6]

    assert shifted.energy(eta_new) == pytest.approx(wall.energy(eta_old), rel=1.0e-12)


def test_sandwich_faces_superpose_about_reference_surface() -> None:
    face = _membrane_skin(stiffness=12.0)
    bottom = shift_reference_surface(face, 0.5)
    top = shift_reference_surface(face, -0.5)
    wall = superpose_linear_abd_walls(bottom, top)

    np.testing.assert_allclose(wall.B, np.zeros((3, 3)), atol=1.0e-12)
    np.testing.assert_allclose(wall.D, 6.0 * np.eye(3), atol=1.0e-12)


def test_sandwich_orthogrid_core_cell_uses_shifted_faces() -> None:
    face = _membrane_skin(stiffness=12.0)
    cell = sandwich_orthogrid_core_cell(
        bottom_face=face,
        top_face=face,
        bottom_face_offset=0.5,
        top_face_offset=-0.5,
        stringer_section=_section(),
        rib_section=_section(),
        stringer_spacing=1.0,
        rib_spacing=1.0,
    )

    np.testing.assert_allclose(cell.skin.B, np.zeros((3, 3)), atol=1.0e-12)
    np.testing.assert_allclose(cell.skin.D, 6.0 * np.eye(3), atol=1.0e-12)
