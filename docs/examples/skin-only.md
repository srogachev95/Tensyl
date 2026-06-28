# Skin and Laminate ABD Stiffness

This example starts with the smallest useful ABD stiffness, then replaces the
isotropic skin with a symmetric laminate.

All examples in this section use one consistent US customary unit set unless
noted otherwise: length in `in`, force in `lbf`, and stress in `psi`. Tensyl
does not convert units; it only carries unit labels when you export data. The
unit policy lives in [Units and Consistency](../user-guide/units-and-consistency.md).

## Isotropic Skin

Build a skin-only ABD stiffness for a flat reference surface. Because the
reference surface is the skin mid-surface, the membrane-bending coupling block
`B` should be zero.

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
stiffness = isotropic_plate(aluminum, thickness=0.080)

assert stiffness.A.shape == (3, 3)
assert stiffness.B.shape == (3, 3)
assert stiffness.D.shape == (3, 3)
assert stiffness.As.shape == (2, 2)
assert abs(stiffness.B).max() == 0.0
```

## Interpretation

This verifies the ABD block shapes and the expected zero coupling for a
symmetric isotropic skin. It does not include stiffeners, shell curvature, local
failure, or buckling. One thing at a time; the matrix has enough opinions
already.

## Symmetric Laminate

Now replace the isotropic skin with a small symmetric cross-ply laminate. The
workflow is still skin-only, but stiffness depends on ply material, thickness,
and angle.

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

The `A` block is not isotropic anymore. The two zero-degree plies make the local
`e1` direction stiffer than `e2`. The symmetric stack keeps `B` near zero, so
membrane strain and bending curvature are not coupled by the chosen reference
surface.

!!! note "Symmetric means symmetric about the reference surface"
    The laminate stack is supplied bottom-to-top. A visually tidy list of plies
    is not enough; the stiffness is symmetric only when the material, thickness,
    and angle sequence mirrors about the reference surface.
