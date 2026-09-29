# Installation

Tensyl requires Python 3.12 or later. Install the published package into your
project:

```bash
uv add tensyl
```

Or use pip in an active environment:

```bash
python -m pip install tensyl
```

Check the version with `python -c "import tensyl; print(tensyl.__version__)"`.

## From Source

The current-main handbook includes features added after 0.3.1. To run its examples:

```bash
git clone https://github.com/srogachev95/Tensyl.git
cd Tensyl
uv sync --group dev
uv run python docs/examples/scripts/walkthrough.py
```

## Unit Policy

Use one consistent unit system. This handbook uses metres, newtons, kilograms,
and kelvins for temperature differences. Tensyl works with numerical values;
[unit labels](../user-guide/units-and-consistency.md) describe the chosen system.

## Verification Commands

Contributor setup and checks live in
[CONTRIBUTING.md](https://github.com/srogachev95/Tensyl/blob/main/CONTRIBUTING.md).

Next: [Calculate the skin stiffness](first-abd-stiffness.md).
