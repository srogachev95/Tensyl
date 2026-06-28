import numpy as np

from tensyl import (
    ABDAtlas,
    BeamSection,
    ConicalFrustum,
    ConstantStiffnessField,
    Cylinder,
    Ellipsoid,
    EnergyHomogenizer,
    HomogenizationResult,
    IsotropicMaterial,
    OrthotropicPlyMaterial,
    Ply,
    Sphere,
    SphericalCap,
    ValidityContext,
    equilateral_isogrid_cell,
    isotropic_plate,
    laminate_plate,
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


def _sp8007_orthotropic_coefficients(stiffness, *, tolerance=1.0e-9):
    unsupported = {
        "A16": stiffness.A[0, 2],
        "A26": stiffness.A[1, 2],
        "B16": stiffness.B[0, 2],
        "B26": stiffness.B[1, 2],
        "B61": stiffness.B[2, 0],
        "B62": stiffness.B[2, 1],
        "D16": stiffness.D[0, 2],
        "D26": stiffness.D[1, 2],
    }
    nonzero = {name: value for name, value in unsupported.items() if abs(value) > tolerance}
    if nonzero:
        msg = (
            "SP-8007 orthotropic-cylinder coefficients assume axial/circumferential "
            f"orthotropy; unsupported coupling terms are nonzero: {nonzero}"
        )
        raise ValueError(msg)

    return {
        "Ebar_x": stiffness.A[0, 0],
        "Ebar_y": stiffness.A[1, 1],
        "Ebar_xy": stiffness.A[0, 1],
        "Gbar_xy": stiffness.A[2, 2],
        "Dbar_x": stiffness.D[0, 0],
        "Dbar_y": stiffness.D[1, 1],
        "Dbar_xy": 2.0 * stiffness.D[0, 1] + 4.0 * stiffness.D[2, 2],
        "Cbar_x": stiffness.B[0, 0],
        "Cbar_y": stiffness.B[1, 1],
        "Cbar_xy": stiffness.B[0, 1],
        "Kbar_xy": stiffness.B[2, 2],
    }


def test_first_abd_stiffness_example() -> None:
    stiffness = isotropic_plate(
        IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
        thickness=0.080,
    )

    assert stiffness.A.shape == (3, 3)
    assert stiffness.B.shape == (3, 3)
    assert stiffness.D.shape == (3, 3)
    assert stiffness.As.shape == (2, 2)
    assert np.max(np.abs(stiffness.B)) == 0.0


def test_first_homogenized_cell_and_result_interpretation_examples() -> None:
    result = _orthogrid_result()

    assert result.stiffness.C8.shape == (8, 8)
    assert result.stiffness.validity == result.validity
    assert result.diagnostics["symmetric"]
    assert result.diagnostics["positive_semidefinite"]
    assert result.diagnostics["rank"] == 8
    assert np.isclose(result.stiffness.A[0, 0], 1.4849661467100587e6)
    assert np.isclose(result.stiffness.B[0, 0], 2.4e5)
    assert "membrane_bending_coupling_exceeds_threshold" in result.validity.warnings


def test_stiffened_barrel_example() -> None:
    result = _orthogrid_result()
    surface = Cylinder(radius=120.0, length=300.0)
    field = ConstantStiffnessField(result.stiffness)
    stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

    assert stiffness_at_midbay.frame.label == "cylinder"
    assert result.validity.p_over_R == 8.0 / 120.0


def test_stiffened_dome_concept_example() -> None:
    dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
    stiffness = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
    field = ConstantStiffnessField(stiffness)

    atlas = ABDAtlas.from_field(
        dome,
        field,
        u_values=(0.20, 0.60, 0.95),
        v_values=(0.0, np.pi, 2.0 * np.pi),
    )

    sample = atlas.stiffness_at(dome, 0.60, np.pi)
    assert sample.C8.shape == (8, 8)


def test_sphere_ellipsoid_and_cone_surface_examples() -> None:
    stiffness = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
    field = ConstantStiffnessField(stiffness)

    sphere = Sphere(radius=96.0)
    sphere_stiffness = field.stiffness_at(sphere, 0.60, np.pi)
    assert sphere_stiffness.frame.label == "sphere"

    ellipsoid = Ellipsoid(a=84.0, b=96.0, c=72.0)
    atlas = ABDAtlas.from_field(
        ellipsoid,
        field,
        u_values=(0.30, 0.70),
        v_values=(0.0, np.pi),
    )
    ellipsoid_stiffness = atlas.stiffness_at(ellipsoid, 0.50, 0.50 * np.pi)
    assert ellipsoid_stiffness.C8.shape == (8, 8)

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
    sp8007 = _sp8007_orthotropic_coefficients(result.stiffness)

    report = {
        "radius": surface.radius,
        "length": surface.length,
        "sp8007": sp8007,
        "transverse_shear": {
            "Abar_xz": result.stiffness.As[0, 0],
            "Abar_yz": result.stiffness.As[1, 1],
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
    assert loaded.stiffness.C8.shape == (8, 8)
    assert report["sp8007"]["Ebar_x"] == result.stiffness.A[0, 0]
    assert (
        report["sp8007"]["Dbar_xy"]
        == 2.0 * result.stiffness.D[0, 1] + 4.0 * result.stiffness.D[2, 2]
    )
    assert report["p_over_R"] == 8.0 / 120.0


def test_sp8007_isogrid_data_prep_example() -> None:
    isogrid_skin = isotropic_plate(
        IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
        thickness=0.060,
    )
    isogrid_section = BeamSection(
        EA=2.8e6,
        EIy=1.8e4,
        EIz=5.2e3,
        GJ=3.2e3,
        kGAy=0.9e6,
        kGAz=0.7e6,
    )
    isogrid_cell = equilateral_isogrid_cell(
        skin=isogrid_skin,
        member_section=isogrid_section,
        pitch=6.0,
        eccentricity=0.35,
    )
    isogrid_result = EnergyHomogenizer().compute(
        isogrid_cell,
        validity_context=ValidityContext(
            characteristic_height=0.42,
            pitch=6.0,
            min_radius=120.0,
            response_length=80.0,
        ),
    )
    isogrid_sp8007 = _sp8007_orthotropic_coefficients(isogrid_result.stiffness)

    assert abs(isogrid_sp8007["Ebar_x"] - isogrid_sp8007["Ebar_y"]) < 1.0e-6
    assert abs(isogrid_sp8007["Cbar_x"] - isogrid_sp8007["Cbar_y"]) < 1.0e-6


def test_sp8007_symmetric_laminate_data_prep_example() -> None:
    surface = Cylinder(radius=120.0, length=300.0)
    carbon_epoxy = OrthotropicPlyMaterial(
        E1=18.0e6,
        E2=1.4e6,
        G12=0.75e6,
        nu12=0.28,
        G13=0.75e6,
        G23=0.50e6,
        density=0.058,
    )
    laminate_stiffness = laminate_plate(
        (
            Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
            Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.5 * np.pi),
            Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.5 * np.pi),
            Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
        )
    )
    laminate_sp8007 = _sp8007_orthotropic_coefficients(laminate_stiffness)
    laminate_report = {
        "radius": surface.radius,
        "length": surface.length,
        "sp8007": laminate_sp8007,
        "transverse_shear": {
            "Abar_xz": laminate_stiffness.As[0, 0],
            "Abar_yz": laminate_stiffness.As[1, 1],
        },
    }

    assert abs(laminate_report["sp8007"]["Cbar_x"]) < 1.0e-9
    assert abs(laminate_report["sp8007"]["Cbar_y"]) < 1.0e-9
