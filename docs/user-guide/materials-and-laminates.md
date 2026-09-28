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

## Uniform Temperature Changes

A heated laminate expands even when no mechanical load is applied. Supply
`alpha` on an isotropic material, or `alpha1` and `alpha2` along an orthotropic
ply's material axes, in inverse temperature units. `None` means unknown;
zero explicitly means no expansion. Negative coefficients are allowed.

`laminate_thermal_resultants(plies)` uses the same bottom-to-top stack and
midplane as `laminate_plate`. It returns a separate `ThermalResultants` with
`N_T` and `M_T` per unit **uniform** temperature change:

$$N_T=\sum_k\bar Q_k\bar\alpha_k(z_k-z_{k-1}),\qquad
M_T=\frac12\sum_k\bar Q_k\bar\alpha_k(z_k^2-z_{k-1}^2).$$

Here $\bar\alpha$ is the engineering strain vector, including twice the tensor
shear component. These are the thermal terms in classical laminate theory;
see the hygrothermal development in [NASA RP-1351](https://ntrs.nasa.gov/citations/19950009349).
The section relation is

$$r=C_8\eta-r_T\Delta T,\qquad r_T=[N_T,M_T,0,0]^T.$$

Thus full restraint gives negative thermal resultants. For free expansion,
solve using positive equivalent thermal loads:

```python
from tensyl import IsotropicMaterial, Ply, laminate_plate, laminate_thermal_resultants

plies = (Ply(IsotropicMaterial(E=70e9, nu=0.3, alpha=23e-6), 0.002),)
stiffness = laminate_plate(plies)
thermal = laminate_thermal_resultants(plies)
free_strain = stiffness.strains(thermal.equivalent_load(50.0))
```

For applied mechanical loads `r`, solve
`stiffness.strains(r + thermal.equivalent_load(delta_temperature))`. The existing
stiffness methods keep their mechanical meaning. Keep both objects in the same
frame and at the same reference surface. `thermal.rotate(angle_rad)` follows
`stiffness.rotate`; `thermal.shift_reference_surface(d)` changes the thermal
moment to `M_T - d*N_T`, matching the stiffness reference shift. Both preserve
energy-conjugate engineering conventions.

The helper refuses missing expansion coefficients. It assumes linear elastic,
temperature-independent properties and a uniform temperature change. It does
not include temperature gradients, moisture expansion, or thermal buckling.
