# Validity Limits

Equivalent-wall homogenization is a scale-separated approximation. It is most
appropriate when stiffener height and pitch are small relative to curvature and
response length scales:

$$
\frac{h_s}{R_\text{min}} \ll 1,
\qquad
\frac{p}{R_\text{min}} \ll 1,
\qquad
\frac{p}{L_\text{response}} \ll 1.
$$

Tensyl's default warning thresholds are:

$$
\frac{h_s}{R_\text{min}}\ge 0.05,
\qquad
\frac{p}{R_\text{min}}\ge 0.05,
\qquad
\frac{p}{L_\text{response}}\ge 0.05.
$$

Tensyl also reports a membrane-bending coupling ratio:

$$
\frac{\|\mathbf B\|_F}
{\sqrt{\|\mathbf A\|_F\|\mathbf D\|_F}}.
$$

The default warning threshold is `0.10`. Read this ratio as: how much of the
wall's behavior is membrane-bending cross-talk, relative to the membrane and
bending stiffness it sits between. A large value means strain and curvature are
strongly coupled — usually a sign of eccentric stiffeners or an offset reference
surface, and a hint that a scalar "equivalent modulus" would throw away
something real.

## Interpreting Warnings

Warnings are not pass/fail certification criteria. They are prompts for
engineering review. A warning means the wall law should not be used blindly for
the intended response without checking assumptions, comparing against a detailed
model, or changing the model family.

So a warning fired — now what? In practice:

- re-read the assumptions and confirm the geometry actually matches a
  scale-separated model (is pitch really small next to your response length?);
- compare the homogenized result against a detailed finite-element model of the
  same geometry and loading before trusting it downstream;
- or change the model family entirely if the separation of scales simply does
  not hold.

None of these is optional busywork — they are how you find out whether the
approximation is writing checks the geometry cannot cash. This is exactly the
boundary drawn in ["What Tensyl Is Not"](../index.md).

## Out Of Scope For The First Model Family

The current tangent-plane family does not model:

- local skin buckling between stiffeners;
- stiffener crippling;
- joints, welds, fasteners, or bondlines;
- stiffener intersection stress concentrations;
- local load introduction;
- geometric imperfections;
- nonlinear material response;
- nonlinear postbuckling;
- response modes with wavelength comparable to stiffener pitch.
