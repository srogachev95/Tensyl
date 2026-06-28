# Geometry And Stiffness Fields

Tensyl separates local ABD stiffnesses from shell geometry. Geometry supplies surface
points, frames, metrics, curvature, and integration measures. It does not change
the tangent-plane ABD stiffness.

That last sentence is important enough to say plainly. A barrel, cone, sphere,
or ellipsoid changes where the tangent plane lives, how its local axes are
oriented, and which curvature radius should be used in validity checks. It does
not automatically add shell-curvature terms to a constant ABD matrix. The matrix
changes only when the stiffness field supplies different local stiffness data at
different surface points.

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

The ABD stiffness matrix remains local. Coordinates answer "where is this
surface point?", the local frame answers "what are the 1/2/n directions?", and
the ABD/shear stiffness is interpreted in that local frame. A constant isotropic or
laminate ABD stiffness may be bound to many surface points even when the frame or
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

## What Changes When You Choose A Surface

Choosing a surface changes the geometric context around the ABD law:

- `frame`: the local directions for membrane strain, curvature, transverse
  shear, resultants, stiffener angle, and eccentricity sign;
- `metric` and `jacobian`: the coordinate-to-physical distance and area
  information a later surface workflow needs;
- `curvature`, `principal_curvatures`, and `min_radius`: the curvature data used
  to judge whether the tangent-plane approximation is credible for the chosen
  response.

For a `Cylinder`, `e1` is axial, `e2` is circumferential, and `n` points outward.
The positive minimum radius is the cylinder radius. Attaching a constant
orthogrid ABD stiffness to the cylinder therefore changes the frame label and
validity context, not the numeric `C8` matrix.

For an `Ellipsoid`, the local frame and curvature change from point to point.
That does not make an isotropic constant-field `C8` vary. It does mean a
pointwise stiffened-cell model must define each local cell in the current surface
frame. If the physical stiffener pitch, angle, section, or eccentricity changes
over the ellipsoid, encode that through `HomogenizedStiffnessField` or sampled
`ABDAtlas` values.

## Constant Stiffness Field

```python
from tensyl import ConstantStiffnessField, Cylinder

surface = Cylinder(radius=120.0, length=300.0)
field = ConstantStiffnessField(stiffness)

local_stiffness = field.stiffness_at(surface, 10.0, 0.25)
```

The stiffness tangent is unchanged. The stiffness is rebound to the surface-point frame.

## Stiffness Atlas

`ABDAtlas` samples a `StiffnessField` on a rectangular parameter grid and performs
bilinear interpolation in canonical C8 storage.

```python
import math

from tensyl import ABDAtlas

atlas = ABDAtlas.from_field(
    surface,
    field,
    u_values=(0.0, 150.0, 300.0),
    v_values=(0.0, math.pi, 2.0 * math.pi),
)

interpolated = atlas.stiffness_at(surface, 75.0, 0.5 * math.pi)
```

Atlas interpolation is a convenience for linear ABD stiffnesses. Interpolation error
metadata should be reviewed before relying on a coarse grid.

The atlas interpolates matrix samples; it does not derive a stiffener layout from
the surface. On a curved or nonuniform surface, choose sample points that match
the physical variation you intend to represent.

## Choosing A Response Length

`ValidityContext.response_length` should represent the structural response mode
you intend to model, such as an expected buckle half-wavelength, analysis
feature size, or load redistribution length. It should not default blindly to
the global part length. A pitch that is small compared with the whole barrel can
still be too large for a short-wavelength local response.

Next: [Stiffened Surfaces](stiffened-surfaces.md).
