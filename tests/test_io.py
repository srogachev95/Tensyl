from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from tensyl import (
    ABDStiffness,
    BeamSection,
    EnergyHomogenizer,
    HomogenizationResult,
    IsotropicMaterial,
    ValidityContext,
    ValidityReport,
    isotropic_plate,
    unidirectional_cell,
)
from tensyl.io import (
    SCHEMA_VERSION,
    SchemaError,
    from_json,
    from_schema,
    from_yaml,
    read_json,
    read_yaml,
    to_json,
    to_schema,
    to_yaml,
    write_json,
    write_yaml,
)

FIXTURE_DIR = Path(__file__).parent / "data" / "external_workflows"


def _stiffness() -> ABDStiffness:
    validity = ValidityReport(
        h_over_R=0.01,
        p_over_R=0.02,
        p_over_L_response=None,
        coupling_ratios={"B_fro": 0.03},
        warnings=("review_scale_separation",),
    )
    return ABDStiffness(
        A=np.diag([10.0, 12.0, 3.0]),
        B=np.diag([1.0, 2.0, 0.5]),
        D=np.diag([5.0, 6.0, 1.5]),
        As=np.diag([4.0, 4.5]),
        areal_mass=2.7,
        metadata={"source": "unit_test", "tags": ("alpha", "beta")},
        validity=validity,
    )


def _result() -> HomogenizationResult:
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


def _assert_stiffness_matches(loaded: ABDStiffness, expected: ABDStiffness) -> None:
    np.testing.assert_allclose(loaded.C8, expected.C8)
    assert loaded.frame == expected.frame
    assert loaded.convention == expected.convention
    assert loaded.areal_mass == expected.areal_mass
    assert loaded.metadata["source"] == expected.metadata["source"]
    assert loaded.metadata["tags"] == ["alpha", "beta"]
    assert loaded.validity == expected.validity


def _assert_result_matches(
    loaded: HomogenizationResult | ABDStiffness,
    expected: HomogenizationResult,
) -> None:
    assert isinstance(loaded, HomogenizationResult)
    np.testing.assert_allclose(loaded.stiffness.C8, expected.stiffness.C8)
    assert loaded.validity == expected.validity
    assert loaded.stiffness.validity == loaded.validity
    assert loaded.source == expected.source
    assert loaded.assumptions == expected.assumptions
    assert loaded.diagnostics["symmetric"] is True
    assert loaded.diagnostics["source_equations"] == ["Nemeth 2011 eqs. 30-39"]


def test_abd_stiffness_round_trips_through_yaml() -> None:
    stiffness = _stiffness()
    text = to_yaml(stiffness, units={"length": "m", "force": "N", "mass": "kg"})

    loaded = from_yaml(text)

    assert isinstance(loaded, ABDStiffness)
    _assert_stiffness_matches(loaded, stiffness)


def test_abd_stiffness_round_trips_through_json() -> None:
    stiffness = _stiffness()
    text = to_json(stiffness, units={"length": "m", "force": "N", "mass": "kg"})

    loaded = from_json(text)

    assert text.endswith("\n")
    assert json.loads(text)["schema_version"] == SCHEMA_VERSION
    assert isinstance(loaded, ABDStiffness)
    _assert_stiffness_matches(loaded, stiffness)


def test_homogenization_result_round_trips_through_yaml() -> None:
    result = _result()

    loaded = from_yaml(to_yaml(result))

    _assert_result_matches(loaded, result)


def test_homogenization_result_round_trips_through_json() -> None:
    result = _result()

    loaded = from_json(to_json(result))

    _assert_result_matches(loaded, result)


def test_yaml_file_round_trip(tmp_path) -> None:
    path = tmp_path / "stiffness.yaml"
    stiffness = _stiffness()

    write_yaml(stiffness, path)
    loaded = read_yaml(path)

    assert isinstance(loaded, ABDStiffness)
    np.testing.assert_allclose(loaded.C8, stiffness.C8)


def test_json_file_round_trip(tmp_path) -> None:
    path = tmp_path / "stiffness.json"
    stiffness = _stiffness()

    write_json(stiffness, path)
    loaded = read_json(path)

    assert path.read_text(encoding="utf-8").endswith("\n")
    assert isinstance(loaded, ABDStiffness)
    np.testing.assert_allclose(loaded.C8, stiffness.C8)


@pytest.mark.parametrize(
    ("key", "value", "match"),
    [
        ("schema_version", SCHEMA_VERSION + 1, "schema_version: Input should be 2"),
        ("artifact_type", "nastran_property", "artifact_type: Input should be"),
        ("schema_name", "other.schema", "schema_name: Input should be"),
    ],
)
def test_schema_rejects_unsupported_root_fields(key: str, value: object, match: str) -> None:
    payload = to_schema(_stiffness())
    payload[key] = value

    with pytest.raises(SchemaError, match=match):
        from_schema(payload)


def test_schema_rejects_extra_fields() -> None:
    payload = to_schema(_stiffness())
    payload["unexpected"] = True

    with pytest.raises(SchemaError, match="unexpected: Extra inputs are not permitted"):
        from_schema(payload)


def test_schema_rejects_bad_tangent_shape() -> None:
    payload = to_schema(_stiffness())
    payload["payload"]["tangent_c8"] = [[1.0]]

    with pytest.raises(SchemaError, match="C8 must have 8 rows"):
        from_schema(payload)


def test_schema_rejects_nonfinite_values() -> None:
    payload = to_schema(_stiffness())
    payload["payload"]["tangent_c8"][0][0] = float("nan")

    with pytest.raises(SchemaError, match="C8\\[0\\]\\[\\] must be finite"):
        from_schema(payload)


def test_schema_rejects_non_yaml_compatible_metadata() -> None:
    stiffness = ABDStiffness(
        A=np.eye(3),
        B=np.zeros((3, 3)),
        D=np.eye(3),
        As=np.eye(2),
        metadata={"array": np.array([1.0, 2.0])},
    )

    with pytest.raises(SchemaError, match="metadata.array is not YAML-schema compatible"):
        to_schema(stiffness)


def test_yaml_loader_rejects_unsafe_tags_and_non_mapping_roots() -> None:
    with pytest.raises(SchemaError, match="invalid YAML payload"):
        from_yaml("!!python/object/apply:os.system ['echo unsafe']")

    with pytest.raises(SchemaError, match="YAML root must be a mapping"):
        from_yaml("- not\n- a\n- mapping\n")


def test_json_loader_rejects_invalid_json_and_non_mapping_roots() -> None:
    with pytest.raises(SchemaError, match="invalid JSON payload"):
        from_json("{")

    with pytest.raises(SchemaError, match="JSON root must be a mapping"):
        from_json('["not", "a", "mapping"]')


def test_json_loader_rejects_nonfinite_constants() -> None:
    payload = to_schema(_stiffness())
    payload["payload"]["tangent_c8"][0][0] = float("nan")

    with pytest.raises(SchemaError, match="invalid JSON payload"):
        from_json(json.dumps(payload))


def test_json_loader_rejects_schema_errors() -> None:
    payload = to_schema(_stiffness())
    payload["artifact_type"] = "nastran_property"

    with pytest.raises(SchemaError, match="artifact_type: Input should be"):
        from_json(json.dumps(payload))


@pytest.mark.parametrize(
    "filename",
    [
        "v2_abd_stiffness.yaml",
        "v2_abd_stiffness.json",
    ],
)
def test_v2_abd_stiffness_fixtures_load(filename: str) -> None:
    path = FIXTURE_DIR / filename
    loaded = read_yaml(path) if path.suffix == ".yaml" else read_json(path)

    assert isinstance(loaded, ABDStiffness)
    _assert_stiffness_matches(loaded, _stiffness())


@pytest.mark.parametrize(
    "filename",
    [
        "v2_homogenization_result.yaml",
        "v2_homogenization_result.json",
    ],
)
def test_v2_homogenization_result_fixtures_load(filename: str) -> None:
    path = FIXTURE_DIR / filename
    loaded = read_yaml(path) if path.suffix == ".yaml" else read_json(path)

    _assert_result_matches(loaded, _result())
