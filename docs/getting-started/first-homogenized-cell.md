# First Homogenized Cell

Tangent-plane homogenization adds beam-stiffener contributions to a skin wall
law. The energy homogenizer is the reference path.

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

stringer = BeamSection(
    EA=3.2e6,    # lbf
    EIy=2.4e4,   # lbf*in^2
    EIz=6.5e3,   # lbf*in^2
    GJ=4.0e3,    # lbf*in^2
    kGAy=1.1e6,  # lbf
    kGAz=0.9e6,  # lbf
)

cell = orthogrid_cell(
    skin=skin,
    stringer_section=stringer,
    rib_section=stringer,
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
print(result.validity.warnings)
```

The result carries:

- `law`: a `LinearABDWall`;
- `diagnostics`: symmetry, rank, and positive-semidefinite checks;
- `assumptions`: modeling assumptions recorded by the homogenizer;
- `validity`: scale-separation and coupling warnings.

Warnings do not automatically invalidate a result. They mark assumptions that an
analyst should review before using the wall law in a sizing, buckling, or
finite-element workflow.

In this example the positive eccentricities place both stiffener centroids on
the `+n` side of the skin reference surface, so the homogenized wall has a
nonzero membrane-bending coupling block `B`.

Next: [Result Interpretation](../user-guide/result-interpretation.md).
