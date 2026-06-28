"""Flat-panel validation response targets."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
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
class FlatPanelSmearedResponseCase:
    """Phase 2 no-solver smeared flat-panel response target."""

    name: str
    title: str
    local_abd_spec: Path
    panel_length: float
    panel_width: float
    resultants: np.ndarray
    units: dict[str, Any] = field(default_factory=dict)
    expected_status: str = "smeared_target_only"

    def __post_init__(self) -> None:
        object.__setattr__(self, "panel_length", _positive(self.panel_length, "panel.length"))
        object.__setattr__(self, "panel_width", _positive(self.panel_width, "panel.width"))
        resultants = np.asarray(self.resultants, dtype=np.float64)
        if resultants.shape != (8,) or not np.all(np.isfinite(resultants)):
            msg = "flat-panel resultants must contain eight finite components."
            raise ValueError(msg)
        object.__setattr__(self, "resultants", resultants)

    @property
    def panel_area(self) -> float:
        """Panel planform area."""

        return self.panel_length * self.panel_width


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
        msg = "flat-panel load must provide a resultants mapping."
        raise ValueError(msg)
    values = np.zeros(8, dtype=np.float64)
    for key, value in raw.items():
        component = str(key)
        try:
            index = _RESULTANT_INDEX[component]
        except KeyError as exc:
            msg = f"unsupported flat-panel resultant component: {component!r}"
            raise ValueError(msg) from exc
        values[index] = float(value)
    return values


def _json_mapping(data: Mapping[str, Any]) -> dict[str, Any]:
    values: dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, Mapping):
            values[str(key)] = _json_mapping(value)
        else:
            values[str(key)] = value
    return values


def _display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd()))
    except ValueError:
        return str(resolved)


def load_flat_panel_case(
    data: dict[str, Any],
    *,
    base_dir: Path,
) -> FlatPanelSmearedResponseCase:
    """Load a Phase 2 flat-panel response case."""

    panel = data.get("panel")
    load = data.get("load")
    if not isinstance(panel, Mapping):
        msg = "flat_panel_smeared_response cases require a panel mapping."
        raise ValueError(msg)
    if not isinstance(load, Mapping):
        msg = "flat_panel_smeared_response cases require a load mapping."
        raise ValueError(msg)

    local_ref = base_dir / str(data["local_abd_reference"])
    status = data.get("status", {})
    expected_status = (
        status.get("artifact_promotion", "smeared_target_only")
        if isinstance(status, Mapping)
        else "smeared_target_only"
    )
    return FlatPanelSmearedResponseCase(
        name=str(data["name"]),
        title=str(data.get("title", data["name"])),
        local_abd_spec=local_ref.resolve(),
        panel_length=float(panel["length_e1"]),
        panel_width=float(panel["width_e2"]),
        resultants=_resultants(load),
        units=_json_mapping(data.get("units", {})),
        expected_status=str(expected_status),
    )


def _local_abd_case(path: Path) -> LocalABDCase:
    data = _load_mapping(path)
    case = load_local_abd_case(data)
    if not isinstance(case, LocalABDCase):
        msg = f"{path} did not load as a local ABD case."
        raise TypeError(msg)
    return case


def _response_payload(
    case: FlatPanelSmearedResponseCase,
    local_case: LocalABDCase,
) -> dict[str, Any]:
    stiffness = target_stiffness(local_case)
    eta = np.linalg.solve(stiffness.C8, case.resultants)
    recovered = stiffness.C8 @ eta
    energy_density = 0.5 * float(eta @ case.resultants)
    return {
        "schema_version": "tensyl.validation.flat-panel-smeared-response.v1",
        "case_name": case.name,
        "title": case.title,
        "status": case.expected_status,
        "source": "tensyl_smeared_abd_target",
        "explicit_fe_status": "planned",
        "local_abd_reference": _display_path(case.local_abd_spec),
        "panel": {
            "length_e1": case.panel_length,
            "width_e2": case.panel_width,
            "area": case.panel_area,
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
            "total_strain_energy": energy_density * case.panel_area,
            "end_shortening_e1": float(eta[0] * case.panel_length),
            "transverse_extension_e2": float(eta[1] * case.panel_width),
            "midspan_bending_deflection_k11": float(0.5 * eta[3] * (0.5 * case.panel_length) ** 2),
            "midspan_bending_deflection_k22": float(0.5 * eta[4] * (0.5 * case.panel_width) ** 2),
        },
        "units": case.units,
        "notes": [
            "This artifact is a smeared-panel target computed from Tensyl ABD stiffness.",
            "It is not an explicit finite-element panel comparison.",
        ],
    }


def _metrics_payload(response: dict[str, Any]) -> dict[str, Any]:
    resultants = np.asarray(response["resultants"], dtype=np.float64)
    recovered = np.asarray(response["recovered_resultants"], dtype=np.float64)
    eta = np.asarray(response["generalized_strain"], dtype=np.float64)
    residual = recovered - resultants
    return {
        "schema_version": "tensyl.validation.flat-panel-smeared-metrics.v1",
        "case_name": response["case_name"],
        "case_type": "flat_panel_smeared_response",
        "expected_status": response["status"],
        "checks": {
            "smeared_equilibrium_relative_residual": _relative_norm(residual, resultants),
            "max_abs_resultant_residual": float(np.max(np.abs(residual))),
            "nonzero_generalized_strain_count": int(np.count_nonzero(np.abs(eta) > 1.0e-14)),
            "positive_strain_energy_density": response["response"]["strain_energy_density"] > 0.0,
            "explicit_fe_comparison_available": False,
        },
        "response": dict(response["response"]),
        "comparison": {
            "explicit_fe_status": response["explicit_fe_status"],
            "promoted_solver_metrics": False,
        },
    }


def _relative_norm(delta: np.ndarray, reference: np.ndarray) -> float:
    scale = max(float(np.linalg.norm(reference)), 1.0)
    return float(np.linalg.norm(delta) / scale)


def run_flat_panel_case(
    spec_path: Path,
    case: FlatPanelSmearedResponseCase,
    *,
    artifact_dir: Path,
    command: list[str] | None = None,
) -> dict[str, Path]:
    """Write Phase 2 smeared flat-panel response target artifacts."""

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
            "case_type": "flat_panel_smeared_response",
            "phase": "phase_2_flat_panel_response",
            "artifact_role": "tensyl_smeared_panel_target",
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
