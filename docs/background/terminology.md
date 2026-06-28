# Terminology

## Wall Law

A wall law is a local constitutive relation between generalized wall strains
and generalized stress resultants on a plate or shell reference surface. It is
always expressed in an explicit local frame
$\{\mathbf e_1,\mathbf e_2,\mathbf n\}$.

Tensyl says "wall" instead of only "plate," "shell," or "laminate" because the
same local constitutive law can be embedded in a flat panel, a cylindrical
barrel, a dome, or another shell midsurface. The wall law is local mechanics;
the shell surface supplies geometry and kinematics.

The first concrete wall-law class is `LinearABDWall`. It stores an $8 \times 8$
linear tangent whose block views are `A`, `B`, `D`, and `As`.

## Concept Model

| Tensyl object | Engineering object | What it represents |
| --- | --- | --- |
| `IsotropicMaterial`, `OrthotropicPlyMaterial` | material property set | Constituent stiffness and density values before any wall thickness or stacking operation. |
| `Ply`, `isotropic_plate`, `laminate_plate` | skin or laminate | A plate/shell skin wall law about a reference surface. |
| `BeamSection` | stiffener section stiffness values | Centroidal member stiffness products such as `EA`, `EIy`, `EIz`, `GJ`, and shear stiffnesses. |
| `BeamMember`, `StiffenerFamily` | stiffener member or repeated family | A straight member contribution with angle, length or spacing, eccentricity, and multiplicity. |
| `CanonicalUnitCell` | repeating stiffened panel cell | The tangent-plane area represented by one repeated stiffener pattern. |
| `HomogenizationResult` | equivalent-wall computation result | The computed wall law plus diagnostics, assumptions, source, and validity report. |
| `WallField` | spatial distribution of wall laws | A rule for obtaining a wall law at a point on a surface. |
| `Surface` | shell midsurface geometry | Positions, local frames, metric, curvature, and radius data for embedding wall laws. |

## Name Mapping

| Tensyl name | Structural-engineering name |
| --- | --- |
| `LinearABDWall` | equivalent wall stiffness or shell wall constitutive law |
| `A` | extensional or membrane stiffness block |
| `B` | membrane-bending coupling stiffness block |
| `D` | bending and twisting stiffness block |
| `As` | transverse-shear stiffness block |
| `BeamSection` | stiffener section stiffness values |
| `CanonicalUnitCell` | repeating stiffened panel cell |
| `WallField` | spatial distribution of wall laws over a surface |
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
wall is sufficiently close to the reduced model.

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
