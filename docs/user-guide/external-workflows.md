# External Workflows

Tensyl provides solver-neutral YAML and JSON serialization for ABD stiffnesses and
homogenization results.

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
