# Terminology

## Wall Law

A wall law relates generalized strains to generalized stress resultants at a
point on a plate or shell midsurface. In Tensyl, the first wall law is
`LinearABDWall`.

## ABD Blocks

The membrane, coupling, and bending blocks are:

| Block | Engineering meaning | Common units, US customary |
| --- | --- | --- |
| `A` | Membrane stiffness | `lbf/in` |
| `B` | Membrane-bending coupling | `lbf` |
| `D` | Bending and twisting stiffness | `lbf*in` |
| `As` | Transverse-shear stiffness | `lbf/in` |

`B` is zero for many symmetric skins about the reference surface. Eccentric
stiffeners and unsymmetric laminates commonly make `B` nonzero.

## Resultants

Membrane resultants `N11`, `N22`, and `N12` are force per unit length.
Bending resultants `M11`, `M22`, and `M12` are moment per unit length.
Transverse-shear resultants `Q13` and `Q23` are force per unit length.

## Stiffener Pitch And Cell Area

Pitch is the spacing between repeated stiffeners or repeated cells. A cell area
is the tangent-plane area represented by one canonical repeating unit.

Equivalent-wall homogenization is most defensible when pitch is small compared
with the response length scale that the model is meant to capture.

## Eccentricity

Stiffener eccentricity is the signed distance from the wall reference surface to
the stiffener centroid along the positive wall normal. Eccentricity drives
membrane-bending coupling in the equivalent wall law.

## Tangent Plane

Tangent-plane homogenization treats the repeating cell as locally flat. Surface
curvature enters later through shell kinematics and validity checks, not through
the first local cell stiffness assembly.
