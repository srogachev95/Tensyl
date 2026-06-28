"""Versioned solver-neutral schema for external workflows."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from os import PathLike
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from tensyl._version import tensyl_version
from tensyl.core.constitutive import ABDStiffness
from tensyl.core.conventions import Frame2D, StrainConvention
from tensyl.homogenizers import HomogenizationResult, ValidityReport
from tensyl.typing import FloatArray

SCHEMA_NAME = "tensyl.external_workflow"
SCHEMA_VERSION = 2

type SchemaName = Literal["tensyl.external_workflow"]
type SchemaVersion = Literal[2]
type ArtifactType = Literal["abd_stiffness", "homogenization_result"]
type HomogenizationSource = Literal["energy", "direct_ec", "rve", "imported"]
type PlainYaml = None | str | bool | int | float | list[PlainYaml] | dict[str, PlainYaml]


class SchemaError(ValueError):
    """Raised when a Tensyl external-workflow payload is malformed."""


class _SchemaModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


def _validation_error(exc: ValidationError) -> SchemaError:
    message = "; ".join(
        f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors()
    )
    if not message:
        message = "invalid schema payload."
    return SchemaError(message)


def _plain_yaml_value(value: Any, *, path: str) -> PlainYaml:
    if value is None or isinstance(value, (str, bool)):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return int(value)
    if isinstance(value, float):
        if not np.isfinite(value):
            msg = f"{path} must be finite."
            raise ValueError(msg)
        return value
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        checked = float(value)
        if not np.isfinite(checked):
            msg = f"{path} must be finite."
            raise ValueError(msg)
        return checked
    if isinstance(value, Mapping):
        result: dict[str, PlainYaml] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                msg = f"{path} mapping keys must be strings."
                raise ValueError(msg)
            result[key] = _plain_yaml_value(item, path=f"{path}.{key}")
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_plain_yaml_value(item, path=f"{path}[]") for item in value]
    msg = f"{path} is not YAML-schema compatible."
    raise ValueError(msg)


def _plain_yaml_mapping(
    value: Mapping[str, Any] | None,
    *,
    path: str,
) -> dict[str, PlainYaml] | None:
    if value is None:
        return None
    return cast(dict[str, PlainYaml], _plain_yaml_value(value, path=path))


def _finite_float(value: Any, *, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        msg = f"{path} must be a finite number."
        raise ValueError(msg)
    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{path} must be finite."
        raise ValueError(msg)
    return checked


def _finite_vector(value: Any, *, length: int, path: str) -> list[float]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        msg = f"{path} must be a sequence."
        raise ValueError(msg)
    if len(value) != length:
        msg = f"{path} must have length {length}."
        raise ValueError(msg)
    return [_finite_float(item, path=f"{path}[]") for item in value]


def _finite_matrix(value: Any, *, shape: tuple[int, int], path: str) -> list[list[float]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        msg = f"{path} must be a sequence of rows."
        raise ValueError(msg)
    rows, cols = shape
    if len(value) != rows:
        msg = f"{path} must have {rows} rows."
        raise ValueError(msg)
    return [
        _finite_vector(row, length=cols, path=f"{path}[{index}]") for index, row in enumerate(value)
    ]


def _as_array(values: Sequence[float] | Sequence[Sequence[float]]) -> FloatArray:
    return np.array(values, dtype=np.float64)


class ProducerSchema(_SchemaModel):
    name: str
    version: str

    @classmethod
    def from_tensyl(cls) -> ProducerSchema:
        return cls(name="tensyl", version=tensyl_version())


class FrameSchema(_SchemaModel):
    e1: list[float]
    e2: list[float]
    n: list[float]
    label: str

    @field_validator("e1", "e2", "n", mode="before")
    @classmethod
    def _validate_vector(cls, value: Any) -> list[float]:
        return _finite_vector(value, length=3, path="frame vector")

    @classmethod
    def from_tensyl(cls, frame: Frame2D) -> FrameSchema:
        return cls(
            e1=frame.e1.tolist(),
            e2=frame.e2.tolist(),
            n=frame.n.tolist(),
            label=frame.label,
        )

    def to_tensyl(self) -> Frame2D:
        return Frame2D(
            e1=_as_array(self.e1),
            e2=_as_array(self.e2),
            n=_as_array(self.n),
            label=self.label,
        )


class StrainConventionSchema(_SchemaModel):
    membrane_order: tuple[str, str, str]
    bending_order: tuple[str, str, str]
    shear_order: tuple[str, str]
    engineering_shear: bool
    reference_surface: str
    normal_positive: str

    @classmethod
    def from_tensyl(cls, convention: StrainConvention) -> StrainConventionSchema:
        return cls(
            membrane_order=convention.membrane_order,
            bending_order=convention.bending_order,
            shear_order=convention.shear_order,
            engineering_shear=convention.engineering_shear,
            reference_surface=convention.reference_surface,
            normal_positive=convention.normal_positive,
        )

    def to_tensyl(self) -> StrainConvention:
        return StrainConvention(
            membrane_order=self.membrane_order,
            bending_order=self.bending_order,
            shear_order=self.shear_order,
            engineering_shear=self.engineering_shear,
            reference_surface=self.reference_surface,
            normal_positive=self.normal_positive,
        )


class ValidityReportSchema(_SchemaModel):
    h_over_R: float | None = Field(default=None, allow_inf_nan=False)
    p_over_R: float | None = Field(default=None, allow_inf_nan=False)
    p_over_L_response: float | None = Field(default=None, allow_inf_nan=False)
    coupling_ratios: dict[str, float]
    warnings: tuple[str, ...]

    @field_validator("h_over_R", "p_over_R", "p_over_L_response", mode="before")
    @classmethod
    def _validate_optional_float(cls, value: Any) -> float | None:
        if value is None:
            return None
        return _finite_float(value, path="validity ratio")

    @field_validator("coupling_ratios", mode="before")
    @classmethod
    def _validate_coupling_ratios(cls, value: Any) -> dict[str, float]:
        if not isinstance(value, Mapping):
            msg = "coupling_ratios must be a mapping."
            raise ValueError(msg)
        return {
            str(key): _finite_float(item, path=f"coupling_ratios.{key}")
            for key, item in value.items()
        }

    @classmethod
    def from_tensyl(cls, validity: ValidityReport) -> ValidityReportSchema:
        return cls(
            h_over_R=validity.h_over_R,
            p_over_R=validity.p_over_R,
            p_over_L_response=validity.p_over_L_response,
            coupling_ratios=dict(validity.coupling_ratios),
            warnings=validity.warnings,
        )

    def to_tensyl(self) -> ValidityReport:
        return ValidityReport(
            h_over_R=self.h_over_R,
            p_over_R=self.p_over_R,
            p_over_L_response=self.p_over_L_response,
            coupling_ratios=self.coupling_ratios,
            warnings=self.warnings,
        )


class ABDStiffnessSchema(_SchemaModel):
    tangent_c8: list[list[float]]
    frame: FrameSchema
    strain_convention: StrainConventionSchema
    areal_mass: float | None = Field(default=None, allow_inf_nan=False)
    metadata: dict[str, PlainYaml]
    validity: ValidityReportSchema | None

    @field_validator("tangent_c8", mode="before")
    @classmethod
    def _validate_tangent(cls, value: Any) -> list[list[float]]:
        return _finite_matrix(value, shape=(8, 8), path="C8")

    @field_validator("areal_mass", mode="before")
    @classmethod
    def _validate_optional_areal_mass(cls, value: Any) -> float | None:
        if value is None:
            return None
        return _finite_float(value, path="areal_mass")

    @field_validator("metadata", mode="before")
    @classmethod
    def _validate_metadata(cls, value: Any) -> dict[str, PlainYaml]:
        checked = _plain_yaml_mapping(value, path="metadata")
        return {} if checked is None else checked

    @classmethod
    def from_tensyl(cls, stiffness: ABDStiffness) -> ABDStiffnessSchema:
        if stiffness.validity is not None and not isinstance(stiffness.validity, ValidityReport):
            msg = "validity must be None or a ValidityReport for schema export."
            raise SchemaError(msg)
        return cls(
            tangent_c8=stiffness.C8.tolist(),
            frame=FrameSchema.from_tensyl(stiffness.frame),
            strain_convention=StrainConventionSchema.from_tensyl(stiffness.convention),
            areal_mass=stiffness.areal_mass,
            metadata=cast(
                dict[str, PlainYaml], _plain_yaml_value(stiffness.metadata, path="metadata")
            ),
            validity=(
                None
                if stiffness.validity is None
                else ValidityReportSchema.from_tensyl(stiffness.validity)
            ),
        )

    def to_tensyl(self) -> ABDStiffness:
        return ABDStiffness.from_tangent(
            _as_array(self.tangent_c8),
            frame=self.frame.to_tensyl(),
            convention=self.strain_convention.to_tensyl(),
            areal_mass=self.areal_mass,
            metadata=self.metadata,
            validity=None if self.validity is None else self.validity.to_tensyl(),
        )


class HomogenizationResultSchema(_SchemaModel):
    stiffness: ABDStiffnessSchema
    validity: ValidityReportSchema
    diagnostics: dict[str, PlainYaml]
    assumptions: tuple[str, ...]
    source: HomogenizationSource

    @field_validator("diagnostics", mode="before")
    @classmethod
    def _validate_diagnostics(cls, value: Any) -> dict[str, PlainYaml]:
        checked = _plain_yaml_mapping(value, path="diagnostics")
        return {} if checked is None else checked

    @model_validator(mode="after")
    def _validate_stiffness_validity(self) -> HomogenizationResultSchema:
        if self.stiffness.validity is not None and self.stiffness.validity != self.validity:
            msg = "homogenization_result stiffness validity does not match result validity."
            raise ValueError(msg)
        return self

    @classmethod
    def from_tensyl(cls, result: HomogenizationResult) -> HomogenizationResultSchema:
        return cls(
            stiffness=ABDStiffnessSchema.from_tensyl(result.stiffness),
            validity=ValidityReportSchema.from_tensyl(result.validity),
            diagnostics=cast(
                dict[str, PlainYaml],
                _plain_yaml_value(result.diagnostics, path="diagnostics"),
            ),
            assumptions=result.assumptions,
            source=result.source,
        )

    def to_tensyl(self) -> HomogenizationResult:
        validity = self.validity.to_tensyl()
        stiffness = self.stiffness.to_tensyl()
        return HomogenizationResult(
            stiffness=stiffness.with_validity(validity),
            validity=validity,
            diagnostics=self.diagnostics,
            assumptions=self.assumptions,
            source=self.source,
        )


class ExternalWorkflowEnvelope(_SchemaModel):
    schema_name: SchemaName
    schema_version: SchemaVersion
    artifact_type: ArtifactType
    producer: ProducerSchema
    units: dict[str, PlainYaml] | None = None
    payload: ABDStiffnessSchema | HomogenizationResultSchema

    @field_validator("units", mode="before")
    @classmethod
    def _validate_units(cls, value: Any) -> dict[str, PlainYaml] | None:
        return _plain_yaml_mapping(value, path="units")

    @model_validator(mode="after")
    def _validate_artifact_payload(self) -> ExternalWorkflowEnvelope:
        if self.artifact_type == "abd_stiffness" and not isinstance(
            self.payload, ABDStiffnessSchema
        ):
            msg = "abd_stiffness artifact requires an ABDStiffness payload."
            raise ValueError(msg)
        if self.artifact_type == "homogenization_result" and not isinstance(
            self.payload, HomogenizationResultSchema
        ):
            msg = "homogenization_result artifact requires a HomogenizationResult payload."
            raise ValueError(msg)
        return self

    @classmethod
    def from_tensyl(
        cls,
        obj: ABDStiffness | HomogenizationResult,
        *,
        units: Mapping[str, Any] | None = None,
    ) -> ExternalWorkflowEnvelope:
        if isinstance(obj, HomogenizationResult):
            artifact_type: ArtifactType = "homogenization_result"
            payload: ABDStiffnessSchema | HomogenizationResultSchema = (
                HomogenizationResultSchema.from_tensyl(obj)
            )
        elif isinstance(obj, ABDStiffness):
            artifact_type = "abd_stiffness"
            payload = ABDStiffnessSchema.from_tensyl(obj)
        else:
            msg = f"unsupported schema object type {type(obj).__name__!r}."
            raise SchemaError(msg)

        return cls(
            schema_name=SCHEMA_NAME,
            schema_version=SCHEMA_VERSION,
            artifact_type=artifact_type,
            producer=ProducerSchema.from_tensyl(),
            units=_plain_yaml_mapping(units, path="units"),
            payload=payload,
        )

    def to_tensyl(self) -> ABDStiffness | HomogenizationResult:
        if self.artifact_type == "abd_stiffness" and isinstance(self.payload, ABDStiffnessSchema):
            return self.payload.to_tensyl()
        if self.artifact_type == "homogenization_result" and isinstance(
            self.payload, HomogenizationResultSchema
        ):
            return self.payload.to_tensyl()
        msg = "artifact type and payload are inconsistent."
        raise SchemaError(msg)


def _model_dump(model: BaseModel) -> dict[str, Any]:
    return model.model_dump(mode="json")


def to_schema(
    obj: ABDStiffness | HomogenizationResult,
    *,
    units: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a versioned solver-neutral schema payload for ``obj``."""

    try:
        return _model_dump(ExternalWorkflowEnvelope.from_tensyl(obj, units=units))
    except ValidationError as exc:
        raise _validation_error(exc) from exc
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def from_schema(payload: Mapping[str, Any]) -> ABDStiffness | HomogenizationResult:
    """Reconstruct a Tensyl object from a versioned solver-neutral schema payload."""

    try:
        return ExternalWorkflowEnvelope.model_validate(payload).to_tensyl()
    except ValidationError as exc:
        raise _validation_error(exc) from exc
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def to_yaml(
    obj: ABDStiffness | HomogenizationResult,
    *,
    units: Mapping[str, Any] | None = None,
) -> str:
    """Serialize ``obj`` to a safe YAML string."""

    return yaml.safe_dump(to_schema(obj, units=units), sort_keys=False)


def to_json(
    obj: ABDStiffness | HomogenizationResult,
    *,
    units: Mapping[str, Any] | None = None,
) -> str:
    """Serialize ``obj`` to a deterministic JSON string."""

    try:
        return json.dumps(to_schema(obj, units=units), indent=2, allow_nan=False) + "\n"
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def from_yaml(text: str) -> ABDStiffness | HomogenizationResult:
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


def _reject_json_constant(value: str) -> None:
    msg = f"invalid JSON constant {value!r}."
    raise ValueError(msg)


def from_json(text: str) -> ABDStiffness | HomogenizationResult:
    """Load a Tensyl object from a JSON string."""

    try:
        payload = json.loads(text, parse_constant=_reject_json_constant)
    except (json.JSONDecodeError, ValueError) as exc:
        msg = "invalid JSON payload."
        raise SchemaError(msg) from exc
    if not isinstance(payload, Mapping):
        msg = "JSON root must be a mapping."
        raise SchemaError(msg)
    return from_schema(payload)


def write_yaml(
    obj: ABDStiffness | HomogenizationResult,
    path: str | PathLike[str],
    *,
    units: Mapping[str, Any] | None = None,
) -> None:
    """Write ``obj`` to ``path`` as safe YAML."""

    Path(path).write_text(to_yaml(obj, units=units), encoding="utf-8")


def write_json(
    obj: ABDStiffness | HomogenizationResult,
    path: str | PathLike[str],
    *,
    units: Mapping[str, Any] | None = None,
) -> None:
    """Write ``obj`` to ``path`` as JSON."""

    Path(path).write_text(to_json(obj, units=units), encoding="utf-8")


def read_yaml(path: str | PathLike[str]) -> ABDStiffness | HomogenizationResult:
    """Read a Tensyl object from a safe YAML file."""

    return from_yaml(Path(path).read_text(encoding="utf-8"))


def read_json(path: str | PathLike[str]) -> ABDStiffness | HomogenizationResult:
    """Read a Tensyl object from a JSON file."""

    return from_json(Path(path).read_text(encoding="utf-8"))


__all__ = [
    "SCHEMA_NAME",
    "SCHEMA_VERSION",
    "SchemaError",
    "from_json",
    "from_schema",
    "from_yaml",
    "read_json",
    "read_yaml",
    "to_json",
    "to_schema",
    "to_yaml",
    "write_json",
    "write_yaml",
]
