"""Versioned solver-neutral YAML schema for external workflows."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version
from os import PathLike
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np
import yaml

from tensyl.core.constitutive import LinearABDWall
from tensyl.core.conventions import Frame2D, StrainConvention
from tensyl.homogenizers import HomogenizationResult, ValidityReport
from tensyl.typing import FloatArray

SCHEMA_NAME = "tensyl.external_workflow"
SCHEMA_VERSION = 1

_SUPPORTED_ARTIFACTS = {"linear_abd_wall", "homogenization_result"}
_SUPPORTED_SOURCES = {"energy", "direct_ec", "rve", "imported"}


class SchemaError(ValueError):
    """Raised when a Tensyl external-workflow payload is malformed."""


def _tensyl_version() -> str:
    try:
        return version("tensyl")
    except PackageNotFoundError:  # pragma: no cover - editable tree before install
        return "0.0.0"


def _plain_value(value: Any, *, path: str) -> Any:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        if not np.isfinite(value):
            msg = f"{path} must be finite."
            raise SchemaError(msg)
        return value
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        checked = float(value)
        if not np.isfinite(checked):
            msg = f"{path} must be finite."
            raise SchemaError(msg)
        return checked
    if isinstance(value, Mapping):
        result: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                msg = f"{path} mapping keys must be strings."
                raise SchemaError(msg)
            result[key] = _plain_value(item, path=f"{path}.{key}")
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_plain_value(item, path=f"{path}[]") for item in value]
    msg = f"{path} is not YAML-schema compatible."
    raise SchemaError(msg)


def _mapping(value: Any, *, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        msg = f"{name} must be a mapping."
        raise SchemaError(msg)
    return value


def _required(mapping: Mapping[str, Any], key: str, *, name: str) -> Any:
    if key not in mapping:
        msg = f"{name} is missing required key {key!r}."
        raise SchemaError(msg)
    return mapping[key]


def _string(value: Any, *, name: str) -> str:
    if not isinstance(value, str):
        msg = f"{name} must be a string."
        raise SchemaError(msg)
    return value


def _optional_string(value: Any, *, name: str) -> str | None:
    if value is None:
        return None
    return _string(value, name=name)


def _float(value: Any, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        msg = f"{name} must be a finite number."
        raise SchemaError(msg)
    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{name} must be finite."
        raise SchemaError(msg)
    return checked


def _optional_float(value: Any, *, name: str) -> float | None:
    if value is None:
        return None
    return _float(value, name=name)


def _float_vector(value: Any, *, length: int, name: str) -> FloatArray:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        msg = f"{name} must be a sequence."
        raise SchemaError(msg)
    if len(value) != length:
        msg = f"{name} must have length {length}."
        raise SchemaError(msg)
    return np.array([_float(item, name=f"{name}[]") for item in value], dtype=np.float64)


def _float_matrix(value: Any, *, shape: tuple[int, int], name: str) -> FloatArray:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        msg = f"{name} must be a sequence of rows."
        raise SchemaError(msg)
    rows, cols = shape
    if len(value) != rows:
        msg = f"{name} must have {rows} rows."
        raise SchemaError(msg)
    matrix = []
    for index, row in enumerate(value):
        matrix.append(_float_vector(row, length=cols, name=f"{name}[{index}]"))
    return np.array(matrix, dtype=np.float64)


def _frame_to_schema(frame: Frame2D) -> dict[str, Any]:
    return {
        "e1": frame.e1.tolist(),
        "e2": frame.e2.tolist(),
        "n": frame.n.tolist(),
        "label": frame.label,
    }


def _frame_from_schema(value: Any) -> Frame2D:
    payload = _mapping(value, name="frame")
    return Frame2D(
        e1=_float_vector(_required(payload, "e1", name="frame"), length=3, name="frame.e1"),
        e2=_float_vector(_required(payload, "e2", name="frame"), length=3, name="frame.e2"),
        n=_float_vector(_required(payload, "n", name="frame"), length=3, name="frame.n"),
        label=_string(_required(payload, "label", name="frame"), name="frame.label"),
    )


def _convention_to_schema(convention: StrainConvention) -> dict[str, Any]:
    return {
        "membrane_order": list(convention.membrane_order),
        "bending_order": list(convention.bending_order),
        "shear_order": list(convention.shear_order),
        "engineering_shear": convention.engineering_shear,
        "reference_surface": convention.reference_surface,
        "normal_positive": convention.normal_positive,
    }


def _string_tuple(value: Any, *, name: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        msg = f"{name} must be a sequence of strings."
        raise SchemaError(msg)
    return tuple(_string(item, name=f"{name}[]") for item in value)


def _string_tuple3(value: Any, *, name: str) -> tuple[str, str, str]:
    items = _string_tuple(value, name=name)
    if len(items) != 3:
        msg = f"{name} must have length 3."
        raise SchemaError(msg)
    return items


def _string_tuple2(value: Any, *, name: str) -> tuple[str, str]:
    items = _string_tuple(value, name=name)
    if len(items) != 2:
        msg = f"{name} must have length 2."
        raise SchemaError(msg)
    return items


def _convention_from_schema(value: Any) -> StrainConvention:
    payload = _mapping(value, name="strain_convention")
    engineering_shear = _required(payload, "engineering_shear", name="strain_convention")
    if not isinstance(engineering_shear, bool):
        msg = "strain_convention.engineering_shear must be a boolean."
        raise SchemaError(msg)
    return StrainConvention(
        membrane_order=_string_tuple3(
            _required(payload, "membrane_order", name="strain_convention"),
            name="strain_convention.membrane_order",
        ),
        bending_order=_string_tuple3(
            _required(payload, "bending_order", name="strain_convention"),
            name="strain_convention.bending_order",
        ),
        shear_order=_string_tuple2(
            _required(payload, "shear_order", name="strain_convention"),
            name="strain_convention.shear_order",
        ),
        engineering_shear=engineering_shear,
        reference_surface=_string(
            _required(payload, "reference_surface", name="strain_convention"),
            name="strain_convention.reference_surface",
        ),
        normal_positive=_string(
            _required(payload, "normal_positive", name="strain_convention"),
            name="strain_convention.normal_positive",
        ),
    )


def _validity_to_schema(validity: Any) -> dict[str, Any] | None:
    if validity is None:
        return None
    if not isinstance(validity, ValidityReport):
        msg = "validity must be None or a ValidityReport for schema export."
        raise SchemaError(msg)
    return {
        "h_over_R": validity.h_over_R,
        "p_over_R": validity.p_over_R,
        "p_over_L_response": validity.p_over_L_response,
        "coupling_ratios": _plain_value(validity.coupling_ratios, path="validity.coupling_ratios"),
        "warnings": list(validity.warnings),
    }


def _validity_from_schema(value: Any) -> ValidityReport | None:
    if value is None:
        return None
    payload = _mapping(value, name="validity")
    coupling_ratios = _mapping(
        _required(payload, "coupling_ratios", name="validity"),
        name="validity.coupling_ratios",
    )
    return ValidityReport(
        h_over_R=_optional_float(
            _required(payload, "h_over_R", name="validity"), name="validity.h_over_R"
        ),
        p_over_R=_optional_float(
            _required(payload, "p_over_R", name="validity"), name="validity.p_over_R"
        ),
        p_over_L_response=_optional_float(
            _required(payload, "p_over_L_response", name="validity"),
            name="validity.p_over_L_response",
        ),
        coupling_ratios={
            _string(key, name="validity.coupling_ratios key"): _float(
                item, name=f"validity.coupling_ratios.{key}"
            )
            for key, item in coupling_ratios.items()
        },
        warnings=_string_tuple(
            _required(payload, "warnings", name="validity"), name="validity.warnings"
        ),
    )


def _wall_to_payload(wall: LinearABDWall) -> dict[str, Any]:
    return {
        "tangent_c8": wall.C8.tolist(),
        "frame": _frame_to_schema(wall.frame),
        "strain_convention": _convention_to_schema(wall.convention),
        "areal_mass": wall.areal_mass,
        "metadata": _plain_value(wall.metadata, path="metadata"),
        "validity": _validity_to_schema(wall.validity),
    }


def _wall_from_payload(value: Any) -> LinearABDWall:
    payload = _mapping(value, name="payload")
    return LinearABDWall.from_tangent(
        _float_matrix(_required(payload, "tangent_c8", name="payload"), shape=(8, 8), name="C8"),
        frame=_frame_from_schema(_required(payload, "frame", name="payload")),
        convention=_convention_from_schema(_required(payload, "strain_convention", name="payload")),
        areal_mass=_optional_float(
            _required(payload, "areal_mass", name="payload"),
            name="areal_mass",
        ),
        metadata=_mapping(_required(payload, "metadata", name="payload"), name="metadata"),
        validity=_validity_from_schema(_required(payload, "validity", name="payload")),
    )


def _result_to_payload(result: HomogenizationResult) -> dict[str, Any]:
    return {
        "law": _wall_to_payload(result.law),
        "validity": _validity_to_schema(result.validity),
        "diagnostics": _plain_value(result.diagnostics, path="diagnostics"),
        "assumptions": list(result.assumptions),
        "source": result.source,
    }


def _result_from_payload(value: Any) -> HomogenizationResult:
    payload = _mapping(value, name="payload")
    validity = _validity_from_schema(_required(payload, "validity", name="payload"))
    if validity is None:
        msg = "homogenization_result validity must not be null."
        raise SchemaError(msg)
    law = _wall_from_payload(_required(payload, "law", name="payload"))
    if law.validity is not None and law.validity != validity:
        msg = "homogenization_result law validity does not match result validity."
        raise SchemaError(msg)
    source = _string(_required(payload, "source", name="payload"), name="source")
    if source not in _SUPPORTED_SOURCES:
        msg = f"unsupported homogenization source {source!r}."
        raise SchemaError(msg)
    diagnostics = _plain_value(
        _mapping(_required(payload, "diagnostics", name="payload"), name="diagnostics"),
        path="diagnostics",
    )
    assumptions = _string_tuple(
        _required(payload, "assumptions", name="payload"), name="assumptions"
    )
    return HomogenizationResult(
        law=law.with_validity(validity),
        validity=validity,
        diagnostics=diagnostics,
        assumptions=assumptions,
        source=cast(Literal["energy", "direct_ec", "rve", "imported"], source),
    )


def to_schema(
    obj: LinearABDWall | HomogenizationResult,
    *,
    units: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a versioned solver-neutral schema payload for ``obj``."""

    if isinstance(obj, HomogenizationResult):
        artifact_type = "homogenization_result"
        payload = _result_to_payload(obj)
    elif isinstance(obj, LinearABDWall):
        artifact_type = "linear_abd_wall"
        payload = _wall_to_payload(obj)
    else:
        msg = f"unsupported schema object type {type(obj).__name__!r}."
        raise SchemaError(msg)

    return {
        "schema_name": SCHEMA_NAME,
        "schema_version": SCHEMA_VERSION,
        "artifact_type": artifact_type,
        "producer": {"name": "tensyl", "version": _tensyl_version()},
        "units": None if units is None else _plain_value(units, path="units"),
        "payload": payload,
    }


def from_schema(payload: Mapping[str, Any]) -> LinearABDWall | HomogenizationResult:
    """Reconstruct a Tensyl object from a versioned solver-neutral schema payload."""

    root = _mapping(payload, name="schema")
    schema_name = _string(_required(root, "schema_name", name="schema"), name="schema_name")
    if schema_name != SCHEMA_NAME:
        msg = f"unsupported schema_name {schema_name!r}."
        raise SchemaError(msg)
    schema_version = _required(root, "schema_version", name="schema")
    if schema_version != SCHEMA_VERSION:
        msg = f"unsupported schema_version {schema_version!r}."
        raise SchemaError(msg)
    artifact_type = _string(_required(root, "artifact_type", name="schema"), name="artifact_type")
    if artifact_type not in _SUPPORTED_ARTIFACTS:
        msg = f"unsupported artifact_type {artifact_type!r}."
        raise SchemaError(msg)

    _mapping(_required(root, "producer", name="schema"), name="producer")
    units = _required(root, "units", name="schema")
    if units is not None:
        _plain_value(_mapping(units, name="units"), path="units")

    artifact_payload = _required(root, "payload", name="schema")
    if artifact_type == "linear_abd_wall":
        return _wall_from_payload(artifact_payload)
    return _result_from_payload(artifact_payload)


def to_yaml(
    obj: LinearABDWall | HomogenizationResult,
    *,
    units: Mapping[str, Any] | None = None,
) -> str:
    """Serialize ``obj`` to a safe YAML string."""

    return yaml.safe_dump(to_schema(obj, units=units), sort_keys=False)


def from_yaml(text: str) -> LinearABDWall | HomogenizationResult:
    """Load a Tensyl object from a safe YAML string."""

    try:
        payload = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        msg = "invalid YAML payload."
        raise SchemaError(msg) from exc
    if not isinstance(payload, Mapping):
        msg = "YAML root must be a mapping."
        raise SchemaError(msg)
    return from_schema(payload)


def write_yaml(
    obj: LinearABDWall | HomogenizationResult,
    path: str | PathLike[str],
    *,
    units: Mapping[str, Any] | None = None,
) -> None:
    """Write ``obj`` to ``path`` as safe YAML."""

    Path(path).write_text(to_yaml(obj, units=units), encoding="utf-8")


def read_yaml(path: str | PathLike[str]) -> LinearABDWall | HomogenizationResult:
    """Read a Tensyl object from a safe YAML file."""

    return from_yaml(Path(path).read_text(encoding="utf-8"))


__all__ = [
    "SCHEMA_NAME",
    "SCHEMA_VERSION",
    "SchemaError",
    "from_schema",
    "from_yaml",
    "read_yaml",
    "to_schema",
    "to_yaml",
    "write_yaml",
]
