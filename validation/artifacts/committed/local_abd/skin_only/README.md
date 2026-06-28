# Skin-Only Local ABD Artifacts

This directory contains Tensyl target artifacts and the first promoted
CalculiX extraction artifacts for the Phase 1 skin-only local ABD case.

## Committed Now

| File | Role |
| --- | --- |
| `target_abd.json` | Tensyl closed-form isotropic skin stiffness in local ABD order. |
| `metrics.json` | Target-side conditioning, symmetry, and canonical strain-energy checks. |
| `manifest.json` | Provenance for the Tensyl target generation; `solver_required` is `false`. |
| `extracted_abd.json` | CalculiX-generated membrane/bending ABD stiffness in Tensyl order. |
| `comparison_metrics.json` | Blockwise residuals comparing `extracted_abd.json` to `target_abd.json`. |
| `extraction_manifest.json` | Solver, command, input, and raw-output provenance for the extraction run. |

The current `metrics.json` is not a comparison against CalculiX output. It is a
target-health record. Use `comparison_metrics.json` for the solver comparison.

## Current Comparison

The promoted extraction covers the membrane/bending `ABD6` block only:

- `ABD6_relative_frobenius_error`: `3.79e-8`;
- `A_relative_frobenius_error`: `3.79e-8`;
- `B_relative_frobenius_error`: `2.69e-10`;
- `D_relative_frobenius_error`: `1.03e-7`;
- `symmetric_actual_ABD6`: `true`.

Raw meshes, decks, restart files, and exploratory logs belong under
`validation/artifacts/scratch/`, not in this committed directory.

## Current Limitations

The skin-only path is the first solver-backed extraction slice. The current
workspace has not promoted transverse-shear `As` extraction, full `8 x 8`
solver assembly, mesh-convergence documentation, or any stiffened-cell
solver-backed extraction artifacts.
