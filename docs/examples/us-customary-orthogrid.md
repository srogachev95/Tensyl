# US Customary Orthogrid Stiffness

This example computes a first equivalent ABD stiffness for an orthogrid panel. The
numbers are illustrative and should not be used as allowables.

## Problem

Build a US customary orthogrid ABD stiffness about the skin reference surface. Both
stringers and ribs are external to the `+n` side, so the eccentricity is
positive and membrane-bending coupling is expected.

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

stiffness = result.stiffness

assert stiffness.constant_tangent.shape == (8, 8)
assert result.diagnostics["symmetric"]
assert result.stiffness.B[0, 0] > 0.0
```

Review `result.validity.warnings` before using the ABD stiffness downstream.

## Selected Output

Rounded diagonal values:

| Block | Diagonal values |
| --- | --- |
| `A` | `1.485e6`, `1.352e6`, `3.990e5` `lbf/in` |
| `B` | `2.400e5`, `1.800e5`, `-3.609e4` `lbf` |
| `D` | `1.133e5`, `8.559e4`, `1.670e4` `lbf*in` |
| `As` | `4.157e5`, `3.782e5` `lbf/in` |

## Interpretation

The diagonal `A` terms show the membrane stiffness added by the grid. Nonzero
`B` comes from eccentric stiffeners relative to the reference surface.
Diagnostics confirm the assembled tangent is symmetric and positive
semidefinite for this model; they do not prove local stiffener strength,
crippling resistance, or shell buckling margin.
