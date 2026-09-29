# SP-8007 Data Handoff

Extract the barred stiffness coefficients used by an orthotropic-cylinder
calculation while keeping the full ABD stiffness alongside them. For a cylinder,
local `e1` is axial and `e2` is circumferential.

## Coefficient Extraction

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

`Dbar_xy` combines bending and twisting as `2*D12 + 4*D66`, following the
engineering twist convention. It has the same force–length units as `D`.

## Orthogrid Handoff

Continue with the aluminum panel from the [family workflow](rib-patterns.md).
The same script also builds an equilateral isogrid:

```python
--8<-- "docs/examples/scripts/panel_workflows.py:sp8007"
```

The returned values have units N/m for the extensional constants, N for coupling,
and N m for bending. Carry cylinder radius, length, reference surface, and the
validity context into the downstream calculation with these constants.

`orthotropic_coefficients()` records off-axis entries in `unsupported_terms`
and `warnings` when they exceed the requested tolerance. That identifies which
parts of the full stiffness need treatment in the chosen cylinder equations.
The default filter combines absolute `tolerance` and block-relative
`relative_tolerance`; setting the latter to zero uses an absolute cutoff.

## Isogrid Variant

The isogrid uses equal ribs at 0° and ±60°. Its axial and circumferential barred
extensional constants agree to roundoff. For eccentric ribs, SP-8007's printed
isogrid bending equations need the explicit `EA*z²` terms described in the
[reconciliation report](../validation/sp8007-reconciliation.md#correcting-the-isogrid-typo).
That report compares all barred coefficients in the source's original units.

## Symmetric Laminate Variant

Use `symmetric.orthotropic_coefficients()` with the symmetric stack from the
[laminate example](materials-and-laminates.md#orthotropic-laminate). The same
coefficient view applies to a laminate or a homogenized ribbed panel. A symmetric
stack about its midplane gives coupling constants near zero.

Save the original stiffness or result through the
[JSON/YAML workflow](external-workflows.md#yaml-and-json) so the downstream
analysis retains the complete local constitutive data.
