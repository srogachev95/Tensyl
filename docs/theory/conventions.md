# Frames and Conventions

An ABD stiffness is expressed in a right-handed local frame:

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

## Rotation of ABD Stiffnesses

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

The default reference surface is the mid-surface. If a stiffness is shifted by
distance $d$ along the positive normal, membrane strain at the old surface is:

$$
\boldsymbol\epsilon_\text{old}
=
\boldsymbol\epsilon_\text{new} - d\boldsymbol\kappa.
$$

Use `shift_reference_surface` when superposing facesheets or moving an ABD stiffness
to a different shell reference surface.

```
        +n
        ^
        |  positive eccentricity
        |      o stiffener centroid
--------+-------------------------- reference surface
       e1 ->       e2 completes the right-handed tangent frame
```

## Eccentricity Inputs

Every eccentricity input follows the same sign rule:

> Eccentricity is the signed distance from the reference surface to the
> stiffener or face centroid, measured along `+n`.

This applies to:

- `BeamMember.eccentricity`;
- `StiffenerFamily.eccentricity`;
- `stringer_eccentricity`;
- `rib_eccentricity`;
- sandwich `bottom_face_offset` and `top_face_offset`.

For a cylinder whose local normal points outward, an external stringer has
positive `stringer_eccentricity`. An internal stringer has negative
eccentricity.

!!! warning "The eccentricity sign is not cosmetic"
    Flip it and you change the membrane-bending coupling block `B`, which gives
    you a *physically different ABD stiffness*. Tensyl raises no exception and no
    validation error, and the result looks entirely ordinary. Decide which way
    `+n` points before you type a sign.

Positive eccentricity adds membrane-bending coupling according to the chosen
reference surface. Moving the reference surface also changes `B`. Equal and
opposite faces in a symmetric sandwich can cancel coupling when the face stiffnesses
and offsets are symmetric.

## Member Angles

Member angles are measured in the local tangent frame:

- `0` is along local `e1`;
- `pi/2` is along local `e2`;
- positive angles follow Tensyl's positive in-plane rotation convention about
  `n`.

For the built-in `Cylinder`, `e1` is axial and `e2` is circumferential. A
longitudinal stringer uses angle `0`; a ring rib uses angle `pi/2`.

## Engineering Shear

Tensyl's public strain convention uses engineering shear components
`gamma12`, `gamma13`, and `gamma23`. Tensor shear is rejected because an
unnoticed factor-of-two convention mix would corrupt the stiffnesses, energies,
and resultants while leaving the matrices looking well-formed.
