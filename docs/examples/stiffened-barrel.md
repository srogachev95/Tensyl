# Stiffened Barrel With Constant Stiffness

This example takes the orthogrid stiffness from the previous step and attaches
it to a cylindrical midsurface. The stiffness is constant over the barrel.

## Problem

Compute one homogenized orthogrid ABD stiffness, then bind it to a cylinder
frame at a point on the barrel.

```python
from tensyl import (
    BeamSection,
    ConstantStiffnessField,
    Cylinder,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)

radius = 120.0
surface = Cylinder(radius=radius, length=300.0)

skin = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1), thickness=0.080)
section = BeamSection(EA=3.2e6, EIy=2.4e4, EIz=6.5e3, GJ=4.0e3, kGAy=1.1e6, kGAz=0.9e6)
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
        min_radius=radius,
        response_length=80.0,
    ),
)

field = ConstantStiffnessField(result.stiffness)
stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

assert stiffness_at_midbay.frame.label == "cylinder"
assert stiffness_at_midbay.C8.shape == (8, 8)
assert result.validity.p_over_R == 8.0 / radius
```

## Interpretation

For `Cylinder`, `e1` is axial, `e2` is circumferential, and `n` points outward.
The orthogrid constructor maps stringers to `e1` and ribs to `e2`.

`ConstantStiffnessField` binds the same homogenized `C8` tangent to the cylinder
frame at each point. The barrel radius enters the validity ratio `p_over_R`; it
does not recalculate the local orthogrid stiffness.

This is still stiffness-property preparation. Loads, boundary conditions,
knockdown factors, and buckling margins belong to a separate workflow.
