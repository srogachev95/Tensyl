# Stiffened Cone Concept Example

This example attaches a constant ABD stiffness to a conical frustum and uses the
local curvature radius in a validity context. Tensyl supports the smooth
frustum midsurface, not the cone apex.

```python
from tensyl import (
    ConicalFrustum,
    ConstantStiffnessField,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
)

surface = ConicalFrustum(radius_start=80.0, radius_end=96.0, length=120.0)
stiffness = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.080)
field = ConstantStiffnessField(stiffness)

point = surface.point_at(60.0, 0.0)
local_stiffness = field.stiffness_at(surface, point.u, point.v)

context = ValidityContext(
    characteristic_height=0.50,
    pitch=8.0,
    min_radius=point.min_radius,
    response_length=80.0,
)

assert local_stiffness.C8.shape == (8, 8)
assert context.min_radius == point.min_radius
```

If stiffener pitch or orientation changes along the frustum, provide a
pointwise `HomogenizedStiffnessField` cell factory or sample local stiffnesses into a
`ABDAtlas`.
