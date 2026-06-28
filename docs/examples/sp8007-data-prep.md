# SP-8007 Data Prep Example

This example prepares equivalent wall data that an analyst could hand to a
separate SP-8007-style cylinder workflow. Tensyl does not compute SP-8007
knockdown factors or margins.

```python
from tensyl import (
    BeamSection,
    Cylinder,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)
from tensyl.io import from_yaml, to_yaml

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
        min_radius=120.0,
        response_length=80.0,
    ),
)
surface = Cylinder(radius=120.0, length=300.0)

report = {
    "radius": surface.radius,
    "length": surface.length,
    "A11": result.law.A[0, 0],
    "B11": result.law.B[0, 0],
    "D11": result.law.D[0, 0],
    "As11": result.law.As[0, 0],
    "h_over_R": result.validity.h_over_R,
    "p_over_R": result.validity.p_over_R,
    "p_over_L_response": result.validity.p_over_L_response,
    "warnings": result.validity.warnings,
}

artifact = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)
loaded = from_yaml(artifact)

assert loaded.law.C8.shape == (8, 8)
assert report["p_over_R"] == 8.0 / 120.0
```

The report preserves stiffness blocks, geometry scalars, validity ratios, and
warnings. Equivalent orthotropic constants are a later reduction and are not
computed by this example.
