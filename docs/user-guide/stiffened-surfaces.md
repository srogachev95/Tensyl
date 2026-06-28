# Stiffened Surfaces

Tensyl keeps local stiffness computation separate from shell geometry. Compute a
ABD stiffness in the local tangent plane, then attach it to a surface through a stiffness
field.

The surface does not silently alter the ABD matrix. It supplies the local
surface frame, curvature, metric, and validity radius. The ABD stiffness changes
only when the field supplies a different tangent at a point, for example through
a pointwise cell factory or a sampled atlas.

## Flat Panel

```python
from tensyl import ConstantStiffnessField, FlatPlate

surface = FlatPlate()
field = ConstantStiffnessField(result.stiffness)
local_stiffness = field.stiffness_at(surface, 0.0, 0.0)
```

The flat panel recipe is:

1. build a skin or laminate ABD stiffness;
2. build stiffener `BeamSection` values;
3. build a `CanonicalUnitCell`;
4. homogenize with `EnergyHomogenizer`;
5. attach `result.stiffness` through `ConstantStiffnessField`.

## Stiffened Barrel

```python
from tensyl import ConstantStiffnessField, Cylinder, ValidityContext

radius = 120.0
surface = Cylinder(radius=radius, length=300.0)
field = ConstantStiffnessField(result.stiffness)
stiffness_at_midbay = field.stiffness_at(surface, 150.0, 0.0)

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

The barrel radius enters the validity review through `min_radius`; it does not
modify a constant-field `C8` tangent. If the barrel has station-dependent pitch,
section, material, or stiffener angle, represent that variation with
`HomogenizedStiffnessField` or `ABDAtlas` instead of expecting the cylinder
geometry to infer it.

Use a constant stiffness field when the same local ABD stiffness is acceptable
everywhere. Use `ABDAtlas` or `HomogenizedStiffnessField` when stiffness properties vary
with station, angle, pitch, or local stiffener definition.

## Stiffened Dome

`Sphere`, `SphericalCap`, and `Ellipsoid` provide curved midsurfaces with local
frames that change over the surface.

```python
from tensyl import Sphere, SphericalCap, ABDAtlas

complete_dome = Sphere(radius=96.0)
dome = SphericalCap(radius=96.0, half_angle_rad=1.0)
atlas = ABDAtlas.from_field(
    dome,
    field,
    u_values=(0.20, 0.60, 0.95),
    v_values=(0.0, 3.141592653589793, 6.283185307179586),
)
```

The first homogenizer is tangent-plane only. Tensyl does not automatically
build geodesic stiffener layouts over a dome. For varying stiffener orientation
or pitch, provide a pointwise cell factory through `HomogenizedStiffnessField` or
sample already-computed local stiffnesses into an `ABDAtlas`. The local cell must be
consistent with each surface-point frame.

For a sphere, the chart coordinates are `(phi, theta)`: `e1` is meridional and
`e2` is circumferential away from the poles. For an ellipsoid, Tensyl uses the
same latitude-longitude style chart, but a triaxial ellipsoid does not provide
uniform physical pitch from uniform coordinate spacing.

An ellipsoid is therefore a good place to be explicit. A constant isotropic ABD
field remains constant as a matrix even though the frame and curvature change
over the surface. A stiffened ellipsoid has pointwise stiffness variation only
if the modeled local cells or atlas samples vary pointwise.

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

This is still stiffness-property preparation, not shell analysis. A separate shell,
buckling, or sizing workflow must apply loads, boundary conditions, and failure
criteria.
