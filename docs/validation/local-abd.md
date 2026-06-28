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
| `validation/cases/local_abd/skin_only.yml` | Executable now by the no-solver runner; solver-backed extraction planned. | Closed-form isotropic plate. |
| `validation/cases/local_abd/unidirectional.yml` | Planned solver-backed extraction. | `unidirectional_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/orthogrid_zero_eccentricity.yml` | Planned solver-backed extraction. | `orthogrid_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/orthogrid_eccentric.yml` | Planned solver-backed extraction. | `orthogrid_cell` with `EnergyHomogenizer`. |
| `validation/cases/local_abd/isogrid_equilateral.yml` | Planned solver-backed extraction. | `equilateral_isogrid_cell` with `EnergyHomogenizer`. |

The executable skin-only spec can be run with:

```bash
uv run python validation/scripts/run_case.py validation/cases/local_abd/skin_only.yml
```

The remaining specs use `case_type: local_abd_periodic_cell`. That type is a
runner contract for the solver-backed phase and is intentionally marked as
planned in each file.

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

A case can be promoted only when:

- the spec is committed and names the runner status honestly;
- all eight generalized-strain extraction load cases complete;
- the manifest records the solver versions, mesh settings, command, inputs, and
  generated outputs;
- metrics satisfy the case tolerances or the deviation is explained in the
  committed summary;
- raw solver files stay out of git;
- this page is updated if the executable status, thresholds, or artifact paths
  change.
