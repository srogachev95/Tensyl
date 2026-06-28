# Phase 3 Barrel Response

Phase 3 tests a Tensyl tangent-plane wall law after it is embedded in cylindrical
geometry. The current committed slice is a smeared barrel target only: it uses a
Phase 1 local ABD reference, applies a uniform barrel-wall resultant, and records
the response and validity ratios that future explicit barrel models must compare
against.

It is not an explicit barrel FE validation result. Cylinders are persuasive, so
the paperwork has to be stubborn.

## Status

| Case spec | Status today | Reference |
| --- | --- | --- |
| `validation/cases/barrels/orthogrid_axial_smeared.yml` | Tensyl smeared target executable; explicit FE barrel comparison planned. | `orthogrid_zero_eccentricity` local ABD target. |

Run the current Phase 3 baseline with:

```bash
uv run python validation/scripts/run_case.py validation/cases/barrels/orthogrid_axial_smeared.yml
```

Regenerate the committed smeared target artifacts with:

```bash
uv run python validation/scripts/run_case.py validation/cases/barrels/orthogrid_axial_smeared.yml --artifacts validation/artifacts/committed/barrels/orthogrid_axial_smeared
```

## Response Contract

The case uses a local cylindrical wall frame:

- `e1`: axial;
- `e2`: circumferential;
- `n`: outward radial.

The runner solves the same linear system used for the flat-panel target,

$$
\mathbf C_8 \boldsymbol\eta = \mathbf r,
$$

but reports barrel-specific response quantities: axial end shortening,
circumferential arc change, hoop radius change, total strain energy over the
cylindrical midsurface area, and validity ratios.

The first target records:

$$
\frac{p}{R}, \qquad \frac{p}{L_\mathrm{response}},
$$

and reserves $\frac{h}{R}$ for cases with a declared physical stiffener height.
Those ratios are the handles for later sweeps. One barrel result without a sweep
is a postcard, not a map.

## Artifact Roles

Committed Phase 3 smeared targets live under
`validation/artifacts/committed/barrels/<case-id>/`.

| File | Role |
| --- | --- |
| `smeared_response.json` | Tensyl smeared cylindrical-wall response target for the prescribed uniform resultant. |
| `metrics.json` | Equilibrium residual, energy positivity, validity ratios, and explicit-FE availability checks. |
| `manifest.json` | Provenance for the case spec, local ABD reference, command, and software versions. |

These files are comparison oracles for future explicit barrel FE runs. They do
not contain buckling factors, mode-shape MAC, nonlinear collapse loads, or
explicit-solver displacement-field residuals.

## Promotion Path

An explicit barrel comparison can be promoted only after the detailed barrel
model records:

- solver, mesh, boundary-condition, and command provenance;
- axial, radial, and circumferential response quantities on a compatible frame;
- a mesh-size rationale or convergence check;
- trend data against `p/R`, `h/R`, or response wavelength over pitch;
- a clear distinction between global smeared response and local bay or
  stiffener behavior.

The first barrel target is intentionally axial and zero-eccentric. More curved,
eccentric, pressure-loaded, and buckling cases belong after this target can be
regenerated and compared without ambiguity.
