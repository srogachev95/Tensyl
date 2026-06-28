# Validation Gallery

The gallery is the public evidence index for committed validation artifacts. It
is generated from manifests and metrics under `validation/artifacts/committed/`,
so target artifacts and solver-backed comparisons stay visibly separate.

Regenerate the summary and plot with:

```bash
uv run python validation/scripts/build_gallery_summary.py
```

The generated machine-readable summary is
`validation/artifacts/committed/gallery_summary.json`.

## Current Solver Comparison Plot

![Bar chart of promoted skin-only ABD6 solver comparison errors.](../assets/validation/gallery-solver-errors.svg)

Only one solver-backed comparison is promoted today: the skin-only local ABD
`ABD6` extraction. The stiffened local ABD, flat-panel, and barrel rows below
are target oracles or planned comparison scaffolds until explicit solver metrics
are promoted.

## Summary Matrix

| Case | Phase | Artifact role | Solver evidence | Primary metric |
| --- | --- | --- | --- | --- |
| `local_abd_skin_only` | Phase 1 local ABD | `calculix_extraction` | Promoted CalculiX `ABD6` comparison. | `ABD6_relative_frobenius_error = 3.79e-8` |
| `local_abd_unidirectional` | Phase 1 local ABD | `tensyl_target` | Planned; no promoted stiffened FE comparison. | `symmetric_C8 = true` |
| `local_abd_orthogrid_zero_eccentricity` | Phase 1 local ABD | `tensyl_target` | Planned; no promoted stiffened FE comparison. | `symmetric_C8 = true` |
| `local_abd_orthogrid_eccentric` | Phase 1 local ABD | `tensyl_target` | Planned; no promoted stiffened FE comparison. | `symmetric_C8 = true` |
| `local_abd_isogrid_equilateral` | Phase 1 local ABD | `tensyl_target` | Planned; no promoted stiffened FE comparison. | `symmetric_C8 = true` |
| `flat_panel_orthogrid_axial_smeared` | Phase 2 flat panel | `tensyl_smeared_panel_target` | Target only; explicit FE panel comparison planned. | `smeared_equilibrium_relative_residual = 3.41e-16` |
| `barrel_orthogrid_axial_smeared` | Phase 3 barrel | `tensyl_smeared_barrel_target` | Target only; explicit FE barrel comparison planned. | `p_over_R = 0.0667`, `p_over_L_response = 0.0833` |

## What Counts As A Result

The table uses three evidence levels:

- **Promoted solver comparison**: a solver-backed artifact with comparison
  metrics and provenance. Currently this exists only for the skin-only `ABD6`
  extraction.
- **Target oracle**: a Tensyl-generated target with metrics and manifest, ready
  for future solver comparison. These are real reference values, not agreement
  evidence.
- **Planned comparison**: a case whose solver model, parser, or promotion path is
  documented but not yet promoted.

When future FE cases are promoted, they should add generated metrics and plots
here rather than replacing the target rows. A good gallery can say "not yet"
without coughing.
