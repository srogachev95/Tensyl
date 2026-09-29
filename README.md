<img src="https://raw.githubusercontent.com/srogachev95/Tensyl/main/docs/assets/brand/tensyl-logo.jpeg" alt="Tensyl logo" width="300">

# Tensyl

**Equivalent stiffness for stiffened plates and shells, in Python.**

Describe a skin, rib sections, and a repeating pattern. Tensyl combines their
strain energy into plate stiffness blocks for stretching (`A`), coupling (`B`),
bending (`D`), and transverse shear (`As`). Use the result to calculate strains,
recover rib forces, compare stiffness and mass, or prepare a shell analysis.

[Engineering handbook](https://srogachev95.github.io/Tensyl/) ·
[Worked panel](https://srogachev95.github.io/Tensyl/getting-started/first-abd-stiffness/) ·
[Verification](https://srogachev95.github.io/Tensyl/validation/) ·
[Changelog](https://github.com/srogachev95/Tensyl/blob/main/CHANGELOG.md)

## Install

Python 3.12 or later:

```bash
uv add tensyl
```

Or use `python -m pip install tensyl` in an active environment.

## Start with a Skin

Calculate a 2 mm aluminum plate using metres, newtons, and kilograms:

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=70e9, nu=0.33, density=2700)
skin_thickness = 0.002
skin = isotropic_plate(aluminum, thickness=skin_thickness)
```

The skin has membrane stiffness `A11 = 157.109 MN/m`, bending stiffness
`D11 = 52.3697 N m`, and areal mass `5.4 kg/m²`.
The [walkthrough](https://srogachev95.github.io/Tensyl/getting-started/first-homogenized-cell/) adds blade ribs,
explains the resulting stiffness and mass, then applies a membrane load.

## Build and Use a Panel Model

- **Materials:** isotropic skins, orthotropic laminates, stacking notation,
  density, and uniform-temperature thermal resultants.
- **Ribs:** beam stiffness input, geometry-derived thin-wall sections,
  laminated walls, and open or skin-closed hat torsion.
- **Patterns:** named grids, sandwich cores, independent rib families,
  custom graph cells, and drawn-versus-modeled rib-density checks.
- **Analysis workflows:** coupled load-to-strain solves, member forces,
  rotations, reference shifts, and stiffness/mass sweeps.
- **Shell properties:** constant or varying fields on plates, cylinders,
  spheres, cones, and ellipsoids; sampled stiffness atlases.
- **Handoff:** JSON/YAML artifacts, Abaqus general-section keywords,
  and orthotropic-cylinder coefficient extraction.

These capabilities are available in Tensyl 0.4.0. See the
[release notes](https://github.com/srogachev95/Tensyl/blob/v0.4.0/CHANGELOG.md)
for changes since 0.3.1. To run the handbook examples from this checkout:

```bash
uv sync --group dev
uv run python docs/examples/scripts/walkthrough.py
```

## Mechanics and Verification

The homogenizer follows Nemeth's equivalent-plate energy method. The handbook
explains [the mechanics](https://srogachev95.github.io/Tensyl/theory/tangent-plane-homogenization/),
[modeling choices](https://srogachev95.github.io/Tensyl/theory/validity/), and
[sources](https://srogachev95.github.io/Tensyl/references/).
Verification includes independent grid-formula checks, SP-8007 reconciliation,
and a retained CalculiX skin membrane/bending comparison.

See [CONTRIBUTING.md](https://github.com/srogachev95/Tensyl/blob/main/CONTRIBUTING.md)
for development and checks. Licensed under the
[MIT license](https://github.com/srogachev95/Tensyl/blob/main/LICENSE).
