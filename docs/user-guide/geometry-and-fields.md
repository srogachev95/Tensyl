# Geometry And Wall Fields

Tensyl separates local wall laws from shell geometry. Geometry supplies surface
points, frames, metrics, curvature, and integration measures. It does not change
the tangent-plane wall law.

## Built-In Surfaces

Available surfaces include:

- `FlatPlate`;
- `Cylinder`;
- `Sphere`;
- `SphericalCap`;
- `ConicalFrustum`;
- `Ellipsoid`.

Each surface exposes:

```python
point = surface.point_at(u, v)
```

The point contains position, tangent vectors, metric, curvature, Jacobian,
principal curvatures, and a local `Frame2D`.

The wall stiffness matrix remains local. Coordinates answer "where is this
surface point?", the local frame answers "what are the 1/2/n directions?", and
the ABD/shear law is interpreted in that local frame. A constant isotropic or
laminate wall law may be bound to many surface points even when the frame or
curvature changes across the surface.

Tensyl uses signed curvature from the surface normal convention. Built-in
convex surfaces use outward normals, so their nonzero principal curvatures are
negative. `SurfacePoint.min_radius` is the positive radius magnitude to use in
scale-separation validity checks. These conventions follow the standard first
and second fundamental form treatment of parametric surfaces listed in
[References](../references.md).

`Sphere` and `SphericalCap` use spherical coordinates `(phi, theta)`, with
`e1` in the meridional direction and `e2` in the circumferential direction.
Their single chart excludes poles. `Ellipsoid` uses the same latitude-longitude
style chart; for a triaxial ellipsoid the coordinate tangent directions are not
generally orthogonal, so `e1` follows the meridional coordinate direction and
`e2` is the right-handed orthonormal tangent completion. `ConicalFrustum` uses
`(x, theta)` and excludes apex singularities.

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

## Choosing A Response Length

`ValidityContext.response_length` should represent the structural response mode
you intend to model, such as an expected buckle half-wavelength, analysis
feature size, or load redistribution length. It should not default blindly to
the global part length. A pitch that is small compared with the whole barrel can
still be too large for a short-wavelength local response.

Next: [Stiffened Surfaces](stiffened-surfaces.md).
