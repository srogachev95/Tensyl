# Tensyl

Tensyl is a Python library for equivalent-wall homogenization of stiffened
thin-wall structures. It helps structural analysts build, check, transform, and
export local wall laws for skins, laminates, and stiffened repeating cells.

In one line: Tensyl replaces a panel full of stiffeners with a single equivalent
wall — a small, auditable stiffness matrix that behaves like the real thing under
global loads, without the cost of modeling every rib.

The public package name is `tensyl`.

!!! tip "New here? Read in this order"
    Start with [Background](background/motivation.md) for the why, then
    [Terminology](background/terminology.md) for the vocabulary — it is the
    glossary the rest of the manual leans on. Theory and the User Guide make a
    lot more sense once those two are in hand.

## What Tensyl Computes

Tensyl computes a local wall constitutive law in laminated-plate notation:

$$
\begin{bmatrix}
\mathbf N \\
\mathbf M \\
\mathbf Q
\end{bmatrix}
=
\mathbf C_\text{wall}
\begin{bmatrix}
\boldsymbol\epsilon^0 \\
\boldsymbol\kappa \\
\boldsymbol\gamma_s^0
\end{bmatrix}.
$$

The first public wall law is `LinearABDWall`. It stores the membrane stiffness
`A`, membrane-bending coupling `B`, bending/twisting stiffness `D`, and
transverse-shear stiffness `As` as one canonical $8\times8$ tangent operator.

## What Tensyl Is Not

Tensyl is not a certification buckling solver, local stress recovery tool, or
replacement for detailed finite-element analysis. The tangent-plane
homogenization tools assume scale separation between stiffener pitch, stiffener
height, local curvature radius, and the structural response length of interest.

Use Tensyl to form and audit equivalent wall laws. Use detailed analysis for
local buckling, crippling, joints, cutouts, load introduction, nonlinear
postbuckling, and final allowables.

## Documentation Map

- [Getting started](getting-started/installation.md) covers installation and the
  shortest path to a wall law.
- [Background](background/motivation.md) introduces the engineering motivation,
  history, and terminology.
- [Theory](theory/equivalent-wall.md) explains conventions, wall laws, and
  tangent-plane homogenization.
- [User guide](user-guide/materials-and-laminates.md) documents the main
  analyst workflows.
- [Examples](examples/us-customary-orthogrid.md) provides worked examples and
  executable snippets.
- [API reference](api/core.md) exposes the public Python interfaces.
- [References](references.md) lists the external sources used by the
  documentation.

## First Workflow

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=10.0e6, nu=0.33, density=0.1)
wall = isotropic_plate(aluminum, thickness=0.080)

print(wall.A)
print(wall.D)
```

This example uses a consistent US customary unit system: force in `lbf`, length
in `in`, stress in `psi`, and mass density in units compatible with the
analyst's workflow. Tensyl records unit labels in exported artifacts but does
not convert units.
