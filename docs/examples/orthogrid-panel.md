# Orthogrid Panel and Barrel

This example adds stiffeners to the skin, computes a homogenized ABD stiffness,
and attaches the result to a cylindrical midsurface. The numbers are
illustrative, not allowables.

## Orthogrid Panel

Build an orthogrid panel about the skin reference surface. Stringers run along
local `e1`; ribs run along local `e2`. Both stiffener families are external to
the `+n` side of the skin reference surface, so positive eccentricity should
create membrane-bending coupling.

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

assert stiffness.C8.shape == (8, 8)
assert result.diagnostics["symmetric"]
assert result.diagnostics["positive_semidefinite"]
assert stiffness.B[0, 0] > 0.0
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

The diagonal `A` terms show membrane stiffness added by the grid. Nonzero `B`
comes from eccentric stiffeners relative to the reference surface. Diagnostics
confirm the assembled tangent is symmetric and positive semidefinite for this
model; they do not prove local stiffener strength, crippling resistance, or a
shell buckling margin.

## Constant-Stiffness Barrel

Attach the same orthogrid stiffness to a cylindrical midsurface. This binds the
constant `C8` tangent to the cylinder frame at the requested point; it does not
recompute the local stiffened cell.

```python
from tensyl import ConstantStiffnessField, Cylinder

radius = 120.0
surface = Cylinder(radius=radius, length=300.0)
field = ConstantStiffnessField(result.stiffness)
stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

assert stiffness_at_midbay.frame.label == "cylinder"
assert stiffness_at_midbay.C8.shape == (8, 8)
assert result.validity.p_over_R == 8.0 / radius
```

For `Cylinder`, `e1` is axial, `e2` is circumferential, and `n` points outward.
The orthogrid constructor maps stringers to `e1` and ribs to `e2`.

The barrel radius enters the validity ratio `p_over_R`; it does not recalculate
the local orthogrid stiffness. This is still stiffness-property preparation.
Loads, boundary conditions, knockdown factors, and buckling margins belong to a
separate workflow.

!!! tip "Check the frame before the solver sees it"
    A constant field keeps the matrix fixed, but the solver still consumes
    stiffness in local directions. Confirm axial and circumferential axes before
    exporting the property. Axis swaps have excellent handwriting.
