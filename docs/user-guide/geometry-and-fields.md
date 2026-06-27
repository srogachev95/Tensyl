# Geometry And Wall Fields

Tensyl separates local wall laws from shell geometry. Geometry supplies surface
points, frames, metrics, curvature, and integration measures. It does not change
the tangent-plane wall law.

## Built-In Surfaces

Available surfaces include:

- `FlatPlate`;
- `Cylinder`;
- `SphericalCap`;
- `Ellipsoid`.

Each surface exposes:

```python
point = surface.point_at(u, v)
```

The point contains position, tangent vectors, metric, curvature, Jacobian,
principal curvatures, and a local `Frame2D`.

## Constant Wall Field

```python
from tensyl import ConstantWallField, Cylinder

surface = Cylinder(radius=120.0, length=300.0)
field = ConstantWallField(wall)

local_wall = field.law_at(surface, 10.0, 0.25)
```

The wall tangent is unchanged. The law is rebound to the surface-point frame.

## Wall Atlas

`WallAtlas` samples a `WallField` on a rectangular parameter grid and performs
bilinear interpolation in canonical C8 storage.

```python
import math

from tensyl import WallAtlas

atlas = WallAtlas.from_field(
    surface,
    field,
    u_values=(0.0, 150.0, 300.0),
    v_values=(0.0, math.pi, 2.0 * math.pi),
)

interpolated = atlas.law_at(surface, 75.0, 0.5 * math.pi)
```

Atlas interpolation is a convenience for linear wall laws. Interpolation error
metadata should be reviewed before relying on a coarse grid.
