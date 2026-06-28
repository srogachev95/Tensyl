"""Case loading and validation execution."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from tensyl import IsotropicMaterial, isotropic_plate
from tensyl_validation.artifacts import ArtifactManifest, write_json
from tensyl_validation.local_abd import LocalABDCase, load_local_abd_case, run_local_abd_case
from tensyl_validation.metrics import skin_only_metrics


@dataclass(frozen=True, slots=True)
class SkinOnlySmokeCase:
    """Tiny confirmation case that needs Tensyl but no external solver."""

    name: str
    material: IsotropicMaterial
    thickness: float
    shear_correction: float = 5.0 / 6.0
    units: dict[str, str] = field(default_factory=dict)


def _load_skin_only_smoke(data: dict[str, Any]) -> SkinOnlySmokeCase:
    material_data = data["material"]
    material = IsotropicMaterial(
        E=float(material_data["E"]),
        nu=float(material_data["nu"]),
        density=(None if material_data.get("density") is None else float(material_data["density"])),
    )
    return SkinOnlySmokeCase(
        name=str(data["name"]),
        material=material,
        thickness=float(data["thickness"]),
        shear_correction=float(data.get("shear_correction", 5.0 / 6.0)),
        units={str(key): str(value) for key, value in data.get("units", {}).items()},
    )


ValidationCase = SkinOnlySmokeCase | LocalABDCase


def load_case(path: Path) -> ValidationCase:
    """Load a validation case spec."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"{path} must contain a mapping."
        raise ValueError(msg)
    case_type = data.get("case_type")
    if (
        case_type == "skin_only_isotropic"
        and data.get("schema_version") == "tensyl.validation.local_abd.case.v1"
    ):
        return load_local_abd_case(data)
    if case_type == "skin_only_isotropic":
        return _load_skin_only_smoke(data)
    if case_type in {"local_abd", "local_abd_periodic_cell"}:
        return load_local_abd_case(data)
    msg = f"unsupported validation case_type: {case_type!r}"
    raise ValueError(msg)


def run_case(
    spec_path: Path,
    *,
    artifact_dir: Path,
    command: list[str] | None = None,
) -> dict[str, Path]:
    """Run a no-solver case and write metrics plus a manifest."""

    case = load_case(spec_path)
    if isinstance(case, LocalABDCase):
        return run_local_abd_case(
            spec_path,
            case,
            artifact_dir=artifact_dir,
            command=command,
        )

    stiffness = isotropic_plate(
        case.material,
        thickness=case.thickness,
        shear_correction=case.shear_correction,
        metadata={"validation_case": case.name},
    )

    metrics = skin_only_metrics(stiffness, material=case.material, thickness=case.thickness)
    metrics["case_name"] = case.name
    metrics["units"].update(case.units)

    metrics_path = artifact_dir / "metrics.json"
    manifest_path = artifact_dir / "manifest.json"
    write_json(metrics_path, metrics)
    manifest = ArtifactManifest(
        case_name=case.name,
        command=[] if command is None else command,
        inputs=[spec_path],
        outputs=[metrics_path, manifest_path],
        metadata={"case_type": "skin_only_isotropic", "solver_required": False},
    )
    write_json(manifest_path, manifest.as_dict())
    return {"metrics": metrics_path, "manifest": manifest_path}
