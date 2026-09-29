# File Format

## Schema

Every external-workflow artifact has:

- `schema_name`;
- `schema_version`;
- `artifact_type`;
- `producer`;
- `units`;
- `payload`.

Schema **version 3** supports:

| Artifact type | Reconstructed object | Preserved inputs |
| --- | --- | --- |
| `abd_stiffness` | `ABDStiffness` | Tangent, frame, convention, mass, metadata, validity |
| `homogenization_result` | `HomogenizationResult` | Stiffness plus diagnostics and assumptions |
| `canonical_unit_cell` | `CanonicalUnitCell` | Skin, area, members and full beam sections, offsets, multiplicity, frame, drawing, metadata |
| `abd_atlas` | `ABDAtlas` | Built-in surface definition, coordinate grids, stiffness samples, metadata |
| `thermal_resultants` | `ThermalResultants` | N_T and M_T per temperature increment, frame and convention |

The canonical stiffness payload is the $8\times8$ `tangent_c8` operator. ABD and
transverse-shear blocks are reconstructed from that canonical tangent on load.

Malformed payloads raise `SchemaError`. Loading cells and atlases runs their
normal constructors, so positive dimensions, valid indices, compatible frames,
consistent conventions, increasing grids, and rectangular sample shape remain
mandatory. Mechanics numbers must be finite numbers, not booleans or numeric
strings. If an atlas carries a `sample_digest`, it must match the restored
samples. This is a numeric consistency check, not a digital signature.

## Migration from Version 2

The readers still accept version 2 stiffness and homogenization-result
artifacts. Their numerical meaning is unchanged. All writers now emit version
3, including when re-exporting a v2 artifact. Version 2 cannot claim one of the
new artifact types, and other versions are refused. Downstream readers should
accept v3 before consuming newly written files. The package version remains
independent of this schema version; the validation campaign schemas have their
own names and versions.

## Cell Inputs and Sampled Atlases

Save the canonical inputs alongside a result when you need to repeat its
homogenization. For example, after building `cell`:

```python
from tensyl import CanonicalUnitCell, EnergyHomogenizer
from tensyl.io import from_json, to_json

saved = to_json(cell)
restored = from_json(saved)
assert isinstance(restored, CanonicalUnitCell)
recomputed = EnergyHomogenizer().compute(restored)
```

The artifact stores the resolved skin and beam properties used in the solve.
It does not serialize a Python factory or reconstruct the original material
layup or named-builder arguments. Member thermal expansion is preserved; skin
thermal loads remain a separate `thermal_resultants` artifact.

Atlases use the same `to_json`, `to_yaml`, and file helpers. The supported
surfaces are `FlatPlate`, `Cylinder`, `Sphere`, `SphericalCap`,
`ConicalFrustum`, and `Ellipsoid`, with their explicit constructor parameters.
Custom surface implementations and live field callables are refused; no Python
code is executed from a serialized factory. Loading rebuilds the sampled atlas
and recomputes its derived metadata, while retaining caller provenance. Save a
sampled atlas rather than its live field when you need a portable handoff.

