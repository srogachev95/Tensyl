from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    BeamSection,
    DirectECHomogenizer,
    EnergyHomogenizer,
    HomogenizationInputError,
    IsotropicMaterial,
    StiffenerFamily,
    ValidityContext,
    equilateral_isogrid_cell,
    isotropic_plate,
    orthogrid_cell,
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
        eccentricity=0.0,
    )

    stiffness = EnergyHomogenizer().compute(cell).stiffness
    assert section.kGAy is not None
    assert section.kGAz is not None

    assert stiffness.A[0, 0] == pytest.approx(section.EA / spacing)
    assert stiffness.A[2, 2] == pytest.approx(0.25 * section.kGAy / spacing)
    assert stiffness.D[0, 0] == pytest.approx(section.EIy / spacing)
    assert stiffness.D[1, 1] == pytest.approx(section.EIz / spacing)
    assert stiffness.D[2, 2] == pytest.approx(0.25 * section.GJ / spacing)
    assert stiffness.As[0, 0] == pytest.approx(section.kGAz / spacing)
    assert stiffness.As[1, 1] == pytest.approx(0.0)


def test_energy_homogenizer_matches_explicit_cell_energy() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
    cell = orthogrid_cell(
        skin=skin,
        stringer_section=_section(),
        rib_section=_section(),
        stringer_spacing=0.25,
        rib_spacing=0.40,
        stringer_eccentricity=0.012,
        rib_eccentricity=0.009,
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


def test_direct_homogenizer_matches_energy_for_unidirectional_family() -> None:
    skin = _zero_skin()
    section = _section()
    spacing = 1.7

    energy = EnergyHomogenizer().compute(
        unidirectional_cell(
            skin=skin,
            member_section=section,
            spacing=spacing,
            eccentricity=0.04,
            angle_rad=0.37,
        )
    )
    direct = DirectECHomogenizer().compute(
        skin=skin,
        families=(
            StiffenerFamily(
                section=section,
                spacing=spacing,
                angle_rad=0.37,
                eccentricity=0.04,
            ),
        ),
    )

    np.testing.assert_allclose(direct.stiffness.C8, energy.stiffness.C8, rtol=1.0e-12, atol=1.0e-12)


def test_rotating_cell_matches_rotated_homogenized_stiffness() -> None:
    section = _section()
    angle = 0.41
    original = orthogrid_cell(
        skin=_zero_skin(),
        stringer_section=section,
        rib_section=section,
        stringer_spacing=1.3,
        rib_spacing=1.9,
        stringer_eccentricity=0.05,
        rib_eccentricity=0.02,
    )
    rotated = CanonicalUnitCell(
        area=original.area,
        skin=original.skin,
        members=tuple(
            BeamMember(
                section=member.section,
                length=member.length,
                angle_rad=member.angle_rad + angle,
                eccentricity=member.eccentricity,
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


def test_equilateral_isogrid_has_expected_membrane_symmetry() -> None:
    section = _section(shear=False)
    cell = equilateral_isogrid_cell(
        skin=_zero_skin(),
        member_section=section,
        pitch=2.0,
        eccentricity=0.0,
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
        eccentricity=0.2,
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
        eccentricity=0.0,
    )

    result = EnergyHomogenizer().compute(cell)

    assert result.diagnostics["rank"] < 8
    assert "rank_deficient_tangent" in result.validity.warnings


def test_direct_homogenizer_uses_typed_input_error() -> None:
    with pytest.raises(HomogenizationInputError, match="requires at least one stiffener family"):
        DirectECHomogenizer().compute(skin=_zero_skin(), families=())
