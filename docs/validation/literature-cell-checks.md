# Literature Cell Checks

Tensyl now has two kinds of literature-facing local checks. The SP-8007 audit
compares the barred orthogrid and isogrid constants used in a cylinder buckling
workflow. The Nemeth checks are narrower and more local: they compare Tensyl's
cell stiffness assembly against an independent transcription of the
basic-cell energy-equivalence method.

These are not finite-element validation cases. They do not prove that a smeared
wall will match a detailed panel, barrel, joint, cutout, or local buckling mode.
They prove something earlier in the chain: for a repeated stiffener cell, the
member lengths, angles, densities, eccentricities, and section stiffnesses are
being converted into the same tangent-plane ABD operator as the published
basic-cell equations.

## Nemeth Cell Comparator

The comparator lives in `validation/lib/tensyl_validation/nemeth.py`. It follows
Michael P. Nemeth's *A Treatise on Equivalent-Plate Stiffnesses for Stiffened
Laminated-Composite Plates and Plate-Like Lattices*, NASA/TP-2011-216882,
Eqs. 30-39 and Appendix E. The implementation is deliberately outside the
public `tensyl` package. Validation tooling may import Tensyl, but Tensyl must
not import validation tooling.

The tests compare Tensyl's energy homogenizer with this independent assembly for
representative cells:

- orthogrids with skin, braces, unequal member sections, and eccentric members;
- single- and double-braced orthogrids;
- centered and eccentric equilateral isogrids;
- isosceles-triangle and Kagome cells;
- hexagonal and star cells, including omitted member shear terms.

The reference code keeps the same generalized strain convention as Tensyl, but
it does not call the homogenizer or reuse its member tangent helper. That
separation matters. A bug in member density, brace multiplicity, diagonal angle,
eccentric axial coupling, or optional shear handling should appear as a matrix
difference in the comparator tests.

## What This Evidence Means

A passing Nemeth check says the local stiffness calculation is internally
consistent with the first-approximation equivalent-plate method used for the
named grid family. It is a formula-level confirmation case.

It does not say the homogenized model is the right model for every downstream
response. Pitch-to-wavelength separation, curvature, intersections, local bay
behavior, stiffener crippling, and load introduction still need explicit
validation. Those questions belong to the finite-element validation campaign.

## Sources

- Michael P. Nemeth, *A Treatise on Equivalent-Plate Stiffnesses for Stiffened
  Laminated-Composite Plates and Plate-Like Lattices*, NASA/TP-2011-216882,
  2011.
- Mark W. Hilburger, *Buckling of Thin-Walled Circular Cylinders*,
  NASA/SP-8007-2020/REV 2, 2020.
