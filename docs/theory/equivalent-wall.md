# Equivalent-Wall Mechanics

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

The current public strain convention uses engineering shear strains. Tensor
shear conventions are rejected so twist and shear factors are not silently
mixed.

## Stored Energy Contract

Tensyl treats a wall law as a generalized hyperelastic operator in the
small-strain wall sense. That means the law derives from a stored-energy
potential:

$$
\mathbf r(\boldsymbol\eta)=
\frac{\partial W}{\partial\boldsymbol\eta},
\qquad
\mathbf C(\boldsymbol\eta)=
\frac{\partial^2 W}{\partial\boldsymbol\eta^2}.
$$

For a linear wall:

$$
W(\boldsymbol\eta)=
\frac{1}{2}\boldsymbol\eta^T\mathbf C_\text{wall}\boldsymbol\eta.
$$

This use of "hyperelastic" does not mean finite-strain continuum
hyperelasticity. It means the generalized wall law has an energy potential.

## Linear ABD Wall

`LinearABDWall` stores:

$$
\mathbf C_\text{wall}
=
\begin{bmatrix}
\mathbf A & \mathbf B & \mathbf 0 \\
\mathbf B & \mathbf D & \mathbf 0 \\
\mathbf 0 & \mathbf 0 & \mathbf A_s
\end{bmatrix}.
$$

The $8\times8$ tangent is the canonical payload. The `A`, `B`, `D`, and `As`
properties are read-only views of that payload.
