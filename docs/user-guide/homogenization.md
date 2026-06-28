# Homogenization

The reference homogenizer is `EnergyHomogenizer`. It computes a local
equivalent ABD stiffness for a canonical tangent-plane unit cell.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
stiffness = result.stiffness
```

`result.stiffness` is an `ABDStiffness`. The same validity report is also attached to
`stiffness.validity`, so warnings travel with the ABD stiffness when it is passed to later
workflow steps.

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

## Diagnostics

Homogenization results include:

- `diagnostics["symmetric"]`;
- `diagnostics["positive_semidefinite"]`;
- `diagnostics["rank"]`;
- member and cell metadata where available.

Malformed or unsupported inputs raise typed homogenization exceptions. Finite
rank-deficient assemblies are returned with diagnostics and warnings so the
caller can decide whether the mechanism is acceptable.

!!! note "Diagnostics check the math, not the design"
    A clean diagnostics report does not mean the design is valid. Symmetry and
    positive energy are minimum consistency checks on the assembled operator —
    they say nothing about local failure, joints, finite-element correlation,
    shell buckling margins, or manufacturing detail. Passing here is table
    stakes, not a verdict.

## Comparing ABD Stiffnesses

Compare ABD stiffnesses block by block:

- compare `A`, `B`, `D`, and `As`;
- compare coupling ratios and warnings;
- rotate stiffnesses into a common frame before comparing anisotropic blocks;
- avoid comparing scalar equivalent moduli unless the reduction assumptions are
  stated.

Next: [Result Interpretation](result-interpretation.md).
