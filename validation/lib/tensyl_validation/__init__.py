"""Research-grade validation helpers for Tensyl.

This package is deliberately outside ``src/tensyl``. Validation tooling may
import Tensyl; Tensyl must not import validation tooling.
"""

from tensyl_validation.artifacts import ArtifactManifest, write_json
from tensyl_validation.cases import SkinOnlySmokeCase, load_case, run_case
from tensyl_validation.local_abd import LocalABDCase, load_local_abd_case, target_stiffness
from tensyl_validation.metrics import skin_only_metrics
from tensyl_validation.solvers import SolverInventory, check_solver_inventory

__all__ = [
    "ArtifactManifest",
    "LocalABDCase",
    "SkinOnlySmokeCase",
    "SolverInventory",
    "check_solver_inventory",
    "load_case",
    "load_local_abd_case",
    "run_case",
    "skin_only_metrics",
    "target_stiffness",
    "write_json",
]
