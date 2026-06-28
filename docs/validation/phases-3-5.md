# Phases 3-5 Recommendations

This page is a documentation scaffold for the later FEM validation laboratory
phases. It does not promote solver results and should not be read as evidence
that Tensyl has already passed barrel, limitation-atlas, or gallery-level
finite-element validation.

The phase names below are validation-laboratory phases. They are related to, but
not identical with, the library implementation phases described elsewhere in the
project documentation.

## Status Summary

| Phase | Intended validation question | Status today | Evidence required before promotion |
| --- | --- | --- | --- |
| Phase 3 barrel response | Does a tangent-plane wall law remain credible when embedded in cylindrical geometry? | One smeared axial barrel target is executable; no promoted public solver cases. | Reproducible explicit barrel cases with solver provenance, mesh rationale, field metrics, and trends against validity ratios. |
| Phase 4 limitation atlas | Where is the homogenized wall model the wrong tool? | Planned; no promoted public solver cases. | Deliberate disagreement cases tied to documented validity warnings or out-of-scope behavior. |
| Phase 5 public validation gallery | Can stable cases be summarized as public evidence without hiding limitations? | Planned; no gallery page or summary matrix is promoted. | Generated tables, plots, regeneration commands, artifact manifests, and clear classification of confirmation, transition, and limitation cases. |

Until explicit solver artifacts exist, public docs should say "planned",
"scaffolded", or "smeared target only", not "validated". A missing result is a
perfectly respectable result when it is labeled before it can breed.

Current concrete pages:

- [Phase 3 Barrel Response](barrels.md) for the first smeared barrel target;
- [Phase 4 Limitation Atlas](limitations.md) for planned limitation cases;
- [Validation Gallery](gallery.md) for the generated summary table and plot.

## Phase 3: Barrel Response

Phase 3 should test the tangent-plane stiffness in cylindrical geometry. The
minimum useful comparison is a pair of models for the same barrel:

- an explicit stiffened-shell model with skin, stringers, rings, and documented
  local axes;
- a smeared-shell model using the Tensyl wall law exported with the same units,
  reference surface, and strain-resultant convention.

Recommended first cases:

| Case | Classification | Primary metric |
| --- | --- | --- |
| Orthogrid barrel in axial compression | Confirmation or transition, depending on pitch and radius. | Axial load-displacement slope and total strain energy. |
| Orthogrid barrel under pressure | Transition. | Radial displacement field and reaction balance. |
| Combined pressure and compression | Transition. | Coupled displacement fields and strain energy. |
| Linear eigenbuckling barrel | Transition. | Buckling factor and mode-shape MAC after compatible normalization. |
| Nonlinear imperfect barrel, when supported by the solver path | Limitation or transition. | Load-displacement path, onset load, collapse load, and imperfection sensitivity. |

Recommended sweeps:

- stiffener pitch over radius, `p/R`;
- stiffener height over radius, `h/R`;
- response wavelength over pitch;
- eccentricity and reference-surface placement;
- mesh density for skin bays and stiffener members.

Promotion should require solver version metadata, mesh settings, generated input
fingerprints, Tensyl artifact fingerprints, and a short interpretation of the
observed trend. Agreement in one barrel should not be generalized to all barrels
without a sweep. Cylinders have a habit of charging interest on small
assumptions.

## Phase 4: Limitation Atlas

Phase 4 should document cases where equivalent stiffness is expected to lose
local information. These cases are not failures of the validation lab; they are
guardrails for users.

Recommended limitation cases:

| Limitation | Why it belongs here | Expected documentation outcome |
| --- | --- | --- |
| Local skin buckling between stiffeners | A smeared wall law has no individual bay. | State that global ABD agreement does not imply bay-buckling prediction. |
| Bay-scale modal response | Mode wavelengths approach the stiffener pitch. | Tie error growth to response wavelength over pitch. |
| Stiffener intersection stress concentration | Homogenization averages intersections into a wall law. | Mark local stress peaks as out of scope for the wall model. |
| Cutouts and local load introduction | The load path is not locally periodic. | Require detailed FE modeling near the feature. |
| Abrupt stiffness-field changes | Atlas interpolation and homogenization assume smooth enough variation. | Report field-gradient diagnostics and warn against over-interpreting local values. |
| Large pitch or tall stiffeners on curved shells | Tangent-plane assumptions degrade with `p/R` and `h/R`. | Connect observed error to documented validity ratios. |

Each limitation case should be written so the expected disagreement is named
before results are interpreted. The goal is not to rescue every residual. The
goal is to tell users which question Tensyl was never answering.

## Phase 5: Public Validation Gallery

Phase 5 should turn promoted cases into a public evidence gallery. This phase
should only summarize cases whose artifacts can be regenerated from committed
specs and documented solver setup.

Recommended gallery structure:

- a summary matrix with rows for cases and columns for classification,
  solver-backed status, response quantity, agreement metric, and artifact path;
- per-case pages or sections with units, axes, boundary conditions, mesh
  rationale, solver provenance, and regeneration command;
- plots generated from committed metrics rather than hand-copied values;
- notes that distinguish Tensyl target artifacts from finite-element extraction
  or response evidence;
- a limitations section placed beside successes, not in a footnote.

Promotion gates for a gallery entry:

- the case spec is committed and names its classification;
- solver inputs are generated by documented commands;
- metrics are script-generated and stored in a small committed artifact;
- raw solver outputs stay out of git unless there is a reviewed reason;
- the page records whether the case confirms, maps a transition, or demonstrates
  a limitation;
- the validation index is updated so the public status table remains honest.

The gallery should be useful to an analyst who wants to rerun the evidence and
to a maintainer who wants to know what changed after a mechanics refactor. A
pretty plot without provenance is decoration, and decoration is not a validation
strategy.
