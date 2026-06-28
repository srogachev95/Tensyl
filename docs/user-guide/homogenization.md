# Homogenization

The reference homogenizer is `EnergyHomogenizer`. It computes a local
equivalent wall law for a canonical tangent-plane unit cell.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
wall = result.law
```

`result.law` is a `LinearABDWall`. The same validity report is also attached to
`wall.validity`, so warnings travel with the wall law when it is passed to later
workflow steps.

Use the result object first. It contains the wall law and the context needed to
judge the calculation:

- `result.law.A`, `B`, `D`, and `As` are the stiffness blocks;
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

Diagnostics do not prove a design is valid. Symmetry and positive energy are
minimum consistency checks. They do not verify local failure, joints, finite
element correlation, shell buckling margins, or manufacturing detail.

## Comparing Wall Laws

Compare wall laws block by block:

- compare `A`, `B`, `D`, and `As`;
- compare coupling ratios and warnings;
- rotate laws into a common frame before comparing anisotropic blocks;
- avoid comparing scalar equivalent moduli unless the reduction assumptions are
  stated.

Next: [Result Interpretation](result-interpretation.md).
