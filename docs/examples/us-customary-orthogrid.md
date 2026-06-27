# US Customary Orthogrid Wall

This example computes a first equivalent wall law for an orthogrid panel. The
numbers are illustrative and should not be used as allowables.

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

wall = result.law

assert wall.constant_tangent.shape == (8, 8)
assert result.diagnostics["symmetric"]
```

Review `result.validity.warnings` before using the wall law downstream.
