# Terminology

## ABD Stiffness

The local plate or shell relation between membrane strains, curvatures,
transverse shears, and their force/moment resultants. Tensyl represents it with
`ABDStiffness` in specified axes and about a specified reference surface.

## Concept Model

| Tensyl object | Engineering meaning |
| --- | --- |
| `IsotropicMaterial`, `OrthotropicPlyMaterial` | Elastic properties, optional mass density, and thermal expansion |
| `Ply` | A material layer with thickness and orientation |
| `ABDStiffness` | Plate stiffness and optional areal mass |
| `BeamSection` | Rib axial, bending, torsional, and optional shear stiffness products |
| `BeamMember`, `StiffenerFamily` | A rib or family with direction, length/spacing, and offsets |
| `CanonicalUnitCell` | Skin and represented ribs over a repeating panel area |
| `HomogenizationResult` | Equivalent stiffness with assumptions, diagnostics, and validity report |
| `Surface` | Position, frame, metric, and curvature of a plate or shell surface |
| `StiffnessField`, `ABDAtlas` | Stiffness distribution given by a callable or sampled grid |
| `ThermalResultants` | Membrane and moment loads per uniform temperature increment |

## Name Mapping

A *rib*, *stiffener*, and beam *member* refer to the same modeled contribution
here. A *skin* is the plate or laminate between the ribs. A *repeat cell* is the
area whose member energy is spread over the equivalent plate.

## ABD Blocks

`A` is membrane stiffness (N/m), `B` is membrane–bending coupling (N), `D` is
bending and twisting stiffness (N m), and `As` is transverse shear stiffness
(N/m). [The plate relation](../theory/equivalent-stiffness.md) defines their order.

## Resultants

Membrane and transverse shear resultants are forces per panel width. Moment
resultants are moments per width, giving units N m/m = N in SI. A recovered
rib force, by comparison, is the force in one physical rib.

<span id="why-not-scalar-equivalent-modulus"></span>
## Equivalent Modulus

A modulus obtained by reducing the membrane stiffness at a selected shell
thickness. Use [reduced orthotropic properties](../user-guide/solver-handoff.md#reduced-orthotropic-properties)
when the downstream model calls for material constants.

## Stiffener Pitch and Cell Area

Pitch describes a repeat distance. In named orthogrids, `e1_pitch` and
`e2_pitch` measure the cell along the corresponding axes. A rib along `e1` is
spaced by `e2_pitch`. Cell area is the represented tangent-plane panel area.

## Eccentricity

Signed distance along `+n` from the panel reference surface to the effective rib
centroid. It creates membrane–bending coupling about that reference.

## Tangent Plane

The locally flat plane spanned by surface directions `e1` and `e2`. Tensyl
assembles each cell's stiffness in that plane and places it on the surface
through a stiffness field.
