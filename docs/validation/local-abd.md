# Phase 1 Local ABD Extraction

Phase 1 defines local finite-element extraction cases for the ABD tangent used
by Tensyl. The intent is deliberately local: impose generalized strains on a
representative tangent-plane cell, recover generalized resultants, assemble the
same component order that Tensyl uses, and compare the finite-element tangent to
the Tensyl reference.

This page is a public contract for the case specs. It is not a claim that every
case already has solver artifacts. The distinction matters; otherwise validation
turns into a very nicely formatted rumor.

## Status

| Case spec | Status today | Reference |
| --- | --- | --- |
| `validation/cases/local_abd/skin_only.yml` | Tensyl target executable; CalculiX membrane/bending `ABD6` extraction promoted. | Closed-form isotropic plate. |
| `validation/cases/local_abd/unidirectional.yml` | Tensyl target executable; solver-backed extraction planned. | `unidirectional_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/orthogrid_zero_eccentricity.yml` | Tensyl target executable; solver-backed extraction planned. | `orthogrid_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/orthogrid_eccentric.yml` | Tensyl target executable; solver-backed extraction planned. | `orthogrid_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/isogrid_equilateral.yml` | Tensyl target executable; solver-backed extraction planned. | `equilateral_isogrid_cell` with `EnergyHomogenizer`. |

One case can be run with:

```bash
uv run python validation/scripts/run_case.py validation/cases/local_abd/skin_only.yml
```

All five Tensyl target artifacts can be regenerated with:

```bash
uv run python validation/scripts/run_matrix.py validation/cases/local_abd/*.yml --artifacts validation/artifacts/committed
```

The first stiffened preflight deck set can be generated with:

```bash
uv run python validation/scripts/run_local_abd_solver.py validation/cases/local_abd/unidirectional.yml --prepare-probe-decks
```

Specs that include stiffeners use `case_type: local_abd_periodic_cell`. The
current runner computes the Tensyl target ABD for that contract. The FE
extraction side is being introduced skin-only first. The zero-eccentric
unidirectional case now has deterministic CalculiX probe decks for beam/shell
coupling review, but those decks are not promoted extraction artifacts. Standard
CalculiX beam sections are geometry-plus-material definitions, while Tensyl's
`BeamSection` stores stiffness products directly. Until the geometry-to-section
mapping is audited, stiffened extraction cases remain planned.

For the skin-only slice, separate the target and extraction artifact roles:

| Role | Current path | Meaning |
| --- | --- | --- |
| Tensyl target | `validation/artifacts/committed/local_abd/skin_only/target_abd.json` | Closed-form Tensyl stiffness in the documented component order. This is the comparison target. |
| Target-side checks | `validation/artifacts/committed/local_abd/skin_only/metrics.json` | Conditioning, symmetry, and canonical strain-energy checks computed from the Tensyl target only. This is not a solver comparison. |
| Target manifest | `validation/artifacts/committed/local_abd/skin_only/manifest.json` | Provenance for the target artifact generation. Its metadata marks `artifact_role: tensyl_target` and `solver_required: false`. |
| CalculiX extraction | `validation/artifacts/committed/local_abd/skin_only/extracted_abd.json` | Solver-extracted membrane/bending `ABD6` stiffness. `As` is intentionally unsupported in this artifact. |
| Comparison metrics | `validation/artifacts/committed/local_abd/skin_only/comparison_metrics.json` | FE-vs-Tensyl residuals for the promoted `ABD6` extraction. |
| Extraction manifest | `validation/artifacts/committed/local_abd/skin_only/extraction_manifest.json` | Solver, command, input, and raw-output provenance for the extraction run. |

## Axes and Component Order

All Phase 1 cases use a right-handed local tangent frame:

$$
\mathbf e_1 \times \mathbf e_2 = \mathbf n.
$$

The reference surface is the skin midsurface unless the case says otherwise.
Positive eccentricity is measured from that reference surface along `+n`, matching
the convention in [Frames and Conventions](../theory/conventions.md).

The extracted stiffness must use Tensyl's generalized strain and resultant
ordering:

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
\end{bmatrix}^T,
$$

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

Engineering shear strains are used for `gamma_12`, `gamma_13`, and `gamma_23`.
Do not silently substitute tensor shear. Factor-of-two mistakes wear good shoes.

## Units

The Phase 1 specs use US customary units:

| Quantity | Unit |
| --- | --- |
| Length | `in` |
| Force | `lbf` |
| Stress and modulus | `psi` |
| `A` and `As` blocks | `lbf/in` |
| `B` block | `lbf` |
| `D` block | `lbf*in` |
| Curvature inputs | `1/in` |

Tensyl does not convert units. The finite-element deck, Tensyl reference, and
reported artifacts must use the same system end to end.

## Expected Metrics

Each solver-backed run should report at least:

- the extracted `8 x 8` tangent in Tensyl order;
- blockwise `A`, `B`, `D`, and `As` absolute and relative differences;
- an energy-norm comparison over the eight extraction load cases;
- a symmetry residual for the extracted tangent;
- case-specific invariant checks from the YAML spec;
- solver, mesh, command, and input fingerprints in a manifest.

The committed artifacts currently include Tensyl-side targets and target metrics
under `validation/artifacts/committed/local_abd/<case-id>/`. Those files are the
comparison oracle for the solver-backed extraction, not evidence that the FE
side has agreed yet.

The promoted skin-only CalculiX slice exercises the membrane and bending ABD
components first. Its `ABD6_relative_frobenius_error` is `3.79e-8`, with
`A_relative_frobenius_error = 3.79e-8`, `B_relative_frobenius_error = 2.69e-10`,
and `D_relative_frobenius_error = 1.03e-7`. Transverse shear extraction for
`As`, full `8 x 8` assembly, mesh-convergence promotion, and stiffened-cell
solver models are still open items. The unidirectional probe decks share the
skin and beam nodes along the stiffener centerline and use a rectangular
CalculiX beam proxy that preserves the target `EA` and `EIy` only. They are
useful for coupling checks, not for FE-vs-Tensyl agreement claims. This staged
approach is intentional; plates are easier to interrogate before ribs and
stringers start rearranging the furniture.

The initial tolerances in the YAML specs are promotion thresholds, not laws of
nature. If the solver model exposes a better justified tolerance, update the spec
and record the reason with the promoted artifact.

## Case Intent

Skin-only checks the extraction machinery against the closed-form isotropic plate
ABD. With the reference surface at the skin midsurface, `B` must be zero, `A11`
must match `A22`, and `D11` must match `D22`.

Unidirectional adds one zero-eccentric stiffener family along local `e1`. It
should increase `A11` relative to skin-only and preserve zero membrane-bending
coupling.

Zero-eccentric orthogrid adds stringers along `e1` and ribs along `e2`, both on
the reference surface. It exercises two orthogonal member families while keeping
the `B` block negligible.

Eccentric orthogrid uses the same family layout with positive centroid offsets
along `+n`. It exists to catch reference-surface and sign-convention mistakes:
the leading `B` terms should be positive in the declared frame.

Equilateral isogrid uses three equal member families at `0`, `+60`, and `-60`
degrees. With zero eccentricity, it should keep `B` negligible and show the
expected equilateral symmetry in the leading `A` and `D` terms.

The mechanics background follows the ABD and equivalent-plate conventions in
[Equivalent-Stiffness Mechanics](../theory/equivalent-stiffness.md) and the
sources listed in [References](../references.md), especially Nemeth's equivalent
plate treatise and the Reissner-Mindlin plate references.

## Artifact Promotion

Scratch solver output belongs under `validation/artifacts/scratch/local_abd/`.
Committed Phase 1 artifacts belong under
`validation/artifacts/committed/local_abd/<case-id>/`.

A full `8 x 8` solver-backed case can be promoted only when:

- the spec is committed and names the runner status honestly;
- all eight generalized-strain extraction load cases complete;
- the manifest records the solver versions, mesh settings, command, inputs, and
  generated outputs;
- metrics satisfy the case tolerances or the deviation is explained in the
  committed summary;
- raw solver files stay out of git;
- this page is updated if the executable status, thresholds, or artifact paths
  change.

Partial slices, such as the current skin-only `ABD6` extraction, must name their
supported blocks and unsupported blocks in the committed artifacts instead of
implying full-case promotion.
