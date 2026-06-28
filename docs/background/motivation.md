# Motivation

Stiffened thin-wall structures appear throughout aerospace engineering:
integrally stiffened panels, launch-vehicle barrels, ring-and-stringer shells,
isogrids, orthogrids, sandwich walls, and lattice-like facesheets.

Detailed stiffener-by-stiffener models are the gold standard — and a slog.
Rebuilding every rib for a trade study you will throw away next week is a poor
use of a Tuesday. Equivalent-wall modeling smears the stiffeners into a single
continuum wall law: you trade local detail for a small, auditable matrix that
still gets the global membrane, bending, twisting, and shear story right.

Tensyl's core rule is:

$$
\boxed{\text{Compute a local equivalent-wall constitutive law; embed that law in geometry-specific shell kinematics.}}
$$

This separation keeps the local homogenization problem small and auditable. A
wall law can be computed on a tangent plane, checked for validity, rotated, and
then attached to a flat panel, cylindrical barrel, dome, or other surface.

## Analyst Use Cases

Tensyl is intended for:

- early sizing of stiffened skins and shell walls;
- trade studies over stiffener pitch, height, orientation, and material;
- comparison of canonical grids such as unidirectional, orthogrid, isogrid,
  hexagonal, star, and sandwich-core cells;
- building solver-neutral wall-law artifacts for external workflows;
- creating reduced models for global stiffness studies.

Tensyl is not intended to hide the assumptions behind equivalent-wall modeling.
Every homogenized result carries diagnostics and validity information because a
wall law is useful only when its assumptions match the structural question.

New to the vocabulary — "wall law," "tangent plane," "scale separation,"
"pitch"? The [Terminology](terminology.md) page defines each precisely and is
worth a read before the Theory section.
