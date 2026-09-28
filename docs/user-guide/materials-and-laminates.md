# Materials and Laminates

Tensyl supports skin-only ABD stiffnesses for isotropic plates and orthotropic
laminates.

## Isotropic Plate

```python
from tensyl import IsotropicMaterial, isotropic_plate

material = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
stiffness = isotropic_plate(material, thickness=0.080)
```

Inputs must be consistent. In the US customary examples here, `E` is in `psi`
and `thickness` is in `in` — see [Units and Consistency](units-and-consistency.md).

## Orthotropic Laminate

Laminate plies are supplied bottom-to-top through the section thickness.

```python
import math

from tensyl import OrthotropicPlyMaterial, Ply, laminate_plate

ply_material = OrthotropicPlyMaterial(
    E1=20.0e6,
    E2=1.4e6,
    G12=0.8e6,
    nu12=0.28,
    G13=0.7e6,
    G23=0.55e6,
)

stiffness = laminate_plate(
    [
        Ply(ply_material, thickness=0.005, angle_rad=0.0),
        Ply(ply_material, thickness=0.005, angle_rad=math.pi / 2.0),
        Ply(ply_material, thickness=0.005, angle_rad=math.pi / 2.0),
        Ply(ply_material, thickness=0.005, angle_rad=0.0),
    ]
)
```

For a symmetric laminate about the reference surface, the `B` block should be
zero within numerical tolerance. Unsymmetric layups can produce nonzero
membrane-bending coupling.

## Angles and Stacking Strings

Use `Ply.from_degrees(material, thickness, angle_deg, label="")` when the
source drawing gives degrees. For equal-thickness plies of one material, the
same stack can be written as a stacking string:

```python
from tensyl import layup, laminate_plate

plies = layup(ply_material, 0.005, "[0/±45/90]s")
stiffness = laminate_plate(plies)
```

This expands, **bottom to top along `+n`**, to
`0, +45, -45, 90, 90, -45, +45, 0` degrees. The symmetric suffix mirrors the
whole stack and duplicates the middle ply. `[0/90]2s` first repeats `0, 90`
twice, then mirrors, giving `0, 90, 0, 90, 90, 0, 90, 0`. Reversing an
unsymmetric stack reverses its B block about the midplane, so stacking order
is part of the mechanics input.

| Syntax | Expansion |
| --- | --- |
| `±45` or `+-45` | `+45, -45` |
| `∓45` | `-45, +45` |
| `0_2` or `0₂` | `0, 0` |
| `±45_2` | `+45, -45, +45, -45` |
| `[0/90]2` | `0, 90, 0, 90` |

Angles may be signed decimals; spaces around entries are accepted. Repeat
counts must be positive integers. Nested brackets, commas, exponent notation,
and unrecognized suffixes raise `ValueError`. Use explicit `Ply` objects for
mixed materials or ply thicknesses.

## Shear Correction

`isotropic_plate` and `laminate_plate` expose transverse-shear behavior through
the `As` block. The shear correction factor is an explicit modeling choice; it
should be chosen consistently with the plate or shell theory used downstream.
