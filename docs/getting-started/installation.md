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

Tensyl does not own a unit system. All numeric inputs must already be in one
consistent unit system.

For US customary examples in this manual, use:

| Quantity | Unit |
| --- | --- |
| Length | `in` |
| Force | `lbf` |
| Stress | `psi` |
| Moment | `lbf*in` |
| Membrane stiffness | `lbf/in` |
| Bending stiffness | `lbf*in` |

For SI examples, use `m`, `N`, and `Pa`. Do not mix unit systems inside one
wall law or one cell.

## Verification Commands

Contributors should run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
uv run mkdocs build --strict
```
