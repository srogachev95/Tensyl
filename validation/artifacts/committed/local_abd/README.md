# Local ABD Committed Artifacts

This directory is reserved for curated Phase 1 local ABD extraction artifacts.

Commit compact outputs only:

- `target_abd.json` files with Tensyl-side reference stiffnesses;
- `metrics.json` files with blockwise ABD comparison metrics;
- `manifest.json` files with solver, mesh, command, and input fingerprints;
- short mesh-convergence summaries;
- plots or tables small enough to review in git.

Do not commit raw meshes, solver decks, restart files, or exploratory scratch
output. Those belong under `validation/artifacts/scratch/local_abd/`.

The current subdirectories contain Tensyl target artifacts and target-side
metrics. No local ABD case has a promoted FE extraction result yet. The YAML
specs under `validation/cases/local_abd/` define the expected artifact layout and
promotion rules for the first promoted solver-backed run.
