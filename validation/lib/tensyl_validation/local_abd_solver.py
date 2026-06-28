"""Solver-backed local ABD extraction runners."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from math import sqrt
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from tensyl_validation.artifacts import ArtifactManifest, write_json
from tensyl_validation.calculix import (
    CalculixBeamStiffness,
    CalculixSkinPatch,
    CalculixStressTable,
    CalculixUnidirectionalStiffenedPatch,
    GeneralizedStrainLoadCase,
    parse_calculix_stress_dat,
    render_skin_patch_inp,
    render_unidirectional_stiffened_probe_decks,
)
from tensyl_validation.cases import load_case as load_validation_case
from tensyl_validation.local_abd import LocalABDCase, target_stiffness
from tensyl_validation.metrics import abd6_comparison_metrics
from tensyl_validation.solvers import check_solver_inventory

_COMPONENT_INDEX = {
    "epsilon_11": 0,
    "epsilon_22": 1,
    "gamma_12": 2,
    "kappa_11": 3,
    "kappa_22": 4,
    "kappa_12": 5,
}


class UnsupportedSolverExtractionError(RuntimeError):
    """Raised when a local ABD case has no promoted solver extraction path."""


@dataclass(frozen=True, slots=True)
class ExtractionLoadCase:
    """One membrane/bending extraction load case."""

    case_id: str
    component: str
    magnitude: float

    def calculix_case(self) -> GeneralizedStrainLoadCase:
        values = [0.0] * 6
        values[_COMPONENT_INDEX[self.component]] = self.magnitude
        return GeneralizedStrainLoadCase(
            self.case_id,
            (values[0], values[1], values[2], values[3], values[4], values[5]),
        )


def _load_spec(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        msg = f"{path} must contain a mapping."
        raise ValueError(msg)
    return data


def _skin_patch(case: LocalABDCase, data: dict[str, Any]) -> CalculixSkinPatch:
    cell = data.get("cell", {})
    dimensions = cell.get("dimensions", {}) if isinstance(cell, dict) else {}
    fe_model = data.get("fe_model", {})
    length = float(dimensions.get("e1_length", 6.0))
    width = float(dimensions.get("e2_length", 6.0))
    nominal_size = (
        float(fe_model.get("nominal_element_size", 0.5)) if isinstance(fe_model, dict) else 0.5
    )
    return CalculixSkinPatch(
        length=length,
        width=width,
        thickness=case.skin_thickness,
        youngs_modulus=case.material.E,
        poissons_ratio=case.material.nu,
        divisions_x=max(1, round(length / nominal_size)),
        divisions_y=max(1, round(width / nominal_size)),
        name=case.name,
    )


def _unidirectional_stiffened_patch(
    case: LocalABDCase,
    data: dict[str, Any],
) -> CalculixUnidirectionalStiffenedPatch:
    if case.model != "unidirectional" or case.section is None:
        msg = "unidirectional stiffener probe requires a unidirectional beam-section case."
        raise ValueError(msg)
    geometry = case.geometry
    if float(geometry.get("eccentricity", 0.0)) != 0.0:
        msg = "unidirectional stiffener probe currently supports zero eccentricity only."
        raise UnsupportedSolverExtractionError(msg)
    if float(geometry.get("angle_rad", 0.0)) != 0.0:
        msg = "unidirectional stiffener probe currently supports members aligned with e1 only."
        raise UnsupportedSolverExtractionError(msg)
    spacing = float(geometry["spacing"])
    patch = _skin_patch(case, data)
    if abs(patch.width - spacing) > 1.0e-9:
        msg = "unidirectional stiffener probe expects one pitch across the patch width."
        raise UnsupportedSolverExtractionError(msg)
    return CalculixUnidirectionalStiffenedPatch(
        skin=patch,
        beam=CalculixBeamStiffness(
            EA=case.section.EA,
            EIy=case.section.EIy,
            EIz=case.section.EIz,
            GJ=case.section.GJ,
            kGAy=case.section.kGAy,
            kGAz=case.section.kGAz,
        ),
    )


def _extraction_load_cases(data: dict[str, Any]) -> tuple[ExtractionLoadCase, ...]:
    extraction = data.get("extraction", {})
    raw_cases = extraction.get("load_cases", []) if isinstance(extraction, dict) else []
    load_cases: list[ExtractionLoadCase] = []
    for raw_case in raw_cases:
        if not isinstance(raw_case, dict):
            continue
        component = str(raw_case["component"])
        if component not in _COMPONENT_INDEX:
            continue
        load_cases.append(
            ExtractionLoadCase(
                case_id=str(raw_case["id"]),
                component=component,
                magnitude=float(raw_case["magnitude"]),
            )
        )
    expected = set(_COMPONENT_INDEX)
    actual = {load_case.component for load_case in load_cases}
    if actual != expected:
        missing = ", ".join(sorted(expected - actual))
        msg = f"skin-only ABD extraction requires all six ABD load cases; missing: {missing}"
        raise ValueError(msg)
    return tuple(load_cases)


def _resultants_from_stress(
    table: CalculixStressTable,
    *,
    thickness: float,
    is_bending: bool,
) -> np.ndarray:
    means = table.component_means()
    bottom, top = table.top_bottom_component_means()
    if not means:
        msg = "CalculiX stress output did not contain stress rows."
        raise ValueError(msg)
    membrane = np.array(
        [means["sxx"] * thickness, means["syy"] * thickness, means["sxy"] * thickness],
        dtype=np.float64,
    )
    if bottom and top:
        # CalculiX reports the two through-thickness shell stress layers at
        # Gauss points z = +/- h / (2 * sqrt(3)). Convert their stress
        # difference back to the exact first moment of a linear stress field.
        moment = np.array(
            [
                (top["sxx"] - bottom["sxx"]) * thickness**2 * sqrt(3.0) / 12.0,
                (top["syy"] - bottom["syy"]) * thickness**2 * sqrt(3.0) / 12.0,
                (top["sxy"] - bottom["sxy"]) * thickness**2 * sqrt(3.0) / 12.0,
            ],
            dtype=np.float64,
        )
    else:
        moment = np.zeros(3, dtype=np.float64)
    if is_bending:
        return np.concatenate([membrane, moment])
    return np.concatenate([membrane, moment])


def extract_skin_only_abd6_from_stress_tables(
    tables_by_component: dict[str, CalculixStressTable],
    *,
    thickness: float,
    magnitudes_by_component: dict[str, float],
) -> np.ndarray:
    """Assemble an ABD6 tangent from CalculiX stress tables."""

    tangent = np.zeros((6, 6), dtype=np.float64)
    for component, column in _COMPONENT_INDEX.items():
        table = tables_by_component[component]
        magnitude = magnitudes_by_component[component]
        if magnitude == 0.0:
            msg = f"load-case magnitude for {component} must be nonzero."
            raise ValueError(msg)
        tangent[:, column] = (
            _resultants_from_stress(
                table,
                thickness=thickness,
                is_bending=component.startswith("kappa"),
            )
            / magnitude
        )
    return tangent


def _extracted_payload(case: LocalABDCase, abd6: np.ndarray) -> dict[str, Any]:
    return {
        "schema_version": "tensyl.validation.local-abd-extracted.v1",
        "case_name": case.name,
        "source": "calculix_stress_table",
        "order": ["11", "22", "12", "k11", "k22", "k12"],
        "blocks": {
            "A": abd6[:3, :3].tolist(),
            "B": abd6[:3, 3:6].tolist(),
            "D": abd6[3:6, 3:6].tolist(),
            "ABD6": abd6.tolist(),
        },
        "unsupported_blocks": ["As"],
        "notes": [
            "Skin-only solver extraction currently covers membrane and bending ABD terms.",
            "Transverse-shear As extraction is intentionally not populated by this artifact.",
        ],
    }


def run_skin_only_solver_extraction(
    spec_path: Path,
    *,
    artifact_dir: Path,
    work_dir: Path,
    command: list[str] | None = None,
    project_root: Path | None = None,
) -> dict[str, Path]:
    """Run CalculiX skin-only ABD extraction and write compact artifacts."""

    loaded = load_validation_case(spec_path)
    if not isinstance(loaded, LocalABDCase) or loaded.model != "skin_only":
        msg = "run_skin_only_solver_extraction only supports skin-only local ABD cases."
        raise ValueError(msg)
    data = _load_spec(spec_path)
    root = Path.cwd() if project_root is None else project_root
    inventory = check_solver_inventory(root)
    if not inventory.ccx.ok or inventory.ccx.path is None:
        msg = "CalculiX/CCX is required for skin-only solver extraction."
        raise RuntimeError(msg)

    patch = _skin_patch(loaded, data)
    load_cases = _extraction_load_cases(data)
    case_work_dir = work_dir / loaded.name
    case_work_dir.mkdir(parents=True, exist_ok=True)

    tables: dict[str, CalculixStressTable] = {}
    magnitudes: dict[str, float] = {}
    raw_outputs: list[Path] = []
    for extraction_case in load_cases:
        calculix_case = extraction_case.calculix_case()
        deck_path = case_work_dir / f"{extraction_case.case_id}.inp"
        deck_path.write_text(render_skin_patch_inp(patch, calculix_case), encoding="utf-8")
        subprocess.run(
            [inventory.ccx.path, extraction_case.case_id],
            cwd=case_work_dir,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        dat_path = case_work_dir / f"{extraction_case.case_id}.dat"
        raw_outputs.append(dat_path)
        tables[extraction_case.component] = parse_calculix_stress_dat(
            dat_path.read_text(encoding="utf-8")
        ).table_for_set("SKIN")
        magnitudes[extraction_case.component] = extraction_case.magnitude

    abd6 = extract_skin_only_abd6_from_stress_tables(
        tables,
        thickness=loaded.skin_thickness,
        magnitudes_by_component=magnitudes,
    )
    target_abd6 = target_stiffness(loaded).C8[:6, :6]

    extracted_path = artifact_dir / "extracted_abd.json"
    comparison_path = artifact_dir / "comparison_metrics.json"
    manifest_path = artifact_dir / "extraction_manifest.json"
    write_json(extracted_path, _extracted_payload(loaded, abd6))
    write_json(
        comparison_path,
        abd6_comparison_metrics(abd6, target_abd6, case_name=loaded.name),
    )
    manifest = ArtifactManifest(
        case_name=loaded.name,
        command=[] if command is None else command,
        inputs=[spec_path],
        outputs=[extracted_path, comparison_path, manifest_path],
        metadata={
            "case_type": "local_abd",
            "model": "skin_only",
            "artifact_role": "calculix_extraction",
            "solver_required": True,
            "ccx": inventory.ccx.as_dict(),
            "raw_work_dir": str(case_work_dir),
            "raw_outputs": [str(path) for path in raw_outputs],
            "unsupported_blocks": ["As"],
        },
    )
    write_json(manifest_path, manifest.as_dict())
    return {
        "extracted": extracted_path,
        "comparison": comparison_path,
        "manifest": manifest_path,
    }


def prepare_unidirectional_stiffened_probe_decks(
    spec_path: Path,
    *,
    artifact_dir: Path,
    work_dir: Path,
    command: list[str] | None = None,
) -> dict[str, Path]:
    """Write CalculiX probe decks for the zero-eccentric unidirectional case."""

    loaded = load_validation_case(spec_path)
    if not isinstance(loaded, LocalABDCase) or loaded.model != "unidirectional":
        msg = "prepare_unidirectional_stiffened_probe_decks requires a unidirectional case."
        raise ValueError(msg)
    data = _load_spec(spec_path)
    patch = _unidirectional_stiffened_patch(loaded, data)
    load_cases = tuple(
        extraction_case.calculix_case() for extraction_case in _extraction_load_cases(data)
    )

    case_work_dir = work_dir / loaded.name
    case_work_dir.mkdir(parents=True, exist_ok=True)
    deck_paths: list[Path] = []
    for case_id, deck in render_unidirectional_stiffened_probe_decks(patch, load_cases).items():
        deck_path = case_work_dir / f"{case_id}.inp"
        deck_path.write_text(deck, encoding="utf-8")
        deck_paths.append(deck_path)

    summary_path = artifact_dir / "probe_summary.json"
    manifest_path = artifact_dir / "probe_manifest.json"
    write_json(
        summary_path,
        {
            "schema_version": "tensyl.validation.local-abd-probe.v1",
            "case_name": loaded.name,
            "model": loaded.model,
            "status": "review_deck_only",
            "solver_extraction_promoted": False,
            "deck_count": len(deck_paths),
            "deck_directory": str(case_work_dir),
            "notes": [
                "Decks use shared shell/beam nodes on the skin reference surface.",
                "The CalculiX rectangular beam proxy preserves target EA and EIy only.",
                "These decks are not promoted FE extraction artifacts.",
            ],
        },
    )
    manifest = ArtifactManifest(
        case_name=loaded.name,
        command=[] if command is None else command,
        inputs=[spec_path],
        outputs=[summary_path, manifest_path],
        metadata={
            "case_type": "local_abd",
            "model": loaded.model,
            "artifact_role": "calculix_probe_deck",
            "solver_required": False,
            "solver_extraction_promoted": False,
            "raw_work_dir": str(case_work_dir),
            "deck_paths": [str(path) for path in deck_paths],
            "unsupported_blocks": ["A", "B", "D", "As"],
            "reason_not_promoted": (
                "CalculiX rectangular beam sections cannot yet represent the "
                "Tensyl BeamSection stiffness tuple EA/EIy/EIz/GJ/kGAy/kGAz "
                "with audited equivalence."
            ),
        },
    )
    write_json(manifest_path, manifest.as_dict())
    return {"summary": summary_path, "manifest": manifest_path, "decks": case_work_dir}


def _stress_block_summary(table: CalculixStressTable, element_set: str) -> dict[str, Any]:
    filtered = table.table_for_set(element_set)
    means = filtered.component_means()
    return {
        "element_set": element_set.upper(),
        "row_count": len(filtered.rows),
        "component_means": means,
    }


def run_unidirectional_stiffened_probe(
    spec_path: Path,
    *,
    artifact_dir: Path,
    work_dir: Path,
    command: list[str] | None = None,
    project_root: Path | None = None,
) -> dict[str, Path]:
    """Run non-promoted CalculiX probe decks for a unidirectional stiffener."""

    root = Path.cwd() if project_root is None else project_root
    inventory = check_solver_inventory(root)
    if not inventory.ccx.ok or inventory.ccx.path is None:
        msg = "CalculiX/CCX is required for unidirectional stiffener probe runs."
        raise RuntimeError(msg)

    loaded = load_validation_case(spec_path)
    if not isinstance(loaded, LocalABDCase) or loaded.model != "unidirectional":
        msg = "run_unidirectional_stiffened_probe requires a unidirectional case."
        raise ValueError(msg)
    data = _load_spec(spec_path)
    load_cases = _extraction_load_cases(data)
    prepared = prepare_unidirectional_stiffened_probe_decks(
        spec_path,
        artifact_dir=artifact_dir,
        work_dir=work_dir,
        command=command,
    )
    case_work_dir = prepared["decks"]

    run_summaries: list[dict[str, Any]] = []
    raw_outputs: list[Path] = []
    for extraction_case in load_cases:
        subprocess.run(
            [inventory.ccx.path, extraction_case.case_id],
            cwd=case_work_dir,
            check=True,
            capture_output=True,
            text=True,
            timeout=120,
        )
        dat_path = case_work_dir / f"{extraction_case.case_id}.dat"
        raw_outputs.append(dat_path)
        table = parse_calculix_stress_dat(dat_path.read_text(encoding="utf-8"))
        skin = _stress_block_summary(table, "SKIN")
        stiffener = _stress_block_summary(table, "STIFFENER")
        run_summaries.append(
            {
                "case_id": extraction_case.case_id,
                "component": extraction_case.component,
                "magnitude": extraction_case.magnitude,
                "dat_path": str(dat_path),
                "stress_blocks": {
                    "SKIN": skin,
                    "STIFFENER": stiffener,
                },
                "checks": {
                    "skin_stress_rows_present": skin["row_count"] > 0,
                    "stiffener_stress_rows_present": stiffener["row_count"] > 0,
                },
            }
        )

    run_summary_path = artifact_dir / "probe_run_summary.json"
    run_manifest_path = artifact_dir / "probe_run_manifest.json"
    write_json(
        run_summary_path,
        {
            "schema_version": "tensyl.validation.local-abd-probe-run.v1",
            "case_name": loaded.name,
            "model": loaded.model,
            "status": "solver_probe_completed_not_promoted",
            "solver_extraction_promoted": False,
            "load_case_count": len(run_summaries),
            "load_cases": run_summaries,
            "notes": [
                "This run verifies executable CalculiX probe decks and stress block presence.",
                "It is not an FE-vs-Tensyl stiffness comparison.",
            ],
        },
    )
    manifest = ArtifactManifest(
        case_name=loaded.name,
        command=[] if command is None else command,
        inputs=[spec_path],
        outputs=[run_summary_path, run_manifest_path],
        metadata={
            "case_type": "local_abd",
            "model": loaded.model,
            "artifact_role": "calculix_probe_run",
            "solver_required": True,
            "solver_extraction_promoted": False,
            "ccx": inventory.ccx.as_dict(),
            "raw_work_dir": str(case_work_dir),
            "raw_outputs": [str(path) for path in raw_outputs],
            "unsupported_blocks": ["A", "B", "D", "As"],
            "reason_not_promoted": (
                "Probe runs verify deck execution and stress block availability only; "
                "stiffness extraction still requires an audited beam-section mapping."
            ),
        },
    )
    write_json(run_manifest_path, manifest.as_dict())
    return {
        "probe_summary": prepared["summary"],
        "probe_manifest": prepared["manifest"],
        "run_summary": run_summary_path,
        "run_manifest": run_manifest_path,
        "decks": case_work_dir,
    }
