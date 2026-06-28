# Motivation

Stiffened plates and shells appear throughout aerospace engineering:
integrally stiffened panels, launch-vehicle barrels, ring-and-stringer shells,
isogrids, orthogrids, sandwich sections, and lattice-like facesheets.

Detailed stiffener-by-stiffener models are the gold standard — and a slog.
Rebuilding every rib for a trade study you will throw away next week is a poor
use of a Tuesday. Equivalent-stiffness modeling smears the stiffeners into a single
continuum ABD stiffness: you trade local detail for a small, auditable matrix that
still gets the global membrane, bending, twisting, and shear story right.

Tensyl's core rule is: **Compute a local equivalent-stiffness model; embed that stiffness in geometry-specific shell kinematics.**

This separation keeps the local homogenization problem small and auditable. A
ABD stiffness can be computed on a tangent plane, checked for validity, rotated, and
then attached to a flat panel, cylindrical barrel, dome, or other surface.

![Two isogrid-stiffened cylinder specimens from Nemeth's equivalent-plate treatise.](../assets/nemeth-treatise/fig-03-isogrid-stiffened-cylinders.jpg)

*Source: Nemeth, NASA/TP-2011-216882, figure 3; full citation in
[References](../references.md).*

## Use Cases

Tensyl is intended for:

- early sizing of stiffened skins and shell sections;
- trade studies over stiffener pitch, height, orientation, and material;
- comparison of canonical grids such as unidirectional, orthogrid, isogrid,
  hexagonal, star, and sandwich-core cells;
- building solver-neutral stiffness artifacts for external workflows;
- creating reduced models for global stiffness studies.

Tensyl is not intended to hide the assumptions behind equivalent-stiffness modeling.
Every homogenized result carries diagnostics and validity information because a
ABD stiffness is useful only when its assumptions match the structural question.

New to the vocabulary — "ABD stiffness," "tangent plane," "scale separation,"
"pitch"? The [Terminology](terminology.md) page defines each precisely and is
worth a read before the Theory section.
