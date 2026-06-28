"""Local ABD validation case targets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, cast

import numpy as np

from tensyl import (
    ABDStiffness,
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    equilateral_isogrid_cell,
    isotropic_plate,
    orthogrid_cell,
    unidirectional_cell,
)
from tensyl_validation.artifacts import ArtifactManifest, write_json

LocalABDModel = Literal[
    "skin_only",
    "unidirectional",
    "orthogrid",
    "equilateral_isogrid",
]


@dataclass(frozen=True, slots=True)
class LocalABDCase:
    """Case spec for a local ABD extraction target."""

    name: str
    model: LocalABDModel
    material: IsotropicMaterial
    skin_thickness: float
    units: dict[str, str] = field(default_factory=dict)
    shear_correction: float = 5.0 / 6.0
    section: BeamSection | None = None
    stringer_section: BeamSection | None = None
    rib_section: BeamSection | None = None
    geometry: dict[str, float] = field(default_factory=dict)
    validity_context: ValidityContext | None = None
    expected_status: str = "confirmation"


def _required_float(data: Mapping[str, Any], key: str) -> float:
    try:
        return float(data[key])
    except KeyError as exc:
        msg = f"missing required local ABD field: {key}"
        raise ValueError(msg) from exc


def _material(data: Mapping[str, Any]) -> IsotropicMaterial:
    return IsotropicMaterial(
        E=_required_float(data, "E"),
        nu=_required_float(data, "nu"),
        density=None if data.get("density") is None else float(data["density"]),
    )


def _beam_section(data: Mapping[str, Any] | None) -> BeamSection | None:
    if data is None:
        return None
    return BeamSection(
        EA=_required_float(data, "EA"),
        EIy=_required_float(data, "EIy"),
        EIz=_required_float(data, "EIz"),
        GJ=_required_float(data, "GJ"),
        kGAy=None if data.get("kGAy") is None else float(data["kGAy"]),
        kGAz=None if data.get("kGAz") is None else float(data["kGAz"]),
        EIyz=float(data.get("EIyz", 0.0)),
        metadata={str(key): value for key, value in data.get("metadata", {}).items()},
    )


def _validity_context(data: Mapping[str, Any] | None) -> ValidityContext | None:
    if data is None:
        return None
    return ValidityContext(
        characteristic_height=(
            None
            if data.get("characteristic_height") is None
            else float(data["characteristic_height"])
        ),
        pitch=None if data.get("pitch") is None else float(data["pitch"]),
        min_radius=None if data.get("min_radius") is None else float(data["min_radius"]),
        response_length=(
            None if data.get("response_length") is None else float(data["response_length"])
        ),
    )


def _section_from_library(
    library: Mapping[str, Any],
    name: str | None,
) -> BeamSection | None:
    if name is None:
        return None
    try:
        section_data = library[name]
    except KeyError as exc:
        msg = f"unknown section reference in local ABD case: {name!r}"
        raise ValueError(msg) from exc
    if not isinstance(section_data, Mapping):
        msg = f"section reference {name!r} must resolve to a mapping."
        raise ValueError(msg)
    return _beam_section(section_data)


def _load_periodic_cell_case(data: Mapping[str, Any]) -> LocalABDCase:
    materials = data.get("materials")
    skin = data.get("skin")
    cell = data.get("cell")
    if not isinstance(materials, Mapping):
        msg = "local_abd_periodic_cell cases require a materials mapping."
        raise ValueError(msg)
    if not isinstance(skin, Mapping):
        msg = "local_abd_periodic_cell cases require a skin mapping."
        raise ValueError(msg)
    if not isinstance(cell, Mapping):
        msg = "local_abd_periodic_cell cases require a cell mapping."
        raise ValueError(msg)

    material_name = str(skin["material"])
    material_data = materials.get(material_name)
    if not isinstance(material_data, Mapping):
        msg = f"unknown skin material reference in local ABD case: {material_name!r}"
        raise ValueError(msg)

    arguments = cell.get("arguments")
    if not isinstance(arguments, Mapping):
        msg = "local_abd_periodic_cell cases require cell.arguments."
        raise ValueError(msg)
    library = data.get("section_library", {})
    if not isinstance(library, Mapping):
        msg = "section_library must be a mapping when provided."
        raise ValueError(msg)

    constructor = str(cell.get("constructor", cell.get("topology", "")))
    if constructor == "unidirectional_cell":
        model: LocalABDModel = "unidirectional"
        section = _section_from_library(library, str(arguments["member_section"]))
        stringer_section = section
        rib_section = section
        geometry = {
            "spacing": float(arguments["spacing"]),
            "eccentricity": float(arguments.get("eccentricity", 0.0)),
            "angle_rad": float(arguments.get("angle_rad", 0.0)),
        }
    elif constructor == "orthogrid_cell":
        model = "orthogrid"
        section = None
        stringer_section = _section_from_library(library, str(arguments["stringer_section"]))
        rib_section = _section_from_library(library, str(arguments["rib_section"]))
        geometry = {
            "stringer_spacing": float(arguments["stringer_spacing"]),
            "rib_spacing": float(arguments["rib_spacing"]),
            "stringer_eccentricity": float(arguments.get("stringer_eccentricity", 0.0)),
            "rib_eccentricity": float(arguments.get("rib_eccentricity", 0.0)),
        }
    elif constructor == "equilateral_isogrid_cell":
        model = "equilateral_isogrid"
        section = _section_from_library(library, str(arguments["member_section"]))
        stringer_section = section
        rib_section = section
        geometry = {
            "pitch": float(arguments["pitch"]),
            "eccentricity": float(arguments.get("eccentricity", 0.0)),
        }
    else:
        msg = f"unsupported local ABD cell constructor: {constructor!r}"
        raise ValueError(msg)

    status = data.get("status", {})
    artifact_status = (
        status.get("artifact_promotion", "confirmation")
        if isinstance(status, Mapping)
        else "confirmation"
    )
    return LocalABDCase(
        name=str(data["name"]),
        model=model,
        material=_material(material_data),
        skin_thickness=float(skin["thickness"]),
        shear_correction=float(skin.get("shear_correction", 5.0 / 6.0)),
        units={str(key): str(value) for key, value in data.get("units", {}).items()},
        section=section,
        stringer_section=stringer_section,
        rib_section=rib_section,
        geometry=geometry,
        validity_context=_validity_context(data.get("validity_context")),
        expected_status=str(artifact_status),
    )


def _load_skin_only_local_case(data: Mapping[str, Any]) -> LocalABDCase:
    status = data.get("status", {})
    artifact_status = (
        status.get("artifact_promotion", "confirmation")
        if isinstance(status, Mapping)
        else "confirmation"
    )
    return LocalABDCase(
        name=str(data["name"]),
        model="skin_only",
        material=_material(data["material"]),
        skin_thickness=float(data["thickness"]),
        shear_correction=float(data.get("shear_correction", 5.0 / 6.0)),
        units={str(key): str(value) for key, value in data.get("units", {}).items()},
        expected_status=str(artifact_status),
    )


def load_local_abd_case(data: dict[str, Any]) -> LocalABDCase:
    """Load a local ABD case from a YAML mapping."""

    if data.get("case_type") == "skin_only_isotropic":
        return _load_skin_only_local_case(data)
    if data.get("case_type") == "local_abd_periodic_cell":
        return _load_periodic_cell_case(data)

    raw_model = str(data["model"])
    allowed_models: set[LocalABDModel] = {
        "skin_only",
        "unidirectional",
        "orthogrid",
        "equilateral_isogrid",
    }
    if raw_model not in allowed_models:
        msg = f"unsupported local ABD model: {raw_model!r}"
        raise ValueError(msg)
    model = cast(LocalABDModel, raw_model)
    geometry = {str(key): float(value) for key, value in data.get("geometry", {}).items()}
    section = _beam_section(data.get("section"))
    return LocalABDCase(
        name=str(data["name"]),
        model=model,  # type: ignore[arg-type]
        material=_material(data["material"]),
        skin_thickness=float(data["skin_thickness"]),
        shear_correction=float(data.get("shear_correction", 5.0 / 6.0)),
        units={str(key): str(value) for key, value in data.get("units", {}).items()},
        section=section,
        stringer_section=_beam_section(data.get("stringer_section")) or section,
        rib_section=_beam_section(data.get("rib_section")) or section,
        geometry=geometry,
        validity_context=_validity_context(data.get("validity_context")),
        expected_status=str(data.get("expected_status", "confirmation")),
    )


def _skin(case: LocalABDCase) -> ABDStiffness:
    return isotropic_plate(
        case.material,
        thickness=case.skin_thickness,
        shear_correction=case.shear_correction,
        metadata={"validation_case": case.name, "validation_model": case.model},
    )


def target_stiffness(case: LocalABDCase) -> ABDStiffness:
    """Compute the Tensyl target stiffness for a local ABD validation case."""

    skin = _skin(case)
    geometry = case.geometry
    if case.model == "skin_only":
        return skin
    homogenizer = EnergyHomogenizer()
    if case.model == "unidirectional":
        if case.section is None:
            msg = "unidirectional local ABD cases require a beam section."
            raise ValueError(msg)
        cell = unidirectional_cell(
            skin=skin,
            member_section=case.section,
            spacing=_required_float(geometry, "spacing"),
            eccentricity=float(geometry.get("eccentricity", 0.0)),
            angle_rad=float(geometry.get("angle_rad", 0.0)),
        )
    elif case.model == "orthogrid":
        if case.stringer_section is None or case.rib_section is None:
            msg = "orthogrid local ABD cases require stringer and rib sections."
            raise ValueError(msg)
        cell = orthogrid_cell(
            skin=skin,
            stringer_section=case.stringer_section,
            rib_section=case.rib_section,
            stringer_spacing=_required_float(geometry, "stringer_spacing"),
            rib_spacing=_required_float(geometry, "rib_spacing"),
            stringer_eccentricity=float(geometry.get("stringer_eccentricity", 0.0)),
            rib_eccentricity=float(geometry.get("rib_eccentricity", 0.0)),
        )
    elif case.model == "equilateral_isogrid":
        if case.section is None:
            msg = "equilateral isogrid local ABD cases require a beam section."
            raise ValueError(msg)
        cell = equilateral_isogrid_cell(
            skin=skin,
            member_section=case.section,
            pitch=_required_float(geometry, "pitch"),
            eccentricity=float(geometry.get("eccentricity", 0.0)),
        )
    else:  # pragma: no cover - guarded during loading.
        msg = f"unsupported local ABD model: {case.model!r}"
        raise ValueError(msg)
    return homogenizer.compute(cell, validity_context=case.validity_context).stiffness


def stiffness_payload(stiffness: ABDStiffness) -> dict[str, Any]:
    """Return a compact JSON payload for a stiffness target."""

    return {
        "schema_version": "tensyl.validation.local-abd-target.v1",
        "order": ["11", "22", "12", "k11", "k22", "k12", "13", "23"],
        "blocks": {
            "A": stiffness.A.tolist(),
            "B": stiffness.B.tolist(),
            "D": stiffness.D.tolist(),
            "As": stiffness.As.tolist(),
            "C8": stiffness.C8.tolist(),
        },
        "areal_mass": stiffness.areal_mass,
        "metadata": dict(stiffness.metadata),
        "validity": _validity_payload(stiffness.validity),
    }


def _validity_payload(validity: Any) -> dict[str, Any] | None:
    if validity is None:
        return None
    return {
        "h_over_R": getattr(validity, "h_over_R", None),
        "p_over_R": getattr(validity, "p_over_R", None),
        "p_over_L_response": getattr(validity, "p_over_L_response", None),
        "coupling_ratios": dict(getattr(validity, "coupling_ratios", {})),
        "warnings": list(getattr(validity, "warnings", ())),
    }


def local_abd_target_metrics(case: LocalABDCase, stiffness: ABDStiffness) -> dict[str, Any]:
    """Return compact target-side metrics for a local ABD case."""

    abd = stiffness.C8[:6, :6]
    eigenvalues = np.linalg.eigvalsh(stiffness.C8)
    strain_cases = np.eye(8, dtype=np.float64)
    energies = [stiffness.energy(row) for row in strain_cases]
    return {
        "schema_version": "tensyl.validation.local-abd-metrics.v1",
        "case_name": case.name,
        "case_type": "local_abd",
        "model": case.model,
        "expected_status": case.expected_status,
        "units": case.units,
        "checks": {
            "symmetric_C8": bool(np.allclose(stiffness.C8, stiffness.C8.T)),
            "min_C8_eigenvalue": float(np.min(eigenvalues)),
            "max_C8_eigenvalue": float(np.max(eigenvalues)),
            "condition_number_C8": float(np.linalg.cond(stiffness.C8)),
            "rank_C8": int(np.linalg.matrix_rank(stiffness.C8)),
            "symmetric_ABD": bool(np.allclose(abd, abd.T)),
        },
        "canonical_unit_strain_energies": energies,
        "validity_warnings": (
            [] if stiffness.validity is None else list(stiffness.validity.warnings)
        ),
    }


def run_local_abd_case(
    spec_path: Path,
    case: LocalABDCase,
    *,
    artifact_dir: Path,
    command: list[str] | None = None,
) -> dict[str, Path]:
    """Write Tensyl-side target artifacts for a local ABD case."""

    stiffness = target_stiffness(case)
    target_path = artifact_dir / "target_abd.json"
    metrics_path = artifact_dir / "metrics.json"
    manifest_path = artifact_dir / "manifest.json"
    write_json(target_path, stiffness_payload(stiffness))
    write_json(metrics_path, local_abd_target_metrics(case, stiffness))
    manifest = ArtifactManifest(
        case_name=case.name,
        command=[] if command is None else command,
        inputs=[spec_path],
        outputs=[target_path, metrics_path, manifest_path],
        metadata={
            "case_type": "local_abd",
            "model": case.model,
            "solver_required": False,
            "artifact_role": "tensyl_target",
        },
    )
    write_json(manifest_path, manifest.as_dict())
    return {"target": target_path, "metrics": metrics_path, "manifest": manifest_path}
