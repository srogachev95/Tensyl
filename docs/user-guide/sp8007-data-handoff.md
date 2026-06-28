# SP-8007 Data Handoff

Tensyl can prepare equivalent stiffness-property data for a separate
SP-8007-style or orthotropic-cylinder calculation. Tensyl does not compute
SP-8007 knockdown factors, buckling loads, margins, or allowables.

An analyst commonly needs these data categories from a stiffness model:

- SP-8007 orthotropic-cylinder extensional coefficients `Ebar_x`, `Ebar_y`,
  `Ebar_xy`, and `Gbar_xy`;
- bending and twisting coefficients `Dbar_x`, `Dbar_y`, and `Dbar_xy`;
- membrane-bending coupling coefficients `Cbar_x`, `Cbar_y`, `Cbar_xy`, and
  `Kbar_xy` when coupling is not negligible;
- transverse-shear stiffnesses `As` when relevant;
- whether membrane-bending coupling `B` is negligible or must be retained;
- cylinder radius and length from geometry;
- pitch, stiffener height, and validity ratios such as `h_over_R`, `p_over_R`,
  and `p_over_L_response`;
- warnings, assumptions, and serialized artifacts for traceability.

## Extracting Stiffness Data

```python
from tensyl import Cylinder
from tensyl.io import to_yaml

surface = Cylinder(radius=120.0, length=300.0)
point = surface.point_at(150.0, 0.0)

stiffness = result.stiffness
report = {
    "radius": surface.radius,
    "length": surface.length,
    "A": stiffness.A,
    "B": stiffness.B,
    "D": stiffness.D,
    "As": stiffness.As,
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

Use the serialized artifact as a traceable record of the stiffness-property
calculation. Unit labels are metadata; Tensyl does not convert values.

## SP-8007 Coefficients

For the built-in `Cylinder`, Tensyl's local `e1` direction is axial and local
`e2` is circumferential. Under the SP-8007 Section 4.1.2 orthotropic-cylinder
assumption that the orthotropy axes coincide with those directions, the barred
coefficients used in Eqs. 54-59 and 71-81 map to Tensyl's local ABD stiffness as:

| SP-8007 coefficient | Tensyl source |
| --- | --- |
| `Ebar_x` | `A[0, 0]` |
| `Ebar_y` | `A[1, 1]` |
| `Ebar_xy` | `A[0, 1]` |
| `Gbar_xy` | `A[2, 2]` |
| `Dbar_x` | `D[0, 0]` |
| `Dbar_y` | `D[1, 1]` |
| `Dbar_xy` | `2*D[0, 1] + 4*D[2, 2]` |
| `Cbar_x` | `B[0, 0]` |
| `Cbar_y` | `B[1, 1]` |
| `Cbar_xy` | `B[0, 1]` |
| `Kbar_xy` | `B[2, 2]` |

`Dbar_xy` is not just `D[2, 2]`; SP-8007 uses a modified twisting coefficient
that combines anticlastic bending and engineering twist terms. Tensyl's public
strain convention uses engineering shear/twist ordering
`(e11, e22, gamma12, k11, k22, k12, gamma13, gamma23)`, so the coefficient is
`2*D12 + 4*D66`.

!!! warning "Do not silently drop the off-axis terms"
    This coefficient set does not represent every possible ABD stiffness. If `A16`,
    `A26`, `B16`, `B26`, `B61`, `B62`, `D16`, or `D26` are not negligible,
    rotate the stiffness into its orthotropic axes or use a more general downstream
    buckling workflow. Dropping those terms to make the data fit the SP-8007
    mold throws away real anisotropy — and nothing will tell you that you did.

The data-prep example includes orthogrid, equilateral-isogrid, and symmetric
laminate variants that all use this same extraction rule.

## Source Context

NASA SP-8007 is shell-buckling guidance. Nemeth's equivalent-plate work is a
source for stiffened equivalent-plate stiffness concepts. Tensyl's role here is
to compute and preserve local equivalent-ABD stiffness data for use by another
calculation.

Next: [SP-8007 Data Prep Example](../examples/sp8007-data-prep.md).
