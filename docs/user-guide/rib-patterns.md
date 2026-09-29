# Rib Patterns and Repeat Cells

Choose a named pattern when the drawing has a regular grid, independent families
when each rib direction has its own spacing, or a graph when you want to specify
the nodes and edges yourself. All three feed the same energy calculation.

The examples share a 2 mm aluminum skin and a 25 mm blade:

```python
--8<-- "docs/examples/scripts/panel_workflows.py:setup"
```

## Named Cells

| Constructor | Pattern in plain terms |
| --- | --- |
| `unidirectional_cell` | One family of parallel stiffeners at any angle |
| `orthogrid_cell` | Crossing members along `e1` and `e2` |
| `braced_orthogrid_cell` | An orthogrid with one or two diagonal braces |
| `diamond_cell` | `e1` members with crossing diagonals and no `e2` members |
| `equilateral_isogrid_cell` | Equal members at `0`, `+60`, and `-60` degrees |
| `isosceles_triangle_grid_cell` | `e1` members joined by mirrored diagonals |
| `kagome_cell` | Short `e1` members joined by longer diagonals |
| `hexagonal_grid_cell` | Vertical members joined by mirrored diagonals |
| `star_cell` | A repeating six-point star pattern |
| `sandwich_*_core_cell` | A named grid core between two shifted faces |


The [orthogrid walkthrough](../getting-started/first-homogenized-cell.md) shows the
pitch convention: `e1_pitch` measures the repeat along `e1`; members running in
`e1` are separated by `e2_pitch`. The
[Nemeth pattern catalogue](../validation/nemeth-cells.md#available-patterns)
shows the other topologies and their source definitions.

For sandwich builders, use the core midplane as the common reference by default.
Face offsets locate the faces relative to it. If another reference is chosen,
set `core_axial_eccentricity` and both face offsets consistently.

## Independent Families

Specify the perpendicular spacing of each family directly:

```python
--8<-- "docs/examples/scripts/panel_workflows.py:families"
```

Each family contributes `multiplicity / spacing` of rib length per area.
Families can have unrelated spacings and angles; they need no common repeat box.
The result has the same stiffness as the walkthrough's orthogrid.

Angles are radians from local `e1` toward `e2` about `+n`. Eccentricities are
signed distances along `+n` from the panel reference surface. The default shear
eccentricity equals the axial eccentricity; set it separately for a section with
distinct effective axial and shear offsets.

## Graph Cells

Define a repeat rectangle with one complete rib on each of its lower and left
edges. Repeating the rectangle supplies the adjacent copies:

```python
--8<-- "docs/examples/scripts/panel_workflows.py:graph"
```

The graph builder derives member lengths and angles from the node coordinates.
Area has units m² and the repeat vectors have units m. For plotting,
`custom_cell.geometry.segments(repeat_a=2, repeat_b=2)` returns line segments;
the [plotting example](../validation/nemeth-cells.md#viewing-any-named-cell)
shows how to draw them.

## Check the Drawn Member Density

`density_audit` contains `(drawn, modeled)` length per area for each family:
10 m⁻¹ for `e1`, and 6.66667 m⁻¹ for `e2` in this example. The modeled value is
$\sum_m\mu_m L_m/A_\mathrm{cell}$.

The audit tiles the drawing 3×3, clips one repeat parallelogram, and merges
overlapping collinear segments within each family. Opposite-boundary ribs are
periodic copies: represent them as two half-members or one full member. Use a
stable family name for each physical family, so drawn and modeled quantities
refer to the same ribs. Unequal densities are returned for inspection.

Next: [Read the homogenization result](homogenization.md).

[Complete patterns and workflows script](../examples/scripts/panel_workflows.py).
