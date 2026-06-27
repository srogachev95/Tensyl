# External Workflows

Phase 5 starts with solver-neutral YAML serialization. The goal is to let an
analyst compute, validate, save, reload, and hand off a Tensyl wall law without
binding the mechanics kernel to Nastran, a finite-element package, or a shell
solver.

The current implementation supports:

- `LinearABDWall` artifacts;
- `HomogenizationResult` artifacts;
- YAML read/write through `tensyl.io`;
- explicit schema versioning and producer metadata;
- Pydantic v2 validation for the schema payload;
- frame, convention, validity, diagnostics, assumptions, and metadata
  preservation.

It does not export solver property cards, shell sections, mesh data, or local
stress recovery data.

## YAML API

```python
from pathlib import Path

from tensyl.io import from_yaml, read_yaml, to_yaml, write_yaml

text = to_yaml(result, units={"length": "m", "force": "N", "mass": "kg"})
loaded = from_yaml(text)

write_yaml(result, Path("wall-law.yaml"), units={"length": "m", "force": "N"})
same_result = read_yaml(Path("wall-law.yaml"))
```

`to_yaml` and `write_yaml` accept either a `LinearABDWall` or a
`HomogenizationResult`. `from_yaml` and `read_yaml` reconstruct the appropriate
object from the artifact type stored in the file.

Tensyl records unit labels but does not infer or convert units. All stiffnesses,
lengths, masses, diagnostics, and metadata must already be in a consistent unit
system chosen by the caller.

## Schema V1

Every file uses a mapping root:

```yaml
schema_name: tensyl.external_workflow
schema_version: 1
artifact_type: homogenization_result
producer:
  name: tensyl
  version: 0.1.0
units:
  length: m
  force: N
payload:
  ...
```

The supported `artifact_type` values are:

- `linear_abd_wall`;
- `homogenization_result`.

The primary wall-law payload is the canonical \(8\times8\) `tangent_c8`
operator. The ABD and transverse-shear blocks are not serialized as separate
authoritative values because `LinearABDWall` already exposes them as views of
the canonical C8 storage. Reloading a file reconstructs the wall through the
same constructors used by ordinary Tensyl code, so shape, finite-value,
symmetry, frame, and convention validation still apply.

For a `LinearABDWall`, the payload stores:

- `tangent_c8`;
- frame vectors and frame label;
- strain-convention ordering, shear convention, reference surface, and normal
  convention;
- `areal_mass`;
- YAML-compatible wall metadata;
- optional `ValidityReport`.

For a `HomogenizationResult`, the payload stores the wall payload plus:

- result-level validity;
- diagnostics;
- assumptions;
- homogenizer source.

The imported result reattaches `result.validity` to `result.law.validity`, so
validity warnings continue to travel with the wall law after reload.

## Validation And Safety

YAML loading uses PyYAML's safe loader, then validates the payload with
Pydantic v2 models before reconstructing Tensyl value objects. Tensyl rejects:

- custom or unsafe YAML tags;
- non-mapping roots;
- unsupported schema names or versions;
- unknown artifact types;
- non-finite floats such as `NaN` and infinities;
- malformed matrix/vector shapes;
- metadata that cannot be represented with plain YAML scalars, lists, and
  mappings.

Malformed payloads raise `SchemaError`.

## Migration Policy

`schema_version` is an integer. Version 1 is the first public external-workflow
schema.

Before `1.0.0`, Tensyl may add fields to the schema when older readers can
ignore them safely. Any incompatible wire-shape change must increment
`schema_version` and keep the old loader path or document a migration command.
Solver-specific export formats should consume this neutral schema instead of
becoming the canonical persistence format.

Deferred Phase 5 work includes JSON, Nastran and other finite-element adapters,
shell-section export, sizing and optimization workflows, and performance
benchmarks.
