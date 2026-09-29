# Units and Consistency

Choose base units before building a material or cell. All calculations use the
supplied numerical values, and export labels record their meaning. This handbook
uses metres, newtons, kilograms, and kelvins for temperature increments.

## The Rule

Derive every input from the same length, force, and mass system. Convert material
moduli, dimensions, densities, and loads before constructing the model. For
example, enter 70 GPa as `70e9` Pa and 2 mm as `0.002` m in the SI examples.

## Reference Unit Systems

| Quantity | SI handbook | Inch–pound force system |
| --- | --- | --- |
| Length | m | in |
| Force | N | lbf |
| Modulus/stress | Pa = N/m² | psi = lbf/in² |
| `EA`, `kGA` | N | lbf |
| `EI`, `GJ` | N m² | lbf in² |
| `A`, `As` | N/m | lbf/in |
| `B` | N | lbf |
| `D` | N m | lbf in |
| Moment resultant | N m/m | lbf in/in |
| Mass density | kg/m³ | lbf s²/in⁴ for inch–lbf–second dynamics |
| Areal mass | kg/m² | lbf s²/in³ for inch–lbf–second dynamics |

Mass density is **mass per volume**, distinct from weight density. If a source
gives lbm/in³, convert it to the mass unit used by the dynamic solver or record
that independent mass label explicitly for a static property comparison.
For SI conversion, 1 in = 0.0254 m, 1 lbf ≈ 4.448221615 N, and
1 lbm = 0.45359237 kg. Thus 0.1 lbm/in³ is approximately 2768 kg/m³.

Source comparisons such as SP-8007 retain the source's inch–pound stiffness units.
Their input and output tables state those units directly.

## Recording Units in Exports

With the `result` from the walkthrough, the following is a complete export step:

```python
from tensyl.io import to_yaml

text = to_yaml(result, units={"length": "m", "force": "N", "mass": "kg"})
```

Labels travel in the artifact; numerical values are preserved. See
[files and sweeps](external-workflows.md) for the supported artifact types.
