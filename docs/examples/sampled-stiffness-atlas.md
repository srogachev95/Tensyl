# Variable Stiffness Fields

These examples cover two ways to represent stiffness that varies over a surface:
interpolate sampled ABD stiffnesses with `ABDAtlas`, or recompute the local
homogenized cell at each surface point.

## Sampled Stiffness Atlas

Sample a station-varying skin field on a cylinder and interpolate between the
samples.

```python
import math

from tensyl import ABDAtlas, Cylinder, IsotropicMaterial, isotropic_plate


class TaperedSkinField:
    def __init__(self, material):
        self.material = material

    def stiffness_at(self, surface, u, v):
        point = surface.point_at(u, v)
        thickness = 0.070 + 0.00010 * point.u
        return isotropic_plate(
            self.material,
            thickness=thickness,
            frame=point.frame,
            metadata={"thickness": thickness},
        )


surface = Cylinder(radius=120.0, length=300.0)
field = TaperedSkinField(IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1))

atlas = ABDAtlas.from_field(
    surface,
    field,
    u_values=(0.0, 150.0, 300.0),
    v_values=(0.0, math.pi),
)

root = atlas.stiffness_at(surface, 0.0, 0.0)
mid = atlas.stiffness_at(surface, 75.0, 0.5 * math.pi)
tip = atlas.stiffness_at(surface, 300.0, math.pi)

assert root.A[0, 0] < mid.A[0, 0] < tip.A[0, 0]
assert mid.frame.label == "cylinder"
assert atlas.metadata["interpolation"] == "bilinear_c8"
```

## Interpretation

The atlas interpolates sampled canonical `C8` matrices. It does not know why the
samples vary; here the reason is skin thickness. In a real workflow, the samples
could come from measurements, sizing output, or a more expensive local model.

Use a grid that resolves the physical variation you intend to represent. A
coarse atlas is convenient, not prophetic.

!!! warning "Interpolation is not mechanics"
    `ABDAtlas` interpolates sampled matrices. It does not know whether the
    underlying structure varies smoothly, whether the sample grid is dense
    enough, or whether a sharp design change sits between two stations.

## Pointwise Homogenized Field

Use `HomogenizedStiffnessField` when the local cell definition should be rebuilt
from the surface point. This example varies stringer spacing with axial station,
so the local orthogrid ABD stiffness changes with station too.

```python
from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    StiffnessCache,
    ValidityContext,
    orthogrid_cell,
)

section = BeamSection(EA=3.2e6, EIy=2.4e4, EIz=6.5e3, GJ=4.0e3, kGAy=1.1e6, kGAz=0.9e6)


def cell_factory(surface, point):
    del surface
    stringer_spacing = 6.0 + point.u / 150.0
    rib_spacing = 8.0
    skin = isotropic_plate(field.material, thickness=0.080, frame=point.frame)
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


homogenized = HomogenizedStiffnessField(
    surface,
    cell_factory,
    EnergyHomogenizer(),
    cache=StiffnessCache(),
    validity_context_factory=validity_context,
)

station_0 = homogenized.stiffness_at(surface, 0.0, 0.0)
station_150 = homogenized.stiffness_at(surface, 150.0, 0.0)

assert station_0.frame.label == "cylinder"
assert station_150.validity is not None
assert station_0.A[0, 0] > station_150.A[0, 0]
assert station_150.validity.p_over_R == 8.0 / 120.0
```

The stiffness changes because the cell factory changes the local cell. The
cylinder itself does not curve the ABD matrix. At each point:

1. `surface.point_at(u, v)` supplies the local frame and `min_radius`.
2. `cell_factory` builds a skin and orthogrid cell in that frame.
3. `EnergyHomogenizer` computes the local ABD stiffness.
4. `validity_context` attaches scale-separation ratios for that point.

Use this pattern when the structure has station-dependent pitch, section,
material, laminate, or stiffener orientation.
