import numpy as np

from tensyl import (
    BeamSection,
    ConstantWallField,
    Cylinder,
    EnergyHomogenizer,
    HomogenizationResult,
    IsotropicMaterial,
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


def test_sp8007_data_prep_and_serialization_example() -> None:
    result = _orthogrid_result()
    surface = Cylinder(radius=120.0, length=300.0)

    report = {
        "radius": surface.radius,
        "length": surface.length,
        "A11": result.law.A[0, 0],
        "B11": result.law.B[0, 0],
        "D11": result.law.D[0, 0],
        "As11": result.law.As[0, 0],
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
    assert report["p_over_R"] == 8.0 / 120.0
