"""Barrel validation response targets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from math import pi
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from tensyl_validation.artifacts import ArtifactManifest, write_json
from tensyl_validation.local_abd import LocalABDCase, load_local_abd_case, target_stiffness

_RESULTANT_INDEX = {
    "N11": 0,
    "N22": 1,
    "N12": 2,
    "M11": 3,
    "M22": 4,
    "M12": 5,
    "Q13": 6,
    "Q23": 7,
}
_STRAIN_ORDER = [
    "epsilon_11",
    "epsilon_22",
    "gamma_12",
    "kappa_11",
    "kappa_22",
    "kappa_12",
    "gamma_13",
    "gamma_23",
]


@dataclass(frozen=True, slots=True)
class BarrelSmearedResponseCase:
    """Phase 3 no-solver smeared barrel response target."""

    name: str
    title: str
    local_abd_spec: Path
    radius: float
    length: float
    angle_rad: float
    resultants: np.ndarray
    units: dict[str, Any] = field(default_factory=dict)
    validity_context: dict[str, float | None] = field(default_factory=dict)
    expected_status: str = "smeared_target_only"

    def __post_init__(self) -> None:
        object.__setattr__(self, "radius", _positive(self.radius, "barrel.radius"))
        object.__setattr__(self, "length", _positive(self.length, "barrel.length_e1"))
        object.__setattr__(self, "angle_rad", _positive(self.angle_rad, "barrel.angle_rad"))
        resultants = np.asarray(self.resultants, dtype=np.float64)
        if resultants.shape != (8,) or not np.all(np.isfinite(resultants)):
            msg = "barrel resultants must contain eight finite components."
            raise ValueError(msg)
        object.__setattr__(self, "resultants", resultants)

    @property
    def arc_length(self) -> float:
        """Circumferential arc length represented by the barrel case."""

        return self.radius * self.angle_rad

    @property
    def area(self) -> float:
        """Barrel midsurface area represented by the case."""

        return self.length * self.arc_length


def _positive(value: float, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be a finite positive number."
        raise ValueError(msg)
    return checked


def _load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"{path} must contain a mapping."
        raise ValueError(msg)
    return data


def _resultants(data: Mapping[str, Any]) -> np.ndarray:
    raw = data.get("resultants")
    if not isinstance(raw, Mapping):
        msg = "barrel load must provide a resultants mapping."
        raise ValueError(msg)
    values = np.zeros(8, dtype=np.float64)
    for key, value in raw.items():
        component = str(key)
        try:
            index = _RESULTANT_INDEX[component]
        except KeyError as exc:
            msg = f"unsupported barrel resultant component: {component!r}"
            raise ValueError(msg) from exc
        values[index] = float(value)
    return values


def _json_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, Mapping):
            values[str(key)] = _json_mapping(value)
        elif value is None:
            values[str(key)] = None
        else:
            values[str(key)] = value
    return values


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd()))
    except ValueError:
        return str(resolved)


def load_barrel_case(
    data: dict[str, Any],
    *,
    base_dir: Path,
) -> BarrelSmearedResponseCase:
    """Load a Phase 3 smeared barrel response case."""

    barrel = data.get("barrel")
    load = data.get("load")
    if not isinstance(barrel, Mapping):
        msg = "barrel_smeared_response cases require a barrel mapping."
        raise ValueError(msg)
    if not isinstance(load, Mapping):
        msg = "barrel_smeared_response cases require a load mapping."
        raise ValueError(msg)

    status = data.get("status", {})
    expected_status = (
        status.get("artifact_promotion", "smeared_target_only")
        if isinstance(status, Mapping)
        else "smeared_target_only"
    )
    validity = data.get("validity_context", {})
    if not isinstance(validity, Mapping):
        msg = "validity_context must be a mapping when provided."
        raise ValueError(msg)
    return BarrelSmearedResponseCase(
        name=str(data["name"]),
        title=str(data.get("title", data["name"])),
        local_abd_spec=(base_dir / str(data["local_abd_reference"])).resolve(),
        radius=float(barrel["radius"]),
        length=float(barrel["length_e1"]),
        angle_rad=float(barrel.get("angle_rad", 2.0 * pi)),
        resultants=_resultants(load),
        units=_json_mapping(data.get("units", {})),
        validity_context={str(key): _optional_float(value) for key, value in validity.items()},
        expected_status=str(expected_status),
    )


def _local_abd_case(path: Path) -> LocalABDCase:
    data = _load_mapping(path)
    return load_local_abd_case(data)


def _validity_metrics(case: BarrelSmearedResponseCase) -> dict[str, float | None]:
    pitch = case.validity_context.get("pitch")
    height = case.validity_context.get("characteristic_height")
    response_length = case.validity_context.get("response_length")
    return {
        "p_over_R": None if pitch is None else pitch / case.radius,
        "h_over_R": None if height is None else height / case.radius,
        "p_over_L_response": (
            None if pitch is None or response_length is None else pitch / response_length
        ),
    }


def _response_payload(
    case: BarrelSmearedResponseCase,
    local_case: LocalABDCase,
) -> dict[str, Any]:
    stiffness = target_stiffness(local_case)
    eta = np.linalg.solve(stiffness.C8, case.resultants)
    recovered = stiffness.C8 @ eta
    energy_density = 0.5 * float(eta @ case.resultants)
    hoop_radius_change = eta[1] * case.radius
    return {
        "schema_version": "tensyl.validation.barrel-smeared-response.v1",
        "case_name": case.name,
        "title": case.title,
        "status": case.expected_status,
        "source": "tensyl_smeared_abd_target",
        "explicit_fe_status": "planned",
        "local_abd_reference": _display_path(case.local_abd_spec),
        "barrel": {
            "radius": case.radius,
            "length_e1": case.length,
            "angle_rad": case.angle_rad,
            "arc_length_e2": case.arc_length,
            "area": case.area,
        },
        "order": {
            "resultants": list(_RESULTANT_INDEX),
            "generalized_strains": _STRAIN_ORDER,
        },
        "resultants": case.resultants.tolist(),
        "generalized_strain": eta.tolist(),
        "recovered_resultants": recovered.tolist(),
        "response": {
            "strain_energy_density": energy_density,
            "total_strain_energy": energy_density * case.area,
            "axial_end_shortening_e1": float(eta[0] * case.length),
            "circumferential_arc_change_e2": float(eta[1] * case.arc_length),
            "hoop_radius_change": float(hoop_radius_change),
            "twist_shear_arc_shift": float(eta[2] * case.arc_length),
        },
        "validity_ratios": _validity_metrics(case),
        "units": case.units,
        "notes": [
            (
                "This artifact is a smeared cylindrical-wall target computed "
                "from Tensyl ABD stiffness."
            ),
            "It is not an explicit finite-element barrel comparison.",
        ],
    }


def _metrics_payload(response: dict[str, Any]) -> dict[str, Any]:
    resultants = np.asarray(response["resultants"], dtype=np.float64)
    recovered = np.asarray(response["recovered_resultants"], dtype=np.float64)
    eta = np.asarray(response["generalized_strain"], dtype=np.float64)
    residual = recovered - resultants
    return {
        "schema_version": "tensyl.validation.barrel-smeared-metrics.v1",
        "case_name": response["case_name"],
        "case_type": "barrel_smeared_response",
        "expected_status": response["status"],
        "checks": {
            "smeared_equilibrium_relative_residual": _relative_norm(residual, resultants),
            "max_abs_resultant_residual": float(np.max(np.abs(residual))),
            "nonzero_generalized_strain_count": int(np.count_nonzero(np.abs(eta) > 1.0e-14)),
            "positive_strain_energy_density": response["response"]["strain_energy_density"] > 0.0,
            "explicit_fe_comparison_available": False,
        },
        "response": dict(response["response"]),
        "validity_ratios": dict(response["validity_ratios"]),
        "comparison": {
            "explicit_fe_status": response["explicit_fe_status"],
            "promoted_solver_metrics": False,
        },
    }


def _relative_norm(delta: np.ndarray, reference: np.ndarray) -> float:
    scale = max(float(np.linalg.norm(reference)), 1.0)
    return float(np.linalg.norm(delta) / scale)


def run_barrel_case(
    spec_path: Path,
    case: BarrelSmearedResponseCase,
    *,
    artifact_dir: Path,
    command: list[str] | None = None,
) -> dict[str, Path]:
    """Write Phase 3 smeared barrel response target artifacts."""

    local_case = _local_abd_case(case.local_abd_spec)
    response = _response_payload(case, local_case)
    response_path = artifact_dir / "smeared_response.json"
    metrics_path = artifact_dir / "metrics.json"
    manifest_path = artifact_dir / "manifest.json"
    write_json(response_path, response)
    write_json(metrics_path, _metrics_payload(response))
    manifest = ArtifactManifest(
        case_name=case.name,
        command=[] if command is None else command,
        inputs=[spec_path, Path(_display_path(case.local_abd_spec))],
        outputs=[response_path, metrics_path, manifest_path],
        metadata={
            "case_type": "barrel_smeared_response",
            "phase": "phase_3_barrel_response",
            "artifact_role": "tensyl_smeared_barrel_target",
            "solver_required": False,
            "explicit_fe_status": "planned",
            "explicit_fe_comparison": False,
            "local_abd_case": local_case.name,
        },
    )
    write_json(manifest_path, manifest.as_dict())
    return {
        "response": response_path,
        "metrics": metrics_path,
        "manifest": manifest_path,
    }
