# Terminology

## ABD Stiffness

An ABD stiffness is the local rule that turns plate or shell deformation into
force and moment resultants. Given membrane strain, curvature, and transverse
shear measured on a reference surface, it answers: what membrane forces, bending
moments, and shear resultants does this wall produce?

That rule only has meaning in a stated local frame
$\{\mathbf e_1,\mathbf e_2,\mathbf n\}$. The same numeric stiffness can describe
a flat panel, a cylindrical barrel, a dome, or another shell midsurface, but only
after the local directions and reference surface are clear. The ABD stiffness
owns the local mechanics; the surface owns the geometry and shell kinematics.

Tensyl uses the word "stiffness" deliberately. This object is not the whole
plate, shell, laminate, or solver model. It is the constitutive law those models
can consume. The first concrete class is `ABDStiffness`, which stores one
canonical $8 \times 8$ linear tangent with read-only block views `A`, `B`, `D`,
and `As`.   

## Concept Model

| Tensyl object | Engineering object | What it represents |
| --- | --- | --- |
| `IsotropicMaterial`, `OrthotropicPlyMaterial` | material property set | Constituent stiffness and density values before any section thickness or stacking operation. |
| `Ply`, `isotropic_plate`, `laminate_plate` | skin or laminate | A plate/shell skin ABD stiffness about a reference surface. |
| `BeamSection` | stiffener section stiffness values | Centroidal member stiffness products such as `EA`, `EIy`, `EIz`, `GJ`, and shear stiffnesses. |
| `BeamMember`, `StiffenerFamily` | stiffener member or repeated family | A straight member contribution with angle, length or spacing, eccentricity, and multiplicity. |
| `CanonicalUnitCell` | repeating stiffened panel cell | The tangent-plane area represented by one repeated stiffener pattern. |
| `HomogenizationResult` | equivalent-stiffness computation result | The computed ABD stiffness plus diagnostics, assumptions, source, and validity report. |
| `StiffnessField` | spatial distribution of ABD stiffnesses | A rule for obtaining an ABD stiffness at a point on a surface. |
| `Surface` | shell midsurface geometry | Positions, local frames, metric, curvature, and radius data for embedding ABD stiffnesses. |

## Name Mapping

| Tensyl name | Structural-engineering name |
| --- | --- |
| `ABDStiffness` | equivalent ABD stiffness or shell stiffness model |
| `A` | extensional or membrane stiffness block |
| `B` | membrane-bending coupling stiffness block |
| `D` | bending and twisting stiffness block |
| `As` | transverse-shear stiffness block |
| `BeamSection` | stiffener section stiffness values |
| `CanonicalUnitCell` | repeating stiffened panel cell |
| `StiffnessField` | spatial distribution of ABD stiffnesses over a surface |
| `ValidityReport` | scale-separation and coupling warning report |

## ABD Blocks

| Block | Engineering meaning | Common US units | Common SI units |
| --- | --- | --- | --- |
| `A` | membrane stiffness | `lbf/in` | `N/m` |
| `B` | membrane-bending coupling | `lbf` | `N` |
| `D` | bending and twisting stiffness | `lbf*in` | `N*m` |
| `As` | transverse-shear stiffness | `lbf/in` | `N/m` |

`B` is zero for many symmetric skins about their mid-surface. Eccentric
stiffeners, unsymmetric laminates, or an intentionally shifted reference
surface commonly make `B` nonzero.

## Resultants

Membrane resultants `N11`, `N22`, and `N12` are force per unit length. Bending
resultants `M11`, `M22`, and `M12` are moment per unit length. Transverse-shear
resultants `Q13` and `Q23` are force per unit length.

## Why Not Scalar Equivalent Modulus?

A scalar equivalent modulus is a derived interpretation, not the primary Tensyl
output. Scalar reductions can hide anisotropy, membrane-bending coupling,
twist coupling, transverse-shear behavior, and frame orientation. Tensyl keeps
the full ABD and transverse-shear operator as the primary result. Use scalar
engineering constants only when the reduction assumptions are stated and the
stiffness is sufficiently close to the reduced model.

## Stiffener Pitch and Cell Area

Pitch is the spacing between repeated stiffeners or repeated cells. A cell area
is the tangent-plane area represented by one canonical repeating unit.

Equivalent-stiffness homogenization is most defensible when pitch is small compared
with the response length scale that the model is meant to capture.

## Eccentricity

Stiffener eccentricity is the signed distance from the reference surface to
the stiffener centroid along the positive surface normal. Eccentricity drives
membrane-bending coupling in the equivalent ABD stiffness.

## Tangent Plane

Tangent-plane homogenization treats the repeating cell as locally flat. Surface
curvature enters later through shell kinematics and validity checks, not through
the first local cell stiffness assembly.
