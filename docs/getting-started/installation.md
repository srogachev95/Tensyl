# Installation

Tensyl is developed for Python 3.12 and later.

```bash
uv add tensyl
```

For local development from the repository:

```bash
uv sync --dev
uv run pytest
```

The package import name is:

```python
import tensyl
```

## Unit Policy

Tensyl does not own a unit system: every input must already be in one consistent
set of units, and Tensyl will not catch you if it isn't. This matters enough to
get its own page — see [Units and Consistency](../user-guide/units-and-consistency.md)
for the rule, the reference tables, and the failure mode to watch for.

## Verification Commands

Contributors should run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv run mkdocs build --strict
```
