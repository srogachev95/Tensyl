from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    EnergyHomogenizer,
    IsotropicMaterial,
    Ply,
    blade_section,
    isotropic_plate,
    laminate_plate,
    orthogrid_cell,
    shift_reference_surface,
    unidirectional_cell,
    validity_report_for_stiffness,
)
from tests._helpers import beam_section, zero_skin


def _eccentric_grid():
    material = IsotropicMaterial(E=10.6e6, nu=0.33)
    blade = blade_section(material=material, height=0.5, thickness=0.05)
    return orthogrid_cell(
        skin=isotropic_plate(material, thickness=0.08),
        e1_section=blade.section,
        e2_section=blade.section,
        e1_pitch=4.0,
        e2_pitch=5.0,
        e1_axial_eccentricity=0.29,
        e2_axial_eccentricity=0.29,
    )


def test_residual_coupling_is_invariant_to_reference_and_rotation() -> None:
    result = EnergyHomogenizer().compute(_eccentric_grid())
    residual = result.validity.coupling_ratios["B_residual"]
    assert 0.0 < residual < result.validity.coupling_ratios["B_fro"]
    for angle in (-1.1, 0.0, 0.37, np.pi / 2):
        for offset in (-0.4, 0.0, 0.2):
            stiffness = shift_reference_surface(result.stiffness.rotate(angle), offset)
            report = validity_report_for_stiffness(stiffness)
            assert report.coupling_ratios["B_residual"] == pytest.approx(residual, rel=1e-11)
            warning = "membrane_bending_coupling_exceeds_threshold"
            assert (warning in report.warnings) == (warning in result.validity.warnings)


def test_symmetric_laminate_only_has_reference_surface_coupling() -> None:
    material = IsotropicMaterial(E=70e9, nu=0.3)
    plate = laminate_plate((Ply(material, 0.001), Ply(material, 0.001)))
    for offset in (-0.01, 0.0, 0.003):
        report = validity_report_for_stiffness(shift_reference_surface(plate, offset))
        assert report.coupling_ratios["B_residual"] == pytest.approx(0.0, abs=1e-12)
        assert "membrane_bending_coupling_exceeds_threshold" not in report.warnings


def test_unidirectional_neutral_offset_matches_the_axial_neutral_surface() -> None:
    # With no skin and a shared axial/shear offset, B is exactly offset * A.
    cell = unidirectional_cell(
        skin=zero_skin(), member_section=beam_section(), spacing=2.0, axial_eccentricity=0.3
    )
    result = EnergyHomogenizer().compute(cell)
    assert result.diagnostics["neutral_surface_offset"] == pytest.approx(
        result.stiffness.B[0, 0] / result.stiffness.A[0, 0]
    )
    assert result.validity.coupling_ratios["B_residual"] == pytest.approx(0.0, abs=1e-14)


@pytest.mark.parametrize("scale", [1e-120, 1.0, 1e120])
def test_residual_coupling_uses_a_mandel_projection_at_any_stiffness_scale(scale: float) -> None:
    # An independent diagonal example: Mandel doubles the 66 coefficient.
    A = np.diag([4.0, 2.0, 1.0])
    B = np.diag([1.0, -0.4, 0.3])
    D = np.diag([3.0, 2.0, 1.0])
    d = (4.0 - 0.8 + 1.2) / (16.0 + 4.0 + 4.0)
    a = np.array([4.0, 2.0, 2.0])
    b = np.array([1.0, -0.4, 0.6])
    bending = np.array([3.0, 2.0, 2.0])
    expected = np.linalg.norm(b - d * a) / np.sqrt(
        np.linalg.norm(a) * np.linalg.norm(bending - 2 * d * b + d**2 * a)
    )
    report = validity_report_for_stiffness(
        ABDStiffness(A=A * scale, B=B * scale, D=D * scale, As=np.eye(2) * scale)
    )
    assert report.coupling_ratios["B_residual"] == pytest.approx(expected)
    assert report.coupling_ratios["B_fro"] == pytest.approx(
        np.linalg.norm(B) / np.sqrt(np.linalg.norm(A) * np.linalg.norm(D))
    )


def test_zero_stiffness_has_finite_zero_coupling() -> None:
    report = validity_report_for_stiffness(zero_skin())
    assert report.coupling_ratios == {"B_fro": 0.0, "B_residual": 0.0}
    assert "rank_deficient_tangent" in report.warnings


def test_cell_pitch_fills_missing_context_without_overriding_the_caller() -> None:
    from tensyl import ValidityContext

    cell = _eccentric_grid()
    partial = ValidityContext(characteristic_height=0.5, min_radius=100.0, response_length=200.0)
    report = EnergyHomogenizer().compute(cell, validity_context=partial).validity
    assert partial.pitch is None
    assert report.h_over_R == pytest.approx(0.005)
    assert report.p_over_R == pytest.approx(5.0 / 100.0)
    assert report.p_over_L_response == pytest.approx(5.0 / 200.0)

    explicit = ValidityContext(pitch=2.0, min_radius=100.0, response_length=200.0)
    report = EnergyHomogenizer().compute(cell, validity_context=explicit).validity
    assert report.p_over_R == pytest.approx(2.0 / 100.0)
    assert report.p_over_L_response == pytest.approx(2.0 / 200.0)


def test_pitch_from_oblique_repeat_vectors_uses_their_lengths() -> None:
    from tensyl import CellEdge, CellNode, CellVector, ValidityContext, graph_unit_cell

    cell = graph_unit_cell(
        skin=zero_skin(),
        area=6.0,
        nodes=(CellNode(0.0, 0.0), CellNode(3.0, 4.0)),
        edges=(CellEdge(0, 1, beam_section(), axial_eccentricity=0.0),),
        repeat_vectors=(CellVector(3.0, 4.0), CellVector(0.0, 2.0)),
    )
    report = (
        EnergyHomogenizer()
        .compute(cell, validity_context=ValidityContext(min_radius=100.0))
        .validity
    )
    assert report.p_over_R == pytest.approx(0.05)


def test_family_pitch_uses_largest_spacing() -> None:
    from tensyl import StiffenerFamily, ValidityContext, stiffener_family_cell

    cell = stiffener_family_cell(
        skin=zero_skin(),
        families=(
            StiffenerFamily(beam_section(), 2.0, 0.0, 0.0),
            StiffenerFamily(beam_section(), 7.0, 0.4, 0.0),
        ),
    )
    report = (
        EnergyHomogenizer()
        .compute(cell, validity_context=ValidityContext(min_radius=100.0))
        .validity
    )
    assert report.p_over_R == pytest.approx(0.07)


def test_missing_context_and_unavailable_checks_remain_distinct() -> None:
    from tensyl import BeamMember, CanonicalUnitCell, ValidityContext

    no_geometry = CanonicalUnitCell(
        area=1.0, skin=zero_skin(), members=(BeamMember(beam_section(), 1.0, 0.0, 0.0),)
    )
    missing = EnergyHomogenizer().compute(no_geometry).validity
    assert "validity_context_missing" in missing.warnings
    partial = EnergyHomogenizer().compute(no_geometry, validity_context=ValidityContext()).validity
    assert "validity_context_missing" not in partial.warnings
    assert "p_over_R_unavailable" in partial.warnings
    inferred = EnergyHomogenizer().compute(_eccentric_grid()).validity
    assert "validity_context_missing" not in inferred.warnings
    assert "h_over_R_unavailable" in inferred.warnings
    assert "p_over_R_unavailable" in inferred.warnings
    assert "p_over_L_response_unavailable" in inferred.warnings


def test_validity_context_from_surface_point_supports_flat_and_curved_geometry() -> None:
    from tensyl import Cylinder, FlatPlate, ValidityContext

    flat = ValidityContext.from_surface_point(FlatPlate().point_at(0.0, 0.0))
    assert flat.min_radius == np.inf
    assert flat.pitch is None
    curved = ValidityContext.from_surface_point(
        Cylinder(radius=12.0).point_at(0.2, 0.4),
        characteristic_height=0.2,
        pitch=1.5,
        response_length=20.0,
    )
    assert curved == ValidityContext(
        min_radius=12.0, characteristic_height=0.2, pitch=1.5, response_length=20.0
    )
