"""Research-grade validation helpers for Tensyl.

This package is deliberately outside ``src/tensyl``. Validation tooling may
import Tensyl; Tensyl must not import validation tooling.
"""

from tensyl_validation.artifacts import ArtifactManifest, write_json
from tensyl_validation.cases import SkinOnlySmokeCase, load_case, run_case
from tensyl_validation.metrics import skin_only_metrics
from tensyl_validation.solvers import SolverInventory, check_solver_inventory

__all__ = [
    "ArtifactManifest",
    "SkinOnlySmokeCase",
    "SolverInventory",
    "check_solver_inventory",
    "load_case",
    "run_case",
    "skin_only_metrics",
    "write_json",
]
