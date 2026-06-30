# Validation Roadmap

Tensyl's independent FEM validation program is **TBD** for the first official
release. The library exposes mechanics models, examples, and documented
assumptions, but this release does not claim a completed finite-element
validation campaign.

That is deliberate. Validation should be boring in the best way: repeatable
cases, plain comparison tables, reviewable plots, solver versions, input decks,
and enough provenance that another engineer can rerun the evidence without
guessing which button was pressed.

## What We Want To Build

The goal is a public evidence base that compares Tensyl's equivalent-stiffness
predictions against independent finite-element models. The planned validation
work will focus on:

- local ABD extraction for skin-only, unidirectional, orthogrid, eccentric
  orthogrid, and isogrid cells;
- flat-panel and barrel response comparisons using equivalent stiffnesses;
- limitation cases that show where the homogenized model should not be trusted;
- compact artifacts: manifests, metrics, plots, and comparison tables that can
  be reviewed without digging through raw solver output.

Until those artifacts are promoted, validation status should be read as planned
work rather than product evidence.

The first literature-facing audit is the
[SP-8007 reconciliation](sp8007-reconciliation.md). It compares Tensyl's
orthogrid and equilateral-isogrid stiffnesses with the SP-8007 elastic-constant
formulas, without treating either source as ground truth. The important result
is not a single pass/fail number. It is a map of which terms agree by convention
and which terms diverge because the models retain different bending physics.

## Why This Is LLM-Led

This is a good LLM-led project because most of the work is mechanical, exacting,
and repetitive: generate cases, write solver decks, run solvers, parse output,
compute residuals, make plots, record manifests, and keep the documentation
honest. None of that removes the need for engineering review. It moves the
human effort to the part where judgment matters.

The expected benefits are practical:

- hundreds of hours of repetitive setup and bookkeeping can be automated;
- every run can produce verifiable evidence instead of a hand-waved conclusion;
- comparison data becomes a durable asset for users, maintainers, and future
  regression tests;
- provenance and limitations can be written down as the evidence is generated,
  not reconstructed later from memory;
- reviewers can focus on mechanics, assumptions, and failure modes rather than
  manually shepherding solver files.

In short: let the machine do the clerical lifting, then make the evidence easy
for humans to distrust productively. That is usually where good validation
starts.
