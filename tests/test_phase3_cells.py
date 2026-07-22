from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest
from hypothesis import given
from hypothesis import strategies as st

from tensyl import (
    CellEdge,
    CellNode,
    CellVector,
    EnergyHomogenizer,
    IsotropicMaterial,
    braced_orthogrid_cell,
    diamond_cell,
    equilateral_isogrid_cell,
    equilateral_star_cell,
    graph_unit_cell,
    hexagonal_grid_cell,
    isosceles_triangle_grid_cell,
    isotropic_plate,
    kagome_cell,
    orthogrid_cell,
    regular_hexagonal_grid_cell,
    sandwich_hexagonal_core_cell,
    sandwich_orthogrid_core_cell,
    sandwich_star_core_cell,
    shift_reference_surface,
    star_cell,
    superpose_abd_stiffnesses,
    unidirectional_cell,
)
from tests._helpers import (
    assert_energy_consistent as _assert_energy_consistent,
)
from tests._helpers import (
    beam_section as _section,
)
from tests._helpers import (
    membrane_skin as _membrane_skin,
)
from tests._helpers import (
    zero_skin as _zero_skin,
)


def test_phase3_reference_inventory_is_present() -> None:
    path = Path(__file__).parent / "data" / "nemeth_phase3_cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))

    assert {case["id"] for case in cases} == {
        "braced_orthogrid_double",
        "braced_orthogrid_single",
        "diamond",
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
        edges=(CellEdge(0, 1, section=section, axial_eccentricity=0.2, label="edge"),),
        repeat_vectors=(CellVector(3.0, 4.0), CellVector(-0.32, 0.24)),
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
            edges=(CellEdge(0, 2, section=_section(), axial_eccentricity=0.0),),
        )


def test_braced_orthogrid_single_has_half_diagonal_density() -> None:
    section = _section()
    double = braced_orthogrid_cell(
        skin=_zero_skin(),
        e1_section=section,
        e2_section=section,
        positive_diagonal_section=section,
        e1_pitch=1.9,
        e2_pitch=1.3,
        e1_axial_eccentricity=0.0,
        e2_axial_eccentricity=0.0,
        diagonal_axial_eccentricity=0.0,
        diagonal_pattern="double",
    )
    single = braced_orthogrid_cell(
        skin=_zero_skin(),
        e1_section=section,
        e2_section=section,
        positive_diagonal_section=section,
        e1_pitch=1.9,
        e2_pitch=1.3,
        e1_axial_eccentricity=0.0,
        e2_axial_eccentricity=0.0,
        diagonal_axial_eccentricity=0.0,
        diagonal_pattern="single",
    )

    double_brace_density = sum(
        member.multiplicity * member.length / double.area
        for member in double.members
        if "diagonal" in member.label
    )
    single_brace_density = sum(
        member.multiplicity * member.length / single.area
        for member in single.members
        if "diagonal" in member.label
    )

    assert single_brace_density == pytest.approx(0.5 * double_brace_density)


def test_braced_orthogrid_diagonal_uses_coordinate_pitch_ratio() -> None:
    cell = braced_orthogrid_cell(
        skin=_zero_skin(),
        e1_section=_section(),
        e2_section=_section(),
        positive_diagonal_section=_section(),
        e1_pitch=4.0,
        e2_pitch=3.0,
        e1_axial_eccentricity=0.0,
        e2_axial_eccentricity=0.0,
        diagonal_axial_eccentricity=0.0,
    )

    positive = next(member for member in cell.members if member.label == "positive_diagonal")
    assert positive.length == pytest.approx(5.0)
    assert positive.angle_rad == pytest.approx(np.arctan2(3.0, 4.0))


@pytest.mark.parametrize(
    ("cell", "expected_vectors"),
    [
        (
            braced_orthogrid_cell(
                skin=_zero_skin(),
                e1_section=_section(),
                e2_section=_section(),
                positive_diagonal_section=_section(),
                e1_pitch=4.0,
                e2_pitch=3.0,
                e1_axial_eccentricity=0.0,
                e2_axial_eccentricity=0.0,
                diagonal_axial_eccentricity=0.0,
            ),
            {
                "1-2": (4.0, 0.0),
                "3-4": (0.0, 3.0),
                "5-6": (4.0, 3.0),
                "7-8": (-4.0, 3.0),
            },
        ),
        (
            braced_orthogrid_cell(
                skin=_zero_skin(),
                e1_section=_section(),
                e2_section=_section(),
                positive_diagonal_section=_section(),
                e1_pitch=4.0,
                e2_pitch=3.0,
                e1_axial_eccentricity=0.0,
                e2_axial_eccentricity=0.0,
                diagonal_axial_eccentricity=0.0,
                diagonal_pattern="single",
            ),
            {
                "1-2": (8.0, 0.0),
                "3-4": (0.0, 6.0),
                "5-6": (8.0, 6.0),
                "5-7": (8.0, 0.0),
                "5-8": (0.0, 6.0),
                "7-8": (-8.0, 6.0),
            },
        ),
        (
            isosceles_triangle_grid_cell(
                skin=_zero_skin(),
                e1_section=_section(),
                positive_diagonal_section=_section(),
                e1_pitch=4.0,
                e2_pitch=3.0,
                e1_axial_eccentricity=0.0,
                diagonal_axial_eccentricity=0.0,
            ),
            {"1-2": (4.0, 0.0), "3-4": (2.0, 3.0), "5-6": (-2.0, 3.0)},
        ),
        (
            kagome_cell(
                skin=_zero_skin(),
                e1_section=_section(),
                positive_diagonal_section=_section(),
                e1_pitch=4.0,
                e2_pitch=3.0,
                e1_axial_eccentricity=0.0,
                diagonal_axial_eccentricity=0.0,
            ),
            {
                "1-2": (4.0, 0.0),
                "3-4": (4.0, 0.0),
                "5-6": (4.0, 6.0),
                "7-8": (-4.0, 6.0),
            },
        ),
        (
            hexagonal_grid_cell(
                skin=_zero_skin(),
                e2_section=_section(),
                positive_diagonal_section=_section(),
                e1_half_pitch=4.0,
                diagonal_e2_rise=3.0,
                e2_member_length=2.0,
                e2_axial_eccentricity=0.0,
                diagonal_axial_eccentricity=0.0,
            ),
            {
                "2-1": (2.0, -1.5),
                "2-3": (-2.0, -1.5),
                "2-5": (0.0, 2.0),
                "5-4": (2.0, 1.5),
                "5-6": (-2.0, 1.5),
            },
        ),
    ],
)
def test_drawable_edges_match_nemeth_basic_cell_table_vectors(
    cell,
    expected_vectors: dict[str, tuple[float, float]],
) -> None:
    geometry = cell.geometry
    assert geometry is not None
    actual = {}
    for edge in geometry.edges:
        start = geometry.nodes[edge.start]
        end = geometry.nodes[edge.end]
        actual[edge.label] = (end.e1 - start.e1, end.e2 - start.e2)

    assert actual.keys() == expected_vectors.keys()
    for label, expected in expected_vectors.items():
        assert actual[label] == pytest.approx(expected)


def test_star_geometry_retains_all_twelve_table_9_members() -> None:
    width = 4.0
    height = 3.0
    cell = star_cell(
        skin=_zero_skin(),
        e1_section=_section(),
        positive_diagonal_section=_section(),
        e1_pitch=width,
        e2_pitch=height,
        e1_axial_eccentricity=0.0,
        diagonal_axial_eccentricity=0.0,
    )
    geometry = cell.geometry
    assert geometry is not None

    assert len(geometry.edges) == 12
    assert {
        family: sum(edge.family == family for edge in geometry.edges)
        for family in {
            "e1",
            "positive_diagonal",
            "negative_diagonal",
        }
    } == {"e1": 4, "positive_diagonal": 4, "negative_diagonal": 4}
    diagonal_length = np.hypot(0.5 * width, height) / 3.0
    for edge in geometry.edges:
        start = geometry.nodes[edge.start]
        end = geometry.nodes[edge.end]
        length = np.hypot(end.e1 - start.e1, end.e2 - start.e2)
        expected = width / 3.0 if edge.family == "e1" else diagonal_length
        assert length == pytest.approx(expected)


def test_diamond_cell_has_no_e2_family_and_connected_drawable_edges() -> None:
    cell = diamond_cell(
        skin=_zero_skin(),
        e1_section=_section(),
        positive_diagonal_section=_section(),
        e1_pitch=2.0,
        e2_pitch=1.0,
        e1_axial_eccentricity=0.0,
        diagonal_axial_eccentricity=0.0,
    )

    assert {member.label for member in cell.members} == {
        "e1",
        "positive_diagonal",
        "negative_diagonal",
    }
    assert cell.geometry is not None
    assert {edge.family for edge in cell.geometry.edges} == {
        "e1",
        "positive_diagonal",
        "negative_diagonal",
    }
    used_nodes = {index for edge in cell.geometry.edges for index in (edge.start, edge.end)}
    assert used_nodes == set(range(len(cell.geometry.nodes)))


@pytest.mark.parametrize(
    "cell",
    [
        unidirectional_cell(
            skin=_zero_skin(),
            member_section=_section(),
            spacing=1.0,
            axial_eccentricity=0.0,
        ),
        orthogrid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            e2_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            e2_axial_eccentricity=0.0,
        ),
        equilateral_isogrid_cell(
            skin=_zero_skin(),
            member_section=_section(),
            side_length=1.0,
            axial_eccentricity=0.0,
        ),
        braced_orthogrid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            e2_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            e2_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        braced_orthogrid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            e2_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            e2_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
            diagonal_pattern="single",
        ),
        diamond_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        isosceles_triangle_grid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        kagome_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        hexagonal_grid_cell(
            skin=_zero_skin(),
            e2_section=_section(),
            positive_diagonal_section=_section(),
            e1_half_pitch=1.0,
            diagonal_e2_rise=0.8,
            e2_member_length=0.6,
            e2_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        regular_hexagonal_grid_cell(
            skin=_zero_skin(),
            member_section=_section(),
            side_length=1.0,
            axial_eccentricity=0.0,
        ),
        star_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
            e1_axial_eccentricity=0.0,
            diagonal_axial_eccentricity=0.0,
        ),
        equilateral_star_cell(
            skin=_zero_skin(),
            member_section=_section(),
            side_length=1.0,
            axial_eccentricity=0.0,
        ),
        sandwich_orthogrid_core_cell(
            bottom_face=_membrane_skin(),
            top_face=_membrane_skin(),
            bottom_face_to_reference=0.5,
            top_face_to_reference=-0.5,
            e1_section=_section(),
            e2_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
        ),
        sandwich_hexagonal_core_cell(
            bottom_face=_membrane_skin(),
            top_face=_membrane_skin(),
            bottom_face_to_reference=0.5,
            top_face_to_reference=-0.5,
            e2_section=_section(),
            diagonal_section=_section(),
            e1_half_pitch=1.0,
            diagonal_e2_rise=0.8,
            e2_member_length=0.6,
        ),
        sandwich_star_core_cell(
            bottom_face=_membrane_skin(),
            top_face=_membrane_skin(),
            bottom_face_to_reference=0.5,
            top_face_to_reference=-0.5,
            e1_section=_section(),
            diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=0.9,
        ),
    ],
)
def test_named_cell_geometry_can_be_tiled_for_visualization(cell) -> None:
    geometry = cell.geometry
    assert geometry is not None
    assert geometry.repeat_area == pytest.approx(cell.area)

    segments = geometry.segments(repeat_a=2, repeat_b=3)
    assert len(segments) == 6 * len(geometry.edges)
    assert all(segment.family for segment in segments)
    coordinates = np.array(
        [
            [segment.start_e1, segment.start_e2, segment.end_e1, segment.end_e2]
            for segment in segments
        ]
    )
    assert np.all(np.isfinite(coordinates))


def test_equilateral_triangle_constructor_matches_existing_isogrid() -> None:
    section = _section()
    pitch = 2.0
    triangle = isosceles_triangle_grid_cell(
        skin=_zero_skin(),
        e1_section=section,
        positive_diagonal_section=section,
        e1_pitch=pitch,
        e2_pitch=np.sqrt(3.0) * pitch / 2.0,
        e1_axial_eccentricity=0.03,
        diagonal_axial_eccentricity=0.03,
    )
    isogrid = equilateral_isogrid_cell(
        skin=_zero_skin(),
        member_section=section,
        side_length=pitch,
        axial_eccentricity=0.03,
    )

    np.testing.assert_allclose(
        EnergyHomogenizer().compute(triangle).stiffness.C8,
        EnergyHomogenizer().compute(isogrid).stiffness.C8,
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_kagome_matches_isosceles_triangle_energy_output() -> None:
    section = _section()
    triangle = isosceles_triangle_grid_cell(
        skin=_zero_skin(),
        e1_section=section,
        positive_diagonal_section=section,
        e1_pitch=1.4,
        e2_pitch=0.9,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.04,
    )
    kagome = kagome_cell(
        skin=_zero_skin(),
        e1_section=section,
        positive_diagonal_section=section,
        e1_pitch=1.4,
        e2_pitch=0.9,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.04,
    )

    np.testing.assert_allclose(
        EnergyHomogenizer().compute(kagome).stiffness.C8,
        EnergyHomogenizer().compute(triangle).stiffness.C8,
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_canonical_cell_reconstruction_is_idempotent() -> None:
    cell = kagome_cell(
        skin=_zero_skin(),
        e1_section=_section(),
        positive_diagonal_section=_section(),
        e1_pitch=2.0,
        e2_pitch=1.5,
        e1_axial_eccentricity=0.02,
        diagonal_axial_eccentricity=0.03,
    )

    reconstructed = type(cell)(
        area=cell.area,
        skin=cell.skin,
        members=cell.members,
        frame=cell.frame,
        convention=cell.convention,
        geometry=cell.geometry,
        metadata=cell.metadata,
    )

    assert reconstructed == cell
    np.testing.assert_allclose(
        EnergyHomogenizer().compute(reconstructed).stiffness.C8,
        EnergyHomogenizer().compute(cell).stiffness.C8,
    )


@pytest.mark.parametrize(
    "cell",
    [
        braced_orthogrid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            e2_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.7,
            e2_pitch=1.2,
            e1_axial_eccentricity=0.01,
            e2_axial_eccentricity=0.02,
            diagonal_axial_eccentricity=0.03,
        ),
        isosceles_triangle_grid_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.5,
            e2_pitch=0.8,
            e1_axial_eccentricity=0.01,
            diagonal_axial_eccentricity=0.02,
        ),
        kagome_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.5,
            e2_pitch=0.8,
            e1_axial_eccentricity=0.01,
            diagonal_axial_eccentricity=0.02,
        ),
        hexagonal_grid_cell(
            skin=_zero_skin(),
            e2_section=_section(),
            positive_diagonal_section=_section(),
            e1_half_pitch=1.1,
            diagonal_e2_rise=0.7,
            e2_member_length=0.6,
            e2_axial_eccentricity=0.01,
            diagonal_axial_eccentricity=0.02,
        ),
        star_cell(
            skin=_zero_skin(),
            e1_section=_section(),
            positive_diagonal_section=_section(),
            e1_pitch=1.2,
            e2_pitch=1.0,
            e1_axial_eccentricity=0.01,
            diagonal_axial_eccentricity=0.02,
        ),
    ],
)
def test_phase3_cells_are_energy_consistent(cell) -> None:
    _assert_energy_consistent(cell)


def test_regular_hexagonal_grid_has_sixty_degree_objectivity() -> None:
    cell = regular_hexagonal_grid_cell(
        skin=_zero_skin(),
        member_section=_section(shear=False),
        side_length=1.4,
        axial_eccentricity=0.0,
    )
    stiffness = EnergyHomogenizer().compute(cell).stiffness

    np.testing.assert_allclose(
        stiffness.rotate(-np.pi / 3.0).C8, stiffness.C8, rtol=1.0e-12, atol=1.0e-10
    )


def test_equilateral_star_cell_has_sixty_degree_objectivity() -> None:
    cell = equilateral_star_cell(
        skin=_zero_skin(),
        member_section=_section(shear=False),
        side_length=1.4,
        axial_eccentricity=0.0,
    )
    stiffness = EnergyHomogenizer().compute(cell).stiffness

    np.testing.assert_allclose(
        stiffness.rotate(-np.pi / 3.0).C8, stiffness.C8, rtol=1.0e-12, atol=1.0e-10
    )


@given(offset=st.floats(min_value=-2.0, max_value=2.0, allow_nan=False, allow_infinity=False))
def test_reference_surface_shift_preserves_energy_under_strain_transform(offset: float) -> None:
    stiffness = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
    shifted = shift_reference_surface(stiffness, offset)
    eta_new = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])
    eta_old = eta_new.copy()
    eta_old[0:3] -= offset * eta_new[3:6]

    assert shifted.energy(eta_new) == pytest.approx(stiffness.energy(eta_old), rel=1.0e-12)


def test_sandwich_faces_superpose_about_reference_surface() -> None:
    face = _membrane_skin(stiffness=12.0)
    bottom = shift_reference_surface(face, 0.5)
    top = shift_reference_surface(face, -0.5)
    stiffness = superpose_abd_stiffnesses(bottom, top)

    np.testing.assert_allclose(stiffness.B, np.zeros((3, 3)), atol=1.0e-12)
    np.testing.assert_allclose(stiffness.D, 6.0 * np.eye(3), atol=1.0e-12)


def test_sandwich_orthogrid_core_cell_uses_shifted_faces() -> None:
    face = _membrane_skin(stiffness=12.0)
    cell = sandwich_orthogrid_core_cell(
        bottom_face=face,
        top_face=face,
        bottom_face_to_reference=0.5,
        top_face_to_reference=-0.5,
        e1_section=_section(),
        e2_section=_section(),
        e1_pitch=1.0,
        e2_pitch=1.0,
    )

    np.testing.assert_allclose(cell.skin.B, np.zeros((3, 3)), atol=1.0e-12)
    np.testing.assert_allclose(cell.skin.D, 6.0 * np.eye(3), atol=1.0e-12)
