# Homogenization

The reference homogenizer is `EnergyHomogenizer`.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
wall = result.law
```

`result.law` is a `LinearABDWall`. The same validity report is also attached to
`wall.validity`, so warnings travel with the wall law when it is passed to later
workflow steps.

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
