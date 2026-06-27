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

The default warning threshold is `0.10`.

## Interpreting Warnings

Warnings are not pass/fail certification criteria. They are prompts for
engineering review. A warning means the wall law should not be used blindly for
the intended response without checking assumptions, comparing against a detailed
model, or changing the model family.

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
