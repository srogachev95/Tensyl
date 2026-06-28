# Contributing

Tensyl is a Python 3.12+ scientific library. The public import name is
`tensyl`.

## Development Setup

Use `uv` for dependency management and command execution:

```bash
uv sync --dev
```

Run the full local verification set before opening a pull request:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv run mkdocs build --strict
```

Documentation is part of the product. Changes that alter behavior, public APIs,
mechanics assumptions, examples, or release workflows should update the relevant
documentation in the same change.

## Packaging Checks

Build the release artifacts locally with:

```bash
uv build --out-dir dist
uvx twine check dist/*
```

For an install smoke test, use a fresh temporary environment and install the
built wheel:

```bash
uv venv /tmp/tensyl-wheel-smoke
uv pip install --python /tmp/tensyl-wheel-smoke/bin/python dist/tensyl-*.whl
/tmp/tensyl-wheel-smoke/bin/python -c "import tensyl; print(tensyl.__version__)"
```

## Release Process

Releases are built from Git tags and published to PyPI through Trusted
Publishing. Do not add PyPI API tokens to the repository.

1. Confirm the verification commands pass on `main`.
2. Confirm the PyPI project name `tensyl` still points to this project.
3. Create an annotated tag such as `v0.1.0`.
4. Push the tag to GitHub.
5. Approve the `pypi` environment if GitHub requests approval.
6. Install the published wheel in a fresh environment and run a smoke import.

Release notes should be reflected in `CHANGELOG.md` before the tag is created.
