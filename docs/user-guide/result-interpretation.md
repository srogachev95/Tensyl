# Result Interpretation

`HomogenizationResult` is the main object to inspect after computing a
stiffened ABD stiffness.

```python
from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)

skin = isotropic_plate(
    IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
    thickness=0.080,
)
section = BeamSection(
    EA=3.2e6,
    EIy=2.4e4,
    EIz=6.5e3,
    GJ=4.0e3,
    kGAy=1.1e6,
    kGAz=0.9e6,
)
cell = orthogrid_cell(
    skin=skin,
    stringer_section=section,
    rib_section=section,
    stringer_spacing=6.0,
    rib_spacing=8.0,
    stringer_eccentricity=0.45,
    rib_eccentricity=0.45,
)

result = EnergyHomogenizer().compute(
    cell,
    validity_context=ValidityContext(
        characteristic_height=0.50,
        pitch=8.0,
        min_radius=120.0,
        response_length=80.0,
    ),
)

print(result.stiffness.A)
print(result.stiffness.B)
print(result.stiffness.D)
print(result.stiffness.As)
print(result.diagnostics)
print(result.assumptions)
print(result.validity.warnings)
```

Selected output, rounded:

| Item | Value |
| --- | --- |
| `A11`, `A22`, `A66` | `1.485e6`, `1.352e6`, `3.990e5` `lbf/in` |
| `B11`, `B22`, `B66` | `2.400e5`, `1.800e5`, `-3.609e4` `lbf` |
| `D11`, `D22`, `D66` | `1.133e5`, `8.559e4`, `1.670e4` `lbf*in` |
| `As11`, `As22` | `4.157e5`, `3.782e5` `lbf/in` |
| diagnostics | symmetric, positive-semidefinite, rank `8` |
| warnings | `p_over_R_exceeds_threshold`, `p_over_L_response_exceeds_threshold`, `membrane_bending_coupling_exceeds_threshold` |

For SI inputs the same blocks have units `N/m`, `N`, `N*m`, and `N/m`,
respectively. Tensyl preserves whichever system you fed it (see
[Units and Consistency](units-and-consistency.md)); it never converts.

## Reading The Blocks

- `A` controls membrane force response.
- `B` couples membrane strain to bending resultants and curvature to membrane
  resultants.
- `D` controls bending and twisting moment response.
- `As` controls transverse-shear resultants.

A symmetric tangent is required for an energy-based linear stiffness. A
positive-semidefinite tangent means the assembled stiffness has no negative-energy
mode at the tested tolerance. A rank-deficient tangent means some generalized
strain mode is unsupported by the modeled skin and members; Tensyl returns the
result with warnings instead of hiding that mechanism.

`stiffness.validity == result.validity` means the warnings stay attached when the
ABD stiffness is passed to a geometry field, serialization workflow, or downstream
adapter.

## Comparing Two ABD Stiffnesses

Compare `A`, `B`, `D`, and `As` directly after aligning frames. Compare
coupling ratios and validity warnings. Do not reduce to a scalar equivalent
modulus unless the stiffness is uncoupled enough for that reduction and the
engineering assumptions are written down.

!!! note "Consistency is not correlation"
    Numerical diagnostics prove the assembled operator is *self-consistent*.
    They do not prove a shell buckling margin, local stiffener failure, or
    finite-element correlation — those still have to be earned separately.

Next: [Geometry and Stiffness Fields](geometry-and-fields.md).
