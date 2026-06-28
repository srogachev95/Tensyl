# Sampled Stiffness Atlas

`ABDAtlas` is useful when stiffness varies over a surface and you already have
sampled ABD stiffnesses. This example uses a deliberately simple variation:
skin thickness increases along the barrel station.

## Problem

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
