<span id="validity-limits"></span>
# Modeling Choices

The equivalent plate represents the average response of a repeating skin-and-rib
construction. Choose its inputs around the deformation you want to study:
the rib strain model, section torsion, reference surface, and the distance over
which the panel response changes.

## The Affine Assumption

Every rib follows the prescribed panel strain and curvature through the
[Nemeth member map](tangent-plane-homogenization.md). This gives a direct energy
calculation from section stiffnesses. The cell has no additional displacement
unknowns to solve.

Allowing ribs to bend and rearrange within a cell can reduce its energy at the
same average panel strain. For compatible beam/skin kinematics,

$$
W_\mathrm{relaxed}(\boldsymbol\eta)=\min_{\mathbf q}
W(\boldsymbol\eta,\mathbf q)\le W(\boldsymbol\eta,\mathbf0)
=W_\mathrm{affine}(\boldsymbol\eta).
$$

Here $\mathbf q$ contains the internal cell displacements. This explains why an
affine model can give a higher stiffness than a model with internal relaxation.
The comparison assumes the same members, connections, and admissible
kinematics. Thin-skinned hexagonal and star patterns are useful candidates for
such a comparison because member rearrangement can govern their response.
See [Nemeth and the homogenization sources](../references.md).

## Choose the Response Scales

Use rib/panel height $h_s$, representative pitch $p$, minimum curvature radius
$R_\min$, and response length $L_\mathrm{response}$ to compare the local cell
with the larger deformation:

| Ratio | Interpretation | Default warning threshold |
| --- | --- | --- |
| $h_s/R_\min$ | Height relative to shell curvature | 0.05 |
| $p/R_\min$ | Pitch relative to shell curvature | 0.05 |
| $p/L_\mathrm{response}$ | Pitch relative to response variation | 0.05 |

For bending or buckling, response length might be a bending variation length or
an estimated buckle half-wavelength. For load redistribution, use the distance
over which the resultants change appreciably. Define it from that response,
rather than automatically using the full part length.

`ValidityContext` carries these inputs. If pitch is omitted, Tensyl uses the
longest repeat vector or largest supplied family spacing. An explicit pitch
takes precedence. `ValidityContext.from_surface_point(...)` supplies the local
radius; flat points use infinity, so known height/radius and pitch/radius ratios
are zero. `ValidityThresholds` lets the analysis select other thresholds.

## Interpreting Warnings

Read the numerical ratios alongside the warning codes:

| Code | Meaning |
| --- | --- |
| `validity_context_missing` | Scale context was neither supplied nor inferred. |
| `*_unavailable` | That ratio needs another input. |
| `*_exceeds_threshold` | The computed ratio reached its threshold. |
| `membrane_bending_coupling_exceeds_threshold` | Residual coupling reached its threshold, normally 0.10. |
| `rank_deficient_tangent` | A generalized deformation has no resolved stiffness at the numerical tolerance. |
| `negative_energy_mode` | A negative eigenvalue exceeds roundoff. |

For a scale warning, check the chosen response length and compare the relevant
response with a detailed model when cell deformation is significant. For a
coupling warning, retain the full ABD relation; the derivation below describes
what the diagnostic measures.

## Section and Connection Idealizations

Thin-wall helpers use rectangular strips and centroidal beam stiffness. Their
usual torsion law is the freely warping open-section approximation. A hat can
also use a skin-closed Bredt shear-flow model; the
[section guide](../user-guide/beam-sections-and-cells.md#hats-closed-by-the-skin)
explains the input and the shared skin-energy accounting.

Laminated walls use membrane compliance to obtain an equivalent axial modulus
and shear modulus. That reduction accepts symmetric, membrane-orthotropic walls;
local laminate bending and anisotropic warping call for a richer section model.

<span id="out-of-scope-for-the-first-model-family"></span>
The panel stiffness supplies the constitutive part of a structural analysis.
Use a local model for skin-bay buckling, rib crippling, joints, intersections,
and load introduction. Use the panel or shell model for equilibrium, boundary
conditions, imperfections, and global response. This separates the physical
questions at the scales where they occur.

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

