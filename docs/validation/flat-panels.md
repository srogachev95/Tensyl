# Phase 2 Flat Panel Response

Phase 2 compares equivalent smeared panels with explicit stiffener-by-stiffener
panel models. The current committed slice establishes the smeared side of that
comparison first: a uniform-resultant flat-panel response target computed from a
Phase 1 local ABD reference.

This is not yet an explicit FE agreement claim. It is the reference answer that
future detailed panel models must compare against. A ruler is useful before the
saw comes out.

## Status

| Case spec | Status today | Reference |
| --- | --- | --- |
| `validation/cases/flat_panels/orthogrid_axial_smeared.yml` | Tensyl smeared target executable; explicit FE panel comparison planned. | `orthogrid_zero_eccentricity` local ABD target. |

Run the current Phase 2 baseline with:

```bash
uv run python validation/scripts/run_case.py validation/cases/flat_panels/orthogrid_axial_smeared.yml
```

Regenerate the committed smeared target artifacts with:

```bash
uv run python validation/scripts/run_case.py validation/cases/flat_panels/orthogrid_axial_smeared.yml --artifacts validation/artifacts/committed/flat_panels/orthogrid_axial_smeared
```

## Response Contract

The case prescribes a uniform generalized resultant vector in Tensyl order:

$$
\mathbf r =
\begin{bmatrix}
N_{11} &
N_{22} &
N_{12} &
M_{11} &
M_{22} &
M_{12} &
Q_{13} &
Q_{23}
\end{bmatrix}^T.
$$

The runner loads the referenced local ABD case, computes Tensyl's smeared
stiffness matrix $\mathbf C_8$, and solves

$$
\mathbf C_8 \boldsymbol\eta = \mathbf r
$$

for the uniform generalized strain vector

$$
\boldsymbol\eta =
\begin{bmatrix}
\epsilon_{11}^0 &
\epsilon_{22}^0 &
\gamma_{12}^0 &
\kappa_{11} &
\kappa_{22} &
\kappa_{12} &
\gamma_{13}^0 &
\gamma_{23}^0
\end{bmatrix}^T.
$$

The reported strain-energy density is

$$
U = \frac{1}{2}\boldsymbol\eta^T \mathbf r,
$$

and total strain energy is `U * panel_area`.

## Artifact Roles

Committed Phase 2 smeared targets live under
`validation/artifacts/committed/flat_panels/<case-id>/`.

| File | Role |
| --- | --- |
| `smeared_response.json` | Tensyl smeared response target for the prescribed uniform resultant. |
| `metrics.json` | Equilibrium residual, energy positivity, and explicit-FE availability checks. |
| `manifest.json` | Provenance for the case spec, local ABD reference, command, and software versions. |

These files are comparison oracles for future explicit panel FE runs. They do
not contain explicit-solver metrics, mesh convergence, mode-shape comparisons,
or load-displacement residuals.

## Promotion Path

An explicit flat-panel comparison can be promoted only after the detailed panel
model records:

- solver, mesh, boundary-condition, and command provenance;
- a mesh-size rationale or convergence check;
- load-displacement slope and total-energy comparison against the smeared target;
- a clear statement of whether the response is global enough for homogenization
  to be expected to work;
- any local bay or stiffener modes as limitations rather than failed promises.

The Phase 2 baseline intentionally starts with a global axial resultant and a
zero-eccentric orthogrid target. More interesting cases can wait until the
boring one is boring for the right reasons.
