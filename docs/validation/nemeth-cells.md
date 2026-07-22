# Nemeth Cell Definitions and Verification

Tensyl's named cells reproduce the basic-cell member layouts in Michael P.
Nemeth's *A Treatise on Equivalent-Plate Stiffnesses for Stiffened
Laminated-Composite Plates and Plate-Like Lattices*. The implementation keeps
two representations of each pattern:

- `members` is the density-equivalent list used by the homogenizer;
- `geometry` retains nodes, drawable edges, family names, a boundary when one
  is meaningful, and two repeat vectors.

Keeping these separate matters. A shared boundary member may appear twice in a
drawing but contribute once to the repeated-cell energy.

## Naming and Coordinates

All named constructors use the local right-handed frame `e1`, `e2`, `n`.
Member families are named `e1`, `e2`, `positive_diagonal`, and
`negative_diagonal` according to their direction, not according to a
vehicle-specific role such as stringer or rib.

`e1_pitch` is a coordinate span along `e1`; `e2_pitch` is a coordinate span
along `e2`. Consequently, an `e1` family is spaced by `e2_pitch`, and an `e2`
family is spaced by `e1_pitch`. For a rectangular bay, the positive diagonal
angle is therefore

$$
\phi=\operatorname{atan2}(e2\_pitch,e1\_pitch).
$$

This convention removes the previous ambiguity between a family's direction
and the spacing normal to that family.

Nemeth defines two effective offsets for a nonhomogeneous member:

- `axial_eccentricity` is the extension-weighted offset $\bar z$;
- `shear_eccentricity` is the shear-weighted offset $\bar{\bar z}$.

Both are signed along `+n`. Omitting the shear-weighted value makes it equal to
the axial value, which is the usual homogeneous-member specialization.

## Pattern Coverage

| Constructor | Retained families | Nemeth definition |
| --- | --- | --- |
| `unidirectional_cell` | one arbitrary-angle family | Figures 4-6 |
| `orthogrid_cell` | `e1`, `e2` | orthogonal-grid specialization |
| `braced_orthogrid_cell(diagonal_pattern="double")` | `e1`, `e2`, both diagonals | Figure 14 and table 4 |
| `braced_orthogrid_cell(diagonal_pattern="single")` | `e1`, `e2`, alternating diagonals | Figure 16 and table 5 |
| `diamond_cell` | `e1`, both diagonals; no `e2` family | Figure 15 |
| `equilateral_isogrid_cell` | identical `0`, `+60`, `-60` degree families | equilateral limit of table 6 |
| `isosceles_triangle_grid_cell` | `e1`, both diagonals | Figure 17 and table 6 |
| `kagome_cell` | two `e1` members and both long diagonals | Figure 18 and table 7 |
| `hexagonal_grid_cell` | `e2`, both diagonals | Figure 21 and table 8 |
| `regular_hexagonal_grid_cell` | identical regular-hexagon members | Appendix F specialization |
| `star_cell` | four members from each of three families | Figure 23 and table 9 |
| `equilateral_star_cell` | identical equilateral-star members | Appendix G specialization |
| `sandwich_*_core_cell` | named core plus two shifted faces | Appendices H-J |

The single-brace cell uses Nemeth's $4L_xL_y$ basic-cell area and the six
members in table 5. Its diagonal density is half the crossed-brace case. The
Kagome cell uses twice the isosceles-triangle area and correspondingly doubled
member lengths or multiplicities, reproducing Nemeth's density equivalence.

## Strict Nemeth Kinematics

The default homogenizer follows Nemeth's first approximation, including
$\chi_Z=0$. Member `EIz` and `EIyz` therefore do not contribute by default.
Set `include_in_plane_bending=True` only when the deliberate beyond-Nemeth
extension is wanted; the result records that choice in its assumptions.

For positive effective offsets, Tensyl uses Nemeth's

$$
\gamma_{XY}(z)=\gamma_{XY}^0+z\kappa_{XY}.
$$

The shear contribution to `B66` is therefore positive for positive
`shear_eccentricity` under Tensyl's `+n` convention.

## Visualization Path

Every named constructor returns a non-`None` `cell.geometry`. No plotting
package is required by Tensyl. A renderer consumes ordinary segment records:

```python
geometry = cell.geometry
assert geometry is not None
segments = geometry.segments(repeat_a=3, repeat_b=2)

for segment in segments:
    axes.plot(
        [segment.start_e1, segment.end_e1],
        [segment.start_e2, segment.end_e2],
        label=segment.family,
    )
```

`geometry.repeat_vectors` exposes the translations directly, while
`geometry.boundary` identifies the ordered basic-cell perimeter when the source
defines one. This is sufficient for Matplotlib, Plotly, CAD, mesh-preview, or
custom SVG adapters without coupling the mechanics package to a renderer.

## Independent Numerical Verification

The validation comparator does not inspect `cell.members` and does not call the
production beam strain transform. Tests transcribe each table's member length,
direction cosines, multiplicity, section, and two effective eccentricities,
then assemble scalar `A`, `B`, `D`, and `As` terms from Nemeth's equations
30-39. This makes the comparison sensitive to a wrong cell area, member count,
angle, eccentricity, half-shear factor, or coupling sign.

The following results use deliberately unequal sections and unequal positive
and negative diagonal eccentricities. Errors are against the independently
assembled full `C8` tangent.

| Source case | Maximum absolute entry error | Relative Frobenius error |
| --- | ---: | ---: |
| Table 4, crossed braced orthogrid | `1.137e-13` | `1.099e-19` |
| Table 5, alternating single brace | `2.842e-14` | `3.658e-20` |
| Figure 15, diamond | `4.547e-13` | `1.595e-16` |
| Table 6, equilateral limit | `6.821e-13` | `3.780e-16` |
| Table 6, isosceles triangle | `4.547e-13` | `2.071e-16` |
| Table 7, Kagome | `4.547e-13` | `2.071e-16` |
| Table 8, hexagonal | `5.684e-14` | `1.573e-16` |
| Table 9, star | `4.547e-13` | `2.434e-16` |

These are floating-point roundoff-level differences, not fitted tolerances.
The tests also verify the corrected rectangular-diagonal angle, the table-5
half-density relation, the sign and independent weighting of `B11` and `B66`,
the opt-in `EIz` extension, repeat-cell areas, family labels, and tiled segment
generation.

The source is Nemeth, NASA/TP-2011-216882; see the complete citation in
[References](../references.md).
