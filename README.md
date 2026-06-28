# Tensyl

Tensyl is a Python scientific-computing library for equivalent-stiffness
homogenization of stiffened plates and shells. It helps engineering teams build,
check, transform, and export local ABD stiffnesses for skins, laminates, and
stiffened repeating cells.

In one line: Tensyl replaces a panel full of stiffeners with a single equivalent
stiffness - a small, auditable stiffness matrix that behaves like the real thing
under global loads, without the cost of modeling every rib.

The public Python package name is `tensyl`.

## What Tensyl Computes

Tensyl computes a local constitutive stiffness in laminated-plate notation. The
primary object, `ABDStiffness`, maps generalized mid-surface strains, curvatures,
and transverse-shear strains to membrane resultants, bending resultants, and
transverse-shear resultants.

The canonical tangent is an 8 by 8 operator with these public blocks:

- `A`: membrane stiffness;
- `B`: membrane-bending coupling;
- `D`: bending and twisting stiffness;
- `As`: transverse-shear stiffness.

Tensyl keeps stiffness as the first-class result. Scalar equivalent moduli are
derived interpretations, not the product.

## Quick Start

For local development from this repository:

```bash
uv sync --dev
```

Then run a skin-only ABD stiffness:

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum_2024_like = IsotropicMaterial(
    E=10.6e6,      # psi
    nu=0.33,
    density=0.1,  # workflow-selected consistent mass unit
)

stiffness = isotropic_plate(aluminum_2024_like, thickness=0.080)

print(stiffness.A)   # membrane stiffness, lbf/in
print(stiffness.B)   # zero for a symmetric mid-surface isotropic skin
print(stiffness.D)   # bending stiffness, lbf*in
print(stiffness.As)  # transverse shear stiffness, lbf/in
```

Tensyl does not own a unit system. Inputs must already be in one consistent set
of units, and exported unit labels are metadata only. It will not rescue a mixed
unit deck. That is not spite; it is algebra.

## Homogenized Stiffener Cells

The tangent-plane homogenizer adds beam-stiffener contributions to a skin
stiffness. The energy method is the reference path for built-in cell workflows.

```python
from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)

skin = isotropic_plate(
    IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
    thickness=0.080,
)

section = BeamSection(
    EA=3.2e6,
    EIy=2.4e4,
    EIz=6.5e3,
    GJ=4.0e3,
    kGAy=1.1e6,
    kGAz=0.9e6,
)

cell = orthogrid_cell(
    skin=skin,
    stringer_section=section,
    rib_section=section,
    stringer_spacing=6.0,
    rib_spacing=8.0,
    stringer_eccentricity=0.45,
    rib_eccentricity=0.45,
)

result = EnergyHomogenizer().compute(
    cell,
    validity_context=ValidityContext(
        characteristic_height=0.50,
        pitch=8.0,
        min_radius=120.0,
        response_length=80.0,
    ),
)

print(result.stiffness.constant_tangent)
print(result.validity.warnings)
```

The result carries the homogenized stiffness, diagnostics, modeling assumptions,
and validity warnings. Warnings do not automatically invalidate a result; they
mark assumptions that an engineering workflow should review before using the
ABD stiffness in sizing, buckling, or finite-element work.

## What Tensyl Is Not

Tensyl is not a certification buckling solver, local stress recovery tool, or
replacement for detailed finite-element analysis. The tangent-plane
homogenization tools assume scale separation between stiffener pitch, stiffener
height, local curvature radius, and the structural response length of interest.

Use Tensyl to form and audit equivalent ABD stiffnesses. Use detailed analysis
for local buckling, crippling, joints, cutouts, load introduction, nonlinear
postbuckling, and final allowables.

## Documentation Map

The formal documentation is built with MkDocs from `docs/`.

- [Getting started](docs/getting-started/installation.md) covers setup and the
  shortest path to an ABD stiffness.
- [Background](docs/background/motivation.md) explains the engineering
  motivation and terminology.
- [Theory](docs/theory/equivalent-stiffness.md) documents ABD stiffnesses,
  conventions, tangent-plane homogenization, and validity limits.
- [User guide](docs/user-guide/materials-and-laminates.md) covers the main
  materials, cell, field, and solver-handoff workflows.
- [Examples](docs/examples/skin-only.md) provides worked examples and executable
  snippets.
- [API reference](docs/api/core.md) exposes the public Python interfaces.
- [References](docs/references.md) lists the external sources used by the
  mechanics documentation.

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

## Documentation Authoring

Documentation math should use `$...$` for inline equations and `$$...$$` for
display equations so the same Markdown renders in Obsidian and MkDocs.
