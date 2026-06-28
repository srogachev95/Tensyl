# Equivalent-Stiffness Mechanics

An equivalent ABD stiffness is the constitutive part of a plate or shell model. It
does not solve shell equilibrium and it does not decide boundary conditions. It
answers a local question: for generalized strains measured on a reference
surface, what generalized resultants are produced?

Tensyl uses a generalized strain vector:

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

Those eight numbers are really three familiar things stacked together: three
membrane strains, three curvatures, and two transverse shears. Feed them in, get
the eight matching resultants out — that is the whole job of an ABD stiffness.

The current public strain convention uses engineering shear strains. Tensor
shear conventions are rejected so twist and shear factors are not silently
mixed.

!!! note "Ordering is part of the public API contract"
    The component order above is not arbitrary house style — it is a contract.
    User code should not reorder the matrices without also transforming the
    strains and resultants to match, or the energy and resultants will quietly
    stop meaning what they say.

## Stored Energy Contract

Tensyl treats an ABD stiffness as a generalized hyperelastic operator in the
small-strain stiffness sense. That means the stiffness derives from a stored-energy
potential:

$$
\mathbf r(\boldsymbol\eta)=
\frac{\partial W}{\partial\boldsymbol\eta},
\qquad
\mathbf C(\boldsymbol\eta)=
\frac{\partial^2 W}{\partial\boldsymbol\eta^2}.
$$

For a linear stiffness:

$$
W(\boldsymbol\eta)=
\frac{1}{2}\boldsymbol\eta^T\mathbf C_\text{stiffness}\boldsymbol\eta.
$$

This use of "hyperelastic" does not mean finite-strain continuum
hyperelasticity. It means the generalized ABD stiffness has an energy potential.

## Linear ABD Stiffness

`ABDStiffness` stores:

$$
\mathbf C_\text{stiffness}
=
\begin{bmatrix}
\mathbf A & \mathbf B & \mathbf 0 \\
\mathbf B & \mathbf D & \mathbf 0 \\
\mathbf 0 & \mathbf 0 & \mathbf A_s
\end{bmatrix}.
$$

The $8\times8$ tangent is the canonical payload. The `A`, `B`, `D`, and `As`
properties are read-only views of that payload.

`A`, `B`, and `D` follow the usual first-order plate/shell ABD notation used in
laminated plate theory. `As` is the transverse-shear block retained for
first-order shear-deformation workflows. See [References](../references.md) for
plate, shell, laminate, and equivalent-plate sources.

## What the ABD Stiffness Does Not Prove

An ABD stiffness is a constitutive approximation. It does not prove that a stiffener
layout is manufacturable, that local crippling is acceptable, that joints are
adequately modeled, or that a shell buckling calculation is valid. Tensyl
reports diagnostics and scale-separation warnings so the downstream workflow can
decide whether the local equivalent-stiffness approximation is acceptable for the
intended use.

For how these ABD stiffnesses are actually computed and inspected in practice, see
[Homogenization](../user-guide/homogenization.md) in the User Guide.
