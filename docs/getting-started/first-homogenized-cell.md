# First Homogenized Cell

A real panel may contain hundreds of stiffeners. Tensyl starts with one
repeating patch and replaces that detailed pattern with an equivalent ABD
stiffness for the whole panel.

This example uses an orthogrid: one member family runs along local `e1`, and a
second runs along local `e2`. The repeat box is `8.0` units wide along `e1` and
`6.0` units high along `e2`. Tensyl calls those dimensions `e1_pitch` and
`e2_pitch`. The `e1` members are therefore `6.0` units apart, while the `e2`
members are `8.0` units apart.

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
    EA=3.2e6,    # lbf
    EIy=2.4e4,   # lbf*in^2
    EIz=6.5e3,   # lbf*in^2
    GJ=4.0e3,    # lbf*in^2
    kGAy=1.1e6,  # lbf
    kGAz=0.9e6,  # lbf
)

cell = orthogrid_cell(
    skin=skin,
    e1_section=section,
    e2_section=section,
    e1_pitch=8.0,
    e2_pitch=6.0,
    e1_axial_eccentricity=0.45,
    e2_axial_eccentricity=0.45,
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

stiffness = result.stiffness
print(result.validity.warnings)
```

The result keeps more than the four stiffness blocks:

- `stiffness` is the equivalent `ABDStiffness`;
- `diagnostics` reports basic matrix checks, including symmetry and unsupported
  deformation modes;
- `assumptions` records modeling choices made during the calculation;
- `validity` reports scale-separation and coupling warnings.

Warnings do not automatically invalidate a result. They mark assumptions that an
engineering workflow should review before using the ABD stiffness in sizing,
buckling, or finite-element work.

In this example both stiffener centroids sit on the `+n` side of the skin
reference surface. Their positive offsets therefore create a nonzero `B` block,
which couples stretching and bending.

Next: [Homogenization and Results](../user-guide/homogenization.md).
