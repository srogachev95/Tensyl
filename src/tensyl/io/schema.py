"""Versioned solver-neutral schema for external workflows."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import fields
from os import PathLike
from pathlib import Path
from typing import Annotated, Any, Literal, cast

import numpy as np
import yaml
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from tensyl._version import tensyl_version
from tensyl.cells import (
    BeamMember,
    CanonicalUnitCell,
    CellGeometry,
    CellGeometryEdge,
    CellNode,
    CellVector,
)
from tensyl.core.constitutive import ABDStiffness
from tensyl.core.conventions import Frame2D, StrainConvention
from tensyl.core.thermal import ThermalResultants
from tensyl.core.typing import FloatArray
from tensyl.fields import ABDAtlas
from tensyl.geometry import (
    ConicalFrustum,
    Cylinder,
    Ellipsoid,
    FlatPlate,
    Sphere,
    SphericalCap,
    Surface,
)
from tensyl.homogenizers import HomogenizationResult, ValidityReport
from tensyl.sections import BeamSection

SCHEMA_NAME = "tensyl.external_workflow"
SCHEMA_VERSION = 3

type SchemaName = Literal["tensyl.external_workflow"]
type SchemaVersion = Literal[2, 3]
type ArtifactType = Literal[
    "abd_stiffness",
    "homogenization_result",
    "canonical_unit_cell",
    "abd_atlas",
    "thermal_resultants",
]
type WorkflowObject = (
    ABDStiffness | HomogenizationResult | CanonicalUnitCell | ABDAtlas | ThermalResultants
)
type HomogenizationSource = Literal["energy", "direct_ec", "rve", "imported"]
type PlainYaml = None | str | bool | int | float | list[PlainYaml] | dict[str, PlainYaml]


class SchemaError(ValueError):
    """Raised when an external-workflow payload is malformed."""


class _SchemaModel(BaseModel):
    # External artifacts should fail loudly when they carry unexpected keys.
    # That keeps schema drift visible instead of quietly dropping data.
    model_config = ConfigDict(extra="forbid")


def _validation_error(exc: ValidationError) -> SchemaError:
    # Pydantic's nested error objects are precise but noisy for callers. Flatten
    # them into one stable SchemaError message with field paths intact.
    message = "; ".join(
        f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors()
    )
    if not message:
        message = "invalid schema payload."
    return SchemaError(message)


def _plain_yaml_value(value: Any, *, path: str) -> PlainYaml:
    # Only plain JSON/YAML scalars, lists, and string-keyed mappings are allowed
    # in metadata-like fields. This keeps artifacts safe-YAML compatible and
    # solver-neutral.
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
    # bool is an int subclass in Python, but accepting True as 1.0 in mechanics
    # data would be a very unhelpful kind of permissive.
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
    """Serialized local right-handed frame."""

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
    """Serialized generalized strain/resultant ordering and sign convention."""

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
    """Serialized tangent-plane validity ratios and warning codes."""

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
    """Serialized linear ABD stiffness using Tensyl's canonical C8 tangent."""

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
            # Keep the external boundary explicit even for objects supplied
            # by callers outside the typed constructor path.
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
    """Serialized homogenization result plus attached validity and diagnostics."""

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
            # Result validity is duplicated intentionally so downstream tools
            # can read either the result envelope or the stiffness payload. They
            # must agree when both are present.
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


def _mechanics_number(value: Any) -> float:
    return _finite_float(value, path="mechanics value")


type MechanicsNumber = Annotated[float, BeforeValidator(_mechanics_number)]
type Index = Annotated[int, Field(strict=True, ge=0)]


class _MetadataSchema(_SchemaModel):
    metadata: dict[str, PlainYaml]

    @field_validator("metadata", mode="before")
    @classmethod
    def _validate_metadata(cls, value: Any) -> dict[str, PlainYaml]:
        checked = _plain_yaml_mapping(value, path="metadata")
        return {} if checked is None else checked


class BeamSectionSchema(_MetadataSchema):
    EA: MechanicsNumber
    EIy: MechanicsNumber
    EIz: MechanicsNumber
    GJ: MechanicsNumber
    kGAy: MechanicsNumber | None
    kGAz: MechanicsNumber | None
    EIyz: MechanicsNumber
    mass_per_length: MechanicsNumber | None
    thermal_expansion: MechanicsNumber | None

    @classmethod
    def from_tensyl(cls, section: BeamSection) -> BeamSectionSchema:
        return cls(**{name: getattr(section, name) for name in cls.model_fields})

    def to_tensyl(self) -> BeamSection:
        return BeamSection(**self.model_dump())


class BeamMemberSchema(_SchemaModel):
    section: BeamSectionSchema
    length: MechanicsNumber
    angle_rad: MechanicsNumber
    axial_eccentricity: MechanicsNumber
    shear_eccentricity: MechanicsNumber
    multiplicity: MechanicsNumber
    label: str

    @classmethod
    def from_tensyl(cls, member: BeamMember) -> BeamMemberSchema:
        values = {name: getattr(member, name) for name in cls.model_fields}
        values["section"] = BeamSectionSchema.from_tensyl(member.section)
        return cls(**values)

    def to_tensyl(self) -> BeamMember:
        return BeamMember(
            section=self.section.to_tensyl(),
            length=self.length,
            angle_rad=self.angle_rad,
            axial_eccentricity=self.axial_eccentricity,
            shear_eccentricity=self.shear_eccentricity,
            multiplicity=self.multiplicity,
            label=self.label,
        )


class CellNodeSchema(_SchemaModel):
    e1: MechanicsNumber
    e2: MechanicsNumber
    label: str


class CellVectorSchema(_SchemaModel):
    e1: MechanicsNumber
    e2: MechanicsNumber


class CellGeometryEdgeSchema(_SchemaModel):
    start: Index
    end: Index
    family: str
    label: str


class CellGeometrySchema(_SchemaModel):
    nodes: tuple[CellNodeSchema, ...]
    edges: tuple[CellGeometryEdgeSchema, ...]
    repeat_vectors: tuple[CellVectorSchema, CellVectorSchema]
    boundary: tuple[Index, ...]

    @classmethod
    def from_tensyl(cls, geometry: CellGeometry) -> CellGeometrySchema:
        return cls(
            nodes=tuple(CellNodeSchema(e1=n.e1, e2=n.e2, label=n.label) for n in geometry.nodes),
            edges=tuple(
                CellGeometryEdgeSchema(start=e.start, end=e.end, family=e.family, label=e.label)
                for e in geometry.edges
            ),
            repeat_vectors=(
                CellVectorSchema(
                    e1=geometry.repeat_vectors[0].e1, e2=geometry.repeat_vectors[0].e2
                ),
                CellVectorSchema(
                    e1=geometry.repeat_vectors[1].e1, e2=geometry.repeat_vectors[1].e2
                ),
            ),
            boundary=geometry.boundary,
        )

    def to_tensyl(self) -> CellGeometry:
        return CellGeometry(
            nodes=tuple(CellNode(**node.model_dump()) for node in self.nodes),
            edges=tuple(CellGeometryEdge(**edge.model_dump()) for edge in self.edges),
            repeat_vectors=(
                CellVector(**self.repeat_vectors[0].model_dump()),
                CellVector(**self.repeat_vectors[1].model_dump()),
            ),
            boundary=self.boundary,
        )


class CanonicalUnitCellSchema(_MetadataSchema):
    area: MechanicsNumber
    skin: ABDStiffnessSchema
    members: tuple[BeamMemberSchema, ...]
    frame: FrameSchema
    strain_convention: StrainConventionSchema
    geometry: CellGeometrySchema | None

    @classmethod
    def from_tensyl(cls, cell: CanonicalUnitCell) -> CanonicalUnitCellSchema:
        return cls(
            area=cell.area,
            skin=ABDStiffnessSchema.from_tensyl(cell.skin),
            members=tuple(BeamMemberSchema.from_tensyl(m) for m in cell.members),
            frame=FrameSchema.from_tensyl(cell.frame),
            strain_convention=StrainConventionSchema.from_tensyl(cell.convention),
            geometry=None
            if cell.geometry is None
            else CellGeometrySchema.from_tensyl(cell.geometry),
            metadata=dict(cell.metadata),
        )

    def to_tensyl(self) -> CanonicalUnitCell:
        return CanonicalUnitCell(
            area=self.area,
            skin=self.skin.to_tensyl(),
            members=tuple(m.to_tensyl() for m in self.members),
            frame=self.frame.to_tensyl(),
            convention=self.strain_convention.to_tensyl(),
            geometry=None if self.geometry is None else self.geometry.to_tensyl(),
            metadata=self.metadata,
        )


_SURFACE_TYPES = {
    "flat_plate": FlatPlate,
    "cylinder": Cylinder,
    "sphere": Sphere,
    "spherical_cap": SphericalCap,
    "conical_frustum": ConicalFrustum,
    "ellipsoid": Ellipsoid,
}


class SurfaceSchema(_SchemaModel):
    """Finite built-in geometry parameters; no executable factories."""

    kind: Literal[
        "flat_plate", "cylinder", "sphere", "spherical_cap", "conical_frustum", "ellipsoid"
    ]
    parameters: dict[str, Any]

    @model_validator(mode="after")
    def _validate_parameters(self) -> SurfaceSchema:
        expected = {f.name for f in fields(_SURFACE_TYPES[self.kind])}
        if set(self.parameters) != expected:
            raise ValueError(f"Surface parameters for {self.kind} must be {sorted(expected)}.")
        for name, value in self.parameters.items():
            if name == "label":
                if not isinstance(value, str):
                    raise ValueError("Surface label must be a string.")
            elif name in ("origin", "e1", "e2"):
                _finite_vector(value, length=3, path=name)
            elif value is None and self.kind == "cylinder" and name == "length":
                continue
            else:
                _finite_float(value, path=name)
        return self

    @classmethod
    def from_tensyl(cls, surface: Surface) -> SurfaceSchema:
        for kind, surface_type in _SURFACE_TYPES.items():
            if type(surface) is surface_type:
                values = {f.name: getattr(surface, f.name) for f in fields(surface_type)}
                values = {
                    k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in values.items()
                }
                return cls.model_validate({"kind": kind, "parameters": values})
        raise SchemaError(f"Unsupported atlas surface type {type(surface).__name__!r}.")

    def to_tensyl(self) -> Surface:
        return _SURFACE_TYPES[self.kind](**self.parameters)


class ABDAtlasSchema(_MetadataSchema):
    surface: SurfaceSchema
    u_values: tuple[MechanicsNumber, ...]
    v_values: tuple[MechanicsNumber, ...]
    stiffnesses: tuple[tuple[ABDStiffnessSchema, ...], ...]

    @classmethod
    def from_tensyl(cls, atlas: ABDAtlas) -> ABDAtlasSchema:
        return cls(
            surface=SurfaceSchema.from_tensyl(atlas.surface),
            u_values=atlas.u_values,
            v_values=atlas.v_values,
            stiffnesses=tuple(
                tuple(ABDStiffnessSchema.from_tensyl(s) for s in row) for row in atlas.stiffnesses
            ),
            metadata=dict(atlas.metadata),
        )

    def to_tensyl(self) -> ABDAtlas:
        atlas = ABDAtlas(
            surface=self.surface.to_tensyl(),
            u_values=self.u_values,
            v_values=self.v_values,
            stiffnesses=tuple(tuple(s.to_tensyl() for s in row) for row in self.stiffnesses),
            metadata=self.metadata,
        )
        recorded = self.metadata.get("sample_digest")
        if recorded is not None and recorded != atlas.metadata["sample_digest"]:
            raise SchemaError("Atlas sample_digest does not match its numeric samples.")
        return atlas


class ThermalResultantsSchema(_SchemaModel):
    N_T: list[float]
    M_T: list[float]
    frame: FrameSchema
    strain_convention: StrainConventionSchema

    @field_validator("N_T", "M_T", mode="before")
    @classmethod
    def _validate_vector(cls, value: Any) -> list[float]:
        return _finite_vector(value, length=3, path="thermal resultant")

    @classmethod
    def from_tensyl(cls, result: ThermalResultants) -> ThermalResultantsSchema:
        return cls(
            N_T=result.N_T.tolist(),
            M_T=result.M_T.tolist(),
            frame=FrameSchema.from_tensyl(result.frame),
            strain_convention=StrainConventionSchema.from_tensyl(result.convention),
        )

    def to_tensyl(self) -> ThermalResultants:
        return ThermalResultants(
            _as_array(self.N_T),
            _as_array(self.M_T),
            self.frame.to_tensyl(),
            self.strain_convention.to_tensyl(),
        )


type WorkflowPayload = (
    ABDStiffnessSchema
    | HomogenizationResultSchema
    | CanonicalUnitCellSchema
    | ABDAtlasSchema
    | ThermalResultantsSchema
)


class ExternalWorkflowEnvelope(_SchemaModel):
    """Versioned top-level envelope for solver-neutral workflow artifacts."""

    schema_name: SchemaName
    schema_version: SchemaVersion
    artifact_type: ArtifactType
    producer: ProducerSchema
    units: dict[str, PlainYaml] | None = None
    payload: WorkflowPayload

    @field_validator("units", mode="before")
    @classmethod
    def _validate_units(cls, value: Any) -> dict[str, PlainYaml] | None:
        return _plain_yaml_mapping(value, path="units")

    @model_validator(mode="after")
    def _validate_artifact_payload(self) -> ExternalWorkflowEnvelope:
        expected = {
            "abd_stiffness": ABDStiffnessSchema,
            "homogenization_result": HomogenizationResultSchema,
            "canonical_unit_cell": CanonicalUnitCellSchema,
            "abd_atlas": ABDAtlasSchema,
            "thermal_resultants": ThermalResultantsSchema,
        }
        if self.schema_version == 2 and self.artifact_type not in (
            "abd_stiffness",
            "homogenization_result",
        ):
            raise ValueError(
                "Schema version 2 supports only stiffness and homogenization result artifacts."
            )
        if not isinstance(self.payload, expected[self.artifact_type]):
            raise ValueError(
                f"{self.artifact_type} artifact requires an "
                f"{expected[self.artifact_type].__name__} payload."
            )
        return self

    @classmethod
    def from_tensyl(
        cls,
        obj: WorkflowObject,
        *,
        units: Mapping[str, Any] | None = None,
    ) -> ExternalWorkflowEnvelope:
        if isinstance(obj, HomogenizationResult):
            # Preserve the result envelope when it exists; exporting only the
            # stiffness would orphan diagnostics and validity context.
            artifact_type: ArtifactType = "homogenization_result"
            payload: WorkflowPayload = HomogenizationResultSchema.from_tensyl(obj)
        elif isinstance(obj, ABDStiffness):
            artifact_type = "abd_stiffness"
            payload = ABDStiffnessSchema.from_tensyl(obj)
        elif isinstance(obj, CanonicalUnitCell):
            artifact_type = "canonical_unit_cell"
            payload = CanonicalUnitCellSchema.from_tensyl(obj)
        elif isinstance(obj, ABDAtlas):
            artifact_type = "abd_atlas"
            payload = ABDAtlasSchema.from_tensyl(obj)
        elif isinstance(obj, ThermalResultants):
            artifact_type = "thermal_resultants"
            payload = ThermalResultantsSchema.from_tensyl(obj)
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

    def to_tensyl(self) -> WorkflowObject:
        return self.payload.to_tensyl()


def _model_dump(model: BaseModel) -> dict[str, Any]:
    # JSON mode normalizes tuples and constrained values into plain containers
    # before YAML or JSON serialization sees them.
    return model.model_dump(mode="json")


def to_schema(
    obj: WorkflowObject,
    *,
    units: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a versioned solver-neutral schema payload.

    Args:
        obj: Stiffness, homogenization result, canonical cell, atlas, or thermal loads.
        units: Optional plain mapping describing the unit system. Tensyl stores
            these values as metadata; it does not convert units.

    Returns:
        Plain Python mapping compatible with JSON and safe YAML.

    Raises:
        SchemaError: If the object cannot be represented by the external
            workflow schema.
    """

    try:
        return _model_dump(ExternalWorkflowEnvelope.from_tensyl(obj, units=units))
    except ValidationError as exc:
        raise _validation_error(exc) from exc
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def from_schema(payload: Mapping[str, Any]) -> WorkflowObject:
    """Reconstruct a Tensyl object from a schema payload.

    Args:
        payload: Versioned external-workflow mapping.

    Returns:
        The stiffness, result, cell, atlas, or thermal loads described by the payload.

    Raises:
        SchemaError: If the payload is missing required fields, has unexpected
            fields, or violates schema validation.
    """

    try:
        return ExternalWorkflowEnvelope.model_validate(payload).to_tensyl()
    except ValidationError as exc:
        raise _validation_error(exc) from exc
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def to_yaml(
    obj: WorkflowObject,
    *,
    units: Mapping[str, Any] | None = None,
) -> str:
    """Serialize an object to a safe YAML string.

    Args:
        obj: Stiffness, homogenization result, canonical cell, atlas, or thermal loads.
        units: Optional plain mapping describing the unit system.

    Returns:
        Safe-YAML text containing the versioned schema payload.

    Raises:
        SchemaError: If the object cannot be represented by the schema.
    """

    return yaml.safe_dump(to_schema(obj, units=units), sort_keys=False)


def to_json(
    obj: WorkflowObject,
    *,
    units: Mapping[str, Any] | None = None,
) -> str:
    """Serialize an object to deterministic JSON text.

    Args:
        obj: Stiffness, homogenization result, canonical cell, atlas, or thermal loads.
        units: Optional plain mapping describing the unit system.

    Returns:
        Pretty-printed JSON text with a trailing newline.

    Raises:
        SchemaError: If the object cannot be represented by the schema or would
            require non-finite JSON constants.
    """

    try:
        return json.dumps(to_schema(obj, units=units), indent=2, allow_nan=False) + "\n"
    except ValueError as exc:
        raise SchemaError(str(exc)) from exc


def from_yaml(text: str) -> WorkflowObject:
    """Load a Tensyl object from a safe YAML string.

    Args:
        text: YAML text containing a versioned external-workflow mapping.

    Returns:
        The stiffness, result, cell, atlas, or thermal loads described by the payload.

    Raises:
        SchemaError: If the YAML is invalid, unsafe, not a mapping, or fails
            schema validation.
    """

    try:
        # safe_load rejects executable YAML tags; schema validation then checks
        # the resulting plain data structure.
        payload = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        msg = "invalid YAML payload."
        raise SchemaError(msg) from exc
    if not isinstance(payload, Mapping):
        msg = "YAML root must be a mapping."
        raise SchemaError(msg)
    return from_schema(payload)


def _reject_json_constant(value: str) -> None:
    # json.loads accepts NaN/Infinity by default. External artifacts should not.
    msg = f"invalid JSON constant {value!r}."
    raise ValueError(msg)


def from_json(text: str) -> WorkflowObject:
    """Load a Tensyl object from a JSON string.

    Args:
        text: JSON text containing a versioned external-workflow mapping.

    Returns:
        The stiffness, result, cell, atlas, or thermal loads described by the payload.

    Raises:
        SchemaError: If the JSON is invalid, contains NaN or infinity, is not a
            mapping, or fails schema validation.
    """

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
    obj: WorkflowObject,
    path: str | PathLike[str],
    *,
    units: Mapping[str, Any] | None = None,
) -> None:
    """Write an object to a safe YAML file.

    Args:
        obj: Stiffness, homogenization result, canonical cell, atlas, or thermal loads.
        path: Destination file path.
        units: Optional plain mapping describing the unit system.

    Raises:
        SchemaError: If the object cannot be represented by the schema.
        OSError: If the file cannot be written.
    """

    Path(path).write_text(to_yaml(obj, units=units), encoding="utf-8")


def write_json(
    obj: WorkflowObject,
    path: str | PathLike[str],
    *,
    units: Mapping[str, Any] | None = None,
) -> None:
    """Write an object to a JSON file.

    Args:
        obj: Stiffness, homogenization result, canonical cell, atlas, or thermal loads.
        path: Destination file path.
        units: Optional plain mapping describing the unit system.

    Raises:
        SchemaError: If the object cannot be represented by the schema.
        OSError: If the file cannot be written.
    """

    Path(path).write_text(to_json(obj, units=units), encoding="utf-8")


def read_yaml(path: str | PathLike[str]) -> WorkflowObject:
    """Read a Tensyl object from a safe YAML file.

    Args:
        path: Source YAML file path.

    Returns:
        ``ABDStiffness`` or ``HomogenizationResult`` described by the file.

    Raises:
        SchemaError: If the file contents fail YAML or schema validation.
        OSError: If the file cannot be read.
    """

    return from_yaml(Path(path).read_text(encoding="utf-8"))


def read_json(path: str | PathLike[str]) -> WorkflowObject:
    """Read a Tensyl object from a JSON file.

    Args:
        path: Source JSON file path.

    Returns:
        ``ABDStiffness`` or ``HomogenizationResult`` described by the file.

    Raises:
        SchemaError: If the file contents fail JSON or schema validation.
        OSError: If the file cannot be read.
    """

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
