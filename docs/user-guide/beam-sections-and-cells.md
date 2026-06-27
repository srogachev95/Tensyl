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
