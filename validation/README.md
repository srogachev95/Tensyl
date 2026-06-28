# Tensyl Validation Laboratory

The validation laboratory is evidence infrastructure for Tensyl. It is allowed
to import `tensyl`; the public package must not import the validation tooling.

The first scaffold contains a no-solver smoke case:

```bash
uv run python validation/scripts/run_case.py validation/cases/smoke/skin_only.yml
```

The first Phase 2 flat-panel case is also a no-solver target. It computes the
smeared response oracle that a future explicit panel model must compare against:

```bash
uv run python validation/scripts/run_case.py validation/cases/flat_panels/orthogrid_axial_smeared.yml
```

Generated scratch output goes under `validation/artifacts/scratch/`, which is
ignored by git. Commit only compact, curated artifacts such as metrics, plots,
case summaries, and solver-version manifests.

External solver setup is project-local:

```bash
uv run python validation/scripts/setup_solvers.py --install-micromamba
uv run python validation/scripts/check_solvers.py --require
```

The solver environment lives in `validation/.solver-env/`. Shell activation is
not required; validation scripts discover tools from explicit environment
variables, the project-local environment, then `PATH`.
