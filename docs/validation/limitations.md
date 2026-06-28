# Phase 4 Limitation Atlas

The limitation atlas is where the validation lab records cases that Tensyl
should not be expected to predict. These are not failed confirmations. They are
boundary markers for the equivalent-wall model.

No limitation case is promoted yet. The table below is the public backlog of
cases that should become deliberate disagreement examples.

## Planned Cases

| Limitation case | Why it matters | Expected signal |
| --- | --- | --- |
| Local skin buckling between stiffeners | A smeared wall law has no individual bay. | Explicit FE shows a bay mode that the smeared model cannot represent. |
| Bay-scale modal response | Modal wavelength approaches stiffener pitch. | Mode-shape MAC degrades as wavelength-to-pitch ratio falls. |
| Stiffener intersection stress concentration | Homogenization averages joints and intersections. | Local stress peaks appear in explicit FE but not in ABD resultants. |
| Cutout or local load introduction | The load path is not locally periodic. | Local displacement and stress fields depend on geometry outside the wall law. |
| Abrupt stiffness-field change | Smooth-field assumptions break down near discontinuities. | Response error grows with stiffness-gradient severity. |
| Tall or sparse stiffeners on a curved shell | Tangent-plane assumptions degrade with `h/R` and `p/R`. | Barrel error trends with validity ratios rather than material constants alone. |

## Promotion Rules

A limitation case can be promoted only when:

- the expected disagreement is stated before results are interpreted;
- the explicit model records solver, mesh, boundary-condition, and command
  provenance;
- the response metric is one Tensyl is not claiming to predict;
- the docs link the disagreement to a validity warning or out-of-scope statement;
- raw solver outputs remain in scratch paths unless there is a reviewed reason
  to commit them.

The point is not to rescue every residual. The point is to make sure users do
not infer local-bay behavior from a clean global ABD comparison. That would be a
very tidy mistake.
