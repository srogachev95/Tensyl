from __future__ import annotations

import inspect
from dataclasses import fields

import numpy as np
import pytest

import tensyl.cells.tangent_plane as tangent_plane_cells
import tensyl.homogenizers.tangent_plane as tangent_plane
from tensyl import (
    ABDStiffness,
    BeamSection,
    EnergyHomogenizer,
    HomogenizationNumericalError,
    IsotropicMaterial,
    StiffenerFamily,
    ValidityContext,
    blade_section,
    equilateral_isogrid_cell,
    isotropic_plate,
    orthogrid_cell,
    stiffener_family_cell,
    unidirectional_cell,
)
from tensyl.cells import BeamMember, CanonicalUnitCell
from tensyl.homogenizers import member_energy
from tests._helpers import beam_section as _section
from tests._helpers import zero_skin as _zero_skin


def test_beam_section_rejects_invalid_stiffness() -> None:
    with pytest.raises(ValueError, match="EA must be finite and positive"):
        BeamSection(EA=0.0, EIy=1.0, EIz=1.0, GJ=1.0)

    with pytest.raises(ValueError, match="bending stiffness block"):
        BeamSection(EA=1.0, EIy=1.0, EIz=1.0, GJ=1.0, EIyz=1.0)


def test_beam_section_rejects_negative_mass_per_length() -> None:
    with pytest.raises(ValueError, match="mass_per_length must be finite and nonnegative"):
        BeamSection(EA=1.0, EIy=1.0, EIz=1.0, GJ=1.0, mass_per_length=-1.0)


def test_stiffened_panel_areal_mass_includes_the_stiffeners() -> None:
    aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
    skin = isotropic_plate(aluminum, thickness=0.08)
    blade = blade_section(material=aluminum, height=0.5, thickness=0.05)
    cell = orthogrid_cell(
        skin=skin,
        e1_section=blade.section,
        e2_section=blade.section,
        e1_pitch=4.0,
        e2_pitch=5.0,
        e1_axial_eccentricity=0.29,
        e2_axial_eccentricity=0.29,
    )

    result = EnergyHomogenizer().compute(cell)

    blade_mass_per_length = 0.1 * 0.5 * 0.05
    expected = 0.1 * 0.08 + blade_mass_per_length / 5.0 + blade_mass_per_length / 4.0
    assert result.stiffness.areal_mass == pytest.approx(expected)


def test_areal_mass_is_omitted_when_a_member_has_no_mass() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1), thickness=0.08)
    cell = unidirectional_cell(
        skin=skin,
        member_section=_section(),
        spacing=4.0,
        axial_eccentricity=0.3,
    )

    result = EnergyHomogenizer().compute(cell)

    assert result.stiffness.areal_mass is None
    assert any("areal mass" in assumption.lower() for assumption in result.assumptions)


def test_canonical_cell_rejects_invalid_area_and_empty_members() -> None:
    with pytest.raises(ValueError, match="area must be finite and positive"):
        CanonicalUnitCell(
            area=0.0,
            skin=_zero_skin(),
            members=(BeamMember(_section(), 1.0, 0.0, 0.0),),
        )

    with pytest.raises(ValueError, match="requires at least one beam member"):
        CanonicalUnitCell(area=1.0, skin=_zero_skin(), members=())


def test_single_member_family_has_expected_axis_aligned_contributions() -> None:
    spacing = 2.0
    section = _section()
    cell = unidirectional_cell(
        skin=_zero_skin(),
        member_section=section,
        spacing=spacing,
        axial_eccentricity=0.0,
    )

    stiffness = EnergyHomogenizer().compute(cell).stiffness
    assert section.kGAy is not None
    assert section.kGAz is not None

    assert stiffness.A[0, 0] == pytest.approx(section.EA / spacing)
    assert stiffness.A[2, 2] == pytest.approx(0.25 * section.kGAy / spacing)
    assert stiffness.D[0, 0] == pytest.approx(section.EIy / spacing)
    assert stiffness.D[1, 1] == pytest.approx(0.0)
    assert stiffness.D[2, 2] == pytest.approx(0.25 * section.GJ / spacing)
    assert stiffness.As[0, 0] == pytest.approx(section.kGAz / spacing)
    assert stiffness.As[1, 1] == pytest.approx(0.0)


def test_distinct_nemeth_eccentricities_have_positive_b11_and_b66_coupling() -> None:
    section = BeamSection(
        EA=1000.0,
        EIy=50.0,
        EIz=30.0,
        GJ=20.0,
        kGAy=240.0,
        kGAz=300.0,
    )
    cell = unidirectional_cell(
        skin=_zero_skin(),
        member_section=section,
        spacing=2.0,
        axial_eccentricity=0.15,
        shear_eccentricity=0.10,
    )

    stiffness = EnergyHomogenizer().compute(cell).stiffness

    assert stiffness.B[0, 0] == pytest.approx(75.0)
    assert stiffness.B[2, 2] == pytest.approx(3.0)


def test_member_in_plane_bending_inertia_does_not_stiffen_the_panel() -> None:
    # Under uniform plate strain and curvature a member's axis stays straight in
    # the panel plane, so EIz and EIyz store no energy in the first-order model.
    slender = BeamSection(EA=1200.0, EIy=50.0, EIz=30.0, GJ=20.0)
    wide = BeamSection(EA=1200.0, EIy=50.0, EIz=3.0e4, GJ=20.0, EIyz=40.0)

    def tangent(section: BeamSection) -> np.ndarray:
        cell = unidirectional_cell(
            skin=_zero_skin(),
            member_section=section,
            spacing=2.0,
            axial_eccentricity=0.1,
            angle_rad=0.3,
        )
        return EnergyHomogenizer().compute(cell).stiffness.C8

    np.testing.assert_array_equal(tangent(slender), tangent(wide))


def test_in_plane_bending_extension_flag_is_gone() -> None:
    constructors = (
        tangent_plane_cells.unidirectional_cell,
        tangent_plane_cells.orthogrid_cell,
        tangent_plane_cells.equilateral_isogrid_cell,
        tangent_plane_cells.graph_unit_cell,
        tangent_plane_cells.sandwich_orthogrid_core_cell,
    )
    value_objects = (BeamMember, tangent_plane_cells.CellEdge, tangent_plane_cells.StiffenerFamily)

    for constructor in constructors:
        assert "include_in_plane_bending" not in inspect.signature(constructor).parameters
    for value_object in value_objects:
        assert "include_in_plane_bending" not in {field.name for field in fields(value_object)}


def test_energy_homogenizer_matches_explicit_cell_energy() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
    cell = orthogrid_cell(
        skin=skin,
        e1_section=_section(),
        e2_section=_section(),
        e1_pitch=0.40,
        e2_pitch=0.25,
        e1_axial_eccentricity=0.012,
        e2_axial_eccentricity=0.009,
    )
    eta = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])

    result = EnergyHomogenizer().compute(cell)
    stiffness_energy = 0.5 * cell.area * float(eta @ result.stiffness.C8 @ eta)
    explicit_energy = cell.area * cell.skin.energy(eta) + sum(
        member_energy(member, eta) for member in cell.members
    )

    assert result.diagnostics["symmetric"] is True
    assert result.diagnostics["positive_semidefinite"] is True
    np.testing.assert_allclose(stiffness_energy, explicit_energy, rtol=1.0e-12, atol=1.0e-10)


def test_energy_homogenizer_projects_isogrid_block_roundoff_without_changing_energy() -> None:
    material = IsotropicMaterial(E=1.06e7, nu=0.33)
    skin_thickness = 0.3876504890620709
    total_height = 2.469107758812606
    section = blade_section(
        material=material,
        height=total_height - skin_thickness,
        thickness=0.9634947882965207,
    )
    cell = equilateral_isogrid_cell(
        skin=isotropic_plate(material, thickness=skin_thickness),
        member_section=section.section,
        side_length=11.653170097619295,
        axial_eccentricity=-(0.5 * skin_thickness + section.centroid_z),
    )
    eta = np.array([0.003, -0.002, 0.001, 0.02, -0.01, 0.04, 0.005, -0.006])

    result = EnergyHomogenizer().compute(cell)
    stiffness_energy = 0.5 * cell.area * float(eta @ result.stiffness.C8 @ eta)
    explicit_energy = cell.area * cell.skin.energy(eta) + sum(
        member_energy(member, eta) for member in cell.members
    )

    np.testing.assert_array_equal(result.stiffness.B, result.stiffness.B.T)
    np.testing.assert_allclose(stiffness_energy, explicit_energy, rtol=1.0e-12, atol=1.0e-10)


def test_energy_homogenizer_raises_typed_error_for_material_block_asymmetry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cell = unidirectional_cell(
        skin=_zero_skin(),
        member_section=_section(),
        spacing=1.0,
        axial_eccentricity=0.0,
    )
    bad_contribution = np.zeros((8, 8))
    bad_contribution[0, 4] = 1.0
    bad_contribution[4, 0] = 1.0

    def materially_asymmetric_contribution(*args, **kwargs):
        del args, kwargs
        return bad_contribution

    monkeypatch.setattr(
        tangent_plane,
        "member_tangent_contribution",
        materially_asymmetric_contribution,
    )

    with pytest.raises(HomogenizationNumericalError, match="tangent B block"):
        EnergyHomogenizer().compute(cell)


def _closed_form_family_tangent(family: StiffenerFamily) -> np.ndarray:
    # Classical smeared-stiffener terms written with scalar projection vectors,
    # independent of Tensyl's 8x8 member transform. r projects wall strain onto
    # the member axis; q gives twice the tensor shear in member axes.
    c = np.cos(family.angle_rad)
    s = np.sin(family.angle_rad)
    r = np.array([c * c, s * s, c * s])
    q = np.array([-2.0 * c * s, 2.0 * c * s, c * c - s * s])
    n = family.multiplicity / family.spacing
    section = family.section
    ea, es = family.axial_eccentricity, family.shear_eccentricity
    assert es is not None
    kgay = section.kGAy or 0.0
    kgaz = section.kGAz or 0.0
    rr = np.outer(r, r)
    qq = np.outer(q, q)
    tangent = np.zeros((8, 8))
    tangent[0:3, 0:3] = n * (section.EA * rr + 0.25 * kgay * qq)
    coupling = n * (section.EA * ea * rr + 0.25 * kgay * es * qq)
    tangent[0:3, 3:6] = coupling
    tangent[3:6, 0:3] = coupling
    tangent[3:6, 3:6] = n * (
        section.EA * ea**2 * rr
        + 0.25 * kgay * es**2 * qq
        + section.EIy * rr
        + 0.25 * section.GJ * qq
    )
    tangent[6:8, 6:8] = n * kgaz * np.outer([c, s], [c, s])
    return tangent


@pytest.mark.parametrize("angle", [0.0, 0.37, -1.1, 0.5 * np.pi, 2.4])
@pytest.mark.parametrize(("axial", "shear"), [(0.0, None), (0.04, None), (0.04, -0.02)])
def test_family_cell_matches_closed_form_smeared_stiffener_terms(
    angle: float, axial: float, shear: float | None
) -> None:
    families = (
        StiffenerFamily(
            section=_section(),
            spacing=1.7,
            angle_rad=angle,
            axial_eccentricity=axial,
            shear_eccentricity=shear,
        ),
        StiffenerFamily(
            section=BeamSection(EA=900.0, EIy=35.0, EIz=20.0, GJ=11.0, kGAy=250.0),
            spacing=2.9,
            angle_rad=angle + 1.0,
            axial_eccentricity=-axial,
            multiplicity=2.0,
        ),
    )

    result = EnergyHomogenizer().compute(
        stiffener_family_cell(skin=_zero_skin(), families=families)
    )

    expected = sum(_closed_form_family_tangent(family) for family in families)
    np.testing.assert_allclose(result.stiffness.C8, expected, rtol=1.0e-12, atol=1.0e-9)


def test_family_cell_adds_family_mass_per_unit_area() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1), thickness=0.08)
    section = BeamSection(EA=1.0e5, EIy=10.0, EIz=5.0, GJ=2.0, mass_per_length=0.004)
    families = (
        StiffenerFamily(section=section, spacing=3.0, angle_rad=0.0, axial_eccentricity=0.2),
        StiffenerFamily(
            section=section,
            spacing=5.0,
            angle_rad=0.5 * np.pi,
            axial_eccentricity=0.2,
            multiplicity=2.0,
        ),
    )

    result = EnergyHomogenizer().compute(stiffener_family_cell(skin=skin, families=families))

    assert result.stiffness.areal_mass == pytest.approx(0.1 * 0.08 + 0.004 / 3.0 + 2 * 0.004 / 5.0)


def test_family_cell_matches_the_equivalent_unidirectional_cell() -> None:
    family = StiffenerFamily(
        section=_section(), spacing=1.7, angle_rad=0.37, axial_eccentricity=0.04
    )

    from_family = EnergyHomogenizer().compute(
        stiffener_family_cell(skin=_zero_skin(), families=(family,))
    )
    from_cell = EnergyHomogenizer().compute(
        unidirectional_cell(
            skin=_zero_skin(),
            member_section=_section(),
            spacing=1.7,
            axial_eccentricity=0.04,
            angle_rad=0.37,
        )
    )

    np.testing.assert_allclose(
        from_family.stiffness.C8, from_cell.stiffness.C8, rtol=1.0e-12, atol=1.0e-12
    )


def test_family_cell_requires_at_least_one_family() -> None:
    with pytest.raises(ValueError, match="at least one stiffener family"):
        stiffener_family_cell(skin=_zero_skin(), families=())


def test_direct_ec_homogenizer_is_retired() -> None:
    import tensyl
    import tensyl.homogenizers

    assert not hasattr(tensyl, "DirectECHomogenizer")
    assert not hasattr(tensyl.homogenizers, "DirectECHomogenizer")


def test_rotating_cell_matches_rotated_homogenized_stiffness() -> None:
    section = _section()
    angle = 0.41
    original = orthogrid_cell(
        skin=_zero_skin(),
        e1_section=section,
        e2_section=section,
        e1_pitch=1.9,
        e2_pitch=1.3,
        e1_axial_eccentricity=0.05,
        e2_axial_eccentricity=0.02,
    )
    rotated = CanonicalUnitCell(
        area=original.area,
        skin=original.skin,
        members=tuple(
            BeamMember(
                section=member.section,
                length=member.length,
                angle_rad=member.angle_rad + angle,
                axial_eccentricity=member.axial_eccentricity,
                shear_eccentricity=member.shear_eccentricity,
                multiplicity=member.multiplicity,
                label=member.label,
            )
            for member in original.members
        ),
    )

    original_stiffness = EnergyHomogenizer().compute(original).stiffness
    rotated_stiffness = EnergyHomogenizer().compute(rotated).stiffness

    np.testing.assert_allclose(
        rotated_stiffness.C8,
        original_stiffness.rotate(-angle).C8,
        rtol=1.0e-12,
        atol=1.0e-10,
    )


def test_identical_homogenization_results_compare_equal_and_hash() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.002)
    cell = unidirectional_cell(
        skin=skin,
        member_section=_section(),
        spacing=0.1,
        axial_eccentricity=0.01,
    )
    first = EnergyHomogenizer().compute(cell)
    second = EnergyHomogenizer().compute(cell)

    assert first == second
    assert hash(first) == hash(second)


def test_rotating_a_homogenized_stiffness_keeps_its_validity_report() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.002)
    cell = unidirectional_cell(
        skin=skin,
        member_section=_section(),
        spacing=0.1,
        axial_eccentricity=0.01,
    )
    result = EnergyHomogenizer().compute(cell)

    rotated = result.stiffness.rotate(0.4)

    assert rotated.validity == result.validity


def test_equilateral_isogrid_has_expected_membrane_symmetry() -> None:
    section = _section(shear=False)
    cell = equilateral_isogrid_cell(
        skin=_zero_skin(),
        member_section=section,
        side_length=2.0,
        axial_eccentricity=0.0,
    )

    stiffness = EnergyHomogenizer().compute(cell).stiffness

    assert stiffness.A[0, 0] == pytest.approx(stiffness.A[1, 1])
    assert stiffness.A[0, 2] == pytest.approx(0.0, abs=1.0e-12)
    assert stiffness.A[1, 2] == pytest.approx(0.0, abs=1.0e-12)
    assert stiffness.A[2, 2] == pytest.approx((stiffness.A[0, 0] - stiffness.A[0, 1]) / 2.0)


def test_validity_report_warns_for_large_scale_ratios() -> None:
    cell = unidirectional_cell(
        skin=_zero_skin(),
        member_section=_section(),
        spacing=1.0,
        axial_eccentricity=0.2,
    )

    result = EnergyHomogenizer().compute(
        cell,
        validity_context=ValidityContext(
            characteristic_height=0.2,
            pitch=1.0,
            min_radius=4.0,
            response_length=10.0,
        ),
    )

    assert result.validity.h_over_R == pytest.approx(0.05)
    assert result.validity.p_over_R == pytest.approx(0.25)
    assert result.validity.p_over_L_response == pytest.approx(0.1)
    assert result.stiffness.validity == result.validity
    assert "h_over_R_exceeds_threshold" in result.validity.warnings
    assert "p_over_R_exceeds_threshold" in result.validity.warnings
    assert "p_over_L_response_exceeds_threshold" in result.validity.warnings


def test_rank_deficient_tangent_is_reported_not_raised() -> None:
    cell = unidirectional_cell(
        skin=_zero_skin(),
        member_section=_section(shear=False),
        spacing=1.0,
        axial_eccentricity=0.0,
    )

    result = EnergyHomogenizer().compute(cell)

    assert result.diagnostics["rank"] < 8
    assert "rank_deficient_tangent" in result.validity.warnings


def test_validity_rank_diagnostic_is_invariant_to_stiffness_scale() -> None:
    stiffness = ABDStiffness.from_tangent(1.0e-12 * np.eye(8))

    report = tangent_plane.validity_report_for_stiffness(stiffness)

    assert "rank_deficient_tangent" not in report.warnings
    assert "negative_energy_mode" not in report.warnings


@pytest.mark.parametrize("scale", [1.0e-12, 1.0, 1.0e12])
def test_validity_negative_energy_diagnostic_is_invariant_to_stiffness_scale(
    scale: float,
) -> None:
    tangent = scale * np.eye(8)
    tangent[7, 7] = -0.1 * scale
    stiffness = ABDStiffness.from_tangent(tangent)

    report = tangent_plane.validity_report_for_stiffness(stiffness)

    assert "negative_energy_mode" in report.warnings
