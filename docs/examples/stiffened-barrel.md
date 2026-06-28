# Stiffened Barrel Example

This example attaches a homogenized orthogrid ABD stiffness to a cylindrical
midsurface. It prepares stiffness-property data; it does not perform shell analysis.

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

surface = Cylinder(radius=radius, length=300.0)
field = ConstantStiffnessField(result.stiffness)
stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

assert stiffness_at_midbay.frame.label == "cylinder"
assert result.validity.p_over_R == 8.0 / radius
```

For `Cylinder`, `e1` is axial and `e2` is circumferential. The orthogrid
constructor maps stringers to `e1` and ribs to `e2`.

This does not choose loads, boundary conditions, knockdown factors, or buckling
margins.
