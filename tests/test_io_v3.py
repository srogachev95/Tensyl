from __future__ import annotations

import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from tensyl import (
    ABDAtlas,
    BeamSection,
    CanonicalUnitCell,
    ConicalFrustum,
    ConstantStiffnessField,
    Cylinder,
    Ellipsoid,
    EnergyHomogenizer,
    FlatPlate,
    IsotropicMaterial,
    Sphere,
    SphericalCap,
    ThermalResultants,
    isotropic_plate,
    unidirectional_cell,
)
from tensyl.geometry import Surface
from tensyl.io import SchemaError, from_json, from_schema, from_yaml, to_json, to_schema, to_yaml


def _cell() -> CanonicalUnitCell:
    return unidirectional_cell(
        skin=isotropic_plate(IsotropicMaterial(E=100, nu=0.3, density=2), 0.1),
        member_section=BeamSection(
            EA=10, EIy=2, EIz=3, GJ=1, thermal_expansion=1e-5, mass_per_length=0.4
        ),
        spacing=2,
        axial_eccentricity=0.2,
    )


def test_v3_cell_round_trip_retains_inputs_geometry_and_recomputed_result() -> None:
    cell = _cell()
    payload = to_schema(cell)
    assert payload["schema_version"] == 3
    assert payload["artifact_type"] == "canonical_unit_cell"
    for restored in (from_schema(payload), from_json(to_json(cell)), from_yaml(to_yaml(cell))):
        assert isinstance(restored, CanonicalUnitCell)
        assert restored.skin == cell.skin
        assert restored.members == cell.members
        assert restored.geometry == cell.geometry
        np.testing.assert_array_equal(
            EnergyHomogenizer().compute(restored).stiffness.C8,
            EnergyHomogenizer().compute(cell).stiffness.C8,
        )
        assert to_schema(restored) == payload

    without_drawing = replace(cell, geometry=None)
    assert to_schema(from_json(to_json(without_drawing))) == to_schema(without_drawing)


@pytest.mark.parametrize(
    "surface",
    [
        FlatPlate(),
        Cylinder(2),
        Sphere(2),
        SphericalCap(2),
        ConicalFrustum(2, 3, 4),
        Ellipsoid(2, 3, 4),
    ],
)
def test_v3_atlas_round_trip_on_every_builtin_surface(surface: Surface) -> None:
    atlas = ABDAtlas.from_field(
        surface,
        ConstantStiffnessField(_cell().skin, orientation_rad=0.2),
        u_values=(0.2, 0.4),
        v_values=(0.3, 0.5),
    )
    restored = from_json(to_json(atlas))
    assert isinstance(restored, ABDAtlas)
    assert restored.metadata["sample_digest"] == atlas.metadata["sample_digest"]
    np.testing.assert_array_equal(
        restored.stiffness_at(restored.surface, 0.3, 0.4).C8,
        atlas.stiffness_at(surface, 0.3, 0.4).C8,
    )
    assert to_schema(restored) == to_schema(atlas)


def test_v3_thermal_round_trip() -> None:
    thermal = ThermalResultants(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])).rotate(0.3)
    assert from_yaml(to_yaml(thermal)) == thermal
    assert from_json(to_json(thermal)) == thermal


def test_v2_is_readable_but_cannot_claim_new_artifact_types() -> None:
    payload = to_schema(_cell().skin)
    payload["schema_version"] = 2
    restored = from_schema(payload)
    assert restored == _cell().skin
    assert to_schema(restored)["schema_version"] == 3
    payload = to_schema(_cell())
    payload["schema_version"] = 2
    with pytest.raises(SchemaError, match="version 2"):
        from_schema(payload)


def test_cell_schema_refuses_unknown_fields_bad_numbers_and_indices() -> None:
    base = to_schema(_cell())
    malformed = []
    payload = deepcopy(base)
    payload["payload"]["members"][0]["section"]["EA"] = True
    malformed.append(payload)
    payload = deepcopy(base)
    payload["payload"]["members"][0]["section"]["surprise"] = 5
    malformed.append(payload)
    payload = deepcopy(base)
    payload["payload"]["geometry"]["edges"][0]["start"] = 999
    malformed.append(payload)
    for payload in malformed:
        with pytest.raises(SchemaError):
            from_schema(payload)


def test_atlas_schema_refuses_stale_digest_and_unknown_surface_parameters() -> None:
    atlas = ABDAtlas.from_field(
        FlatPlate(), ConstantStiffnessField(_cell().skin), u_values=(0, 1), v_values=(0, 1)
    )
    payload = to_schema(atlas)
    payload["payload"]["stiffnesses"][0][0]["tangent_c8"][0][0] += 1
    with pytest.raises(SchemaError, match="digest"):
        from_schema(payload)
    payload = to_schema(atlas)
    payload["payload"]["surface"]["parameters"]["radius"] = 1
    with pytest.raises(SchemaError, match="parameters"):
        from_schema(payload)


def test_atlas_schema_revalidates_grid_shape_and_sample_frame() -> None:
    atlas = ABDAtlas.from_field(
        FlatPlate(), ConstantStiffnessField(_cell().skin), u_values=(0, 1), v_values=(0, 1)
    )
    payload = to_schema(atlas)
    payload["payload"]["u_values"] = [0, 0]
    with pytest.raises(SchemaError, match="increasing"):
        from_schema(payload)
    payload = to_schema(atlas)
    payload["payload"]["stiffnesses"].pop()
    with pytest.raises(SchemaError, match="shape"):
        from_schema(payload)
    payload = to_schema(atlas)
    payload["payload"]["stiffnesses"][0][0]["frame"]["e1"] = [0, 1, 0]
    payload["payload"]["stiffnesses"][0][0]["frame"]["e2"] = [-1, 0, 0]
    with pytest.raises(SchemaError, match="frame"):
        from_schema(payload)


def test_v3_frozen_artifacts_remain_readable() -> None:
    root = Path(__file__).parent / "data" / "external_workflows"
    for name in ("canonical_unit_cell", "abd_atlas", "thermal_resultants"):
        payload = json.loads((root / f"v3_{name}.json").read_text())
        restored = from_schema(payload)
        assert to_schema(restored)["payload"] == payload["payload"]


def test_custom_surface_is_refused_instead_of_losing_its_behavior() -> None:
    class CustomPlate(FlatPlate):
        pass

    atlas = ABDAtlas.from_field(
        CustomPlate(), ConstantStiffnessField(_cell().skin), u_values=(0, 1), v_values=(0, 1)
    )
    with pytest.raises(SchemaError, match="Unsupported atlas surface"):
        to_schema(atlas)
