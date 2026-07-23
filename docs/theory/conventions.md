# Frames and Conventions

Every ABD stiffness belongs to a set of local directions. `e1` and `e2` lie in
the panel, while `n` points away from the reference surface. For a cylinder,
for example, `e1` is axial, `e2` is circumferential, and `n` points outward.

Together they form a right-handed frame:

$$
\{\mathbf e_1,\mathbf e_2,\mathbf n\}.
$$

Tensyl checks that the directions follow this rule:

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

- `BeamMember.axial_eccentricity` and `BeamMember.shear_eccentricity`;
- the corresponding `StiffenerFamily` inputs;
- named-cell family inputs such as `e1_axial_eccentricity` and
  `diagonal_shear_eccentricity`;
- sandwich `bottom_face_to_reference` and `top_face_to_reference` shifts.

For a cylinder whose local normal points outward, an external stiffener has a
positive eccentricity. An internal stiffener has a negative eccentricity.

For most stiffeners, set `axial_eccentricity` to the centroid offset and omit
`shear_eccentricity`. Tensyl then uses the same offset for both axial and
in-plane shear response.

Nemeth also covers nonhomogeneous members whose axial and shear response act at
different effective offsets. Tensyl keeps that option through separate
`axial_eccentricity` and `shear_eccentricity` inputs.

!!! warning "The eccentricity sign is not cosmetic"
    Reversing the sign changes the membrane-bending coupling block `B` and
    therefore describes a different structure. Tensyl cannot infer which side
    of the reference surface the stiffener occupies, so establish `+n` before
    entering the offset.

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
