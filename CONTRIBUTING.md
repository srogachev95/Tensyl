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
uv run python scripts/check_docs_links.py site
```

Documentation is part of the product. Changes that alter behavior, public APIs,
mechanics assumptions, examples, or release workflows should update the relevant
documentation in the same change.

## Handbook Examples

Put complete runnable examples in `docs/examples/scripts/`. The public pages
include marked regions from those scripts with `pymdownx.snippets`; documentation
tests execute the same files. Keep prerequisites explicit when a page continues
an earlier example. Mark solver-input templates and conceptual fragments as such.

After changing example inputs, regenerate the displayed tables and plots:

```bash
uv run python docs/examples/scripts/render_handbook.py
uv run python docs/examples/scripts/stiffness_field_maps.py
```

Preserve public page URLs and heading anchors when moving a topic. The built-site
check covers the heading baseline, local links, scripts, and images. Review
changed pages at desktop and narrow widths as well as running the strict build.

## Engineering Diagrams

Regenerate the SVG schematics from their Python sources:

```bash
uv run python scripts/generate_handbook_diagrams.py
uv run python scripts/generate_section_diagrams.py
```

The handbook renderer uses the walkthrough's repeat dimensions and blade dimensions,
the cylinder's local frame, and analytic plate deformation shapes. Section
drawings use the section builders' wall segments and computed centroids. Keep
physical coordinates separate from page placement, use one scale per view, and
derive dimension endpoints from the geometry. Review rendered drawings for
symmetry, projection, signs, readable labels, and overlaps before committing.
The asset checks catch stale generated files; visual review checks the drawing.

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
