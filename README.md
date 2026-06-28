# Tensyl

Tensyl is a Python scientific-computing library for equivalent-stiffness homogenization
of stiffened plates and shells. The library provides a constitutive kernel,
tangent-plane stiffener-cell homogenizers, geometry/stiffness-field helpers, and
solver-neutral YAML/JSON export.

The formal documentation is built with MkDocs from `docs/`.

## Development

This repository uses `uv` for dependency management and command execution.

```bash
uv sync --dev
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv run mkdocs build --strict
```

The public Python package name is `tensyl`.

Documentation math should use `$...$` for inline equations and `$$...$$` for
display equations so the same Markdown renders in Obsidian and MkDocs.
