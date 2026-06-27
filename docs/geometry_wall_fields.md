# Geometry and Wall Fields

Phase 4 embeds local equivalent-wall laws into shell midsurface geometry without
changing the constitutive law. The separation is the same one used in the white
paper: homogenization computes the local wall tangent
\(\mathbf C_\text{wall}\), while geometry supplies frames, metrics,
curvatures, and integration measures for later shell kinematics [Reddy 2004;
Nemeth 2011].

In weak-form notation, the split is:

$$
\mathbf K =
\int_\Omega
\mathbf B_\text{shell}^T
\mathbf C_\text{wall}
\mathbf B_\text{shell}
\,d\Omega .
$$

`tensyl.geometry` implements only the midsurface data needed to attach a wall
law pointwise. It does not implement shell strain-displacement operators or
solver adapters.

## Surface Points

Every surface exposes:

```python
point = surface.point_at(u, v)
```

The returned `SurfacePoint` contains:

- `position`, `tangent_u`, and `tangent_v`;
- metric tensor \(g_{\alpha\beta}=\mathbf a_\alpha\cdot\mathbf a_\beta\);
- signed curvature tensor
  \(b_{\alpha\beta}=\mathbf n\cdot\partial_{\alpha\beta}\mathbf r\);
- a right-handed orthonormal `Frame2D`;
- surface Jacobian \(\|\mathbf a_1\times\mathbf a_2\|\);
- signed principal curvatures and `min_radius`.

All arrays are read-only. Parameter singularities, such as poles in spherical
and ellipsoidal coordinates, raise `ValueError`.

## Built-In Surfaces

`FlatPlate` uses Cartesian parameters and has zero curvature:

$$
\mathbf r(u,v)=u\mathbf e_1+v\mathbf e_2 .
$$

`Cylinder(radius=R)` uses axial coordinate and angle \((x,\theta)\):

$$
\mathbf r(x,\theta)=
\begin{bmatrix}
x & R\cos\theta & R\sin\theta
\end{bmatrix}^T .
$$

Tensyl uses an outward normal. With the default right-handed frame, `e1` is
axial and `e2` points opposite increasing \(\theta\), so the signed principal
curvatures are:

$$
k_1 = -\frac{1}{R}, \qquad k_2 = 0 .
$$

Validity ratios use the radius magnitude, so this signed-curvature convention
does not make \(h/R\) or \(p/R\) negative.

`SphericalCap(radius=R)` uses polar angle and azimuth \((\phi,\theta)\). With
the outward normal, both principal curvatures are signed negative:

$$
k_\phi = k_\theta = -\frac{1}{R}.
$$

`Ellipsoid(a, b, c)` uses the same angular coordinates as the spherical cap.
The coordinate tangents are generally not orthogonal, so Tensyl computes the
metric and curvature from the parametric derivatives and then builds a separate
orthonormal frame for constitutive-law embedding.

## Wall Fields

`ConstantWallField` binds one `LinearABDWall` to the local frame at every
surface point:

```python
from tensyl import ConstantWallField, Cylinder

field = ConstantWallField(wall)
barrel = Cylinder(radius=2.0)
local_law = field.law_at(barrel, 0.5, 1.2)
```

The C8 tangent is unchanged. Only the frame and metadata are rebound to the
surface point. This is appropriate for uniform flat coupons and barrels where
the local wall law is constant in the surface coordinates.

`HomogenizedWallField` builds a local `CanonicalUnitCell` at each surface point
and sends it through a `Homogenizer`. The cell factory must return a cell whose
skin and frame match the `SurfacePoint.frame`; otherwise Tensyl raises
`ValueError` before homogenization instead of silently attaching a tangent to
the wrong frame.

Pointwise validity can be computed with `validity_report_for_law`. Flat
surfaces use `min_radius=np.inf`, which gives zero curvature ratios. Curved
surfaces pass the positive radius magnitude into `ValidityContext.min_radius`.

## Wall Atlas

`WallAtlas` samples a `WallField` over a rectangular \((u,v)\) grid and
interpolates `LinearABDWall` laws bilinearly in canonical C8 storage. The
interpolated tangent is symmetrized before constructing the output law.

The first atlas implementation intentionally supports only linear wall laws.
It does not interpolate arbitrary nonlinear `ConstitutiveLaw` objects. Atlas
metadata records:

- the interpolation method;
- sampled `u` and `v` grid coordinates;
- sample shape;
- Tensyl version;
- deterministic digest of the grid and sampled C8/frame/convention data;
- warning IDs present on sampled validity reports;
- the maximum adjacent-sample C8 Frobenius gradient;
- grid-cell indices and weights;
- warning IDs present on the four corner validity reports;
- the maximum Frobenius distance between the interpolated tangent and the
  corner tangents.

All atlas samples must match the corresponding surface-point frame and share a
single strain convention. Out-of-grid lookup raises `ValueError`;
interpolation error is metadata, not a hidden guarantee of accuracy.

## Example

```python
import numpy as np

from tensyl import ConstantWallField, Cylinder, WallAtlas

barrel = Cylinder(radius=120.0, length=300.0)
field = ConstantWallField(wall)

atlas = WallAtlas.from_field(
    barrel,
    field,
    u_values=(0.0, 150.0, 300.0),
    v_values=(0.0, np.pi, 2.0 * np.pi),
)

local_law = atlas.law_at(barrel, 75.0, 0.5 * np.pi)
```

The same wall law can be embedded in flat or curved geometry. Curvature enters
later shell kinematics and validity checks; it does not modify the Level 1
homogenized tangent.
