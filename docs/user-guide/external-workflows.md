# External Workflows

Tensyl provides solver-neutral YAML and JSON serialization for ABD stiffnesses and
homogenization results.

## Matrices Copied from Papers

A printed table may round its two copies of an off-diagonal coefficient
differently. `ABDStiffness` keeps its strict roundoff check and raises the
public `StiffnessSymmetryError` when that difference is material. To import
known printed-precision data, opt in explicitly:

```python
import numpy as np
from tensyl import ABDStiffness

A = np.array([[10.0, 2.000001, 0.0], [2.0, 8.0, 0.0], [0.0, 0.0, 3.0]])
stiffness = ABDStiffness.from_published_blocks(
    A, np.zeros((3, 3)), np.eye(3), np.eye(2), rtol=1e-6,
    metadata={"source": "illustrative rounded table"},
)
print(stiffness.metadata["published_blocks"])
```

The constructor requires `max(abs(C - C.T)) <= rtol * max(abs(C))` for
each block separately, then averages that block with its transpose. A large
membrane coefficient cannot hide asymmetry in a small coupling block. Metadata
records each block's largest absolute correction and the largest relative
correction across blocks; absolute values from A, B, and D have different units
and should not be compared directly. This import step does not check energy
positivity or resolve a unit or convention mismatch.

## YAML and JSON

```python
from pathlib import Path

from tensyl.io import from_yaml, read_yaml, to_yaml, write_yaml

text = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)

loaded = from_yaml(text)

write_yaml(
    result,
    Path("stiffness.yaml"),
    units={"length": "in", "force": "lbf", "stress": "psi"},
)

same_result = read_yaml(Path("stiffness.yaml"))
```

The values pass through untouched and the unit labels travel with them as
metadata, so both ends of the workflow have to agree on one consistent system
beforehand (see [Units and Consistency](units-and-consistency.md)).

## Schema

Every external-workflow artifact has:

- `schema_name`;
- `schema_version`;
- `artifact_type`;
- `producer`;
- `units`;
- `payload`.

The first public schema supports:

- `abd_stiffness`;
- `homogenization_result`.

The canonical stiffness payload is the $8\times8$ `tangent_c8` operator. ABD and
transverse-shear blocks are reconstructed from that canonical tangent on load.

Malformed payloads raise `SchemaError`.

## Traceability

For analysis handoff, serialize the `HomogenizationResult` instead of only the
ABD stiffness when possible. The result payload preserves diagnostics, assumptions,
validity warnings, convention metadata, and unit labels alongside the stiffness
tangent.

Next: [FEM Solver Handoff](solver-handoff.md).

## Parameter Sweeps

Use `sweep` to compare a finite Cartesian grid of cell inputs. It visits values
in the mapping's insertion order, with the last parameter changing fastest.
Each row contains the input parameters, all 21 named stiffness coefficients,
`areal_mass`, and a tuple of `warning_codes`.

```python
from tensyl import BeamSection, IsotropicMaterial, isotropic_plate, sweep, unidirectional_cell

material = IsotropicMaterial(E=70e9, nu=0.3, density=2700)

def build_panel(thickness):
    return unidirectional_cell(
        skin=isotropic_plate(material, thickness),
        member_section=BeamSection(EA=1e6, EIy=100, EIz=100, GJ=10, mass_per_length=0.2),
        spacing=0.1, axial_eccentricity=0,
    )

rows = sweep(build_panel, {"thickness": [0.001, 0.002, 0.003]})
for row in rows:
    print(row["thickness"], row["A11"], row["D11"], row["warning_codes"])
```

Pass `homogenizer=` to use a configured homogenizer. The helper materializes
finite input axes and all result rows; choose a modest grid. An empty mapping
calls the builder once with no arguments, while an empty axis produces no
rows. A builder or solver failure stops the sweep and preserves the exception,
adding the failed parameters as a note. Output column names are reserved so an
input cannot overwrite a result. Use the returned dictionaries with the
standard library's `csv.DictWriter` or your own dataframe/reporting tools.
