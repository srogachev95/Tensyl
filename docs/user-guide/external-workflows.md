# External Workflows

Tensyl provides solver-neutral YAML and JSON serialization for wall laws and
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
    Path("wall-law.yaml"),
    units={"length": "in", "force": "lbf", "stress": "psi"},
)

same_result = read_yaml(Path("wall-law.yaml"))
```

Tensyl records unit labels but does not infer or convert units; inputs and
outputs alike must already share one consistent system (see
[Units and Consistency](units-and-consistency.md)).

## Schema

Every external-workflow artifact has:

- `schema_name`;
- `schema_version`;
- `artifact_type`;
- `producer`;
- `units`;
- `payload`.

The first public schema supports:

- `linear_abd_wall`;
- `homogenization_result`.

The canonical wall-law payload is the $8\times8$ `tangent_c8` operator. ABD and
transverse-shear blocks are reconstructed from that canonical tangent on load.

Malformed payloads raise `SchemaError`.

## Traceability

For analysis handoff, serialize the `HomogenizationResult` instead of only the
wall law when possible. The result payload preserves diagnostics, assumptions,
validity warnings, convention metadata, and unit labels alongside the wall
tangent.

Next: [SP-8007 Data Handoff](sp8007-data-handoff.md).
