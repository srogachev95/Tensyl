# Non-Constant Homogenized Stiffness Field

This example is the first one where Tensyl recomputes the local homogenized
stiffness at each surface point. The barrel geometry supplies the local frame
and curvature radius; the cell factory supplies the pointwise stiffener layout.

## Problem

Model a cylindrical barrel where stringer spacing increases with axial station.
Because spacing changes, the local orthogrid ABD stiffness should also change.

```python
from tensyl import (
    BeamSection,
    Cylinder,
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    IsotropicMaterial,
    StiffnessCache,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)

surface = Cylinder(radius=120.0, length=300.0)
material = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
section = BeamSection(EA=3.2e6, EIy=2.4e4, EIz=6.5e3, GJ=4.0e3, kGAy=1.1e6, kGAz=0.9e6)


def cell_factory(surface, point):
    del surface
    stringer_spacing = 6.0 + point.u / 150.0
    rib_spacing = 8.0
    skin = isotropic_plate(material, thickness=0.080, frame=point.frame)
    return orthogrid_cell(
        skin=skin,
        stringer_section=section,
        rib_section=section,
        stringer_spacing=stringer_spacing,
        rib_spacing=rib_spacing,
        stringer_eccentricity=0.45,
        rib_eccentricity=0.45,
        frame=point.frame,
    )


def validity_context(point, cell):
    return ValidityContext(
        characteristic_height=0.50,
        pitch=max(cell.metadata["stringer_spacing"], cell.metadata["rib_spacing"]),
        min_radius=point.min_radius,
        response_length=80.0,
    )


field = HomogenizedStiffnessField(
    surface,
    cell_factory,
    EnergyHomogenizer(),
    cache=StiffnessCache(),
    validity_context_factory=validity_context,
)

station_0 = field.stiffness_at(surface, 0.0, 0.0)
station_150 = field.stiffness_at(surface, 150.0, 0.0)

assert station_0.frame.label == "cylinder"
assert station_150.validity is not None
assert station_0.A[0, 0] > station_150.A[0, 0]
assert station_150.validity.p_over_R == 8.0 / 120.0
```

## Interpretation

The stiffness changes because the cell factory changes the local cell, not
because the cylinder secretly curves the ABD matrix. At each point:

1. `surface.point_at(u, v)` supplies the local frame and `min_radius`.
2. `cell_factory` builds a skin and orthogrid cell in that frame.
3. `EnergyHomogenizer` computes the local ABD stiffness.
4. `validity_context` attaches scale-separation ratios for that point.

This is the pattern to use when a real structure has station-dependent pitch,
section, material, laminate, or stiffener orientation.
