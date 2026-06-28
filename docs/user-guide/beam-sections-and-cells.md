# Beam Sections And Cells

Stiffener homogenization begins with member-local beam-section stiffnesses.

```python
from tensyl import BeamSection

section = BeamSection(
    EA=3.2e6,
    EIy=2.4e4,
    EIz=6.5e3,
    GJ=4.0e3,
    kGAy=1.1e6,
    kGAz=0.9e6,
)
```

Tensyl asks for stiffness products instead of raw dimensions because the current
homogenizer consumes centroidal beam stiffnesses. It does not calculate section
properties from hat, blade, tee, z, or custom cross-section geometry.

For US customary examples:

- `EA`, `kGAy`, and `kGAz` use `lbf`;
- `EIy`, `EIz`, and `GJ` use `lbf*in^2`;
- cell dimensions use `in`.

## Named Cells

Tensyl provides constructors for common tangent-plane patterns:

- `unidirectional_cell`;
- `orthogrid_cell`;
- `braced_orthogrid_cell`;
- `equilateral_isogrid_cell`;
- `isosceles_triangle_grid_cell`;
- `kagome_cell`;
- `hexagonal_grid_cell`;
- `star_cell`;
- sandwich-core variants.

Named constructors are convenience layers over canonical `BeamMember`
contributions. They do not model joint details, intersection stresses, or local
crippling.

## Angles And Eccentricity

Angles are measured in the local wall frame. `0` points along `e1`, `pi/2`
points along `e2`, and positive angles follow the positive rotation convention
about `n`.

Every eccentricity is signed along `+n` from the wall reference surface to the
member centroid. For an outward-normal cylinder, an external stringer has
positive `stringer_eccentricity`; an internal stringer has negative
eccentricity.

!!! warning "A wrong eccentricity sign is silently wrong"
    The sign changes the coupling block `B`, so flipping it produces a different
    physical wall law — with no validation error to catch it. See
    [Frames and Conventions](../theory/conventions.md) for the full sign rule.

## Graph Cells

Use `graph_unit_cell` when a named constructor is not enough. It converts local
tangent-plane nodes and edges into canonical beam members.

```python
from tensyl import CellEdge, CellNode, graph_unit_cell

cell = graph_unit_cell(
    area=48.0,
    skin=skin,
    nodes=(
        CellNode(0.0, 0.0),
        CellNode(6.0, 0.0),
        CellNode(0.0, 8.0),
    ),
    edges=(
        CellEdge(0, 1, section, eccentricity=0.45),
        CellEdge(0, 2, section, eccentricity=0.45),
    ),
)
```

Node coordinates and area must use the same length unit.

Next: [Frames and Conventions](../theory/conventions.md).
