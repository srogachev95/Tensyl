# Homogenization and Results

`EnergyHomogenizer` turns a repeating skin-and-stiffener cell into one equivalent
ABD stiffness. This is Tensyl's reference calculation.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
stiffness = result.stiffness
```

`result.stiffness` is an `ABDStiffness`. The same validity report is attached to
`stiffness.validity`, so warnings travel with the ABD stiffness when it is passed
to later workflow steps.

Keep the result object rather than extracting only its matrix. It carries the
stiffness and the information needed to judge the calculation:

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

The direct method is useful as a supported comparison or a faster route for
simple families. It does not replace the more general energy method.

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
    e1_section=section,
    e2_section=section,
    e1_pitch=8.0,
    e2_pitch=6.0,
    e1_axial_eccentricity=0.45,
    e2_axial_eccentricity=0.45,
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
| `B11`, `B22`, `B66` | `2.400e5`, `1.800e5`, `3.609e4` `lbf` |
| `D11`, `D22`, `D66` | `1.125e5`, `8.451e4`, `1.670e4` `lbf*in` |
| `As11`, `As22` | `4.157e5`, `3.782e5` `lbf/in` |
| diagnostics | symmetric, positive-semidefinite, rank `8` |
| warnings | `p_over_R_exceeds_threshold`, `p_over_L_response_exceeds_threshold`, `membrane_bending_coupling_exceeds_threshold` |

For SI inputs the same blocks have units `N/m`, `N`, `N*m`, and `N/m`,
respectively. Tensyl preserves whichever system you feed it (see
[Units and Consistency](units-and-consistency.md)); it never converts.

## Reading the Blocks

- `A` describes stretching and in-plane shear.
- `B` describes coupling between stretching and bending.
- `D` describes bending and twisting.
- `As` describes transverse shear.

For an energy-based linear model, the stiffness matrix should be symmetric and
should not contain a negative-stiffness mode. A rank-deficient result means the
modeled skin and members do not resist at least one kind of deformation. Tensyl
returns that result with a warning so the unsupported mode can be reviewed.

`stiffness.validity == result.validity` means the warnings stay attached when the
ABD stiffness is passed to a geometry field, serialization workflow, or
downstream adapter.

## Panel Mass

A stiffened panel weighs more than its skin, often a good deal more, so the
homogenized `areal_mass` counts both. Tensyl adds each member's mass per unit
length, spread over the repeat area, to the skin's areal mass:

$$
m_\text{panel} = m_\text{skin} + \frac{1}{A_\text{cell}}
\sum_{\text{members}} n_k\,L_k\,\mu_k ,
$$

where $n_k$ is the member multiplicity, $L_k$ its length inside the cell, and
$\mu_k$ its `BeamSection.mass_per_length`. Thin-wall sections fill in
$\mu_k = \rho A$ whenever their material has a density.

If the skin or any member section has no mass, the result reports
`areal_mass=None` and says so in `result.assumptions`. A skin-only number would
look like an answer while understating the panel, so Tensyl leaves the field
empty instead.

## Diagnostics

Homogenization results include:

- `diagnostics["symmetric"]`;
- `diagnostics["positive_semidefinite"]`;
- `diagnostics["rank"]`;
- member and cell metadata where available.

Malformed or unsupported inputs raise typed homogenization exceptions. Finite
rank-deficient assemblies are returned with diagnostics and warnings so the
caller can decide whether the mechanism is acceptable.

The energy assembly is a floating-point sum, so mathematically identical block
entries can differ in their last few bits when stiffnesses are large. Tensyl
checks those residuals against a dimensionless, scale-aware roundoff limit and
projects qualifying `A`, `B`, `D`, and `As` blocks onto exact symmetry. A
material asymmetry or coupling term outside the supported
ABD-plus-transverse-shear form raises `HomogenizationNumericalError`; it is not
silently discarded. Rank and positive-semidefinite diagnostics use the same
scale-aware principle, which keeps them independent of the chosen consistent
unit system.

!!! note "A clean diagnostics report is a floor, not a finish line"
    Symmetry and positive stiffness are basic consistency checks. They do not
    prove local strength, joint behavior, finite-element correlation, a shell
    buckling margin, or manufacturing suitability.

## Comparing ABD Stiffnesses

Compare ABD stiffnesses block by block:

- compare `A`, `B`, `D`, and `As`;
- compare coupling ratios and warnings;
- rotate stiffnesses into a common frame before comparing anisotropic blocks;
- avoid comparing scalar equivalent moduli unless the reduction assumptions are
  stated.
