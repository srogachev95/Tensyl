# Stiffened Surfaces

Tensyl keeps local wall-law computation separate from shell geometry. Compute a
wall law in the local tangent plane, then attach it to a surface through a wall
field.

## Flat Panel

```python
from tensyl import ConstantWallField, FlatPlate

surface = FlatPlate()
field = ConstantWallField(result.law)
local_wall = field.law_at(surface, 0.0, 0.0)
```

The flat panel recipe is:

1. build a skin or laminate wall law;
2. build stiffener `BeamSection` values;
3. build a `CanonicalUnitCell`;
4. homogenize with `EnergyHomogenizer`;
5. attach `result.law` through `ConstantWallField`.

## Stiffened Barrel

```python
from tensyl import ConstantWallField, Cylinder, ValidityContext

radius = 120.0
surface = Cylinder(radius=radius, length=300.0)
field = ConstantWallField(result.law)
wall_at_midbay = field.law_at(surface, 150.0, 0.0)

context = ValidityContext(
    characteristic_height=0.50,
    pitch=8.0,
    min_radius=radius,
    response_length=80.0,
)
```

For `Cylinder`, local `e1` is axial and local `e2` is circumferential. Axial
stringers map to angle `0`. Ring ribs map to angle `pi/2`. With the built-in
outward normal, an external stiffener uses positive eccentricity.

Use a constant wall field when the same local wall law is acceptable
everywhere. Use `WallAtlas` or `HomogenizedWallField` when wall properties vary
with station, angle, pitch, or local stiffener definition.

## Stiffened Dome

`Sphere`, `SphericalCap`, and `Ellipsoid` provide curved midsurfaces with local
frames that change over the surface.

```python
from tensyl import Sphere, SphericalCap, WallAtlas

complete_dome = Sphere(radius=96.0)
dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
atlas = WallAtlas.from_field(
    dome,
    field,
    u_values=(0.20, 0.60, 0.95),
    v_values=(0.0, 3.141592653589793, 6.283185307179586),
)
```

The first homogenizer is tangent-plane only. Tensyl does not automatically
build geodesic stiffener layouts over a dome. For varying stiffener orientation
or pitch, provide a pointwise cell factory through `HomogenizedWallField` or
sample already-computed local laws into a `WallAtlas`. The local cell must be
consistent with each surface-point frame.

For a sphere, the chart coordinates are `(phi, theta)`: `e1` is meridional and
`e2` is circumferential away from the poles. For an ellipsoid, Tensyl uses the
same latitude-longitude style chart, but a triaxial ellipsoid does not provide
uniform physical pitch from uniform coordinate spacing.

## Conical Frustum

`ConicalFrustum` covers practical cone-like shell sections without including an
apex singularity.

```python
from tensyl import ConicalFrustum, ValidityContext

surface = ConicalFrustum(radius_start=80.0, radius_end=96.0, length=120.0)
point = surface.point_at(60.0, 0.0)

context = ValidityContext(
    characteristic_height=0.50,
    pitch=8.0,
    min_radius=point.min_radius,
    response_length=80.0,
)
```

The cone frame uses `e1` along increasing axial station/generator direction,
`e2` opposite the positive `theta` tangent to keep the same outward-normal
orientation as `Cylinder`, and `n` outward. When `radius_start == radius_end`,
the conical-frustum geometry reduces to the cylinder formulas.

This is still wall-property preparation, not shell analysis. A separate shell,
buckling, or sizing workflow must apply loads, boundary conditions, and failure
criteria.
