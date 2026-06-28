# Stiffened Dome Concept Example

This example shows how to attach stiffness samples to spherical and ellipsoidal
surfaces. It is a conceptual stiffness-field workflow: Tensyl does not automatically
generate geodesic stiffener layouts over a dome.

```python
from tensyl import (
    ConstantStiffnessField,
    Ellipsoid,
    IsotropicMaterial,
    Sphere,
    SphericalCap,
    ABDAtlas,
    isotropic_plate,
)

complete_dome = Sphere(radius=96.0)
dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
ellipsoid = Ellipsoid(a=84.0, b=96.0, c=72.0)
stiffness = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
field = ConstantStiffnessField(stiffness)

sphere_sample = field.stiffness_at(complete_dome, 0.60, 3.141592653589793)

atlas = ABDAtlas.from_field(
    ellipsoid,
    field,
    u_values=(0.30, 0.70),
    v_values=(0.0, 3.141592653589793),
)

sample = atlas.stiffness_at(ellipsoid, 0.50, 0.5 * 3.141592653589793)
assert sphere_sample.C8.shape == (8, 8)
assert sample.C8.shape == (8, 8)
```

For a real dome with varying pitch or stiffener direction, build or sample
local ABD stiffnesses that are consistent with each surface-point frame. The
tangent-plane homogenizer remains local and flat; shell curvature enters
through the surface geometry and validity review.
