# FEM Validation Laboratory

The FEM validation laboratory is Tensyl's evidence bench. Tensyl computes local
equivalent-wall stiffnesses; the lab checks those stiffnesses against explicit
finite-element models and records where the approximation earns trust.

The boundary is deliberate:

```text
validation tooling -> tensyl
tensyl             -> never imports validation tooling
```

That keeps the public package small while letting validation scripts use heavier
external tools. The first case is intentionally modest: a skin-only isotropic
plate smoke test that runs without Gmsh or CalculiX and writes a metrics file
plus a manifest.

```bash
uv run python validation/scripts/run_case.py validation/cases/smoke/skin_only.yml
```

Scratch artifacts are written below `validation/artifacts/scratch/` and ignored
by git. Curated artifacts that are small enough to review belong under
`validation/artifacts/committed/`.

## Solver Setup

The solver-backed phases use CalculiX/CCX for structural solves and Gmsh for
mesh generation. They are installed outside the core `uv` environment by using a
project-local Conda-forge environment:

```bash
uv run python validation/scripts/setup_solvers.py --install-micromamba
uv run python validation/scripts/check_solvers.py --require
```

The setup script reads `validation/solver-environment.yml` and creates
`validation/.solver-env/`. Users do not need to activate that environment.
Discovery order is:

1. `TENSYL_CCX` and `TENSYL_GMSH`;
2. executables in `validation/.solver-env/bin/`;
3. executables on `PATH`.

Default tests skip or avoid solver-backed behavior when those tools are absent.
The explicit check command above is the one that fails loudly, as a setup check
should. Quiet failure is useful in tests; quiet setup is just a future afternoon
lost to a path typo.
