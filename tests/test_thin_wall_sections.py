from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    EnergyHomogenizer,
    IsotropicMaterial,
    ThinWallSegment,
    blade_section,
    channel_section,
    hat_section,
    isotropic_plate,
    orthogrid_cell,
    tee_section,
    thin_wall_section,
    zee_section,
)


def _material() -> IsotropicMaterial:
    return IsotropicMaterial(E=100.0, nu=0.25)


def test_blade_section_matches_closed_form_rectangle() -> None:
    section = blade_section(
        material=_material(),
        height=4.0,
        thickness=0.5,
        shear_correction_y=0.8,
        shear_correction_z=0.7,
    )

    assert section.properties.area == pytest.approx(2.0)
    assert section.centroid_y == pytest.approx(0.0)
    assert section.centroid_z == pytest.approx(2.0)
    assert section.properties.Iy == pytest.approx(0.5 * 4.0**3 / 12.0)
    assert section.properties.Iz == pytest.approx(4.0 * 0.5**3 / 12.0)
    assert section.properties.Iyz == pytest.approx(0.0)
    assert pytest.approx(4.0 * 0.5**3 / 3.0) == section.properties.J
    assert pytest.approx(200.0) == section.section.EA
    assert section.section.EIy == pytest.approx(100.0 * 0.5 * 4.0**3 / 12.0)
    assert section.section.EIz == pytest.approx(100.0 * 4.0 * 0.5**3 / 12.0)
    assert pytest.approx(_material().G * 4.0 * 0.5**3 / 3.0) == section.section.GJ
    assert section.section.kGAy == pytest.approx(0.8 * _material().G * 2.0)
    assert section.section.kGAz == pytest.approx(0.7 * _material().G * 2.0)


def test_horizontal_thin_wall_segment_matches_closed_form_rectangle() -> None:
    section = thin_wall_section(
        material=_material(),
        segments=(ThinWallSegment(-2.0, 0.0, 2.0, 0.0, 0.5),),
    )

    assert section.properties.area == pytest.approx(2.0)
    assert section.properties.Iy == pytest.approx(4.0 * 0.5**3 / 12.0)
    assert section.properties.Iz == pytest.approx(0.5 * 4.0**3 / 12.0)
    assert section.properties.Iyz == pytest.approx(0.0)
    assert section.section.kGAy is None
    assert section.section.kGAz is None


def test_oblique_thin_wall_segment_rotates_centroidal_inertia() -> None:
    section = thin_wall_section(
        material=_material(),
        segments=(ThinWallSegment(0.0, 0.0, 3.0, 4.0, 0.2),),
    )
    length = 5.0
    thickness = 0.2
    along = length**3 * thickness / 12.0
    across = length * thickness**3 / 12.0
    unit_y = 3.0 / 5.0
    unit_z = 4.0 / 5.0
    normal_y = -unit_z
    normal_z = unit_y

    assert section.properties.area == pytest.approx(length * thickness)
    assert section.properties.centroid_y == pytest.approx(1.5)
    assert section.properties.centroid_z == pytest.approx(2.0)
    assert section.properties.Iy == pytest.approx(along * unit_z**2 + across * normal_z**2)
    assert section.properties.Iz == pytest.approx(along * unit_y**2 + across * normal_y**2)
    assert section.properties.Iyz == pytest.approx(
        along * unit_y * unit_z + across * normal_y * normal_z
    )


def test_tee_section_matches_composite_area_parallel_axis_solution() -> None:
    section = tee_section(
        material=_material(),
        web_height=3.0,
        web_thickness=0.2,
        flange_width=2.0,
        flange_thickness=0.2,
    )
    web_area = 3.0 * 0.2
    flange_area = 2.0 * 0.2
    total_area = web_area + flange_area
    centroid_z = (web_area * 1.5 + flange_area * 3.1) / total_area
    web_dz = 1.5 - centroid_z
    flange_dz = 3.1 - centroid_z
    web_iy = 0.2 * 3.0**3 / 12.0
    web_iz = 3.0 * 0.2**3 / 12.0
    flange_iy = 2.0 * 0.2**3 / 12.0
    flange_iz = 0.2 * 2.0**3 / 12.0

    assert section.properties.area == pytest.approx(total_area)
    assert section.properties.centroid_y == pytest.approx(0.0)
    assert section.properties.centroid_z == pytest.approx(centroid_z)
    assert section.properties.Iy == pytest.approx(
        web_iy + web_area * web_dz**2 + flange_iy + flange_area * flange_dz**2
    )
    assert section.properties.Iz == pytest.approx(web_iz + flange_iz)
    assert section.properties.Iyz == pytest.approx(0.0)


def test_unsymmetric_composite_section_tracks_product_inertia_sign() -> None:
    section = thin_wall_section(
        material=_material(),
        segments=(
            ThinWallSegment(0.0, 0.0, 0.0, 2.0, 0.2, label="web"),
            ThinWallSegment(0.0, 0.0, 2.0, 0.0, 0.2, label="flange"),
        ),
    )

    assert section.properties.area == pytest.approx(0.8)
    assert section.properties.centroid_y == pytest.approx(0.5)
    assert section.properties.centroid_z == pytest.approx(0.5)
    vertical_centroidal_iy = 0.2 * 2.0**3 / 12.0
    vertical_centroidal_iz = 2.0 * 0.2**3 / 12.0
    horizontal_centroidal_iy = 2.0 * 0.2**3 / 12.0
    horizontal_centroidal_iz = 0.2 * 2.0**3 / 12.0
    parallel_axis_shift = 0.4 * 0.5**2

    assert section.properties.Iy == pytest.approx(
        vertical_centroidal_iy
        + parallel_axis_shift
        + horizontal_centroidal_iy
        + parallel_axis_shift
    )
    assert section.properties.Iz == pytest.approx(
        vertical_centroidal_iz
        + parallel_axis_shift
        + horizontal_centroidal_iz
        + parallel_axis_shift
    )
    assert section.properties.Iyz == pytest.approx(-0.2)


def test_named_sections_record_geometry_kind_and_positive_properties() -> None:
    material = _material()
    sections = [
        tee_section(
            material=material,
            web_height=3.0,
            web_thickness=0.2,
            flange_width=1.4,
            flange_thickness=0.2,
        ),
        zee_section(
            material=material,
            web_height=3.0,
            web_thickness=0.2,
            top_flange_width=1.1,
            bottom_flange_width=1.3,
            flange_thickness=0.2,
        ),
        channel_section(
            material=material,
            web_height=3.0,
            web_thickness=0.2,
            flange_width=1.2,
            flange_thickness=0.2,
        ),
        hat_section(
            material=material,
            web_height=2.5,
            web_thickness=0.2,
            crown_width=1.2,
            crown_thickness=0.2,
            flange_width=0.8,
            flange_thickness=0.2,
        ),
    ]

    assert {item.section.metadata["section_geometry"] for item in sections} == {
        "tee",
        "zee",
        "channel",
        "hat",
    }
    assert all(item.section.EA > 0.0 for item in sections)
    assert all(item.section.EIy > 0.0 for item in sections)
    assert all(item.section.EIz > 0.0 for item in sections)
    assert all(item.section.GJ > 0.0 for item in sections)


def test_geometry_derived_section_can_drive_homogenizer() -> None:
    material = IsotropicMaterial(E=10.6e6, nu=0.33)
    skin_thickness = 0.080
    skin = isotropic_plate(material, thickness=skin_thickness)
    stringer = hat_section(
        material=material,
        web_height=0.50,
        web_thickness=0.050,
        crown_width=0.40,
        crown_thickness=0.050,
        flange_width=0.20,
        flange_thickness=0.050,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )
    rib = blade_section(
        material=material,
        height=0.35,
        thickness=0.060,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )
    cell = orthogrid_cell(
        skin=skin,
        stringer_section=stringer.section,
        rib_section=rib.section,
        stringer_spacing=6.0,
        rib_spacing=8.0,
        stringer_eccentricity=0.5 * skin_thickness + stringer.centroid_z,
        rib_eccentricity=0.5 * skin_thickness + rib.centroid_z,
    )
    result = EnergyHomogenizer().compute(cell)

    assert result.diagnostics["symmetric"] is True
    assert result.diagnostics["positive_semidefinite"] is True
    assert result.stiffness.C8.shape == (8, 8)
    assert np.linalg.matrix_rank(result.stiffness.C8) == 8


def test_thin_wall_section_rejects_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="at least one segment"):
        thin_wall_section(material=_material(), segments=())
    with pytest.raises(ValueError, match="segment length"):
        thin_wall_section(
            material=_material(),
            segments=(ThinWallSegment(0.0, 0.0, 0.0, 0.0, 0.1),),
        )
    with pytest.raises(ValueError, match="shear_correction_y"):
        blade_section(
            material=_material(),
            height=1.0,
            thickness=0.1,
            shear_correction_y=0.0,
        )
