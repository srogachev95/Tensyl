# Constitutive Kernel

Tensyl's first mechanics layer is a local wall-law kernel. It computes and
transforms a constitutive law in a tangent-plane frame; shell geometry and
homogenized stiffener cells are separate layers.

The Phase 1 implementation follows the convention recommended in the white
paper and keeps the wall law in laminated-plate notation [Nemeth 2011; Reddy
2004].

## Local Frame

A wall law is expressed in an explicit right-handed orthonormal frame:

$$
\{\mathbf e_1,\mathbf e_2,\mathbf n\}.
$$

`Frame2D` validates that $\mathbf e_1$ and $\mathbf e_2$ are tangent directions,
that $\mathbf n$ is the positive normal, and that
$\mathbf e_1 \times \mathbf e_2 = \mathbf n$. A positive rotation angle rotates
the local in-plane frame counterclockwise about $\mathbf n$:

$$
\mathbf e_1'=\cos\psi\,\mathbf e_1+\sin\psi\,\mathbf e_2,
\qquad
\mathbf e_2'=-\sin\psi\,\mathbf e_1+\cos\psi\,\mathbf e_2.
$$

## Generalized Strains and Resultants

The internal generalized strain vector is:

$$
\boldsymbol\eta
=
\begin{bmatrix}
\epsilon_{11}^0 &
\epsilon_{22}^0 &
\gamma_{12}^0 &
\kappa_{11} &
\kappa_{22} &
\kappa_{12} &
\gamma_{13}^0 &
\gamma_{23}^0
\end{bmatrix}^T.
$$

The corresponding generalized resultant vector is:

$$
\mathbf r
=
\begin{bmatrix}
N_{11} &
N_{22} &
N_{12} &
M_{11} &
M_{22} &
M_{12} &
Q_{13} &
Q_{23}
\end{bmatrix}^T.
$$

Phase 1 supports engineering shear strain components only. Tensor shear
conventions are intentionally rejected so that later homogenization formulas do
not silently mix twist and shear factors. The default reference surface is the
wall mid-surface.

## Linear ABD Wall Law

Tensyl's public constitutive contract is hyperelastic in the small-strain,
generalized-wall sense. "Hyperelastic" here means that every law derives from a
stored-energy potential \(W(\boldsymbol\eta)\). It does not mean finite-strain
continuum hyperelasticity.

The derivative tower is:

$$
\mathbf r(\boldsymbol\eta)=\frac{\partial W}{\partial\boldsymbol\eta},
\qquad
\mathbf C(\boldsymbol\eta)=
\frac{\partial^2 W}{\partial\boldsymbol\eta^2}.
$$

`LinearABDWall` implements `LinearLaw`, a refinement of the public
`ConstitutiveLaw`/`HyperelasticLaw` protocol:

```python
from tensyl import ConstitutiveLaw, HyperelasticLaw, LinearABDWall, LinearLaw
```

The linear tangent has the block structure:

$$
\mathbf C_\text{wall}
=
\begin{bmatrix}
\mathbf A & \mathbf B & \mathbf 0 \\
\mathbf B & \mathbf D & \mathbf 0 \\
\mathbf 0 & \mathbf 0 & \mathbf A_s
\end{bmatrix},
\qquad
\mathbf r=\mathbf C_\text{wall}\boldsymbol\eta .
$$

The operator methods are:

- `energy(eta)`, which returns
  \(\frac{1}{2}\boldsymbol\eta^T\mathbf C_\text{wall}\boldsymbol\eta\);
- `resultants(eta)`, which returns $\mathbf C_\text{wall}\boldsymbol\eta$;
- `tangent(eta)`, which returns the tangent required by the general
  hyperelastic contract;
- `constant_tangent`, which is the no-argument $8\times8$ tangent path for
  linear laws;
- `rotate(angle_rad)`, which returns the same wall law expressed in a rotated
  local frame.

The implementation validates matrix shapes, finite entries, and symmetry of the
ABD and transverse-shear blocks. The assembled C8 matrix is the canonical
operator payload; A/B/D/As are exposed as read-only block views. Public
generalized vectors can be wrapped with `generalized_strain(...)` and
`generalized_resultant(...)` so static checkers can distinguish strains from
resultants at API boundaries.

Homogenized laws also carry validity diagnostics through `wall.validity`, so
using `result.law` does not discard the scale-separation and coupling report.

## Skin-Only Plates and Laminates

An isotropic skin uses the plane-stress reduced stiffness:

$$
\mathbf Q = \frac{E}{1-\nu^2}
\begin{bmatrix}
1 & \nu & 0 \\
\nu & 1 & 0 \\
0 & 0 & \frac{1-\nu}{2}
\end{bmatrix}.
$$

For thickness $h$ about the mid-surface:

$$
\mathbf A=\mathbf Qh,\qquad
\mathbf B=\mathbf 0,\qquad
\mathbf D=\frac{\mathbf Qh^3}{12}.
$$

The transverse-shear block is:

$$
\mathbf A_s=\kappa Gh
\begin{bmatrix}
1 & 0 \\
0 & 1
\end{bmatrix},
$$

where $\kappa$ is an explicit shear-correction factor.

Laminate skins use bottom-to-top ply order and classical through-thickness
integration:

$$
A_{ij}=\sum_k \bar Q_{ij}^{(k)}(z_k-z_{k-1}),
$$

$$
B_{ij}=\frac{1}{2}\sum_k \bar Q_{ij}^{(k)}(z_k^2-z_{k-1}^2),
$$

$$
D_{ij}=\frac{1}{3}\sum_k \bar Q_{ij}^{(k)}(z_k^3-z_{k-1}^3).
$$

Example:

```python
from tensyl import IsotropicMaterial, OrthotropicPlyMaterial, Ply
from tensyl import isotropic_plate, laminate_plate

aluminum = IsotropicMaterial(E=70.0e9, nu=0.33, density=2700.0)
skin = isotropic_plate(aluminum, thickness=0.004)

carbon = OrthotropicPlyMaterial(
    E1=140.0e9,
    E2=9.0e9,
    G12=5.0e9,
    nu12=0.28,
    G13=4.0e9,
    G23=3.0e9,
)
laminate = laminate_plate(
    [
        Ply(carbon, thickness=0.000125, angle_rad=0.0),
        Ply(carbon, thickness=0.000125, angle_rad=1.5707963267948966),
        Ply(carbon, thickness=0.000125, angle_rad=1.5707963267948966),
        Ply(carbon, thickness=0.000125, angle_rad=0.0),
    ]
)
```

## Rotation Contract

Tensyl uses separate transforms for generalized strains and generalized
resultants. If

$$
\boldsymbol\eta'=\mathbf T_\eta\boldsymbol\eta,
\qquad
\mathbf r'=\mathbf T_r\mathbf r,
$$

then the rotated tangent is:

$$
\mathbf C'=\mathbf T_r\mathbf C\mathbf T_\eta^{-1}.
$$

This preserves the power pairing:

$$
\mathbf r'^T\boldsymbol\eta'=\mathbf r^T\boldsymbol\eta.
$$

The test suite enforces this power identity, isotropic rotation invariance,
rotate-forward/rotate-back recovery, and 90-degree swapping of orthotropic
principal stiffnesses.
