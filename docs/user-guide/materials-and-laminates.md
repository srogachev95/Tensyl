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

## Shear Correction

`isotropic_plate` and `laminate_plate` expose transverse-shear behavior through
the `As` block. The shear correction factor is an explicit modeling choice; it
should be chosen consistently with the plate or shell theory used downstream.
