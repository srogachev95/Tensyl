# Installation

Tensyl 0.4.0 requires Python 3.12 or later. Install the published package into
your project:

```bash
uv add tensyl
```

Or use pip in an active environment:

```bash
python -m pip install tensyl
```

Check the version with `python -c "import tensyl; print(tensyl.__version__)"`.

This handbook's examples use 0.4.0. To install that exact version, use
`python -m pip install tensyl==0.4.0`. When updating from 0.3.1, see the
[migration notes](https://github.com/srogachev95/Tensyl/blob/v0.4.0/CHANGELOG.md#updating-from-031).

## From Source

Clone the release source to run the complete example scripts:

```bash
git clone --branch v0.4.0 https://github.com/srogachev95/Tensyl.git
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
