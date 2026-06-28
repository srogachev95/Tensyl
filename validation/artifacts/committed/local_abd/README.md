# Local ABD Committed Artifacts

This directory is reserved for curated Phase 1 local ABD extraction artifacts.

Commit compact outputs only:

- `target_abd.json` files with Tensyl-side reference stiffnesses;
- `metrics.json` files with target-side conditioning, symmetry, and
  strain-energy checks;
- `manifest.json` files with target-generation provenance;
- `extracted_abd.json`, `comparison_metrics.json`, and
  `extraction_manifest.json` files only for promoted solver-backed extraction
  slices;
- short mesh-convergence summaries;
- plots or tables small enough to review in git.

Do not commit raw meshes, solver decks, restart files, or exploratory scratch
output. Those belong under `validation/artifacts/scratch/local_abd/`.

The current subdirectories contain Tensyl target artifacts and target-side
metrics. `skin_only/` also contains the promoted CalculiX membrane/bending
`ABD6` extraction slice. The stiffened local ABD directories do not yet contain
promoted solver-backed extraction artifacts; their committed files remain
comparison oracles for future FE extraction runs. The YAML specs under
`validation/cases/local_abd/` define the expected artifact layout and promotion
rules for those planned solver-backed runs.
