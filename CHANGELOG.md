# Changelog

All notable user-facing changes to Tensyl are recorded here.

Tensyl follows pre-1.0 semantic versioning: public APIs may still change between
minor versions, while patch releases should stay backward compatible except for
bug fixes that correct clearly wrong behavior.

## Unreleased

- Add an SP-8007 reconciliation report, validation harness, and public artifacts
  comparing Tensyl orthogrid/isogrid stiffnesses with SP-8007 elastic constants,
  including the corrected isogrid `EA z^2` terms and torsion-constant
  sensitivity plots.

## 0.1.0 - 2026-06-29

Initial public PyPI release.

- Package `tensyl` for Python 3.12 and later.
- Provide core ABD stiffness models, strain/resultant conventions, rotations,
  materials, laminates, sections, tangent-plane cells, homogenizers, geometry
  surfaces, stiffness fields, and solver-neutral YAML/JSON I/O.
- Include validation fixtures and formal MkDocs documentation for mechanics
  assumptions, units, examples, and external-workflow handoff.
- Publish under the MIT license.
