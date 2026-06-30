# Changelog

All notable user-facing changes to Tensyl are recorded here.

Tensyl follows pre-1.0 semantic versioning: public APIs may still change between
minor versions, while patch releases should stay backward compatible except for
bug fixes that correct clearly wrong behavior.

## 0.2.1 - 2026-06-30

- Tighten public README and documentation prose, including solver handoff,
  homogenization, validity, conventions, and example pages.
- Fix documentation consistency around Tensyl's current equivalent-stiffness
  terminology and coefficient handoff wording.

## 0.2.0 - 2026-06-30

- Add `ABDStiffnessCoefficients` and `ABDStiffness.coefficients` so direct
  equation workflows can read named `A`, `B`, `D`, and `As` terms without
  indexing matrices.
- Add `orthotropic_coefficients()` for aligned orthotropic shell handoffs,
  including the modified twisting coefficient `Dbar_xy = 2*D12 + 4*D66` and
  warnings when off-axis terms are present.
- Add an SP-8007 reconciliation report, validation harness, and public artifacts
  comparing Tensyl orthogrid/isogrid stiffnesses with SP-8007 elastic constants,
  including the corrected isogrid `EA z^2` terms and torsion-constant
  sensitivity plots.
- Add Nemeth grid-cell validation comparators for the committed validation
  cases.
- Remove root-level compatibility modules such as `tensyl.constitutive`,
  `tensyl.laminates`, `tensyl.rotations`, `tensyl.conventions`, and
  `tensyl.typing`; import from `tensyl` or the focused subpackages instead.

## 0.1.0 - 2026-06-29

Initial public PyPI release.

- Package `tensyl` for Python 3.12 and later.
- Provide core ABD stiffness models, strain/resultant conventions, rotations,
  materials, laminates, sections, tangent-plane cells, homogenizers, geometry
  surfaces, stiffness fields, and solver-neutral YAML/JSON I/O.
- Include validation fixtures and formal MkDocs documentation for mechanics
  assumptions, units, examples, and external-workflow handoff.
- Publish under the MIT license.
