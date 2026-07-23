# Nemeth Cell Verification

A named cell is a recipe for one repeating piece of a stiffener grid. The
recipe says which members are present, which way they run, and how much panel
area they represent. A missing member or a wrong repeat area changes the
equivalent stiffness even when the calculation itself runs without complaint.

We checked Tensyl's named cells against the layouts and basic-cell tables in
Michael P. Nemeth's *A Treatise on Equivalent-Plate Stiffnesses for Stiffened
Laminated-Composite Plates and Plate-Like Lattices*.

!!! success "Result"
    All eight source cases agree with an independent calculation to floating-point
    rounding. The largest relative matrix difference is less than
    `4e-16`, or about four parts in ten quadrillion.

## What Was Checked

The review covered two parts of every pattern:

1. **The shape:** nodes, member connections, directions, repeat dimensions,
   and basic-cell area were checked against Nemeth's figures and tables.
2. **The stiffness:** each named constructor was compared with a separate
   calculation written directly from Nemeth's table entries and equations.

Tensyl keeps those two jobs separate. `cell.geometry` holds the coordinates and
connections needed to draw the pattern. `cell.members` holds the member lengths
and counts used in the stiffness calculation. This distinction prevents a
shared edge from being counted twice simply because it appears on both sides of
a drawing.

## How Cell Dimensions Are Named

Every cell uses the local directions `e1`, `e2`, and `n`. The first two lie in
the panel; `n` points away from its reference surface.

```text
               e2
               ^
               |  e2_pitch
               |
               +------------> e1
                    e1_pitch
```

The pitch names describe the width and height of the repeat box:

| Input | Physical meaning |
| --- | --- |
| `e1_pitch` | Repeat distance measured along `e1` |
| `e2_pitch` | Repeat distance measured along `e2` |
| `e1_section` | Members that point along `e1` |
| `e2_section` | Members that point along `e2` |
| `positive_diagonal` | A diagonal that rises as `e1` increases |
| `negative_diagonal` | A diagonal that falls as `e1` increases |

This means an `e1` member repeats across the panel by `e2_pitch`, while an
`e2` member repeats by `e1_pitch`. Thinking of the pitches as repeat-box
dimensions is usually clearer than trying to name them after a stiffener
family.

!!! tip "The usual eccentricity input"
    For an ordinary homogeneous stiffener, provide its signed
    `axial_eccentricity` and omit `shear_eccentricity`. Tensyl then uses the
    same offset for both effects. Separate values are available for the less
    common nonhomogeneous-member case.

## Available Patterns

| Constructor | What the repeating pattern contains | Nemeth source |
| --- | --- | --- |
| `unidirectional_cell` | One family of parallel members at any angle | Figures 4-6 |
| `orthogrid_cell` | Crossing `e1` and `e2` members | Orthogonal-grid specialization |
| `braced_orthogrid_cell(diagonal_pattern="double")` | An orthogrid with both diagonals in each bay | Figure 14 and table 4 |
| `braced_orthogrid_cell(diagonal_pattern="single")` | An orthogrid with one alternating diagonal per bay | Figure 16 and table 5 |
| `diamond_cell` | `e1` members and both diagonals, with no `e2` members | Figure 15 |
| `equilateral_isogrid_cell` | Equal members at `0`, `+60`, and `-60` degrees | Equilateral limit of table 6 |
| `isosceles_triangle_grid_cell` | `e1` members with two mirrored diagonals | Figure 17 and table 6 |
| `kagome_cell` | Short `e1` members joined by longer mirrored diagonals | Figure 18 and table 7 |
| `hexagonal_grid_cell` | `e2` members joined by mirrored diagonals | Figure 21 and table 8 |
| `regular_hexagonal_grid_cell` | Equal members forming a regular hexagonal grid | Appendix F |
| `star_cell` | Four short members in each of three directions | Figure 23 and table 9 |
| `equilateral_star_cell` | Equal members forming an equilateral star grid | Appendix G |
| `sandwich_*_core_cell` | A named grid core between two shifted faces | Appendices H-J |

The source figures are reproduced alongside the constructor guide in
[Beam Sections and Cells](../user-guide/beam-sections-and-cells.md#named-cells).

## Viewing Any Named Cell

Every named constructor returns a cell with drawable geometry. Tensyl does not
depend on a plotting library, but it returns ordinary line segments that a
plotter, CAD preview, or SVG writer can use.

This optional Matplotlib helper works with any named cell:

```python
from matplotlib import pyplot as plt


def plot_cell(cell, *, repeat_a=2, repeat_b=2):
    geometry = cell.geometry
    if geometry is None:
        raise ValueError("This cell does not include drawable geometry.")

    _, axes = plt.subplots()
    for segment in geometry.segments(repeat_a=repeat_a, repeat_b=repeat_b):
        axes.plot(
            [segment.start_e1, segment.end_e1],
            [segment.start_e2, segment.end_e2],
            color="black",
        )

    axes.set_aspect("equal")
    axes.set_xlabel("e1")
    axes.set_ylabel("e2")
    return axes
```

After building a named cell, call `plot_cell(cell)` to draw two repeats in each
direction.

`segment.family` identifies the member family when a renderer needs separate
colors or line styles. `geometry.repeat_vectors` gives the two translations
that tile the pattern, and `geometry.boundary` gives the basic-cell outline when
the source defines one.

## How the Numerical Check Works

The comparison is intentionally independent of the production calculation:

1. Each test case gives different properties to the member families so that a
   swapped or missing family cannot hide behind symmetry.
2. The reference calculation uses member lengths, directions, counts, sections,
   and offsets transcribed directly from Nemeth's tables.
3. It calculates every `A`, `B`, `D`, and `As` entry without reading
   `cell.members` or calling Tensyl's production member transformation.
4. The test compares every entry in the resulting stiffness matrices.

This check is sensitive to the mistakes that matter here: the wrong cell area,
member count, angle, offset, shear factor, or coupling sign.

## Results

The largest entry difference reports the biggest numerical gap anywhere in the
matrix. The relative matrix difference compares the size of all differences
with the size of the reference matrix. Its formal name is the relative
Frobenius-norm error.

| Source case | Largest entry difference | Relative matrix difference |
| --- | ---: | ---: |
| Table 4, crossed braced orthogrid | `1.137e-13` | `1.099e-19` |
| Table 5, alternating single brace | `2.842e-14` | `3.658e-20` |
| Figure 15, diamond | `4.547e-13` | `1.595e-16` |
| Table 6, equilateral limit | `6.821e-13` | `3.780e-16` |
| Table 6, isosceles triangle | `4.547e-13` | `2.071e-16` |
| Table 7, Kagome | `4.547e-13` | `2.071e-16` |
| Table 8, hexagonal | `5.684e-14` | `1.573e-16` |
| Table 9, star | `4.547e-13` | `2.434e-16` |

These differences are floating-point rounding, not fitted tolerances.

## What This Result Means

The comparison supports the following claims:

- Tensyl represents the cited Nemeth cell shapes and repeat areas correctly.
- The production stiffness calculation agrees with a separately written
  source calculation for the tested cases.
- The corrected diagonal angle, single-brace member count, offset signs, and
  default member-bending behavior are covered by regression tests.

It is not a physical test campaign. It does not validate joints, local stress,
crippling, buckling, manufacturing details, or the accuracy of a homogenized
model when the grid is too coarse for the structural response of interest.

## Advanced Mechanics Notes

Nemeth defines separate effective offsets for axial and in-plane shear response.
Tensyl exposes them as `axial_eccentricity` and `shear_eccentricity`. Both are
signed along `+n`; when the shear value is omitted, it defaults to the axial
value.

By default, Tensyl also follows Nemeth's first approximation and leaves out
member bending within the panel plane. `BeamSection` still stores `EIz` and
`EIyz`, but the cell uses them only when
`include_in_plane_bending=True` is requested explicitly. The result records
that extension in its assumptions.

Positive shear eccentricity produces positive `B66` coupling under Tensyl's
documented `+n` convention. The equations and sign definitions are given in
[Tangent-Plane Homogenization](../theory/tangent-plane-homogenization.md) and
[Frames and Conventions](../theory/conventions.md).

The single-brace pattern uses the larger basic cell from Nemeth's table 5, so
its diagonal amount per unit area is half that of the crossed-brace pattern.
The Kagome cell similarly uses a larger repeat area and the corresponding
member counts from table 7.

The source is Nemeth, NASA/TP-2011-216882; see the complete citation in
[References](../references.md).
