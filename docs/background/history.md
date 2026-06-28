# Brief History

Equivalent-continuum modeling is older than the finite-element method, and for a
good reason: engineers needed answers before they had the compute to model every
stiffener. The idea has aged well. Tensyl is a modern implementation of a long
tradition, not a new invention.

## Classical Foundations

Aerospace structures have always leaned on stiffeners to raise buckling
resistance and tailor stiffness without paying for it in skin mass. The catch:
analysts then needed a practical way to fold those repeated constructions back
into global plate and shell calculations.

Classical plate and shell theory supplied the language — membrane resultants,
bending resultants, transverse shear, and stiffness matrices. Reissner- and
Mindlin-type first-order shear-deformation theories promoted transverse shear
from an afterthought to an explicit part of the wall model. Laminated-plate
theory then organized anisotropic skins into the familiar `A`, `B`, and `D`
stiffness blocks that Tensyl still speaks in today.

## Tensyl Today

Nemeth's NASA treatise is the primary source for Tensyl's first homogenization
family, and the reason it matters is that it does the unglamorous work: it
surveys decades of equivalent-plate results and lays out *both* the direct
equilibrium-compatibility and the strain-energy methods for stiffened laminated
plates and plate-like lattices, side by side. Tensyl implements that tradition as
a scientific Python library — explicit conventions, typed value objects,
verification checks, and neutral export formats — so the assumptions stay visible
instead of buried in a spreadsheet.

NASA SP-8007 and the related shell-buckling literature are the *why* behind all
of this: they are where equivalent wall properties earn their keep, especially
for thin cylindrical shells. Tensyl does not implement those buckling criteria —
it computes and audits the wall laws that feed them. See [References](../references.md)
for the full lineage.
