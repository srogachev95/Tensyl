from __future__ import annotations

from dataclasses import replace
from typing import TypedDict

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    BeamSection,
    CellEdge,
    CellNode,
    CellVector,
    braced_orthogrid_cell,
    check_cell_geometry,
    diamond_cell,
    equilateral_isogrid_cell,
    equilateral_star_cell,
    graph_unit_cell,
    hexagonal_grid_cell,
    isosceles_triangle_grid_cell,
    kagome_cell,
    orthogrid_cell,
    regular_hexagonal_grid_cell,
    sandwich_hexagonal_core_cell,
    sandwich_orthogrid_core_cell,
    sandwich_star_core_cell,
    star_cell,
    unidirectional_cell,
)
from tests._helpers import beam_section, zero_skin


class _SimpleInputs(TypedDict):
    skin: ABDStiffness
    member_section: BeamSection
    side_length: float
    axial_eccentricity: float


class _DiagonalInputs(TypedDict):
    skin: ABDStiffness
    e1_section: BeamSection
    positive_diagonal_section: BeamSection
    e1_pitch: float
    e2_pitch: float
    e1_axial_eccentricity: float
    diagonal_axial_eccentricity: float


class _Faces(TypedDict):
    bottom_face: ABDStiffness
    top_face: ABDStiffness
    bottom_face_to_reference: float
    top_face_to_reference: float


def _named_cells():
    skin, section = zero_skin(), beam_section()
    simple: _SimpleInputs = dict(
        skin=skin, member_section=section, side_length=2.0, axial_eccentricity=0.1
    )
    diagonal: _DiagonalInputs = dict(
        skin=skin,
        e1_section=section,
        positive_diagonal_section=section,
        e1_pitch=3.0,
        e2_pitch=2.0,
        e1_axial_eccentricity=0.1,
        diagonal_axial_eccentricity=0.1,
    )
    faces: _Faces = dict(
        bottom_face=skin, top_face=skin, bottom_face_to_reference=0.5, top_face_to_reference=-0.5
    )
    return [
        sandwich_orthogrid_core_cell(
            **faces, e1_section=section, e2_section=section, e1_pitch=3.0, e2_pitch=2.0
        ),
        sandwich_hexagonal_core_cell(
            **faces,
            e2_section=section,
            diagonal_section=section,
            e1_half_pitch=2.0,
            diagonal_e2_rise=0.8,
            e2_member_length=1.2,
        ),
        sandwich_star_core_cell(
            **faces, e1_section=section, diagonal_section=section, e1_pitch=3.0, e2_pitch=2.0
        ),
        unidirectional_cell(
            skin=skin, member_section=section, spacing=2.0, axial_eccentricity=0.1, angle_rad=0.4
        ),
        orthogrid_cell(
            skin=skin,
            e1_section=section,
            e2_section=section,
            e1_pitch=3.0,
            e2_pitch=2.0,
            e1_axial_eccentricity=0.1,
            e2_axial_eccentricity=0.1,
        ),
        equilateral_isogrid_cell(**simple),
        equilateral_star_cell(**simple),
        regular_hexagonal_grid_cell(**simple),
        diamond_cell(**diagonal),
        isosceles_triangle_grid_cell(**diagonal),
        kagome_cell(**diagonal),
        star_cell(**diagonal),
        hexagonal_grid_cell(
            skin=skin,
            e2_section=section,
            positive_diagonal_section=section,
            e1_half_pitch=2.0,
            diagonal_e2_rise=0.8,
            e2_member_length=1.2,
            e2_axial_eccentricity=0.1,
            diagonal_axial_eccentricity=0.1,
        ),
        *(
            braced_orthogrid_cell(
                **diagonal, e2_section=section, e2_axial_eccentricity=0.1, diagonal_pattern=pattern
            )
            for pattern in ("single", "double")
        ),
    ]


@pytest.mark.parametrize("cell", _named_cells())
@pytest.mark.parametrize("scale", [1e-3, 1.0, 1e3])
def test_named_cell_drawing_matches_modeled_length_density(cell, scale: float) -> None:
    geometry = cell.geometry
    assert geometry is not None
    cell = replace(
        cell,
        area=cell.area * scale**2,
        members=tuple(replace(m, length=m.length * scale) for m in cell.members),
        geometry=replace(
            geometry,
            nodes=tuple(CellNode(n.e1 * scale, n.e2 * scale) for n in geometry.nodes),
            repeat_vectors=tuple(
                CellVector(v.e1 * scale, v.e2 * scale) for v in geometry.repeat_vectors
            ),
        ),
    )
    densities = check_cell_geometry(cell)
    assert densities
    for drawn, modeled in densities.values():
        assert drawn > 0
        assert drawn == pytest.approx(modeled, rel=1e-10)


def _boundary_cell(multiplicity: float):
    return graph_unit_cell(
        area=2.0,
        skin=zero_skin(),
        nodes=(CellNode(0, 0), CellNode(2, 0), CellNode(0, 1), CellNode(2, 1)),
        edges=(
            CellEdge(0, 1, beam_section(), 0.0, multiplicity=multiplicity, family="rib"),
            CellEdge(2, 3, beam_section(), 0.0, multiplicity=multiplicity, family="rib"),
        ),
        repeat_vectors=(CellVector(2, 0), CellVector(0, 1)),
    )


def test_geometry_audit_detects_double_counted_boundary_ribs() -> None:
    assert check_cell_geometry(_boundary_cell(1.0))["rib"] == pytest.approx((1.0, 2.0))
    assert check_cell_geometry(_boundary_cell(0.5))["rib"] == pytest.approx((1.0, 1.0))


def test_geometry_audit_deduplicates_partial_overlaps() -> None:
    cell = graph_unit_cell(
        area=2.0,
        skin=zero_skin(),
        nodes=(CellNode(0, 0), CellNode(2, 0), CellNode(1, 0)),
        edges=(
            CellEdge(0, 1, beam_section(), 0.0, family="rib"),
            CellEdge(2, 1, beam_section(), 0.0, family="rib"),
        ),
        repeat_vectors=(CellVector(2, 0), CellVector(0, 1)),
    )
    assert check_cell_geometry(cell)["rib"] == pytest.approx((1.0, 1.5))


def test_geometry_audit_is_independent_of_drawing_translation() -> None:
    cell = _boundary_cell(0.5)
    assert cell.geometry is not None
    translated = replace(
        cell,
        geometry=replace(
            cell.geometry,
            nodes=tuple(CellNode(n.e1 + 11.4, n.e2 - 3.7) for n in cell.geometry.nodes),
        ),
    )
    np.testing.assert_allclose(check_cell_geometry(translated)["rib"], (1.0, 1.0))


def test_geometry_audit_rejects_absent_geometry() -> None:
    cell = replace(_boundary_cell(0.5), geometry=None)
    with pytest.raises(ValueError, match="geometry"):
        check_cell_geometry(cell)


def test_geometry_audit_detects_missing_modeled_length() -> None:
    cell = _boundary_cell(0.5)
    cell = replace(cell, members=tuple(replace(m, length=m.length / 2) for m in cell.members))
    assert check_cell_geometry(cell)["rib"] == pytest.approx((1.0, 0.5))


def test_geometry_audit_refuses_ambiguous_member_family_labels() -> None:
    cell = _named_cells()[-1]
    cell = replace(cell, members=tuple(replace(m, label="unknown") for m in cell.members))
    with pytest.raises(ValueError, match="ambiguous"):
        check_cell_geometry(cell)


def test_graph_edges_without_labels_keep_their_family_identity() -> None:
    cell = graph_unit_cell(
        area=2.0,
        skin=zero_skin(),
        nodes=(CellNode(0, 0), CellNode(2, 0), CellNode(0, 1)),
        edges=(
            CellEdge(0, 1, beam_section(), 0.0, family="e1"),
            CellEdge(0, 2, beam_section(), 0.0, family="e2"),
        ),
        repeat_vectors=(CellVector(2, 0), CellVector(0, 1)),
    )
    assert check_cell_geometry(cell)["e1"] == pytest.approx((1.0, 1.0))
    assert check_cell_geometry(cell)["e2"] == pytest.approx((0.5, 0.5))


def test_geometry_audit_refuses_conflicting_edge_and_family_labels() -> None:
    cell = graph_unit_cell(
        area=2.0,
        skin=zero_skin(),
        nodes=(CellNode(0, 0), CellNode(2, 0), CellNode(0, 1)),
        edges=(
            CellEdge(0, 1, beam_section(), 0.0, label="e2", family="e1"),
            CellEdge(0, 2, beam_section(), 0.0, label="vertical", family="e2"),
        ),
        repeat_vectors=(CellVector(2, 0), CellVector(0, 1)),
    )
    with pytest.raises(ValueError, match="ambiguous"):
        check_cell_geometry(cell)


def test_geometry_audit_refuses_drawings_beyond_the_tiled_neighborhood() -> None:
    cell = graph_unit_cell(
        area=2.0,
        skin=zero_skin(),
        nodes=(CellNode(0, 0), CellNode(10, 0)),
        edges=(CellEdge(0, 1, beam_section(), 0.0, family="rib"),),
        repeat_vectors=(CellVector(2, 0), CellVector(0, 1)),
    )
    with pytest.raises(ValueError, match="3x3"):
        check_cell_geometry(cell)
