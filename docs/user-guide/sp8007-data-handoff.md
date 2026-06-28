# SP-8007 Data Handoff

Tensyl can prepare equivalent wall-property data for a separate
SP-8007-style or orthotropic-cylinder calculation. Tensyl does not compute
SP-8007 knockdown factors, buckling loads, margins, or allowables.

An analyst commonly needs these data categories from a wall model:

- extensional stiffnesses `A`;
- bending and twisting stiffnesses `D`;
- transverse-shear stiffnesses `As` when relevant;
- whether membrane-bending coupling `B` is negligible or must be retained;
- equivalent orthotropic constants only under stated reduction assumptions;
- cylinder radius and length from geometry;
- pitch, stiffener height, and validity ratios such as `h_over_R`, `p_over_R`,
  and `p_over_L_response`;
- warnings, assumptions, and serialized artifacts for traceability.

## Extracting Wall Data

```python
from tensyl import Cylinder
from tensyl.io import to_yaml

surface = Cylinder(radius=120.0, length=300.0)
point = surface.point_at(150.0, 0.0)

wall = result.law
report = {
    "radius": surface.radius,
    "length": surface.length,
    "A": wall.A,
    "B": wall.B,
    "D": wall.D,
    "As": wall.As,
    "h_over_R": result.validity.h_over_R,
    "p_over_R": result.validity.p_over_R,
    "p_over_L_response": result.validity.p_over_L_response,
    "warnings": result.validity.warnings,
    "assumptions": result.assumptions,
    "frame_label": point.frame.label,
}

artifact = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)
```

Use the serialized artifact as a traceable record of the wall-property
calculation. Unit labels are metadata; Tensyl does not convert values.

## Equivalent Constants Are A Reduction

For an uncoupled orthotropic wall with negligible `B`, a later workflow may
derive engineering constants from stiffness blocks. That reduction is not the
primary Tensyl output and is not currently implemented as a public helper.

Do not infer scalar equivalent moduli from a coupled or misaligned wall without
documenting the reduction assumptions. If a downstream SP-8007 workflow needs a
specific reduction formula, add and verify that helper as a separate
implementation task with citations.

## Source Context

NASA SP-8007 is shell-buckling guidance. Nemeth's equivalent-plate work is a
source for stiffened equivalent-plate stiffness concepts. Tensyl's role here is
to compute and preserve local equivalent-wall stiffness data for use by another
calculation.

Next: [SP-8007 Data Prep Example](../examples/sp8007-data-prep.md).
