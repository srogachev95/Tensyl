# Frames And Conventions

A wall law is expressed in a right-handed local frame:

$$
\{\mathbf e_1,\mathbf e_2,\mathbf n\}.
$$

`e1` and `e2` are tangent directions. `n` is the positive normal. Tensyl
validates:

$$
\mathbf e_1 \times \mathbf e_2 = \mathbf n.
$$

Positive in-plane rotation is counterclockwise about `n`:

$$
\mathbf e_1'=\cos\psi\,\mathbf e_1+\sin\psi\,\mathbf e_2,
\qquad
\mathbf e_2'=-\sin\psi\,\mathbf e_1+\cos\psi\,\mathbf e_2.
$$

## Rotation Of Wall Laws

Generalized strains and generalized resultants use separate transforms:

$$
\boldsymbol\eta'=\mathbf T_\eta\boldsymbol\eta,
\qquad
\mathbf r'=\mathbf T_r\mathbf r.
$$

The rotated tangent is:

$$
\mathbf C'=\mathbf T_r\mathbf C\mathbf T_\eta^{-1}.
$$

This preserves power:

$$
\mathbf r'^T\boldsymbol\eta'=\mathbf r^T\boldsymbol\eta.
$$

## Reference Surface

The default reference surface is the wall mid-surface. If a wall is shifted by
distance $d$ along the positive normal, membrane strain at the old surface is:

$$
\boldsymbol\epsilon_\text{old}
=
\boldsymbol\epsilon_\text{new} - d\boldsymbol\kappa.
$$

Use `shift_reference_surface` when superposing facesheets or moving a wall law
to a different shell reference surface.
