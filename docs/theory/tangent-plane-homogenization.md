# Tangent-Plane Homogenization

Tensyl begins with one small patch of a repeating stiffener pattern. It
calculates the skin and member stiffness in that patch, then spreads the member
contributions over the patch area. The result is one equivalent ABD stiffness
that a larger plate or shell model can use without drawing every stiffener.

The patch is treated as flat in the local `e1`-`e2` plane. Surface curvature is
handled later, when the stiffness is placed on a barrel, dome, or another shell
surface.

The member contribution follows one compact energy equation:

For a cell with area $A_\text{cell}$, a beam member contributes:

$$
\Delta\mathbf C_m =
\frac{\mu_m L_m}{A_\text{cell}}
\mathbf T_m^T\mathbf K_m\mathbf T_m.
$$

In this equation:

- $\mu_m$ says how many identical members the cell represents;
- $L_m$ is the length of that member inside the cell;
- $\mathbf K_m$ contains the member's beam stiffnesses;
- $\mathbf T_m$ converts panel deformation into deformation along the member.

Adding every member contribution to the skin gives the equivalent stiffness:

$$
\mathbf C_\text{stiffness}
=
\mathbf C_\text{skin}
+
\sum_m \Delta\mathbf C_m.
$$

The energy method is Tensyl's only homogenization path. It works for named
patterns, custom graph cells, and families of parallel stiffeners, and its
assembled stiffness is symmetric by construction. For straight families the
test suite checks it against the classical smeared-stiffener terms written out
by hand, such as $EA\cos^4\theta/b$ in $A_{11}$.

This follows the equivalent-plate idea used by Nemeth for stiffened laminated
plates and plate-like lattices. Tensyl treats those formulas as mechanics
guidance and keeps the energy path as the executable reference.

## How Geometry Enters the ABD Law

The homogenizer answers a local question: how stiff is this repeating patch in
its own directions? At any point on a plate or shell, those directions are the
local right-handed frame:

$$
\{\mathbf e_1,\mathbf e_2,\mathbf n\}.
$$

The same ABD relationship is used at every point:

$$
\mathbf r = \mathbf C_\text{stiffness}\boldsymbol\eta.
$$

Defining a barrel, dome, cone, or ellipsoid does not change the local cell
matrix by itself. Geometry enters later in three ways:

- the surface supplies local directions and curvature;
- a stiffness field selects the ABD stiffness at each point;
- a shell, buckling, or sizing model combines that stiffness with loads,
  boundary conditions, and the full structure.

Keeping these jobs separate makes the result easier to inspect. The cell says
how the local material responds, the surface says where that local patch sits,
and the solver handles the response of the complete structure.

The public stiffness-field helpers implement this separation directly:

- `ConstantStiffnessField` returns the same `C8` stiffness at each point and
  attaches the local frame from `surface.point_at(u, v)`. The numeric matrix is
  unchanged.
- `HomogenizedStiffnessField` calls a user-supplied cell factory at each surface
  point. The ABD stiffness can change pointwise if the factory changes pitch,
  member angle, eccentricity, section, material, or laminate with the local
  geometry.
- `ABDAtlas` stores sampled ABD stiffnesses, interpolates between them, and
  attaches the result to the target point's local frame.

For a cylinder, `e1` is axial, `e2` is circumferential, and `n` is outward. A
longitudinal stringer therefore has angle `0`, and a ring rib has angle
`pi/2`. The cylinder radius does not change the constant-field tangent, but it
does set the curvature scale used by validity ratios such as
$p/R_\text{min}$ and $h_s/R_\text{min}$.

For an ellipsoid, the same rule holds, but the frame and curvature vary over the
surface. Uniform parameter spacing is not uniform physical pitch on a triaxial
ellipsoid. If stiffener pitch or orientation is meant to follow physical
distance, the pointwise cell factory or atlas samples must encode that choice.
Tensyl will not infer a geodesic stiffener layout from the word "ellipsoid".

This is why the method is generalizable under its stated assumptions. Any smooth
surface that can provide a local tangent frame and curvature scale can host the
same local ABD law. The approximation is appropriate when the modeled response
is scale separated from stiffener height, stiffener pitch, and local curvature,
as discussed in [Validity Limits](validity.md). The mechanics basis follows the
equivalent-plate, first-order plate/shell, differential-geometry, and
homogenization sources listed in [References](../references.md).

## Inputs

The calculation needs a skin, one or more stiffener sections, and the repeating
cell that places those stiffeners:

- `skin` is the unstiffened skin or laminate ABD stiffness.
- `BeamSection` holds the stiffness of one member cross-section.
- `BeamMember` places a section in a cell with a length, angle, and offset.
- `CanonicalUnitCell.area` is the panel area represented by that repeat.
- `CanonicalUnitCell.geometry` holds the coordinates needed to draw the cell.

`stiffener_family_cell` takes `StiffenerFamily` inputs instead of individual
members. Each family supplies a section, direction, spacing, and offset, and
becomes one member with `multiplicity / spacing` of length per unit area.

## Beam Section Quantities

`BeamSection` stores centroidal member-local stiffnesses:

| Quantity | Meaning | Common units, US customary |
| --- | --- | --- |
| `EA` | axial stiffness | `lbf` |
| `EIy` | bending stiffness about member-local `y` | `lbf*in^2` |
| `EIz` | bending stiffness about member-local `z` | `lbf*in^2` |
| `GJ` | torsional stiffness | `lbf*in^2` |
| `kGAy` | in-plane shear stiffness | `lbf` |
| `kGAz` | transverse shear stiffness | `lbf` |

If a transverse-shear stiffness is omitted, Tensyl treats its contribution as
zero and records that assumption in the result.

Member bending within the panel plane stores no energy in this model. Under a
uniform wall strain and curvature, a member's axis stays straight in the panel
plane: curvature across the member rotates its cross-section about the member
axis but does not bend it. In Nemeth's notation this is the first-approximation
condition $\chi_Z=0$. `BeamSection` still stores `EIz` and `EIyz` as section
data, but the homogenizer does not use them.

Tensyl 0.3.1 and earlier offered an `include_in_plane_bending` switch that let
`EIz` resist plate curvature across the member. It was removed because beam
theory gives that term no energy; see the
[SP-8007 reconciliation](../validation/sp8007-reconciliation.md#why-earlier-reports-disagreed)
for the consequences.

For the member-frame in-plane shear term, the two effective offsets enter as

$$
\Gamma_{XY}
=
\frac{1}{2}\left(\gamma_{XY}^0+\bar{\bar z}\kappa_{XY}\right).
$$

In plain terms, a positive shear offset produces positive `B66` coupling under
the documented `+n` convention.

`BeamSection` still asks for stiffness products (`EA`, `EIy`, `EIz`, `GJ`,
`kGAy`, `kGAz`) because the homogenizer consumes centroidal beam stiffnesses.
The thin-wall section helpers are an upstream calculation layer; they do not
change the member strain map.

## Thin-Wall Section Geometry

The geometry helpers represent an isotropic stiffener as rectangular wall
segments in the member-local `(y, z)` section plane. The `X` axis runs along the
stiffener, `z` follows the wall normal used for member eccentricity, and `y` is
the in-plane transverse section axis. Section constructors measure `centroid_z`
from their own `z = 0` construction datum; member eccentricity is still measured
from the wall reference surface. If those datums differ, shift the centroid
coordinate before building the cell.

For each segment, Tensyl sums the rectangular area contribution and then shifts
to the section centroid. The resulting geometric properties are:

$$
A = \int_A dA,\qquad
I_y = \int_A (z-z_c)^2\,dA,
$$

$$
I_z = \int_A (y-y_c)^2\,dA,\qquad
I_{yz} = \int_A (y-y_c)(z-z_c)\,dA.
$$

The segment endpoints are midline coordinates. This is the intended thin-wall
modeling convention; local corner buildup, weld radii, and exact flange/web
overlap are outside this geometry helper.

For an isotropic material, the generated `BeamSection` uses:

$$
EA = E A,\qquad EI_y = E I_y,\qquad EI_z = E I_z,\qquad
EI_{yz} = E I_{yz}.
$$

The torsion value uses the open-section St Venant thin-wall approximation:

$$
J_{\mathrm{sv}} \approx \sum_i \frac{l_i t_i^3}{3},\qquad
GJ = G\,J_{\mathrm{sv}}.
$$

This is intentionally modest. It does not include closed-cell Bredt torsion,
restrained warping, local flange/web stress recovery, crippling, or joint
details. If those effects matter, compute the section properties externally and
pass a `BeamSection` directly. There is no shame in outsourcing a problem to the
tool that actually solves it.

There is no universal torsion constant for a stiffener drawing. Use the `GJ`
that belongs to the member idealization and boundary condition in the equivalent
wall. A freely warping blade, tee, angle, or channel should usually use an
open-section St Venant value. A tube, closed hat, or box should use a closed-cell
torsional stiffness only when the closed shear-flow path is truly part of the
member model; if the skin is already modeled as the plate skin, do not count the
same skin again inside the stiffener `J`. If joints, end constraints, or
neighboring structure restrain warping, use a section-analysis or finite-element
torsional stiffness for that restrained condition.

Transverse shear stiffnesses are optional. If `shear_correction_y` or
`shear_correction_z` is supplied, Tensyl computes `kGAy` or `kGAz` as
\(\kappa G A\). If a correction is omitted, the corresponding shear stiffness is
left as `None`, and the homogenization result records the same omitted-shear
assumption used for hand-entered `BeamSection` values.

## Diagnostics

The homogenizer returns `HomogenizationResult`, not just an ABD stiffness. The result
records:

- symmetry, positive-semidefinite status, rank, member count, and cell area;
- assumptions attached to the member strain map and section inputs;
- a `ValidityReport` with scale-separation ratios and warning codes.

!!! note "Agreeing with hand formulas is necessary, not sufficient"
    Matching the closed-form smeared-stiffener terms, Nemeth's tables, and the
    corrected SP-8007 formulas is a good sign, but it is not proof. They all
    share the same first-approximation member kinematics, so they can agree and
    still be wrong together. For high-consequence use, you still need test or
    finite-element evidence.

## Limits

The first homogenizer is a tangent-plane model. It does not model local joints,
fasteners, stiffener crippling, curved stiffener geodesics, or full shell
equilibrium. Use geometry validity ratios such as `h_over_R`, `p_over_R`, and
`p_over_L_response` to decide whether the local flat-cell assumption is
reasonable for the intended response mode.
