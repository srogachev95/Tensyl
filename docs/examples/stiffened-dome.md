# Stiffened Dome Concept Example

This example shows how to attach wall-law samples to spherical and ellipsoidal
surfaces. It is a conceptual wall-field workflow: Tensyl does not automatically
generate geodesic stiffener layouts over a dome.

```python
from tensyl import (
    ConstantWallField,
    Ellipsoid,
    IsotropicMaterial,
    Sphere,
    SphericalCap,
    WallAtlas,
    isotropic_plate,
)

complete_dome = Sphere(radius=96.0)
dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
ellipsoid = Ellipsoid(a=84.0, b=96.0, c=72.0)
wall = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
field = ConstantWallField(wall)

sphere_sample = field.law_at(complete_dome, 0.60, 3.141592653589793)

atlas = WallAtlas.from_field(
    ellipsoid,
    field,
    u_values=(0.30, 0.70),
    v_values=(0.0, 3.141592653589793),
)

sample = atlas.law_at(ellipsoid, 0.50, 0.5 * 3.141592653589793)
assert sphere_sample.C8.shape == (8, 8)
assert sample.C8.shape == (8, 8)
```

For a real dome with varying pitch or stiffener direction, build or sample
local wall laws that are consistent with each surface-point frame. The
tangent-plane homogenizer remains local and flat; shell curvature enters
through the surface geometry and validity review.
