from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _imports_for(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            imports.add(node.module)
    return imports


def test_geometry_does_not_depend_on_cells_homogenizers_fields_or_adapters() -> None:
    forbidden_prefixes = (
        "tensyl.adapters",
        "tensyl.cells",
        "tensyl.fields",
        "tensyl.homogenizers",
        "tensyl.io",
    )
    geometry_files = sorted((ROOT / "src" / "tensyl" / "geometry").glob("*.py"))

    violations: list[str] = []
    for path in geometry_files:
        for module in _imports_for(path):
            if module.startswith(forbidden_prefixes):
                violations.append(f"{path.relative_to(ROOT)} imports {module}")

    assert violations == []


def test_fields_do_not_depend_on_external_workflow_layers() -> None:
    forbidden_prefixes = ("tensyl.adapters", "tensyl.io", "tensyl.optimize")
    field_files = sorted((ROOT / "src" / "tensyl" / "fields").glob("*.py"))

    violations: list[str] = []
    for path in field_files:
        for module in _imports_for(path):
            if module.startswith(forbidden_prefixes):
                violations.append(f"{path.relative_to(ROOT)} imports {module}")

    assert violations == []


def test_io_does_not_depend_on_solver_or_optimization_layers() -> None:
    forbidden_prefixes = ("tensyl.adapters", "tensyl.optimize")
    io_files = sorted((ROOT / "src" / "tensyl" / "io").glob("*.py"))

    violations: list[str] = []
    for path in io_files:
        for module in _imports_for(path):
            if module.startswith(forbidden_prefixes):
                violations.append(f"{path.relative_to(ROOT)} imports {module}")

    assert violations == []
