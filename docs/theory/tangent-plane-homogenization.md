# Tangent-Plane Homogenization

Start with a small repeating patch of skin and ribs. Give it a uniform panel
strain and curvature, calculate the energy stored in the skin and each rib,
and divide the rib energy by the repeat area. Matching that energy defines the
equivalent plate stiffness.

This is the first-approximation equivalent-plate construction in
[Nemeth, NASA/TP-2011-216882, equations 30–39](https://ntrs.nasa.gov/citations/20110004039).
Tensyl applies the same assembly to named grids, custom graph cells, and
independent families of parallel ribs.

## Inputs

| Input | Physical meaning |
| --- | --- |
| `skin` | Plate or laminate stiffness per panel area |
| `BeamSection` | Centroidal stiffness of a rib cross-section |
| `BeamMember` | Rib length, angle, eccentricity, and multiplicity |
| `CanonicalUnitCell.area` | Panel area represented by the repeat |
| `cell.geometry` | Repeat vectors, nodes, and edges used to draw the pattern |

A straight family with spacing $s$ supplies $1/s$ of rib length per panel area.
For a cell member of length $L_m$ and multiplicity $\mu_m$, that density is
$\mu_m L_m/A_\mathrm{cell}$. A shared boundary rib can be represented by two
half-members or one full member.

## Beam Section Quantities

Express panel strains in the member's local directions, indicated by primes.
The member strain map is

$$
\mathbf q_m=\mathbf T_m\boldsymbol\eta=
\begin{bmatrix}
\epsilon_{11}'+z_a\kappa_{11}'\\
(\gamma_{12}'+z_s\kappa_{12}')/2\\
\gamma_{13}'\\\kappa_{11}'\\-\kappa_{12}'/2
\end{bmatrix},\qquad
\mathbf K_m=\operatorname{diag}(EA,kGA_y,kGA_z,EI_y,GJ).
$$

Here $z_a$ is the axial eccentricity and $z_s$ is the in-plane shear eccentricity,
both measured along `+n`. Their usual value is the centroid offset. The five
entries represent axial strain, in-plane shear, transverse shear, bending
curvature, and twist rate. The halves and twist sign follow Nemeth's engineering
shear convention.

The rib contribution and complete plate stiffness are

$$
\Delta\mathbf C_m=\frac{\mu_mL_m}{A_\mathrm{cell}}
\mathbf T_m^T\mathbf K_m\mathbf T_m,\qquad
\mathbf C_8=\mathbf C_\mathrm{skin}+\sum_m\Delta\mathbf C_m.
$$

For a rib aligned with `e1`, this recovers
$\Delta A_{11}=EA/s$, $\Delta B_{11}=EAz_a/s$, and
$\Delta D_{11}=(EI_y+EAz_a^2)/s$. At angle $\theta$, the axial contribution
to $A_{11}$ becomes $EA\cos^4\theta/s$.

The first-approximation strain field keeps the member axis straight within the
panel plane: Nemeth's $\chi_Z=0$. `EIz` and `EIyz` remain available as section
properties; the five-mode energy above uses `EIy` for bending. The historical
change to that mapping is recorded in the
[SP-8007 reconciliation](../validation/sp8007-reconciliation.md#why-earlier-reports-disagreed).

## Thin-Wall Section Geometry

The [section guide](../user-guide/beam-sections-and-cells.md) derives `EA`, `EIy`,
and `GJ` from isotropic strips or laminated walls. Use N for axial and shear
stiffnesses, and N m² for bending and torsional stiffnesses in SI. Omitted
`kGAy` or `kGAz` contributes zero in the corresponding member mode; the result
records that choice.

## How Geometry Enters the ABD Law

The calculation takes place in the local tangent plane. A surface supplies
local directions and curvature; a field supplies the stiffness at that point.
With zero material angle, a constant field uses the original numeric matrix.
A nonzero angle rotates it into the surface axes. A varying field builds a
new local cell as the layout changes. See
[surfaces and fields](../user-guide/geometry-and-fields.md).

## Diagnostics

The result reports positive-semidefinite status, minimum eigenvalue, rank,
member count, cell area, and the best common neutral-surface offset. It also
carries the input assumptions and scale ratios. The
[result guide](../user-guide/homogenization.md#diagnostics) explains how to read them.

<span id="limits"></span>
Next: [Axes and reference surface](conventions.md), then
[modeling choices](validity.md) for the affine strain assumption and response scales.
