# Validity Limits

`ValidityContext`, `ValidityThresholds`, and `ValidityReport` live in
`tensyl.core.validity`; the checks that build a report live in
`tensyl.core.validity_checks`. All four public names, including
`validity_report_for_stiffness`, are available from `tensyl`.

Equivalent-stiffness homogenization is a scale-separated approximation. It is most
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

## Coupling That a Reference Shift Cannot Remove

An eccentric rib creates a nonzero `B` block, but part of that coupling can
come from where the analyst put the reference surface. The warning uses
`coupling_ratios["B_residual"]`, which measures the coupling left after the
best common shift. It is unchanged by an in-plane rotation or reference shift,
up to floating-point roundoff.

First express each block in Mandel components:

$$
\mathbf C_M = \mathbf W\mathbf C\mathbf W,\qquad
\mathbf W=\operatorname{diag}(1,1,\sqrt{2}),\quad
\mathbf C\in\{\mathbf A,\mathbf B,\mathbf D\}.
$$

The Mandel basis is orthonormal, so its Frobenius norm is independent of the
chosen axes. Engineering-shear components do not have that property. See
[Brannon's discussion of Voigt and Mandel representations](https://csmbrannon.net/2015/08/10/fourth-order-tensor-tutorial-excerpts-voigt-and-mandel-representations-as-well-as-isotropy-topics/).

The following projection is Tensyl's diagnostic definition. Minimizing
$\|\mathbf B_M-d\mathbf A_M\|_F^2$ gives

$$
d_* = \frac{\langle\mathbf B_M,\mathbf A_M\rangle_F}
                 {\|\mathbf A_M\|_F^2},\qquad
\mathbf B_* = \mathbf B-d_*\mathbf A,\qquad
\mathbf D_* = \mathbf D-2d_*\mathbf B+d_*^2\mathbf A.
$$

The reported residual is

$$
B_\mathrm{residual}=
\frac{\|\mathbf B_{*,M}\|_F}
     {\sqrt{\|\mathbf A_M\|_F\|\mathbf D_{*,M}\|_F}}.
$$

The default warning threshold is `0.10`. A large residual means a single
reference shift cannot remove the membrane-bending coupling. Keep the full ABD
law when that coupling matters to the response.

`result.diagnostics["neutral_surface_offset"]` gives $d_*$ in the model's
length units, positive along `+n` from the current reference surface. It is a
least-squares offset across all membrane modes, not generally `B11/A11` or a
neutral surface shared by every load direction. If `A` is zero, the diagnostic
uses zero offset because no membrane neutral surface is defined. A zero
normalizing block gives a zero ratio; rank and negative-energy warnings still
need review.

`coupling_ratios["B_fro"]` retains the original engineering-component ratio
$\|\mathbf B\|_F/\sqrt{\|\mathbf A\|_F\|\mathbf D\|_F}$ at the report's chosen
reference surface and axes. It is retained for reading older artifacts and no
longer drives the warning. Transforming a stiffness preserves its attached
report; call `validity_report_for_stiffness(transformed, context=...)` to get
`B_fro` for the new surface and axes.

Very large offsets can lose bending precision through cancellation in the
reference-shift formula. Keep the reference near the panel when possible;
these diagnostics do not recover digits already lost in an imported matrix.

## Interpreting Warnings

Warnings distinguish missing evidence from a computed concern:

| Code | Meaning |
| --- | --- |
| `validity_context_missing` | No scale context was supplied or inferred; scale checks did not run. |
| `h_over_R_unavailable`, `p_over_R_unavailable`, `p_over_L_response_unavailable` | Context exists, but inputs for that particular check are missing. |
| `*_exceeds_threshold` | The ratio was computed and reached its warning threshold. |
| `rank_deficient_tangent` | At least one generalized mode has no resolved stiffness at the numerical rank tolerance. |
| `negative_energy_mode` | The tangent has a negative eigenvalue beyond roundoff. |

`EnergyHomogenizer` fills an omitted pitch from the longest repeat vector in
`cell.geometry`. For `stiffener_family_cell`, it uses the largest family
spacing. This is a conservative cell-size estimate, not a mode-dependent
wavelength. An explicit `ValidityContext.pitch` always wins. Height, curvature,
and response length still need context; an inferred pitch alone cannot run any
of the scale-separation checks.

Use `ValidityContext.from_surface_point(point, characteristic_height=...,
response_length=...)` in a field's validity factory to take the minimum radius
from its `SurfacePoint`. Flat points supply infinity, giving zero height/radius
and pitch/radius ratios when those lengths are known.

These warnings are prompts for engineering review, not certification criteria.
An unavailable check is not a failed check, and absence of a warning does not
prove the assumptions hold.

So a warning fired — now what? In practice:

- re-read the assumptions and confirm the geometry actually matches a
  scale-separated model (is pitch really small next to your response length?);
- compare the homogenized result against a detailed finite-element model of the
  same geometry and loading before trusting it downstream;
- or change the model family entirely if the separation of scales simply does
  not hold.

Those checks establish whether the approximation holds for your geometry.
This is the boundary drawn in
["What Tensyl Is Not"](../index.md).

## The Affine Assumption

The homogenizer makes every rib follow the smeared panel strain through
Nemeth's first-approximation member map. It adds the resulting skin and member
energies without solving for cell-scale displacements. See
[Nemeth, equations 30–39](https://ntrs.nasa.gov/citations/20110004039) and the
[implemented strain map](tangent-plane-homogenization.md).

That constraint can make a panel too stiff. In a beam/skin model where the
affine deformation is admissible, allowing internal displacements to relax
can only lower the minimum energy at fixed macroscopic strain:

$$
W_\mathrm{relaxed}(\boldsymbol\eta)
=\min_{\mathbf q} W(\boldsymbol\eta,\mathbf q)
\le W(\boldsymbol\eta,\mathbf 0)=W_\mathrm{affine}(\boldsymbol\eta).
$$

This is the Voigt-like upper-bound interpretation of the affine model. It is
not a certified bound against every shell or solid model: that comparison
also depends on compatible kinematics, member assumptions, joints, and how
skin and ribs connect. Hexagonal and star patterns with thin skins deserve
particular care because member bending and cell rearrangement can make their
in-plane response much softer than the affine prediction. A small pitch ratio
does not test this limitation; compare the relevant modes with a model that
allows that relaxation.

Section assumptions matter too. Tensyl's thin-wall helpers supply open-section
torsion. A hat closed by its attached skin forms a closed cell and can have a
very different torsional stiffness. Read
[Which J Should Be Used?](../validation/sp8007-reconciliation.md#which-j-should-be-used)
before using an open hat section for that panel.

## Out of Scope for the First Model Family

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
