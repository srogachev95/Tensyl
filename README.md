<img src="docs/assets/brand/tensyl-logo.jpeg" alt="Tensyl logo" width="420">

# Tensyl

Tensyl is a Python scientific-computing library for equivalent-stiffness
homogenization of stiffened plates and shells.

It takes the local things analysts actually have - skins, composite layups,
stiffener sections, repeated cells, curved shell surfaces, and solver handoff
constraints - and turns them into auditable ABD stiffness laws. The product is
not a magic scalar modulus. It is a local constitutive matrix with its
assumptions, diagnostics, coordinate frame, and validity warnings still attached.

In one line: Tensyl replaces a panel full of repeated stiffeners with a single
equivalent stiffness matrix that behaves like the panel under global loads,
without asking the solver to model every rib, stringer, and bay.

The public Python package name is `tensyl`.

## Why Tensyl Exists

Detailed stiffener-by-stiffener shell models are valuable, but they are expensive
when the design question is still local stiffness, not final local failure. Tensyl
sits in that gap. It helps you build the local wall law first, inspect it, compare
it, attach it to geometry, and hand it to the next analysis step in a form that
keeps the mechanics visible.

That means Tensyl is useful when you need to:

- compare skin, laminate, and stiffener layouts before committing to a detailed
  finite-element model;
- reduce orthogrid, isogrid, Kagome, hexagonal, star, or custom repeated cells
  into local ABD stiffnesses;
- keep membrane, bending, membrane-bending coupling, and transverse shear terms
  in one consistent operator;
- move stiffness data across flat panels, cylinders, domes, cones, and ellipsoids
  without losing the local frame;
- export stiffness and homogenization results to solver-neutral YAML or JSON.

Tensyl keeps the matrix honest. It reports symmetry, rank, positive-energy
checks, assumptions, and scale-separation warnings because those are part of the
answer, not bookkeeping.

## Install

```bash
uv add tensyl
```

or:

```bash
pip install tensyl
```

For local development from this repository:

```bash
uv sync --dev
```

## What You Can Build Today

Tensyl already covers the main pieces needed for first-pass equivalent-stiffness
workflows.

**Materials and skins**

- isotropic plate skins with transverse shear;
- orthotropic ply materials;
- bottom-to-top laminate stacks with ply angle, thickness, and density;
- canonical `A`, `B`, `D`, `As`, and `C8` stiffness storage.

**Stiffener sections**

- direct `BeamSection` input when you already have `EA`, `EI`, `GJ`, and shear
  stiffness products from a handbook, CAD workflow, or section solver;
- geometry-derived open thin-wall sections for blade, tee, zee, channel, and hat
  stiffeners;
- custom `ThinWallSegment` layouts for section shapes that do not deserve their
  own named constructor.

**Cell and pattern libraries**

- unidirectional and orthogrid cells;
- braced orthogrid cells;
- equilateral isogrid cells;
- isosceles triangle, Kagome, hexagonal, and star pattern cells;
- sandwich-core variants;
- graph-defined custom unit cells through `CellNode`, `CellEdge`, and
  `graph_unit_cell`.

**Homogenization and review**

- `EnergyHomogenizer` as the reference path;
- `DirectECHomogenizer` where the direct equilibrium-compatibility path applies;
- `HomogenizationResult` with stiffness, diagnostics, assumptions, and validity;
- scale-separation checks for stiffener height, pitch, curvature radius, response
  length, and membrane-bending coupling.

**Geometry and fields**

- flat plates, cylinders, spheres, spherical caps, conical frustums, and
  ellipsoids;
- constant stiffness fields;
- pointwise homogenized stiffness fields with local cell factories;
- sampled stiffness atlases with bilinear interpolation in canonical `C8` storage.

**External workflow handoff**

- YAML and JSON serialization for `ABDStiffness` and `HomogenizationResult`;
- schema versioning, unit labels, diagnostics, assumptions, and validity metadata;
- solver-neutral artifacts that downstream tooling can read without guessing what
  convention produced the numbers.

## Example 1: A Skin-Only ABD Stiffness

Start with the smallest useful stiffness: an isotropic skin about its mid-surface.
The `B` block is zero because this reference surface is symmetric.

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
stiffness = isotropic_plate(aluminum, thickness=0.080)

print(stiffness.A)   # membrane stiffness
print(stiffness.B)   # membrane-bending coupling
print(stiffness.D)   # bending stiffness
print(stiffness.As)  # transverse-shear stiffness
```

The canonical tangent is an `8 x 8` matrix. The named blocks are views into that
operator:

- `A`: membrane stiffness;
- `B`: membrane-bending coupling;
- `D`: bending and twisting stiffness;
- `As`: transverse-shear stiffness.

Tensyl keeps stiffness as the first-class result. Scalar equivalent moduli are
derived interpretations, not the product.

## Example 2: A Composite Laminate

Replace the isotropic skin with a symmetric cross-ply laminate. The workflow is
still skin-only, but the stiffness now comes from ply material, ply thickness,
and ply angle.

```python
import math

from tensyl import OrthotropicPlyMaterial, Ply, laminate_plate

carbon_epoxy = OrthotropicPlyMaterial(
    E1=18.0e6,
    E2=1.4e6,
    G12=0.75e6,
    nu12=0.28,
    G13=0.75e6,
    G23=0.50e6,
    density=0.058,
)

stiffness = laminate_plate(
    (
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.5 * math.pi),
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
    )
)

assert stiffness.C8.shape == (8, 8)
assert abs(stiffness.B).max() < 1.0e-9
```

The two zero-degree plies make the local `e1` direction stiffer than `e2`. The
symmetric stack keeps `B` near zero, so membrane strain and bending curvature are
not coupled by the chosen reference surface.

## Example 3: A Geometry-Derived Orthogrid

If you already know stiffener stiffness products, pass a `BeamSection` directly.
If you have thin-wall dimensions, let Tensyl compute the section properties first.

```python
from tensyl import (
    EnergyHomogenizer,
    IsotropicMaterial,
    blade_section,
    hat_section,
    isotropic_plate,
    orthogrid_cell,
)

aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
skin_thickness = 0.080
skin = isotropic_plate(aluminum, thickness=skin_thickness)

stringer = hat_section(
    material=aluminum,
    web_height=0.50,
    web_thickness=0.050,
    crown_width=0.40,
    crown_thickness=0.050,
    flange_width=0.20,
    flange_thickness=0.050,
)

rib = blade_section(
    material=aluminum,
    height=0.50,
    thickness=0.050,
    shear_correction_y=5.0 / 6.0,
    shear_correction_z=5.0 / 6.0,
)

skin_face_offset = 0.5 * skin_thickness
cell = orthogrid_cell(
    skin=skin,
    stringer_section=stringer.section,
    rib_section=rib.section,
    stringer_spacing=6.0,
    rib_spacing=8.0,
    stringer_eccentricity=skin_face_offset + stringer.centroid_z,
    rib_eccentricity=skin_face_offset + rib.centroid_z,
)

result = EnergyHomogenizer().compute(cell)

print(result.stiffness.A)
print(result.stiffness.B)
print(result.diagnostics)
print(result.validity.warnings)
```

The result carries the homogenized stiffness, diagnostics, modeling assumptions,
and validity warnings. Nonzero `B` is not a nuisance here; it is the stiffness
consequence of eccentric stiffeners relative to the chosen reference surface.

## Example 4: A Custom Cell

Named constructors are convenience. When the topology is your own, build the
tangent-plane graph directly.

```python
from tensyl import BeamSection, CellEdge, CellNode, EnergyHomogenizer, graph_unit_cell

section = BeamSection(
    EA=3.2e6,
    EIy=2.4e4,
    EIz=6.5e3,
    GJ=4.0e3,
    kGAy=1.1e6,
    kGAz=0.9e6,
)

custom = graph_unit_cell(
    area=48.0,
    skin=skin,
    nodes=(
        CellNode(0.0, 0.0),
        CellNode(6.0, 0.0),
        CellNode(0.0, 8.0),
    ),
    edges=(
        CellEdge(0, 1, section, eccentricity=0.45),
        CellEdge(0, 2, section, eccentricity=0.45),
    ),
)

custom_result = EnergyHomogenizer().compute(custom)
```

This is the escape hatch for custom implementations: you provide the cell area,
nodes, edges, sections, and eccentricities; Tensyl canonicalizes the beam-member
contributions and computes the equivalent local wall law.

## Example 5: Put the Stiffness on a Shell

Geometry is separate from constitutive stiffness. A cylinder supplies local
frames and curvature context; it does not secretly rewrite the ABD matrix.

```python
from tensyl import ConstantStiffnessField, Cylinder

surface = Cylinder(radius=120.0, length=300.0)
field = ConstantStiffnessField(result.stiffness)

stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

assert stiffness_at_midbay.frame.label == "cylinder"
assert stiffness_at_midbay.C8.shape == (8, 8)
```

For variable structure, use `HomogenizedStiffnessField` to rebuild the local cell
at each surface point, or sample already-computed stiffnesses into an `ABDAtlas`.
That is where station-dependent pitch, thickness, material, section, and
stiffener angle belong.

## Example 6: Export the Result

Hand off the result, not just the matrix, when you can. The result preserves the
diagnostics and validity context that make the matrix worth trusting.

```python
from pathlib import Path

from tensyl.io import read_yaml, to_yaml, write_yaml

text = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)

write_yaml(
    result,
    Path("stiffness.yaml"),
    units={"length": "in", "force": "lbf", "stress": "psi"},
)

same_result = read_yaml(Path("stiffness.yaml"))
```

Tensyl records unit labels but does not infer or convert units. Inputs and
outputs must already share one consistent system. It will not rescue a mixed
unit deck. That is not spite; it is algebra.

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
- [Background](docs/background/motivation.md) explains the engineering motivation
  and terminology.
- [Theory](docs/theory/equivalent-stiffness.md) documents ABD stiffnesses,
  conventions, tangent-plane homogenization, and validity limits.
- [User guide](docs/user-guide/materials-and-laminates.md) covers materials,
  cells, sections, geometry, fields, and external workflows.
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

Release notes are tracked in [CHANGELOG.md](CHANGELOG.md), and contribution
workflow details are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Documentation Authoring

Documentation math should use `$...$` for inline equations and `$$...$$` for
display equations so the same Markdown renders in Obsidian and MkDocs.
