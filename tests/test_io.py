from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    LinearABDWall,
    ValidityContext,
    ValidityReport,
    isotropic_plate,
    unidirectional_cell,
)
from tensyl.io import (
    SCHEMA_VERSION,
    SchemaError,
    from_schema,
    from_yaml,
    read_yaml,
    to_schema,
    to_yaml,
    write_yaml,
)


def _wall() -> LinearABDWall:
    validity = ValidityReport(
        h_over_R=0.01,
        p_over_R=0.02,
        p_over_L_response=None,
        coupling_ratios={"B_fro": 0.03},
        warnings=("review_scale_separation",),
    )
    return LinearABDWall(
        A=np.diag([10.0, 12.0, 3.0]),
        B=np.diag([1.0, 2.0, 0.5]),
        D=np.diag([5.0, 6.0, 1.5]),
        As=np.diag([4.0, 4.5]),
        areal_mass=2.7,
        metadata={"source": "unit_test", "tags": ("alpha", "beta")},
        validity=validity,
    )


def _result():
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
    section = BeamSection(
        EA=1200.0,
        EIy=50.0,
        EIz=30.0,
        GJ=20.0,
        kGAy=400.0,
        kGAz=300.0,
    )
    cell = unidirectional_cell(
        skin=skin,
        member_section=section,
        spacing=0.8,
        eccentricity=0.04,
    )
    return EnergyHomogenizer().compute(
        cell,
        validity_context=ValidityContext(
            characteristic_height=0.04,
            pitch=0.8,
            min_radius=20.0,
            response_length=10.0,
        ),
    )


def test_linear_wall_round_trips_through_yaml() -> None:
    wall = _wall()
    text = to_yaml(wall, units={"length": "m", "force": "N", "mass": "kg"})

    loaded = from_yaml(text)

    assert isinstance(loaded, LinearABDWall)
    np.testing.assert_allclose(loaded.C8, wall.C8)
    assert loaded.frame == wall.frame
    assert loaded.convention == wall.convention
    assert loaded.areal_mass == wall.areal_mass
    assert loaded.metadata["source"] == "unit_test"
    assert loaded.metadata["tags"] == ["alpha", "beta"]
    assert loaded.validity == wall.validity


def test_homogenization_result_round_trips_through_yaml() -> None:
    result = _result()

    loaded = from_yaml(to_yaml(result))

    assert not isinstance(loaded, LinearABDWall)
    np.testing.assert_allclose(loaded.law.C8, result.law.C8)
    assert loaded.validity == result.validity
    assert loaded.law.validity == loaded.validity
    assert loaded.source == result.source
    assert loaded.assumptions == result.assumptions
    assert loaded.diagnostics["symmetric"] is True
    assert loaded.diagnostics["source_equations"] == ["Nemeth 2011 eqs. 30-39"]


def test_yaml_file_round_trip(tmp_path) -> None:
    path = tmp_path / "wall.yaml"
    wall = _wall()

    write_yaml(wall, path)
    loaded = read_yaml(path)

    assert isinstance(loaded, LinearABDWall)
    np.testing.assert_allclose(loaded.C8, wall.C8)


@pytest.mark.parametrize(
    ("key", "value", "match"),
    [
        ("schema_version", SCHEMA_VERSION + 1, "schema_version: Input should be 1"),
        ("artifact_type", "nastran_property", "artifact_type: Input should be"),
        ("schema_name", "other.schema", "schema_name: Input should be"),
    ],
)
def test_schema_rejects_unsupported_root_fields(key: str, value: object, match: str) -> None:
    payload = to_schema(_wall())
    payload[key] = value

    with pytest.raises(SchemaError, match=match):
        from_schema(payload)


def test_schema_rejects_extra_fields() -> None:
    payload = to_schema(_wall())
    payload["unexpected"] = True

    with pytest.raises(SchemaError, match="unexpected: Extra inputs are not permitted"):
        from_schema(payload)


def test_schema_rejects_bad_tangent_shape() -> None:
    payload = to_schema(_wall())
    payload["payload"]["tangent_c8"] = [[1.0]]

    with pytest.raises(SchemaError, match="C8 must have 8 rows"):
        from_schema(payload)


def test_schema_rejects_nonfinite_values() -> None:
    payload = to_schema(_wall())
    payload["payload"]["tangent_c8"][0][0] = float("nan")

    with pytest.raises(SchemaError, match="C8\\[0\\]\\[\\] must be finite"):
        from_schema(payload)


def test_schema_rejects_non_yaml_compatible_metadata() -> None:
    wall = LinearABDWall(
        A=np.eye(3),
        B=np.zeros((3, 3)),
        D=np.eye(3),
        As=np.eye(2),
        metadata={"array": np.array([1.0, 2.0])},
    )

    with pytest.raises(SchemaError, match="metadata.array is not YAML-schema compatible"):
        to_schema(wall)


def test_yaml_loader_rejects_unsafe_tags_and_non_mapping_roots() -> None:
    with pytest.raises(SchemaError, match="invalid YAML payload"):
        from_yaml("!!python/object/apply:os.system ['echo unsafe']")

    with pytest.raises(SchemaError, match="YAML root must be a mapping"):
        from_yaml("- not\n- a\n- mapping\n")
