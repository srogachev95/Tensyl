# Homogenization and Results

The reference homogenizer is `EnergyHomogenizer`. It computes a local
equivalent ABD stiffness for a canonical tangent-plane unit cell.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
stiffness = result.stiffness
```

`result.stiffness` is an `ABDStiffness`. The same validity report is attached to
`stiffness.validity`, so warnings travel with the ABD stiffness when it is passed
to later workflow steps.

Use the result object first. It contains the ABD stiffness and the context needed to
judge the calculation:

- `result.stiffness.A`, `B`, `D`, and `As` are the stiffness blocks;
- `result.diagnostics` reports numerical checks such as symmetry, rank, and
  positive-semidefinite status;
- `result.assumptions` records modeling assumptions;
- `result.validity.warnings` reports scale-separation and coupling warnings.

## Direct Equilibrium-Compatibility

`DirectECHomogenizer` supports straight stiffener-family inputs where the direct
method is applicable.

```python
from tensyl import DirectECHomogenizer

result = DirectECHomogenizer().compute(cell)
```

Use the direct method as a supported comparison or accelerator, not as a more
general replacement for the energy method.

## Reading the Result

`HomogenizationResult` is the main object to inspect after computing a stiffened
ABD stiffness.

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
respectively. Tensyl preserves whichever system you feed it (see
[Units and Consistency](units-and-consistency.md)); it never converts.

## Reading the Blocks

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
ABD stiffness is passed to a geometry field, serialization workflow, or
downstream adapter.

!!! note "Consistency is not correlation"
    Numerical diagnostics prove the assembled operator is self-consistent. They
    do not prove a shell buckling margin, local stiffener failure, finite-element
    correlation, or manufacturing suitability. Those still have to be earned
    separately; the matrix is not doing unpaid certification work.

## Diagnostics

Homogenization results include:

- `diagnostics["symmetric"]`;
- `diagnostics["positive_semidefinite"]`;
- `diagnostics["rank"]`;
- member and cell metadata where available.

Malformed or unsupported inputs raise typed homogenization exceptions. Finite
rank-deficient assemblies are returned with diagnostics and warnings so the
caller can decide whether the mechanism is acceptable.

!!! note "A clean diagnostics report is a floor, not a finish line"
    Symmetry and positive energy are minimum consistency checks on the assembled
    operator. They say nothing about local failure, joints, finite-element
    correlation, shell buckling margins, or manufacturing detail. A design still
    has to clear all of those on its own.

## Comparing ABD Stiffnesses

Compare ABD stiffnesses block by block:

- compare `A`, `B`, `D`, and `As`;
- compare coupling ratios and warnings;
- rotate stiffnesses into a common frame before comparing anisotropic blocks;
- avoid comparing scalar equivalent moduli unless the reduction assumptions are
  stated.
