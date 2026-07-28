# Changelog

All notable user-facing changes to Tensyl are recorded here.

Tensyl follows pre-1.0 semantic versioning: public APIs may still change between
minor versions, while patch releases should stay backward compatible except for
bug fixes that correct clearly wrong behavior.

## Unreleased

- Project roundoff-level assembled tangents onto Tensyl's symmetric
  ABD-plus-transverse-shear form while rejecting material block asymmetry and
  unsupported coupling through a typed `HomogenizationNumericalError`.
- Make tangent rank, positive-semidefinite diagnostics, and orthotropic
  reduction warnings relative to stiffness scale so floating-point
  interpretation remains stable across practical unit scales.
- Route rotated ABD stiffnesses through the same canonical tangent boundary,
  preventing large valid coupling blocks from failing fixed absolute symmetry
  checks.

## 0.3.0 - 2026-07-22

- Correct thin-wall section properties by treating each segment as a rotated
  rectangular strip and combining centroidal inertia with the parallel-axis
  theorem.
- Rename named-cell inputs around local-frame families and coordinate spans:
  `e1`, `e2`, `positive_diagonal`, `negative_diagonal`, `e1_pitch`, and
  `e2_pitch` replace ambiguous stringer/rib and family-spacing names.
- Add `diamond_cell` for Nemeth's figure-15 pattern.
- Retain plot-agnostic nodes, member-family edges, repeat vectors, and optional
  boundaries on every named cell through `CanonicalUnitCell.geometry` and
  `CellGeometry.segments()`; node coordinates are named `e1` and `e2`.
- Support separate extension-weighted `axial_eccentricity` and shear-weighted
  `shear_eccentricity` inputs, defaulting the latter to the former.
- Correct the eccentric in-plane shear sign so positive shear eccentricity
  produces positive `B66` coupling under the documented `+n` convention.
- Make Nemeth's `chi_Z = 0` assumption the default; retaining member `EIz` and
  `EIyz` is now an explicit `include_in_plane_bending=True` extension.
- Replace the circular Nemeth comparator with independent scalar `A`, `B`, `D`,
  and `As` assembly from basic-cell tables 4-9, and document the roundoff-level
  verification results.
- Add Google-style docstrings across the public API with concise input, output,
  and failure contracts.

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
