# Stiffened Dome Concept Example

This example shows how to attach wall-law samples to a spherical cap. It is a
conceptual wall-field workflow: Tensyl does not automatically generate geodesic
stiffener layouts over a dome.

```python
from tensyl import ConstantWallField, IsotropicMaterial, SphericalCap, WallAtlas, isotropic_plate

dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
wall = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
field = ConstantWallField(wall)

atlas = WallAtlas.from_field(
    dome,
    field,
    u_values=(0.20, 0.60, 0.95),
    v_values=(0.0, 3.141592653589793, 6.283185307179586),
)

sample = atlas.law_at(dome, 0.60, 3.141592653589793)
assert sample.C8.shape == (8, 8)
```

For a real dome with varying pitch or stiffener direction, build or sample
local wall laws that are consistent with each surface-point frame. The
tangent-plane homogenizer remains local and flat; shell curvature enters
through the surface geometry and validity review.
