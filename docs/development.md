# Development and Releases

Tensyl uses `uv` for dependency management and command execution.

Set up the development environment with:

```bash
uv sync --dev
```

Run the standard local verification suite before committing substantive changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv run mkdocs build --strict
```

These checks are the phase 0 quality gate. Hosted CI is intentionally deferred
for now; when CI is added, it should run the same commands.

## Versioning

Tensyl uses pre-1.0 semantic versioning while the mechanics kernel and public
APIs are still taking shape.

- Release versions use `0.y.z` until the project reaches a stable `1.0.0` API.
- Minor version bumps may include public API changes before `1.0.0`.
- Patch version bumps should be limited to compatible fixes and documentation
  corrections.
- Release tags should identify coherent package snapshots whose tests and
  documentation build pass.

The package version is currently declared in `pyproject.toml`.

## Package Layout

Tensyl uses the standard `src/` layout. Implementation code is organized by
mechanics boundary:

```text
src/tensyl/
    core/
    materials/
    sections/
    cells/
    homogenizers/
    verification/
```

Root modules such as `tensyl.constitutive` and `tensyl.laminates` remain as
compatibility exports. New implementation work should go into the focused
subpackage that owns the behavior.
