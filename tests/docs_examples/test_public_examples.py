import numpy as np

from tensyl import (
    BeamSection,
    ConicalFrustum,
    ConstantWallField,
    Cylinder,
    Ellipsoid,
    EnergyHomogenizer,
    HomogenizationResult,
    IsotropicMaterial,
    Sphere,
    SphericalCap,
    ValidityContext,
    WallAtlas,
    isotropic_plate,
    orthogrid_cell,
)
from tensyl.io import from_yaml, to_yaml


def _orthogrid_result():
    skin = isotropic_plate(
        IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
        thickness=0.080,
    )
    section = BeamSection(
        EA=3.2e6,
        EIy=2.4e4,
        EIz=6.5e3,
        GJ=4.0e3,
        kGAy=1.1e6,
        kGAz=0.9e6,
    )
    cell = orthogrid_cell(
        skin=skin,
        stringer_section=section,
        rib_section=section,
        stringer_spacing=6.0,
        rib_spacing=8.0,
        stringer_eccentricity=0.45,
        rib_eccentricity=0.45,
    )
    return EnergyHomogenizer().compute(
        cell,
        validity_context=ValidityContext(
            characteristic_height=0.50,
            pitch=8.0,
            min_radius=120.0,
            response_length=80.0,
        ),
    )


def _sp8007_orthotropic_coefficients(wall, *, tolerance=1.0e-9):
    unsupported = {
        "A16": wall.A[0, 2],
        "A26": wall.A[1, 2],
        "B16": wall.B[0, 2],
        "B26": wall.B[1, 2],
        "B61": wall.B[2, 0],
        "B62": wall.B[2, 1],
        "D16": wall.D[0, 2],
        "D26": wall.D[1, 2],
    }
    nonzero = {name: value for name, value in unsupported.items() if abs(value) > tolerance}
    if nonzero:
        msg = (
            "SP-8007 orthotropic-cylinder coefficients assume axial/circumferential "
            f"orthotropy; unsupported coupling terms are nonzero: {nonzero}"
        )
        raise ValueError(msg)

    return {
        "Ebar_x": wall.A[0, 0],
        "Ebar_y": wall.A[1, 1],
        "Ebar_xy": wall.A[0, 1],
        "Gbar_xy": wall.A[2, 2],
        "Dbar_x": wall.D[0, 0],
        "Dbar_y": wall.D[1, 1],
        "Dbar_xy": 2.0 * wall.D[0, 1] + 4.0 * wall.D[2, 2],
        "Cbar_x": wall.B[0, 0],
        "Cbar_y": wall.B[1, 1],
        "Cbar_xy": wall.B[0, 1],
        "Kbar_xy": wall.B[2, 2],
    }


def test_first_wall_law_example() -> None:
    wall = isotropic_plate(
        IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
        thickness=0.080,
    )

    assert wall.A.shape == (3, 3)
    assert wall.B.shape == (3, 3)
    assert wall.D.shape == (3, 3)
    assert wall.As.shape == (2, 2)
    assert np.max(np.abs(wall.B)) == 0.0


def test_first_homogenized_cell_and_result_interpretation_examples() -> None:
    result = _orthogrid_result()

    assert result.law.C8.shape == (8, 8)
    assert result.law.validity == result.validity
    assert result.diagnostics["symmetric"]
    assert result.diagnostics["positive_semidefinite"]
    assert result.diagnostics["rank"] == 8
    assert np.isclose(result.law.A[0, 0], 1.4849661467100587e6)
    assert np.isclose(result.law.B[0, 0], 2.4e5)
    assert "membrane_bending_coupling_exceeds_threshold" in result.validity.warnings


def test_stiffened_barrel_example() -> None:
    result = _orthogrid_result()
    surface = Cylinder(radius=120.0, length=300.0)
    field = ConstantWallField(result.law)
    wall_at_midbay = field.law_at(surface, 150.0, 0.0)

    assert wall_at_midbay.frame.label == "cylinder"
    assert result.validity.p_over_R == 8.0 / 120.0


def test_stiffened_dome_concept_example() -> None:
    dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
    wall = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
    field = ConstantWallField(wall)

    atlas = WallAtlas.from_field(
        dome,
        field,
        u_values=(0.20, 0.60, 0.95),
        v_values=(0.0, np.pi, 2.0 * np.pi),
    )

    sample = atlas.law_at(dome, 0.60, np.pi)
    assert sample.C8.shape == (8, 8)


def test_sphere_ellipsoid_and_cone_surface_examples() -> None:
    wall = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
    field = ConstantWallField(wall)

    sphere = Sphere(radius=96.0)
    sphere_wall = field.law_at(sphere, 0.60, np.pi)
    assert sphere_wall.frame.label == "sphere"

    ellipsoid = Ellipsoid(a=84.0, b=96.0, c=72.0)
    atlas = WallAtlas.from_field(
        ellipsoid,
        field,
        u_values=(0.30, 0.70),
        v_values=(0.0, np.pi),
    )
    ellipsoid_wall = atlas.law_at(ellipsoid, 0.50, 0.50 * np.pi)
    assert ellipsoid_wall.C8.shape == (8, 8)

    frustum = ConicalFrustum(radius_start=80.0, radius_end=96.0, length=120.0)
    point = frustum.point_at(60.0, 0.0)
    context = ValidityContext(
        characteristic_height=0.50,
        pitch=8.0,
        min_radius=point.min_radius,
        response_length=80.0,
    )
    assert context.min_radius == point.min_radius


def test_sp8007_data_prep_and_serialization_example() -> None:
    result = _orthogrid_result()
    surface = Cylinder(radius=120.0, length=300.0)
    sp8007 = _sp8007_orthotropic_coefficients(result.law)

    report = {
        "radius": surface.radius,
        "length": surface.length,
        "sp8007": sp8007,
        "transverse_shear": {
            "Abar_xz": result.law.As[0, 0],
            "Abar_yz": result.law.As[1, 1],
        },
        "h_over_R": result.validity.h_over_R,
        "p_over_R": result.validity.p_over_R,
        "p_over_L_response": result.validity.p_over_L_response,
        "warnings": result.validity.warnings,
    }

    artifact = to_yaml(
        result,
        units={"length": "in", "force": "lbf", "stress": "psi"},
    )
    loaded = from_yaml(artifact)

    assert isinstance(loaded, HomogenizationResult)
    assert loaded.law.C8.shape == (8, 8)
    assert report["sp8007"]["Ebar_x"] == result.law.A[0, 0]
    assert report["sp8007"]["Dbar_xy"] == 2.0 * result.law.D[0, 1] + 4.0 * result.law.D[2, 2]
    assert report["p_over_R"] == 8.0 / 120.0
