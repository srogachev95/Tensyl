# Changelog

All notable user-facing changes to Tensyl are recorded here.

Tensyl follows pre-1.0 semantic versioning: public APIs may still change between
minor versions, while patch releases should stay backward compatible except for
bug fixes that correct clearly wrong behavior.

## Unreleased

- Base the membrane-bending coupling warning on `B_residual`, measured in
  Mandel components after the best common reference shift. Rotating the axes
  or moving the reference surface no longer changes this indicator. Keep
  `B_fro` for the report's original surface and axes, and report the
  least-squares `neutral_surface_offset` in homogenization diagnostics.
- Compare `ABDStiffness`, `HomogenizationResult`, `SurfacePoint`, and
  `FlatPlate` by value. Equal stiffnesses now work as dictionary keys instead
  of raising NumPy's array truth-value error, and signed zeros no longer split
  the hashes of equal values.
- Keep the attached validity report when rotating an `ABDStiffness`; rotation
  used to drop it silently.
- Reject `Ellipsoid` polar angles outside `(0, pi)`. Those angles used to return
  an inward normal, which silently reversed every eccentricity sign.
- Count stiffener mass in homogenized `areal_mass`. `BeamSection` gains an
  optional `mass_per_length`, thin-wall sections fill it from material
  density, and a result now reports `areal_mass=None` with an assumption when
  the skin or any member has no mass data. It used to report the skin's mass
  alone, which understated a stiffened panel.
- Add `core_axial_eccentricity` to the sandwich core cells. The core used to be
  pinned to the reference surface, which is right only when that surface is the
  core midplane; any other choice of face shifts gave the wrong `D` block.
- Remove the `include_in_plane_bending` option from members, stiffener
  families, and every cell constructor. It let a member's `EIz` resist plate
  curvature across the member, which beam theory does not support; Nemeth's
  first approximation, `chi_Z = 0`, is now the only model. `EIz` and `EIyz`
  stay on `BeamSection` as section data.
- Rebuild the SP-8007 reconciliation without that extension. Every
  coefficient in every case now agrees with the corrected SP-8007 formulas to
  roundoff, so the report drops the low-`EIz` cases, the in-plane inertia
  sweep, and the bending-ratio plot.
- Replace `DirectECHomogenizer` with `stiffener_family_cell`, which turns
  `StiffenerFamily` inputs into a cell for `EnergyHomogenizer`. The direct path
  ran the same strain map through the same assembly, so it was never an
  independent check; the tests now compare family stiffnesses with the
  classical smeared-stiffener terms written out by hand.
- Drop the `symmetric` and `energy_consistent` diagnostics. Both were always
  `True` by construction, so they looked like checks without being any.
- Move `ValidityContext`, `ValidityThresholds`, and `ValidityReport` into
  `tensyl.core.validity`, with `validity_report_for_stiffness` in
  `tensyl.core.validity_checks` (all still exported from `tensyl` and
  `tensyl.homogenizers`), and type `ABDStiffness.validity` as
  `ValidityReport | None`. Anything else now raises `TypeError`.
- Remove the unused `LinearModel` protocol and the `ConstitutiveModel` alias;
  `HyperelasticModel` remains the stored-energy contract.
- Add `Frame2D.is_close` and use it wherever frames must agree: superposition,
  cells, fields, and atlases. Frames that differ only by label or by rotation
  roundoff are now compatible; exact `==` still backs hashing.
- Test Python 3.13 and 3.14 in CI alongside 3.12, and list them in the package
  classifiers.

## 0.3.1 - 2026-07-28

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
