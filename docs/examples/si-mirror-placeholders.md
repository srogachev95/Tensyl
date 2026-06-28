# SI Worked Examples

These examples mirror the US customary workflows with consistent SI inputs.
Tensyl does not convert units; the caller is responsible for using one unit
system throughout.

## Skin-Only Isotropic Stiffness

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=73.1e9, nu=0.33, density=2780.0)
stiffness = isotropic_plate(aluminum, thickness=0.0020)

assert stiffness.A.shape == (3, 3)
assert stiffness.B[0, 0] == 0.0
```

Assumed units:

| Quantity | Unit |
| --- | --- |
| Length | `m` |
| Force | `N` |
| Stress | `Pa` |
| Density | `kg/m^3` |
| Membrane stiffness | `N/m` |
| Bending stiffness | `N*m` |

## SI Orthogrid Sketch

```python
from tensyl import BeamSection

section = BeamSection(
    EA=1.4e7,
    EIy=43.0,
    EIz=12.0,
    GJ=8.0,
    kGAy=4.8e6,
    kGAz=3.9e6,
)
```

This page is runnable for the skin and section snippets. Full SI mirrors for
laminate, orthogrid, isogrid, sandwich, barrel, and dome workflows should use
independently reviewed SI input data before being treated as analyst examples.
