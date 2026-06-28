# Laminate Skin ABD Stiffness

This example replaces the isotropic skin with a small symmetric laminate. The
workflow is still skin-only, but now stiffness depends on ply material,
thickness, and angle.

## Problem

Build a symmetric cross-ply laminate. The stack is symmetric about the reference
surface, so membrane-bending coupling should remain negligible.

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
assert stiffness.A[0, 0] > stiffness.A[1, 1]
```

## Interpretation

The `A` block is not isotropic anymore. The two zero-degree plies make the local
`e1` direction stiffer than `e2`. The symmetric stack keeps `B` near zero, so
membrane strain and bending curvature are not coupled by the chosen reference
surface.
