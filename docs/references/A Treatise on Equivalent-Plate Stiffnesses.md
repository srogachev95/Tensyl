![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-001.jpg?height=334&width=395&top_left_y=369&top_left_x=244)

# A Treatise on Equivalent-Plate Stiffnesses for Stiffened Laminated-Composite Plates and Plate-Like Lattices 

Michael P. Nemeth<br>Langley Research Center, Hampton, Virginia

## The NASA STI Program Office . . . in Profile

Since its founding, NASA has been dedicated to the advancement of aeronautics and space science. The NASA scientific and technical information (STI) program plays a key part in helping NASA maintain this important role.

The NASA STI program operates under the auspices of the Agency Chief Information Officer. It collects, organizes, provides for archiving, and disseminates NASA's STI. The NASA STI program provides access to the NASA Aeronautics and Space Database and its public interface, the NASA Technical Report Server, thus providing one of the largest collections of aeronautical and space science STI in the world. Results are published in both non-NASA channels and by NASA in the NASA STI Report Series, which includes the following report types:

- TECHNICAL PUBLICATION. Reports of completed research or a major significant phase of research that present the results of NASA programs and include extensive data or theoretical analysis. Includes compilations of significant scientific and technical data and information deemed to be of continuing reference value. NASA counterpart of peer-reviewed formal professional papers, but having less stringent limitations on manuscript length and extent of graphic presentations.
- TECHNICAL MEMORANDUM. Scientific and technical findings that are preliminary or of specialized interest, e.g., quick release reports, working papers, and bibliographies that contain minimal annotation. Does not contain extensive analysis.
- CONTRACTOR REPORT. Scientific and technical findings by NASA-sponsored contractors and grantees.
- CONFERENCE PUBLICATION. Collected papers from scientific and technical conferences, symposia, seminars, or other meetings sponsored or co-sponsored by NASA.
- SPECIAL PUBLICATION. Scientific, technical, or historical information from NASA programs, projects, and missions, often concerned with subjects having substantial public interest.
- TECHNICAL TRANSLATION. English-language translations of foreign scientific and technical material pertinent to NASA's mission.

Specialized services also include creating custom thesauri, building customized databases, and organizing and publishing research results.

For more information about the NASA STI program, see the following:

- Access the NASA STI program home page at http://www.sti.nasa.gov
- E-mail your question via the Internet to help@sti.nasa.gov
- Fax your question to the NASA STI Help Desk at 443-757-5803
- Phone the NASA STI Help Desk at 443-757-5802
- Write to:

NASA STI Help Desk
NASA Center for AeroSpace Information
7115 Standard Drive
Hanover, MD 21076-1320
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-003.jpg?height=334&width=395&top_left_y=369&top_left_x=244)

# A Treatise on Equivalent-Plate Stiffnesses for Stiffened Laminated-Composite Plates and Plate-Like Lattices 

Michael P. Nemeth<br>Langley Research Center, Hampton, Virginia

National Aeronautics and
Space Administration

Langley research Center
Hampton, Virginia 23681-2199

Available from:

NASA Center for AeroSpace Information 7115 Standard Drive
Hanover, MD 21076-1320 443-757-5802

## Contents

List of Tables ..... 3
List of Figures ..... 4
Summary ..... 6
Symbols ..... 7
Introduction ..... 14
Direct Equilibrium-Compatibility Method for Rectilinear Stiffener Families ..... 19
Statical Equivalence ..... 21
Kinematical Equivalence ..... 23
Analysis Applications ..... 33
Orthogrid plate with doubly braced bays ..... 33
Orthogrid plate with singly braced bays ..... 34
Isosceles-triangle stiffener pattern ..... 35
Kagome stiffener pattern ..... 35
Basic-Cell Energy-Equivalence Method ..... 36
Analysis Application ..... 41
Orthogrid plate with doubly or singly braced bays ..... 42
Isosceles-triangle and Kagome stiffener patterns ..... 42
Hexagon-shaped stiffener pattern ..... 43
Star-shaped stiffener pattern ..... 43
Equivalent-Plate Stiffness for Sandwich Plates ..... 43
Equivalent-Plate Thickness ..... 47
Concluding Remarks ..... 49
References ..... 49
Tables ..... 60
Figures ..... 70
Appendix A - Equations of First-Order Transverse-Shear Deformation Beam Theory ..... 93
Appendix B - Equivalent-Plate Stiffnesses for a Plate Reinforced with Eccentric Stringers, Ribs, and Diagonal Braces ..... 104
Appendix C - Equivalent-Plate Stiffnesses for a Plate Reinforced with an Isosceles-Triangle or Kagome Grid Stiffener Arrangement ..... 108
Appendix D - Beam-Member Stiffness Coefficients ..... 112
Appendix E - Mathematica ${ }^{\circledR}$ Program for the Basic-Cell Energy-Equivalence Method ..... 115
Appendix F - Equivalent-Plate Stiffnesses for a Plate Reinforced with a Hexagon-Shaped Stiffener Arrangement ..... 125
Appendix G - Equivalent-Plate Stiffnesses for a Plate Reinforced with a Star-Cell-Shaped Stiffener Arrangement ..... 130
Appendix H - Equivalent-Plate Stiffnesses for a Hexagon-Cell-Core Sandwich Plate ..... 135
Appendix I - Equivalent-Plate Stiffnesses for a Orthogrid-Core Sandwich Plate ..... 139
Appendix J - Equivalent-Plate Stiffnesses for a Star-Cell-Core Sandwich Plate ..... 143

## List of Tables

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=47&width=1408&top_left_y=360&top_left_x=249) braces per bay (see figure 14) ..... 60
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=46&width=1408&top_left_y=507&top_left_x=247) brace per bay (see figure 16 ) ..... 61
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=46&width=1485&top_left_y=653&top_left_x=249) ..... 62
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=47&width=1486&top_left_y=751&top_left_x=244) two diagonal oraces per oay (see figure 1 b) ..... 63
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=46&width=1481&top_left_y=898&top_left_x=249) one diagonal brace per bay (see figure 6 b) ..... 64
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=46&width=1464&top_left_y=1044&top_left_x=249) triangle stiffener patern (see figure 7b) ..... 65
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=44&width=1432&top_left_y=1190&top_left_x=249) stiffener pattern (see figure igb) ..... 66
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=48&width=1376&top_left_y=1334&top_left_x=247) stiffener pattern (see figure 21 b) ..... 67
![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-007.jpg?height=46&width=1393&top_left_y=1480&top_left_x=247) stiffener pattern (see figure 230$)$ ..... 68

## List of Figures

1. Space Shuttle and external tank structure ..... 70
2. Densely stiffened orthogrid cylinder ..... 71
3. Isogrid-stiffened cylinders ..... 72
4. Unidirectionally stiffened plate geometry ..... 73
5. Cross-section A-A of a uniformly stiffened panel shown in figure 4b ..... 74
6. Plate and stiffener coordinate systems ..... 74
7. Examples of a nonhomogeneous stiffener cross-section ..... 75
8. Repetitive stiffened-panel element and coordinate systems ..... 75
9. Equivalent-plate wall ..... 75
10. Beam stresses at an arbitrary cross-section. ..... 76
11. Beam force and moment resultants at an arbitrary cross-section ..... 77
12. Stiffener beam forces and moments acting on cross-section of repetitive stiffened- panel element ..... 78
13. Plate stress resultants acting on cross-section of equivalent stiffened-panel wall ..... 78
14. Orthogonal stiffener pattern with two diagonal braces per bay and basic cell ..... 79
15. Diamond-shaped stiffener pattern. ..... 80
16. Orthogonal stiffener pattern with one diagonal brace per bay and basic cell. ..... 81
17. Isosceles-triangle stiffener pattern and basic cell ..... 82
18. Kagome stiffener pattern and basic cell ..... 83
19. Generation of an isosceles-triangle stiffener pattern obtained by translating the basic cell defined in figure 17 ..... 84
20. Generation of a Kagome stiffener pattern obtained by translating the basic cell defined in figure 18 ..... 84
21. Hexagon-shaped stiffener pattern and basic cell ..... 85
22. Generation of a hexagonal stiffener pattern obtained by translating the basic cell defined in figure 21 ..... 86
23. Isosceles-star-shaped stiffener pattern and basic cell ..... 87
24. Generation of an isosceles-star-shaped stiffener pattern obtained by translating the basic cell defined in figure 23 ..... 88
25. Sandwich plate with nonidentical anisotropic face plates and a hexagon-cell core ..... 89
26. Sandwich plate with nonidentical anisotropic face plates and an orthogrid core ..... 90
27. Sandwich plate with nonidentical anisotropic face plates and a star-cell core ..... 91
28. Arbitrary face plate of a sandwich plate ..... 92

## Summary

A survey of studies conducted since 1914 on the use of equivalent-plate stiffnesses in modeling the overall, stiffness-critical response of stiffened plates and shells is presented. Two detailed, comprehensive derivations of first-approximation equivalent-plate stiffnesses are also presented that are based on the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. First, a derivation based purely on static and kinematic equivalence between a stiffened plate and its homogenized equivalent is presented, followed by a derivation based on equivalence of the strain-energy density. In both derivations, the stiffener members are modelled as beams that are shear deformable within and transverse to the plane of the plate, consistent with the classical continuum mechanics representation of solids. Additionally, each stiffener is presumed to be constructed, at most, in a nonhomogeneous manner from orthotropic materials with one axis aligned with the stiffener axis and the other two axes aligned with the cross-sectional axes. This presumption allows the computation of equivalent-plate stiffnesses for stiffened panels such as those in which the stiffener caps are reinforced with high-strength, pultruded rods. Consistent with a first-approximation analysis, inplane bending of the stiffeners and total compatibility between the plate skin and the stiffeners are neglected.

Equivalent-plate stiffness expressions, and a corresponding symbolic manipulation computer program, are also presented for several different stiffener configurations. These expressions are very general and exhibit the full range of anisotropies permitted by the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. The expressions presented in the present study were also compared with available, previously published results. For the most part, the previously published results are for special cases of the general expressions presented herein and are almost in complete agreement. Analysis is also presented that extends the use of the equivalent-plate stiffness expressions to sandwich plates with nonidentical, anisotropic face plates, and expressions for equivalent-plate thicknesses are presented.

## Symbols

The primary symbols used in the present study are given as follows. Additional symbols are defined in Tables 1-9.

| a | dimension of hexagonal beam grid (see figure 21), in. |
| :--- | :--- |
| $\mathrm{A}_{\mathrm{s}}$ | area of prismatic stiffener cross-section (see figure 10), $\mathrm{in}^{2}$ |
| $\mathrm{A}_{\text {cell }}$ | area of basic cell forming beam grid (see equation (39a) and figures 14, 16-18, 21 , and 23), $\mathrm{in}^{2}$ |
| $\mathrm{A}_{11}, \mathrm{~A}_{12}, \mathrm{~A}_{16}, \mathrm{~A}_{22}, \mathrm{~A}_{26}, \mathrm{~A}_{66}$ | equivalent-plate membrane stiffnesses (see equation (22a)), $\mathrm{lb} / \mathrm{in}$. |
| $\mathrm{A}_{44}, \mathrm{~A}_{45}, \mathrm{~A}_{55}$ | equivalent-plate transverse-shearing stiffnesses (see equation (22b)), lb/in. |
| $\begin{aligned} & \mathrm{A}_{11}^{\text {core }}, \mathrm{A}_{12}^{\text {core }}, \mathrm{A}_{16}^{\text {core }}, \\ & \mathrm{A}_{22}^{\text {cocre }}, \mathrm{A}_{26}^{\text {core }}, \mathrm{A}_{66}^{\text {core }} \end{aligned}$ | contribution of sandwich-plate core to equivalent-plate |
| $\begin{aligned} & A_{11}^{\text {plate }}, A_{12}^{\text {plate }}, A_{16}^{\text {plate }}, \\ & A_{22}^{\text {plate }}, A_{26}^{\text {plate }}, A_{616}^{\text {plate }} \end{aligned}$ | plate contribution to equivalent-plate membrane stiffnesses |
| $\begin{aligned} & \mathbf{A}_{11}^{, \text {plate }}, \mathbf{A}_{12}^{, \text {plate }}, \mathbf{A}_{16}^{, \text {plate }}, \\ & \mathbf{A}_{22}^{, \text {plate }}, \mathbf{A}_{26}^{, \text {plate }}, \mathbf{A}_{66}^{, \text {plate }} \end{aligned}$ | contribution of sandwich face plate to equivalent-plate |
| $\mathbf{A}_{44}^{\text {core }}, \mathbf{A}_{45}^{\text {core }}, \mathbf{A}_{55}^{\text {core }}$ | contribution of sandwich-plate core to equivalent-plate transverse-shearing stiffnesses (see equation (47d)), lb/in. |
| $\mathbf{A}_{44}^{\text {plate }}, \mathbf{A}_{45}^{\text {plate }}, \mathbf{A}_{55}^{\text {plate }}$ | plate contribution to equivalent-plate transverse-shearing stiffnesses (see equation (23d)), lb/in. |
| $\mathrm{A}^{\text {, plate }}{ }_{44}, \mathrm{~A}^{\text {, plate }}, \mathrm{A}^{\mathrm{A}^{\text {plate }}}{ }_{55}$ | contribution of sandwich face plate to equivalent-plate transverse-shearing stiffnesses (see equation (46d)), lb/in. |
| $\begin{aligned} & \mathbf{A}_{11}^{\text {stiffener }}, \mathbf{A}_{12}^{\text {stifferer }}, \mathbf{A}_{16}^{\text {stiffener }}, \\ & \mathbf{A}_{22}^{\text {stiffener }}, \mathbf{A}_{26}^{\text {stifferer }}, \mathbf{A}_{66}^{\text {stiffener }} \end{aligned}$ | stiffener contribution to equivalent-plate membrane stiffnesses |
|  | (see equation (23a)), lb/in. |
| $\mathbf{A}_{44}^{\text {stiffener }}, \mathbf{A}_{45}^{\text {stiffener }}, \mathbf{A}_{55}^{\text {stiffencr }}$ | stiffener contribution to equivalent-plate transverse-shearing stiffnesses (see equation (23d)), lb/in. |


| b | dimension of hexagon-shaped stiffener pattern (see figures 21 and 25), in. |
| :--- | :--- |
| B | dimension of star-shaped stiffener pattern (see figures 23 and 27), in. |
| $\mathrm{B}_{11}, \mathrm{~B}_{12}, \mathrm{~B}_{16}, \mathrm{~B}_{22}, \mathrm{~B}_{26}, \mathrm{~B}_{66}$ | equivalent-plate coupling stiffnesses (see equation (22a)), lb |
| $\mathbf{B}_{11}^{\text {plate }}, \mathbf{B}_{12}^{\text {plate }}, \mathbf{B}_{16}^{\text {plate }}$, | plate contribution to equivalent-plate coupling stiffnesses |
| $\mathbf{B}_{22}^{\text {plate }}, \mathbf{B}_{26}^{\text {plate }}, \mathbf{B}_{66}^{\text {plate }}$ | (see equations (23b) and (44b)), lb |
| $\mathbf{B}^{\prime \text { plate }}{ }_{11}, \mathbf{B}_{12}^{\prime \text { plate }}, \mathbf{B}_{16}^{\prime \text { plate }}$, $\mathbf{B}^{\prime \text { plate }}, \mathbf{B}^{\prime \text { plate }}, \mathbf{B}^{\prime \text { plate }}{ }_{66}$ | contribution of sandwich face plate to equivalent-plate coupling stiffnesses (see equation (46b)), lb |
|  |  |
| $\mathbf{B}_{11}^{\text {stiffener }}, \mathbf{B}_{12}^{\text {stiffener }}, \mathbf{B}_{16}^{\text {stiffener }}$, $\mathbf{B}_{22}^{\text {stiffener }}, \mathbf{B}_{26}^{\text {stiffener }}, \mathbf{B}_{66}^{\text {stiffener }}$ | stiffener contribution to equivalent-plate coupling stiffnesses |
|  |  |
| c | dimension of hexagonal beam grid (see figure 21), in. |
| [e] | beam-stiffener constitutive matrix defined by equations (A25) and (D1) |
| $\left[\mathcal{C}_{p}\right]$ | transformed beam constitutive matrix defined by equation (36) with elements given in Appendix D |
| $\left[\mathcal{C}_{P}\right]$ | beam constitutive matrix defined by equation (32) |
| $\mathrm{d}_{\mathrm{s}}$ | stiffener spacing (see figures 4 and 5), in. |
| $\mathrm{D}_{11}, \mathrm{D}_{12}, \mathrm{D}_{16}, \mathrm{D}_{22}, \mathrm{D}_{26}, \mathrm{D}_{66}$ | equivalent-plate bending and twisting stiffnesses (see equation (22a)), in.-lb |
| $\mathrm{D}_{11}^{\text {corc }}, \mathrm{D}_{12}^{\text {corc }}, \mathrm{D}_{16}^{\text {corc }}$, $\mathrm{D}_{22}^{\text {core }}, \mathrm{D}_{26}^{\text {core }}, \mathrm{D}_{66}^{\text {core }}$ | contribution of sandwich-plate core equivalent-plate bending stiffnesses (see equation (47c)), in.-lb |
| $\mathbf{D}_{11}^{\text {plate }}, \mathbf{D}_{12}^{\text {plate }}, \mathbf{D}_{16}^{\text {plate }}$, $\mathbf{D}_{22}^{\text {plate }}, \mathbf{D}_{26}^{\text {plate }}, \mathbf{D}_{66}^{\text {plate }}$ | plate contribution to equivalent-plate bending stiffnesses (see equation (23c) and (44c)), in.-lb |
| $\mathbf{D}^{\prime_{11}}{ }^{\text {plate }}, \mathbf{D}^{\prime p_{12}}, \mathbf{D}^{\prime \text { plate }}{ }_{16}^{\prime \text { plate }}$, $\mathbf{D}_{22}^{\prime \text { plate }}, \mathbf{D}_{26}^{\prime \text { plate }}, \mathbf{D}_{66}^{\prime \text { plate }}$ | contribution of sandwich face plate to equivalent-plate bending stiffnesses (see equation (46c)), in.-lb |


| $\mathbf{D}_{11}^{\text {stiffener }}, \mathbf{D}_{12}^{\text {stiffener }}, \mathbf{D}_{16}^{\text {stiffener }}$, | stiffener contribution to equivalent-plate bending stiffnesses |
| :--- | :--- |
| e | sandwich face plate eccentricity (see figure 28), in. |
| $\mathrm{e}_{1}, \mathrm{e}_{2}$ | face plate eccentricities of sandwich plate (see figures 25-27), in. |
| $\mathrm{e}_{\mathrm{xx}}^{\circ}$ | beam membrane strain (see equations (11) and (A3)) |
| E, G | extensional and shear moduli of isotropic materials, psi |
| $\mathrm{E}_{\mathrm{S}}, \mathrm{G}_{\mathrm{S}}$ | effective extensional and shear moduli of nonhomogeneous stiffeners (see equations (A13) and (A15)), psi |
| $\mathrm{E}_{\mathrm{X}}, \mathrm{E}_{\mathrm{Y}}, \mathrm{E}_{\mathrm{Z}}$ | principal extensional moduli for a homogeneous specially orthotropic material (see equation (A10)), psi |
| [E] | strain-equivalence matrix defined by equations (30) |
| $\varepsilon_{\varepsilon}$ | beam-member strain energy (see equation (31)), lb- $\mathrm{in}^{2}$ |
| $\hat{\varepsilon}_{\varepsilon}$ | strain energy density of equivalent plate (see equations (39)), lb |
| $\hat{\boldsymbol{\varepsilon}}_{\varepsilon}^{\text {plate }}$ | contribution of plate wall to strain energy density of equivalent plate (see equations (39)), lb |
| $\mathrm{G}_{\mathrm{XY}}, \mathrm{G}_{\mathrm{YZ}}, \mathrm{G}_{\mathrm{XZ}}$ | principal shear moduli for a homogeneous specially orthotropic material (see equation (A10)), psi |
| $\mathrm{G}_{\mathrm{xy}}^{\mathrm{s}}, \mathrm{G}_{\mathrm{xz}}^{\mathrm{s}}$ | effective shear moduli for a nonhomogeneous beam (see equation (A13)), psi |
| h | plate-wall thickness of stiffened plate (see figures 5, 8-9, and figure 28), in. |
| $\mathrm{h}_{\mathrm{c}}$ | core thicknesses of sandwich plate (see figures 25-27), in. |
| $\mathrm{h}_{\mathrm{s}}$ | thickness of equivalent-stiffener layer (see figure 9), in. |
| $\mathrm{h}_{1}, \mathrm{~h}_{2}$ | face sheet thicknesses of sandwich plate (see figures 25-27), in. |
| H | dimension of star-shaped stiffener pattern (see figures 23 and 27), in. |


| $\mathrm{I}_{\mathrm{Y} \mathrm{Y}}, \mathrm{I}_{\mathrm{ZZ}}, \mathrm{I}_{\mathrm{YZ}}$ | moments and product of inertia of homogeneous beam (see equations (A8)), in ${ }^{4}$ |
| :--- | :--- |
| $\mathrm{I}_{\mathrm{Y} \mathrm{Y}}^{\mathrm{S}}, \mathrm{I}_{\mathrm{ZZ}}^{\mathrm{S}}, \mathrm{I}_{\mathrm{YZ}}^{\mathrm{S}}$ | effective moments and product of inertia of nonhomogeneous stiffeners (see equations (A13)), in ${ }^{4}$ |
| $I_{\eta \eta}^{s}, I_{\zeta \epsilon}^{s}, I_{\eta \epsilon}^{s}$ | effective moments and product of inertia of nonhomogeneous stiffeners with respect to the stiffness-weighted centroid (see equations (A28)), $\mathrm{in}^{4}$ |
| J | torsional constant of homogeneous isotropic beam (see equation (A9)), $\mathrm{in}^{4}$ |
| $\mathrm{J}_{\mathrm{s}}$ | effective torsional constant for nonhomogeneous stiffeners (see equation (A15)), $\mathrm{in}^{4}$ |
| $\mathrm{k}_{\mathrm{Y}}, \mathrm{k}_{\mathrm{z}}$ | inplane and transverse shear correction factors for homogeneous beams, respectively (see equations (A7)) |
| $\mathrm{k}_{\mathrm{r}}^{\mathrm{s}}, \mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | inplane and transverse effective shear correction factors for nonhomogeneous stiffeners (see equation (A24)), respectively |
| $\mathrm{K}^{\text {plate }}$ | transverse-shear correction factor for plates (see equation (44d)) |
| L | hexagon side length shown in figure 21, in. |
| $\mathrm{L}_{\mathrm{s}}$ | generic beam-stiffener length (see equation (31)), in. |
| $\mathrm{L}_{\mathrm{x}}, \mathrm{L}_{\mathrm{y}}$ | beam-grid stiffener spacing (see figures 14-18,21, and 26), in. |
| $\mathrm{M}_{\mathrm{Y}}(\mathrm{X}), \mathrm{M}_{\mathrm{Z}}(\mathrm{X})$ | beam bending moments (see figure 11), in-lb |
| $\mathfrak{M}_{\mathrm{xx}}, \mathfrak{M}_{\mathrm{yy}}, \mathfrak{M}_{\mathrm{xy}}$ | equivalent-plate bending stress resultants in ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) global plate coordinates (see equations (18) and figure 6), in-lb/in. |
| $\mathfrak{M}_{\mathrm{XX}}, \mathfrak{M}_{\mathrm{YY}}, \mathfrak{M}_{\mathrm{XY}}$ | equivalent-plate bending stress resultants in ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) beam coordinates (see figures 6 and 13), in-lb/in. |
| $\mathcal{M}_{\mathrm{xx}}^{\text {plate }}, \mathcal{E}_{\mathrm{yy}}^{\text {plate }}, \mathcal{M}_{\mathrm{xy}}^{\text {plate }}$ | plate-wall bending stress resultants in ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) global plate coordinates (see equations (21)), in-lb/in. |
| $\mathcal{M}_{\mathrm{XX}}^{\text {plate }}, \mathcal{M}_{\mathrm{YY}}^{\text {plate }}, \mathcal{M}_{\mathrm{XY}}^{\text {plate }}$ | plate-wall bending stress resultants (see equations (1)-(9)) in beam (X, Y, Z) coordinates, in-lb/in. |

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-015.jpg?height=2219&width=399&top_left_y=244&top_left_x=240)
equivalent-stiffener-layer bending stress resultants (see equations (1)-(9)), in-lb/in.
equivalent-plate membrane stress resultants in ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) global plate coordinates (see equations (18) and figure 6), lb/in.
equivalent-plate membrane stress resultants in (X, Y, Z) beam coordinates (see figures 6 and 13), lb/in.
plate-wall membrane stress resultants in $(x, y, z)$ global plate coordinates (see equations (21)), lb/in.
plate-wall membrane stress resultants (see equations (1)-(9)) in ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) beam coordinates, lb/in.
equivalent-stiffener-layer membrane stress resultants (see equations (1)-(9)), lb/in.
beam axial force (see figure 11), lb
equivalent-plate transverse shearing stress resultants in ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) global plate coordinates (see equations (18) and figure 6), in-lb
equivalent-plate transverse shearing stress resultants in (X, Y, Z) beam coordinates (see figures 6 and 13), in-lb
plate-wall transverse shearing stress resultants in $(x, y, z)$ global plate coordinates (see equations (21)), lb/in.
plate-wall transverse shearing stress resultants in (X, Y, Z) beam coordinates (see equations (1)-(9)), lb/in.
equivalent-stiffener-layer transverse shearing stress resultants (see equations (1)-(9)), lb/in.
transformed stiffnesses of laminated-plate theory (see equations (44)), psi
core wall thicknesses of sandwich plate (see figures 25-27), in. beam torque (see figure 11), in-lb
strain transformation matrix and its inverse (see equations (17))

| $\left[\mathrm{T}_{\mathrm{o}}\right],\left[\mathrm{T}_{\mathrm{o}}\right]^{-1}$ | stress transformation matrix and its inverse (see equations (16)) |
| :--- | :--- |
| $\left[\mathrm{T}_{\tau}\right],\left[\mathrm{T}_{\tau}\right]^{-1}$ | transverse shearing strain and stress transformation matrix and its inverse (see equations (16) and (17)) |
| $\mathrm{u}(\mathrm{X}), \mathrm{v}(\mathrm{X}), \mathrm{w}(\mathrm{X})$ | beam displacements of points on the reference axis (see equations (A1), in. |
| U(X, Y, Z), V(X, Y, Z), W(X, Y, Z) | displacements of beam material points (see equations (A1)), in. |
| $\mathrm{V}_{\mathrm{Y}}(\mathrm{X}), \mathrm{V}_{\mathrm{Z}}(\mathrm{X})$ | beam transverse shearing forces (see figure 11), lb |
| (x, y, z) | global plate coordinates (see figure 4), in. |
| ( $\mathrm{x}^{\prime}, \mathrm{y}^{\prime}, \mathrm{z}^{\prime}$ ) | local coordinates of sandwich face plate (see figure 28), in. |
| (X, Y, Z) | noncentroidal beam coordinates (see figure 6), in. |
| $\overline{\mathrm{y}}_{\mathrm{s}}, \overline{\overline{\mathrm{y}}}_{\mathrm{s}}$ | stiffness-weighted eccentricities of nonhomogeneous stiffener (see figure 6 and equation (A13)), in. |
| $\overline{\mathrm{Y}}, \overline{\mathrm{Z}}$ | centroidal coordinates of a homogeneous beam with respect to the (X, Y, Z) beam coordinates (see equations (A8) and figure 6), in. |
| $\overline{\mathrm{z}}_{\mathrm{s}}, \overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ | stiffness-weighted eccentricities of nonhomogeneous stiffener (see figure 6 and equation (A13)), in. |
| $\gamma_{x z}^{\circ}, \gamma_{y z}^{\circ}$ | plate transverse shearing strains with respect to ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) coordinates (see equations (19) and figure 6) |
| $\gamma_{\mathrm{xz}}^{\circ}, \gamma_{\mathrm{yz}}^{\circ}$ | plate transverse shearing strains with respect to (X, Y, Z) coordinates (see equations (10) and figure 6) |
| $\boldsymbol{\Gamma}_{\mathrm{xy}}^{\circ}, \boldsymbol{\Gamma}_{\mathrm{xz}}^{\circ}$ | beam transverse shearing strains (see equations (11) and (A3)) |
| $\varepsilon_{x x}, \varepsilon_{y y}, \gamma_{x y}, \gamma_{x z}, \gamma_{y z}, \varepsilon_{z z}$ | plate strains with respect to $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates (see equations (17) and figure 6) |
| $\varepsilon_{\mathrm{XX}}, \varepsilon_{\mathrm{YY}}, \gamma_{\mathrm{XY}}, \gamma_{\mathrm{XZ}}, \gamma_{\mathrm{YZ}}, \varepsilon_{\mathrm{ZZ}}$ | plate and beam strains with respect to ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates (see equations (10) and figure 6) |
| $\varepsilon_{x x}^{o}, \varepsilon_{y y}^{o}, \gamma_{x y}^{o}$ | plate membrane strains with respect to $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates (see equations (19) and figure 6) |


| $\boldsymbol{\varepsilon}_{\mathrm{XX}}^{\mathrm{o}}, \boldsymbol{\varepsilon}_{\mathrm{YY}}^{\mathrm{o}}, \gamma_{\mathrm{XY}}^{\mathrm{o}}$ | plate membrane strains with respect to $(\mathrm{X}, \mathrm{Y}, \mathrm{Z})$ coordinates (see equations (10) and figure 6) |
| :--- | :--- |
| $\left\{\varepsilon_{b}\right\}$ | vector of beam strains (see equations (30)) |
| $\left\{\varepsilon_{p}\right\}$ | vector of plate strains referred to ( $\mathrm{x}, \mathrm{y}, \mathrm{z}$ ) global plate coordinates (see equations (34)) |
| $\left\{\varepsilon_{P}\right\}$ | vector of plate strains referred to (X, Y, Z) beam coordinates (see equations (30)) |
| $\bar{\xi}_{\mathrm{s}}, \overline{\bar{\xi}}_{\mathrm{s}}$ | eccentricities of nonhomogeneous stiffener (see equations (A27) and (A29)), in. |
| $\bar{\eta}_{\mathrm{s}}, \overline{\bar{\eta}}_{\mathrm{s}}$ | eccentricities of nonhomogeneous stiffener (see equations (A27) and (A29)), in. |
| $\kappa_{\mathrm{xx}}^{\circ}, \kappa_{\mathrm{yy}}^{\circ}, \kappa_{\mathrm{xy}}^{\circ}$ | plate bending strains with respect to $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates (see equations (19) and figure 6), $\mathrm{in}^{-1}$ |
| $\kappa_{X X}^{o}, \kappa_{Y Y}^{o}, \kappa_{X Y}^{o}$ | plate bending strains with respect to ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates (see equations (10)), $\mathrm{in}^{-1}$ |
| $\sigma_{x x}, \sigma_{x y}, \sigma_{x z}, \sigma_{y y}, \sigma_{y z}, \sigma_{z z}$ | beam and plate stresses with respect to $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates (see figure 6), psi |
| $\sigma_{X X}, \sigma_{X Y}, \sigma_{X Z}, \sigma_{Y Y}, \sigma_{Y Z}, \sigma_{Z Z}$ | beam and plate stresses with respect to ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates (see figure 10), psi |
| $\boldsymbol{\tau}^{\circ}$ | beam twisting strain (see equations (A2) and (11)), $\mathrm{in}^{-1}$ |
| $\boldsymbol{\tau}_{\mathrm{r}}^{\mathrm{s}}, \boldsymbol{\tau}_{\mathrm{z}}^{\mathrm{s}}$ | inplane and transverse shear parameters (see equations (29)) |
| $v_{\mathrm{XY}}, v_{\mathrm{XZ}}, v_{\mathrm{YZ}}$ | major principal Poisson's ratios for a homogeneous specially orthotropic material (see equation (A10)) |
| $v_{\mathrm{YX}}, v_{\mathrm{ZX}}, v_{\mathrm{ZY}}$ | minor principal Poisson's ratios for a homogeneous specially orthotropic material (see equation (A10)) |
| $(\xi, \eta, \zeta)$ | stiffness-weighted centroidal coordinates of nonhomogeneous beams and centroidal coordinates of homogeneous beams (see equations (A27) and figures 6 and 11), in. |
| $\varphi_{\mathrm{X}}(\mathrm{X}), \varphi_{\mathrm{Y}}(\mathrm{X}), \varphi_{\mathrm{Z}}(\mathrm{X})$ | dextral rotations of the beam cross-section about the $\mathrm{X}-, \mathrm{Y}-$, and Z-axes, respectively (see equations (A1)) |


| $\Phi$ | angle of diagonal stiffeners (see figures 14, 16-18, 21 and 23), <br> degrees |
| :--- | :--- |
| $\chi_{\mathrm{Y}}^{\circ}, \chi_{\mathrm{Z}}^{\circ}$ | beam bending strains (see equations (11) and (A2)), $\mathrm{in}^{-1}$ |
| $\Psi_{\mathrm{S}}$ | stiffener angle (see figures 4, 6, and 11), degrees |

## Introduction

Stiffened plates and shells are common structural forms used in the aerospace industry. For example, the Space Shuttle liquid-hydrogen tank utilizes a metallic "orthogrid" construction, as shown in figure 1. This type of structural arrangement has two families of uniformly spaced stiffeners that intersect at right angles. Stiffened metallic shells with this type of construction are often referred to as geometrically orthotropic because their overall equivalent extensional and bending stiffnesses are similar to that of a corresponding homogeneous orthotropic material when the stiffnesses of the shell skin and stiffeners are homogenized. A similar densely stiffened metallic orthogrid cylinder is shown in figure 2. Another common structural arrangement that is used for launch vehicles, known as an "isogrid," is shown in figure 3. This type of structural arrangement has three identical families of uniformly spaced stiffeners that intersect one another at a 60-degree angle to yield a geometrically isotropic shell wall. For this type of metallic stiffened shell, the homogenized extensional and bending stiffnesses are like that of an isotropic material.

Approximating the overall behavior of stiffened plate and shell structures by using homogenized, "equivalent" stiffnesses and "effective" thicknesses has been in use for many years (e.g., see references 1-8). In recent times, these plate and shell stiffness representations still see utility in early stages of building-block analysis and design approaches that have evolved and are used extensively by industry. These simplified approaches are particularly useful for navigating the design space rapidly to identify the "first cut" of optimal preliminary designs, which are particularly important to the design of lightweight, high-performance launch vehicles such as the ARES V, previously under development by NASA.

The earliest works that utilize equivalent stiffnesses to analyze the behavior of stiffened plates appear to be that of Huber. ${ }^{1-3}$ Originally, this approach was driven by a lack of analysis methods that could simulate adequately the discrete nature of stiffened structures and the availability of analytical solutions for bending and buckling of homogeneous orthotropic plates. Similarly, the earliest corresponding works for stiffened shells appears to be that published by Flugge ${ }^{4}$ in 1932 and 15 years later by van der Neut. ${ }^{9}$ As time passed and physical understanding matured, theories for analyzing stiffened structures by using equivalent stiffnesses and thickness continued to receive attention. For example, Dale and Smith ${ }^{7}$ used equivalent stiffnesses to study the buckling behavior of compression-loaded sandwich plates with an orthogrid core. In 1946, Smith et. al. ${ }^{8}$ presented an improved formulation that accounts for variations in the neutral-surface position associated with local interactions between a plywood plate and a stiffener. Similarly, in 1947,

Pfluger ${ }^{10}$ presented an improved theory and applied it to the buckling of stiffened plates. Pfluger's work is considered an improvement to Huber's much earlier work because it includes a more accurate treatment of the shearing stresses. One of the earliest works that uses an effective plate thickness for designing stiffened plates was given in 1948 by Gomza \& Seide. ${ }^{11}$ In their study, the effective plate thickness is obtained by adding the stiffener cross-sectional area, divided by the stiffener spacing, to the plate thickness. An early work that developed equivalent-plate stiffnesses for an isotropic corrugated sheet sandwiched between two isotropic flat skins was presented by Libove and Hubka ${ }^{12}$ in 1951. Basically, formulas for equivalent-plate elastic constants were presented, for use with available symmetric-sandwich plate theories ${ }^{13-15}$ that include inplane dilatation and shearing, pure bending and twisting, and transverse shearing. Formulas for equivalent-plate elastic constants associated with coupling between inplane dilatation and pure bending and between inplane shearing and twisting were also presented in anticipation of the extension of sandwich plate theories to unsymmetric sandwich constructions. Experimental results were reported that were characterized as being in "close agreement" with the theoretical predictions for the bending and transverse-shear stiffnesses in the direction perpendicular to the corrugations and for the twisting stiffness. Later, in 1952, Benscoter and $\mathrm{MacNeal}^{16}$ presented an equivalent-plate theory, based on first-order difference equations, for a thin multicell low aspect ratio, supersonic wing with straight spars and perpendicular ribs that includes transverse-shear deformations. Similarly, Horvay ${ }^{17}$ presented an equivalent-plate formulation for a plate-like grid with a stiffener arrangement forming honeycomb cells in 1952.

What may be the earliest work to provide expressions for equivalent-plate stiffnesses of isotropic plates with integral stiffeners was presented by Dow, Libove, and Hubka. ${ }^{18}$ In this early work, 12 independent elastic constants were derived, following a laborious approach, that correspond to the $\mathrm{A}_{11}, \mathrm{~A}_{12}, \mathrm{~A}_{22}, \mathrm{~A}_{66}, \mathrm{~B}_{11}, \mathrm{~B}_{12}, \mathrm{~B}_{22}, \mathrm{~B}_{66}, \mathrm{D}_{11}, \mathrm{D}_{12}, \mathrm{D}_{22}$, and $\mathrm{D}_{66}$ terms appearing in the contemporary constitutive equations for laminated-composite plates (see reference 19) that relate stress resultants to membrane strains and bending curvatures. The expressions given for the elastic constants were obtained by identifying the fundamental repeating element of the stiffened plate and then replacing each stiffener in the repeating element with a homogeneous orthotropic plate that is perfectly bonded to the skin of the stiffened plate. The strains in the repeating-element stiffeners are related to the corresponding plate strains and the strain energy of the repeating element is determined in terms of the equivalent-plate strains. Equations relating the equivalentplate strains and the equivalent-plate stress resultants are obtained by differentiating the strain energy, which yield the equivalent-plate stiffnesses. Several expressions for an average or equivalent-plate thickness were also given that depend on the stiffener arrangement. A somewhat related study that focused on the torsional stiffness of orthogonally stiffened plates was presented by Crawford and Libove. ${ }^{20}$ Around the same time period, Hoppmann and his colleagues ${ }^{21-24}$ conducted experiments to determine the bending and twisting stiffnesses of orthogonally stiffened plates, and used these stiffnesses to perform calculations for static bending and vibration, based on an orthotropic-plate theory. In 1956, Huffington ${ }^{25}$ published an analysis for determining the equivalent-plate stiffnesses for orthogonally stiffened plates without stiffener eccentricity, with respect to the plate skin. Later, in 1957, Bodner ${ }^{26}$ analyzed buckling of ring-stiffened cylinders subjected to hydrostatic pressure by using an equivalent shell-wall thickness and an effective moment of inertia for the rings and shell wall combination. In his analysis, the rings were presumed to contribute only to the circumferential membrane and bending stiffnesses, and
buckling loads were obtained by treating the stiffened shell as an equivalent orthotropic shell that is nonhomogeneous in the radial direction. An effective length between rings was used in the calculation of the bending stiffness such that the maximum circumferential stress can be computed by using basic ring theory. The direction of ring eccentricity, with respect to the shell wall, is not included in the analysis.

During the last fifty years, the equivalent-plate or shell approach was still being used as a firstapproximation method to understand the behavior of eccentrically stiffened and sandwich plates and shells, and in simulating the behavior of massive beam-like, plate-like, and shell-like reticulated orbiting space structures whose discrete-member analysis was beyond the capability of the computing resources available at that time. ${ }^{27-138}$ For example, Stroud ${ }^{30}$ presented a derivation of five elastic constants associated with pure bending and twisting of corrugation-stiffened panels in 1963. These constants were obtained by examining the force-deformation characteristics of a repeating corrugation-plate-skin cell. Results of experiments conducted to determine the elastic constants showed favorable agreement with the proposed theory. In 1964, Meyer \& Bellefante ${ }^{31}$ presented equivalent-plate elastic constants for inplane dilatation and shearing and pure bending of a skin stiffened by an array of stiffeners that enclose equilateral triangles. These constants were also obtained by examining the force-deformation characteristics of a repeating cell. Equivalentshell stiffnesses were presented by Sewall, Clary, and Leadbetter ${ }^{32}$ in 1964 for cylinders with an orthogonal arrangement of rings and stringers sandwiched between inner and outer skins. In this work, the rings are presumed to make a negligible contribution to the longitudinal inplane and bending stiffnesses, the stiffness associated with coupling between longitudinal-circumferential dilatation and coupling between longitudinal-circumferential bending, the inplane shearing stiffness, and the twisting stiffness. Similarly, the stringers are presumed to make a negligible contribution to the circumferential inplane and bending stiffnesses. In contrast, the stringers are presumed to contribute to the coupling between longitudinal-circumferential dilatation, the coupling between longitudinal-circumferential bending, the inplane shearing stiffness, and the twisting stiffness. Block, Card, Mikulas, McElman, and Stein ${ }^{37,38,40,41}$ presented and applied equivalent-shell stiffnesses for orthotropic ring-stiffened corrugated cylinders and ring-and-stringer-stiffened cylinders in 1965 and 1966. In this series of papers, a relatively simple strainenergy approach was used to determine stiffnesses that include inplane dilatation and shearing, pure bending and twisting, and coupling between inplane dilatation and pure bending and between inplane shearing and twisting associated with stiffener eccentricity with respect to shell wall midsurface. Transverse shearing stiffnesses were not considered. Also in 1966, Singer et.al. ${ }^{42}$ published stiffener expressions similar to those given by Block, Card, Mikulas, McElman, and Stein for cylinders with eccentric orthogonal rings and stringers. Their stiffness expressions are based on the presumption that the normal strains vary linearly in the skin and stiffeners and are equal at the point of contact between the skin and a stiffener. In addition, the stiffeners do not contribute to the inplane shearing stiffness, and the torsional stiffness is obtained by adding the torsional stiffness of the stiffeners to that of the skin. In 1968, Jones ${ }^{49,51}$ presented stiffness expressions similar to those given in references 36-39, but for laminated-composite cylinders. This work appears to be the first to express the equivalent-shell stiffnesses in the terminology that has become standard practice for laminated composites in a large portion of the world. In 1969, Soong ${ }^{52-54}$ presented a derivation of the stiffness expressions similar to those given in references 37, 38, 40, and 41, based on a strain-energy approach, but for orthotropic cylinders reinforced with a balanced pair of spiral stiffeners that make an arbitrary angle with the cylinder generators.

Attempts were made in the 1970s to refine the equivalent-plate stiffnesses for isotropic plates and shells with eccentric orthogonal stiffeners. For example, Cusens et.al. ${ }^{58}$ presented an analysis that accounts for the stiffener contributions to the stiffnesses associated with coupling between inplane stretching and between anticlastic bending. In their analysis, the coupling effects are weighted by the size of the area of contact at the stiffener intersections. Similarly, Nishino et.al. ${ }^{63}$ modeled the interaction of the shearing stresses between a plate and an eccentrically located orthogonal stiffening grid and obtained equivalent-plate twisting stiffnesses that include the effects of inplane shearing deformations of the stiffeners. Likewise, Nemeth ${ }^{81}$ derived equivalentplate stiffnesses for single-layer grids made of beam members with inplane and out-of-plane (transverse) shear flexibility in 1979. Stiffness expressions were presented in this study for several grid configurations and in-depth comparisons with corresponding results obtained from discrete finite element models of the grids are given. In 1979 and 1980, $\mathrm{Ko}^{82-84}$ presented equivalent stiffnesses for an isotropic corrugated sheet sandwiched between two isotropic flat skins in a symmetric manner, and for a similar symmetric honeycomb-core sandwich plate. These stiffnesses are modified forms of the corresponding stiffnesses presented by Libove and Hubka ${ }^{12}$ in 1951, that account for corrugated walls with nonuniform thickness, and include the effects of transverse-shear deformations. This approach was extended by Ko to hat-stiffened panels in 1991. ${ }^{108}$ Later, in 1985, Reddy et.al. ${ }^{95}$ presented equivalent stiffnesses for a circular cylindrical shell stiffened by an internal grid. In particular, symmetrically laminated shell walls stiffened with rings, stringers, and a pair of identical helical stiffeners making an arbitrary angle with the shell generators were considered. Expressions are given that include transverse-shear stiffnesses in addition to stiffnesses that account for inplane dilatation and shearing, pure bending and twisting, and coupling between inplane dilatation and pure bending and between inplane shearing and twisting associated with stiffener eccentricity with respect to shell wall mid-surface. Also in 1985, Kolpakov ${ }^{97}$ presented a method for determining the equivalent stiffnesses of elastic frameworks that includes an analysis of a planar beam gridwork with an overall negative-valued Poisson's ratio. Deb and Booton ${ }^{102}$ presented similar equivalent-plate stiffnesses in 1988 for shear deformable, orthogonally stiffened isotropic plates with eccentric stiffeners. Also, in 1988, Boot \& Moore ${ }^{103}$ presented a detailed list of the factors affecting the validity of equivalent-plate stiffnesses, and examined the importance of neglecting the contribution of the stiffeners to the coupling between biaxial stretching, for orthotropic plates. In 1989, Bunakov and Protasov ${ }^{105}$ presented equivalent-continuum stiffnesses for a pair of identical helical stiffeners with a rectangular-cross-section attached to a shell. These stiffnesses are based on a micropolar continuum model and include transverse-shear and bending stiffnesses of the beam members that are associated with deformations within the tangent plane at each point of the shell. In 1990, Won ${ }^{106}$ presented equivalent-plate stiffnesses for isotropic plates reinforced with eccentric, regularly spaced pairs of oblique stiffeners. In his analysis, a uniform biaxial stress state is presumed to exist at the stiffener joints and is used to obtain a stiffener contribution to equivalentplate stiffness associated with "Poisson coupling" between biaxial deformations. In addition, axial stresses in the stiffeners are presumed to develop that resist plate-like inplane shearing and twisting deformations, which leads to additional equivalent-plate stiffness contributions. Three coupled partial differential equations that govern the bending response are derived, in terms of the inplane and out-of-plane displacements, by minimizing the potential energy of the plate-stiffener system. An approximate "Huber-type" differential equation (see references 1-3) is also given, in terms of the out-of-plane displacement, for an orthotropic plate. This simplified equation, given
in terms of the out-of-plane displacement, represents bending about an "equivalent," inextensible neutral surface. The Huber-type equation is obtained by solving the equivalent-plate constitutive equations for the inplane stress resultants in terms of the membrane strains, and then substituting the resulting expressions into the equivalent-plate constitutive equations for the bending stress resultants. This step yields the bending stress resultants in terms of the out-of-plane displacement and second-order derivatives of the inplane stress resultants. The approximate "Huber-type" differential equation is obtained by substituting the equivalent-plate bending stress resultants into the remaining out-of-plane equilibrium equation and then neglecting the second-order derivatives of the inplane stress resultants.

In 1993, Pshenichnov ${ }^{112}$ published a monograph dealing with reticulated plates and shells, with an emphasis on single-layer plate-like and shell-like lattice structures in which the stiffeners are not eccentric with respect to the shell middle surface. The equivalent stiffnesses presented are based on a classical shell theory (no transverse shear flexibility) and are obtained by using tensor transformations to equate beam strains with corresponding shell strains and by equating shell stress resultants with transformed beam forces that are uniformly distributed across an equivalent shell wall. Although the analysis is based on a classical shell theory, an attempt is made to include the effects of stiffener bending in the tangent plane by expressing the beam shearing forces that act in the tangent plane in terms of the derivatives of the corresponding beam moments. These tangential beam moments are expressed in terms of the beam bending strain, in the usual way, but the beam bending strain is obtained in terms of the shell tangential displacements and strains by considering deformation associated with rotation about the unit vector normal to the middle surface. Although this approach captures tangential stiffener bending effects, the effects cannot be represented directly in terms of the shell strains and, as a result, do not enter into the equivalent stiffness expressions for plate-like and shell-like lattices.

In 1995, Jaunky et. al. ${ }^{116,117}$ presented a refined smeared-stiffener theory for grid-stiffened laminated-composite panels, based upon the earlier work presented by Smith et.al. ${ }^{8}$ for a plywood plate with a single central stiffener that has a rectangular cross-section. The refinement presented in their work accounts for the variation of the neutral surface caused by interactions between the skin and the stiffeners. Results presented by these authors show more accurate equivalent-plate stiffness predictions for selected cases, but the analysis used to obtain the equivalent-plate stiffnesses is far more involved than the earlier, less refined approach used in earlier works such as references 37, 38, 40, and 41. Equivalent-shell stiffnesses for circular cylinders made of laminated-composite materials and with rings, stringers, and a pairs of identical geodesic stiffeners were presented by Gerhard et.al. ${ }^{118}$ in 1996 (see pp. 56-75). These equivalent-shell stiffnesses were obtained by using strain transformation equations to express the stiffener strains in terms of the equivalent-plate strains, and by using force transformation equations to relate the force in each stiffener to the equivalent-shell stress resultants. Equivalent stiffnesses for laminated-composite flat plates and circular cylindrical shells stiffened by a grid of beams were presented by Chen and Tsai ${ }^{119}$ in 1996. In their study, generally laminated walls stiffened with ribs, stringers, and a pair of identical diagonal stiffeners with an arbitrary orientation angle were considered. Grid-stiffness expressions are given that include out-of-plane (transverse) and inplane shear flexibility of the stiffeners and inplane stiffener bending in addition to the usual stiffnesses that account for inplane dilatation and shearing and pure bending and twisting. Similarly, Wodesenbet et. al. ${ }^{133}$ presented an improved smeared-stiffener theory for isogrid-
stiffened laminated-composite cylinders in 2003. In this theory, the stiffness contributions of the stiffeners are obtained by relating the beam strains to the plate strains with the standard straintransformation equations, and by expressing the shell stress resultants in terms of the beam forces, and their moments, that act on each stiffener component within a unit cell (repeating element). The equivalent-shell stiffnesses are then obtained by using a superposition of the stress resultant for the skin and the stress resultants for the stiffeners within the unit cell that is weighted by the corresponding volume fractions for the unit cell.

The literature examined during the present study suggests that treating stiffened plates as an equivalent-continuum plate remains a useful design practice, provided the limitations of the theory are kept in mind. The surveyed results also indicate that, to a large extent, the derivations of equivalent-continuum plate stiffnesses have been ad hoc, the terminology is antiquated, and transverse-shear deformations are often neglected. Moreover, the criteria for defining an effective thickness of the equivalent-continuum plate appears to be unclear. The major objective of the present study is to present two systematic methods for deriving first-approximation, equivalentcontinuum stiffnesses for eccentrically stiffened plates, based on a first-order transverse-shear deformation plate theory (e. g., see reference 139). The first method uses equilibrium and compatibility in a direct manner for plates reinforced by one or more families of rectilinear stiffeners. The second method is closely related and is based on using a basic, repetitive cell of the stiffened plate and then defining an equivalence between the strain energy of the basic cell and the corresponding equivalent plate. This method is particularly useful for stiffener arrangements that are not rectilinear. A second objective is to present a systematic set of equations that can be used to determine the equivalent thickness of stiffened plates. Toward these objectives, the analysis approach and details for the direct equilibrium-compatibility method are presented first for plates stiffened by one or more families of continuous rectilinear stiffeners. This first section includes discussions of how statical and kinematical equivalence is achieved between the stiffened plate and the equivalent-continuum plate, and equivalent-plate stiffnesses are given for several stiffening arrangements. Comparisons of the equivalent-plate stiffnesses with corresponding previously published results are also given. Next, the details of the energyequivalence approach are presented, and the method is applied to obtain equivalent-plate stiffnesses for several stiffening arrangements. Additional comparisons of the equivalent-plate stiffnesses with corresponding previously published results and with the stiffnesses obtained herein by using the direct equilibrium-compatibility method are also given. Then, additional analysis is presented that shows how to obtain equivalent-plate stiffnesses for sandwich plates with two nonidentical, generally laminated face plates and a core made from several arrangements of beam stiffeners. Equations are also presented that show several different criteria that can be used to select an equivalent thickness of the equivalent-continuum plate, which may be needed to perform collateral design calculations.

## Direct Equilibrium-Compatibility Method for Rectilinear Stiffener Families

Consider a perfectly flat plate of arbitrary shape, as depicted in figure 4a. Material points of the plate are located by the Cartesian coordinates $(x, y, z)$, and $z=0$ corresponds to the plate midplane. The plate is stiffened by a unidirectional family of identical prismatic beams that generally have nonhomogeneous cross-sections and that are equally spaced, as depicted in figure

4b. An example of the plate cross-section A -A indicated in figure 4 b is shown in figure 5. In this figure, the stiffener spacing is denoted by $\mathrm{d}_{\mathrm{s}}$ and the effective nonhomogeneous-stiffener eccentricity, defined in Appendix A, is given by $\overline{\mathrm{z}}_{s}$. The stiffeners are also presumed to be perfectly bonded to a laminated-composite skin with thickness h , and make an angle $\Psi_{\mathrm{s}}$ with the x -axis of the plate. Material points of the beam are located by the local, noncentroidal Cartesian coordinates ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ), and $\mathrm{Z}=0$ also corresponds to the plate midplane. The geometric relationship between the plate and local beam coordinates is shown in figure 6. As indicated in Appendix A, the coordinates of the centroidal axis are given by $(\mathrm{X}, \overline{\mathrm{Y}}, \overline{\mathrm{Z}})$, with respect to the (X, Y, Z) coordinate frame. Similarly, the coordinates of the stiffness-weighted centroidal axis of nonhomogeneous beams are given by $\left(\mathrm{X}, \overline{\mathrm{y}}_{\mathrm{S}}, \overline{\mathrm{z}}_{\mathrm{S}}\right)$, with respect to the $(\mathrm{X}, \mathrm{Y}, \mathrm{Z})$ coordinate frame. The additional $(\xi, \eta, \zeta)$ coordinate axes shown in figure 6 are used to locate points of the beam with respect to the stiffness-weighted centroid.

The stiffeners are modeled in the present study with the Timoshenko-type first-order sheardeformation beam theory presented in Appendix A, based on the local noncentroidal Cartesian coordinates ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ). In addition, the beam material is presumed to be specially orthotropic with respect to the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinate frame, but may be nonhomogeneous in the cross-sectional planes. In particular, the principal axes of orthotropy are aligned with the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinate axes. Moreover, the effects of cross-sectional warping restraint associated with torsion of noncircular cross-sections are neglected in the kinematic equations and each cross section is presumed to warp in an identical manner. Beam constitutive equations are also presented in Appendix A for the nonhomogeneous specially orthotropic material in terms of effective engineering constants. Using a nonhomogeneous beam theory permits the modeling of tailored beam stiffeners such as those depicted in figure 7. Based on Appendix A, the nonhomogeneous beam stiffener is assigned an effective axial modulus $\mathrm{E}_{\mathrm{s}}$, an effective shear modulus $\mathrm{G}_{\mathrm{s}}$, crosssectional area $A_{s}$, effective moments of inertia $I_{Y Y}^{s}$ and $I_{Z Z}^{s}$, effective product of inertia $I_{Y Z}^{s}$, and effective torsional constant $\mathrm{J}_{\mathrm{S}}$, in addition to the effective eccentricities $\overline{\mathrm{y}}_{\mathrm{S}}, \overline{\mathrm{z}}_{\mathrm{S}}, \overline{\bar{y}}_{\mathrm{S}}$ and $\overline{\bar{z}}_{\mathrm{S}}$. Effective shear correction factors for the beam are denoted by $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ and $\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}}$.

For the structural arrangement depicted by figures 4-6, the repetitive element shown in figure 8 is used herein to represent the essential features of the structure. The stiffener in this repetitive element is positioned so that the effective eccentricity $\bar{y}_{s}=0$. Although a T-shaped stiffener is shown in figure 8, the stiffener may have a nonhomogeneous cross-section with an arbitrary shape. In the analysis that follows, the repetitive stiffened-plate element is modeled as the equivalent-plate element shown in figure 9, which consists of a laminated-composite wall bonded perfectly to a single, equivalent-stiffener layer. The reference surface of the equivalent plate is selected as the midplane of the plate wall, for convenience. The equivalent-stiffener layer is presumed to contribute axial stretching and bending stiffness, inplane shear stiffness, and twisting stiffness in the Y-Z plane, consistent with the classical continuum model of deformation. The approach that is followed in this section is to first establish an equivalence between the internal forces acting on the repetitive stiffened-panel element and the equivalent-plate element. This equivalence is referred to herein as statical equivalence and is based on the presumption that the
variation of stresses across the width of the equivalent-stiffener layer can be neglected for relatively small stiffener spacings. The beam stresses and corresponding resultant forces and moments, defined relative to the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates, that are considered are shown in figures 10 and 11, respectively. Similarly, the beam forces and moments acting on the repetitive stiffened-plate element and the corresponding distributed stress resultants acting on the equivalent-plate element are shown in figures 12 and 13, respectively. Then, an equivalence between the stiffener strains and the corresponding strains in the equivalent-stiffener layer is established, which is referred to herein as kinematical equivalence. The kinematical equivalence is based on the presumption that the strain at any point of a stiffener is identical to the corresponding strain at the corresponding point in the equivalent-stiffener layer of the equivalentplate element. In addition, it is presumed that the variation of strains across the width of the equivalent-stiffener layer can be neglected for relatively small stiffener spacings. With these equivalences established, the stiffener-force contributions to the equivalent-plate stress resultants are expressed in terms of the equivalent-plate strains, and the corresponding equivalent-plate constitutive equations are determined in terms of the plate wall and stiffener properties.

## Statical Equivalence

To establish statical equivalence between the repetitive stiffened-panel and equivalent-plate elements, consider the definition of axial stress resultant for the equivalent plate in the X-Y-Z coordinate system associated with the stiffener, given by

$$
\begin{equation*}
U_{x x}=\int_{-\frac{h}{2}}^{\frac{h}{2}+h_{s}} \sigma_{x x} d Z \tag{1}
\end{equation*}
$$

where $\sigma_{x x}$ is the axial stress, $h$ is the plate thickness, and $h_{s}$ is the thickness of the equivalentstiffener layer shown in figure 9. The integration is partitioned to obtain

$$
\begin{equation*}
U_{\mathrm{xX}}=\int_{-\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}} \sigma_{\mathrm{xX}} \mathrm{dZ}+\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{xX}} \mathrm{dZ} \equiv U_{\mathrm{xX}}^{\text {plate }}+U_{\mathrm{xX}}^{\text {stiffener }} \tag{2}
\end{equation*}
$$

where

$$
\begin{equation*}
\sum_{\mathrm{xx}}^{\text {stiffener }}=\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{xx}} \mathrm{dZ} \tag{3}
\end{equation*}
$$

Here, $\boldsymbol{U}_{\mathrm{xx}}^{\text {plate }}$ refers to the usual definition of the stress resultant for a plate that is given by the first integral in equation (2). Using the definition for the axial beam load, $\mathrm{P}(\mathrm{x})$, defined by equation (A5a) in Appendix A and applying it to the equivalent-stiffener layer of the equivalent-plate element, with the presumption that the variation of $\sigma_{\mathrm{xx}}$ across the width of the equivalentstiffener layer is negligible, gives

$$
\begin{equation*}
\mathrm{P}=\iint_{\mathrm{A}_{\mathrm{S}}} \sigma_{\mathrm{XX}} \mathrm{dYdZ}=\mathrm{d}_{\mathrm{S}} \int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{S}}} \sigma_{\mathrm{XX}} \mathrm{dZ} \tag{4}
\end{equation*}
$$

Using equations (3) and (4) gives

$$
\begin{equation*}
\mathcal{U}_{\mathrm{xx}}^{\text {stiffener }}=\frac{\mathrm{P}}{\mathrm{~d}_{\mathrm{s}}} \tag{5}
\end{equation*}
$$

and equation (2) gives

$$
\begin{equation*}
\boldsymbol{U}_{\mathrm{xx}}=\boldsymbol{U}_{\mathrm{xx}}^{\text {plate }}+\frac{\mathrm{P}}{\mathrm{~d}_{\mathrm{s}}} \tag{6}
\end{equation*}
$$

where $d_{s}$ is the stiffener spacing (see figure 5). Following a similar process of partitioning the integrations and relating the two stiffener coordinate systems, the remaining stress resultants acting on the edge shown in figure 13 are expressed as

$$
\begin{align*}
& \mathcal{U}_{\mathrm{XY}}=\int_{-\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}} \sigma_{\mathrm{XY}} \mathrm{dZ}+\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{XY}} \mathrm{dZ} \equiv \mathcal{U}_{\mathrm{XY}}^{\text {plate }}+\mathcal{U}_{\mathrm{XY}}^{\text {stiffener }}  \tag{7a}\\
& \mathcal{M}_{\mathrm{XX}}=\int_{-\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}} \sigma_{\mathrm{XX}} \mathrm{ZdZ}+\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{XX}} \mathrm{ZdZ} \equiv M_{\mathrm{XX}}^{\text {plate }}+M_{\mathrm{XX}}^{\text {stiffener }}  \tag{7b}\\
& M_{\mathrm{XY}}=\int_{-\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}} \sigma_{\mathrm{XY}} \mathrm{ZdZ}+\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{XY}} \mathrm{ZdZ} \equiv M_{\mathrm{XY}}^{\text {plate }}+M_{\mathrm{XY}}^{\text {stiffener }}  \tag{7c}\\
& \mathrm{Q}_{\mathrm{XZ}}=\int_{-\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}} \sigma_{\mathrm{XZ}} \mathrm{dZ}+\int_{\frac{\mathrm{h}}{2}}^{\frac{\mathrm{h}}{2}+\mathrm{h}_{\mathrm{s}}} \sigma_{\mathrm{XZ}} \mathrm{dZ} \equiv \mathrm{Q}_{\mathrm{XZ}}^{\text {plate }}+\mathrm{Q}_{\mathrm{XZ}}^{\text {stiffener }} \tag{7~d}
\end{align*}
$$

Likewise, applying the definitions of the beam forces $\mathrm{V}_{\mathrm{Y}}(\mathrm{X})$ and $\mathrm{V}_{\mathrm{Z}}(\mathrm{X})$ and beam moments $\mathrm{M}_{\mathrm{Y}}(\mathrm{X})$ and $\mathrm{T}(\mathrm{X})$ defined in Appendix A (see figure 11) to the equivalent-stiffener layer of the equivalentplate element and neglecting the variation of the stresses across the width of the equivalentstiffener layer gives

$$
\begin{equation*}
\mathcal{U}_{\mathrm{XY}}^{\text {stiffener }}=\frac{\mathrm{V}_{\mathrm{Y}}}{\mathrm{~d}_{\mathrm{S}}} \tag{8a}
\end{equation*}
$$

Similarly,

$$
\begin{align*}
& M_{\mathrm{XX}}^{\text {stiffener }}=\frac{\mathrm{M}_{\mathrm{Y}}}{\mathrm{~d}_{\mathrm{s}}}  \tag{8b}\\
& M_{\mathrm{XY}}^{\text {stiffener }}=-\frac{\mathrm{T}}{\mathrm{~d}_{\mathrm{s}}} \tag{8c}
\end{align*}
$$

$$
\begin{equation*}
\mathrm{Q}_{\mathrm{xz}}^{\text {stiffener }}=\frac{\mathrm{V}_{\mathrm{z}}}{\mathrm{~d}_{\mathrm{s}}} \tag{8d}
\end{equation*}
$$

With these results, equations (7a) - (7d) yield

$$
\begin{align*}
& M_{\mathrm{XY}}=M_{\mathrm{XY}}^{\text {plate }}+\frac{\mathrm{V}_{\mathrm{Y}}}{\mathrm{~d}_{\mathrm{s}}}  \tag{9a}\\
& M_{\mathrm{XX}}=M_{\mathrm{XX}}^{\text {plate }}+\frac{\mathrm{M}_{\mathrm{Y}}}{\mathrm{~d}_{\mathrm{s}}}  \tag{9b}\\
& M_{\mathrm{XY}}=M_{\mathrm{XY}}^{\text {plate }}-\frac{\mathrm{T}}{\mathrm{~d}_{\mathrm{s}}}  \tag{9c}\\
& \mathrm{Q}_{\mathrm{XZ}}=\mathrm{Q}_{\mathrm{XZ}}^{\text {plate }}+\frac{\mathrm{V}_{\mathrm{Z}}}{\mathrm{~d}_{\mathrm{s}}} \tag{9d}
\end{align*}
$$

It is worth noting that the beam moment $\mathrm{M}_{\mathrm{z}}(\mathrm{X})$, given by equation (A5f), vanishes when the variation of $\sigma_{\mathrm{xx}}$ across the width of the equivalent-stiffener layer is neglected, consistent with a plate theory based on a classical continuum model.

## Kinematical Equivalence

The next step in the analysis is to establish kinematical equivalence so that the stiffener strains can be related to the appropriate plate strains in the equivalent-stiffener layer of the equivalentplate element. The general expressions for the strains in a plate, modeled with first-order transverse-shear deformation plate theory, are given by (e. g., see reference 139)

$$
\begin{gather*}
\varepsilon_{\mathrm{XX}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\varepsilon_{\mathrm{XX}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})+\mathrm{Z} \kappa_{\mathrm{XX}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})  \tag{10a}\\
\varepsilon_{\mathrm{YY}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\varepsilon_{\mathrm{YY}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})+\mathrm{Z} \kappa_{\mathrm{YY}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})  \tag{10b}\\
\gamma_{\mathrm{XY}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\gamma_{\mathrm{XY}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})+\mathrm{Z} \kappa_{\mathrm{XY}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})  \tag{10c}\\
\gamma_{\mathrm{XZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\gamma_{\mathrm{XZ}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})  \tag{10d}\\
\gamma_{\mathrm{YZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\gamma_{\mathrm{YZ}}^{\mathrm{o}}(\mathrm{X}, \mathrm{Y})  \tag{10e}\\
\varepsilon_{\mathrm{ZZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=0 \tag{10f}
\end{gather*}
$$

These strains are defined with respect to the reference surface (plate wall midplane) of the equivalent-plate element shown in figure 13. Moreover, $\varepsilon_{\mathrm{xx}}^{\circ}$ and $\varepsilon_{\mathrm{yY}}^{\circ}$ are the extensional strains of the plate midplane and $\gamma_{\mathrm{XY}}^{\circ}$ is the corresponding inplane shearing strain. Likewise, $\kappa_{\mathrm{XX}}^{\circ}$ and $\kappa_{\mathrm{YY}}^{\circ}$ are bending strains of the plate midplane and $\kappa_{\mathrm{XY}}^{\circ}$ is the corresponding twisting strain. The symbols $\gamma_{\mathrm{xz}}^{\circ}$ and $\gamma_{\mathrm{yz}}^{\circ}$ denote the transverse shearing strains. The kinematical equivalence is obtained based on the presumption that the strain at any point of a stiffener is identical to the strain at the corresponding point in the equivalent-stiffener layer of the equivalent-plate element. In addition, it is presumed that bending of the stiffener in the plane parallel to the plate midplane is negligible and, as a result, the variation of strains across the width of the equivalent-stiffener layer can be neglected. Furthermore, it is presumed that the eccentric stiffener contributes only half of the inplane shearing strain and half of the change in surface twist of the equivalent-stiffener layer. This presumption is rationalized by noting that the inplane shearing strain and the change in surface twist of a plate are deformation measures that have contributions associated with both cross-sectional faces of a differential plate element, and that the shearing and twisting deformations of the stiffener only act on one face of the equivalent-stiffener layer of the equivalent-plate element. Therefore, this last presumption represents an averaging of the stiffener contribution to the corresponding overall plate strains. Thus, the kinematical equivalence yields the following expressions

$$
\begin{gather*}
\mathrm{e}_{\mathrm{XX}}^{\circ}(\mathrm{X})=\varepsilon_{\mathrm{XX}}^{\circ}(\mathrm{X}, \mathrm{Y})  \tag{11a}\\
\chi_{\mathrm{Z}}^{\circ}(\mathrm{X})=0  \tag{11b}\\
\chi_{\mathrm{Y}}^{\circ}(\mathrm{X})=\kappa_{\mathrm{XX}}^{\circ}(\mathrm{X}, \mathrm{Y})  \tag{11c}\\
\tau^{\circ}(\mathrm{X})=-\frac{1}{2} \kappa_{\mathrm{XY}}^{\circ}(\mathrm{X}, \mathrm{Y})  \tag{11d}\\
\Gamma_{\mathrm{XY}}^{\circ}(\mathrm{X})=\frac{1}{2} \gamma_{\mathrm{XY}}^{\circ}(\mathrm{X}, \mathrm{Y})  \tag{11e}\\
\Gamma_{\mathrm{XZ}}^{\circ}(\mathrm{X})=\gamma_{\mathrm{XZ}}^{\circ}(\mathrm{X}, \mathrm{Y}) \tag{11f}
\end{gather*}
$$

In equations (11), $\tau^{\circ}$ is the change in twist of the beam, associated with torsion, and $\chi_{\mathrm{Y}}^{\circ}$ and $\chi_{\mathrm{Z}}^{\circ}$ are the beam bending strains associated with the changes in curvature in the $\mathrm{X}-\mathrm{Z}$ and $\mathrm{X}-\mathrm{Y}$ planes, respectively. The symbols $\Gamma_{\mathrm{XY}}^{\circ}$ and $\Gamma_{\mathrm{xz}}^{\circ}$ are the transverse shearing strains in the X-Y and X-Z planes, respectively. Substituting these expressions for the strains into the stiffener constitutive equations, given by equations (A19)-(A21) and (A25) in Appendix A, gives

$$
\begin{equation*}
\mathrm{P}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}\left(\boldsymbol{\varepsilon}_{\mathrm{xx}}^{\circ}+\overline{\mathrm{z}}_{\mathrm{s}} \kappa_{\mathrm{xx}}^{\circ}\right) \tag{12a}
\end{equation*}
$$

$$
\begin{gather*}
\mathrm{V}_{\mathrm{Y}}=\frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{2}\left(\gamma_{\mathrm{XY}}^{o}+\overline{\bar{Z}}_{\mathrm{S}} \kappa_{\mathrm{XY}}^{o}\right)  \tag{12b}\\
\mathrm{V}_{\mathrm{Z}}=\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \gamma_{\mathrm{XZ}}^{o}  \tag{12c}\\
\mathrm{~T}=-\frac{1}{2}\left(\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{Z}}_{\mathrm{S}} \gamma_{\mathrm{XY}}^{o}+\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} \kappa_{\mathrm{XY}}^{o}\right)  \tag{12~d}\\
\mathrm{M}_{\mathrm{Y}}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\mathrm{Z}}_{\mathrm{S}} \varepsilon_{\mathrm{XX}}^{o}+\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} \kappa_{\mathrm{XX}}^{o}  \tag{12e}\\
\mathrm{M}_{\mathrm{Z}}=\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YZ}}^{\mathrm{s}} \kappa_{\mathrm{XX}}^{o} \tag{12f}
\end{gather*}
$$

Substituting equations (12) into equations (5) and (8) yields

$$
\begin{gather*}
\mathcal{U}_{\mathrm{XX}}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{S}}}\left(\varepsilon_{\mathrm{XX}}^{\circ}+\overline{\mathrm{z}}_{\mathrm{S}} \kappa_{\mathrm{XX}}^{\circ}\right)  \tag{13a}\\
\mathcal{U}_{\mathrm{XY}}^{\text {stiffener }}=\frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{2 \mathrm{~d}_{\mathrm{S}}}\left(\gamma_{\mathrm{XY}}^{\circ}+\overline{\bar{z}}_{\mathrm{S}} \kappa_{\mathrm{XY}}^{\circ}\right)  \tag{13b}\\
\mathcal{M}_{\mathrm{XX}}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \varepsilon_{\mathrm{XX}}^{\circ}+\frac{\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \kappa_{\mathrm{XX}}^{\circ}  \tag{13c}\\
\mathcal{M}_{\mathrm{XY}}^{\text {stiffener }}=\frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{z}}_{\mathrm{S}}}{2 \mathrm{~d}_{\mathrm{S}}} \gamma_{\mathrm{XY}}^{\circ}+\frac{\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}}{2 \mathrm{~d}_{\mathrm{S}}} \kappa_{\mathrm{XY}}^{\circ}  \tag{13~d}\\
\mathrm{Q}_{\mathrm{XZ}}^{\text {stiffener }}=\frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{S}}} \gamma_{\mathrm{XZ}}^{\circ} \tag{13e}
\end{gather*}
$$

Equations (13) give the contributions of the stiffeners to the pointwise equivalent-plate stress resultants, in the X-Y-Z coordinate system, in terms of the corresponding plate strains. However, another issue must be considered. In particular, the shearing stress resultant, $\boldsymbol{U}_{\mathrm{xy}}$, and twisting stress resultant, $\boldsymbol{M}_{\mathrm{xy}}$, of classical and first-order transverse-shear deformation plate theories are based on the symmetries $\boldsymbol{N}_{\mathrm{xy}}=\boldsymbol{N}_{\mathrm{yx}}$ and $\boldsymbol{M}_{\mathrm{xy}}=\boldsymbol{M}_{\mathrm{yx}}$ of the corresponding stress resultants acting on the cross-sectional faces of a differential plate element. The stiffener is presumed to provide no inplane shear stiffness and twisting stiffness to the equivalent-stiffener layer in the inplane direction parallel to its axis (e.g., see reference 30, p. 30). Therefore, with regard to the constitutive equations, equations (7a) and (7c) must be modified to yield

$$
\begin{align*}
& M_{\mathrm{XY}}=M_{\mathrm{XY}}^{\text {plate }}+\frac{1}{2} M_{\mathrm{XY}}^{\text {stiffener }}  \tag{14a}\\
& M_{\mathrm{XY}}=M_{\mathrm{XY}}^{\text {plate }}+\frac{1}{2} M_{\mathrm{XY}}^{\text {stiffener }} \tag{14b}
\end{align*}
$$

These two equations represent an averaging of the stiffener contribution over both cross-sectional faces of a differential equivalent-plate element. The constitutive equations of the equivalentstiffener layer become

$$
\begin{align*}
& \left\{\begin{array}{c}
{U_{X X}^{\text {stiffener }}}^{U_{Y Y}^{\text {stiffener }}} \\
\frac{1}{2} U_{X Y}^{\text {stiffener }}
\end{array}\right\}=\left[\begin{array}{ccc}
\frac{E_{S} A_{S}}{d_{S}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{k_{Y}^{s} G_{S} A_{S}}{4 d_{S}}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{X X}^{o} \\
\varepsilon_{Y Y}^{o} \\
\gamma_{X Y}^{o}
\end{array}\right\}+\left[\begin{array}{ccc}
\frac{E_{S} A_{S} \bar{z}_{S}}{d_{S}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{k_{Y}^{s} G_{S} A_{S} \overline{\bar{z}}_{S}}{4 d_{S}}
\end{array}\right]\left\{\begin{array}{l}
\kappa_{X X}^{o} \\
\kappa_{Y Y}^{o} \\
\kappa_{X Y}^{o}
\end{array}\right\}  \tag{15a}\\
& \left\{\begin{array}{c}
m_{X X}^{\text {stiffener }} \\
m_{Y Y}^{\text {stiffener }} \\
\frac{1}{2} M_{X Y}^{\text {stiffener }}
\end{array}\right\}=\left[\begin{array}{ccc}
\frac{E_{S} A_{S} \bar{z}_{S}}{d_{S}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{k_{Y}^{s} G_{S} A_{S} \overline{\bar{Z}}_{S}}{4 d_{S}}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{X X}^{o} \\
\varepsilon_{Y Y}^{o} \\
\gamma_{X Y}^{o}
\end{array}\right\}+\left[\begin{array}{ccc}
\frac{E_{S} I_{Y Y}^{s}}{d_{S}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{G_{S} J_{S}}{4 d_{S}}
\end{array}\right]\left\{\begin{array}{l}
\kappa_{X X}^{o} \\
\kappa_{Y Y}^{o} \\
\kappa_{X Y}^{o}
\end{array}\right\}  \tag{15b}\\
& \left\{\begin{array}{c}
Q_{Y Z}^{\text {stiffener }} \\
Q_{X Z}^{\text {stiffener }}
\end{array}\right\}=\left[\begin{array}{cc}
0 & \frac{k_{Z}^{s} G_{S} A_{S}}{d_{S}}
\end{array}\right]\left\{\begin{array}{c}
\gamma_{Y Z}^{o} \\
\gamma_{X Z}^{o}
\end{array}\right\} \tag{15c}
\end{align*}
$$

where it is noted that matrices associated with coupling between inplane and out-of-plane deformations are identical in both equations. It is important to also note that the stiffnesses occupying the third row and third column of the matrices in equation (15a) are associated with transverseshear deformations of the beam member in a plane parallel to the plate midplane. As such, these stiffnesses are referred to herein as "inplane transverse-shearing stiffnesses." In contrast, the stiffness occupying the second row and second column of the matrix in equation (15c) is associated with transverse-shear deformations of the beam member in the direction perpendicular to the plate midplane and is referred to herein as an "out-of-plane transverse-shearing stiffness."

The next step in the analysis is to relate the plate stress resultants in the X-Y-Z coordinate system to the $\mathrm{x}-\mathrm{y}-\mathrm{z}$ coordinate system shown in figure 6 . Using the standard stress and strain transformation equations for the rotation of coordinates depicted in figure 6 gives

$$
\begin{gather*}
\left\{\begin{array}{l}
\sigma_{\mathrm{XX}} \\
\sigma_{\mathrm{YY}} \\
\sigma_{\mathrm{XY}}
\end{array}\right\}=\left[\begin{array}{ccc}
\cos ^{2} \Psi_{\mathrm{S}} & \sin ^{2} \Psi_{\mathrm{S}} & 2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
\sin ^{2} \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}} & -2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
-\sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}}-\sin ^{2} \Psi_{\mathrm{S}}
\end{array}\right]\left\{\begin{array}{l}
\sigma_{\mathrm{xx}} \\
\sigma_{\mathrm{yy}} \\
\sigma_{\mathrm{xy}}
\end{array}\right\} \equiv\left[\mathrm{T}_{\sigma}\right]\left\{\begin{array}{l}
\sigma_{\mathrm{xx}} \\
\sigma_{\mathrm{yy}} \\
\sigma_{\mathrm{xy}}
\end{array}\right\}  \tag{16a}\\
\left\{\begin{array}{l}
\sigma_{\mathrm{YZ}} \\
\sigma_{\mathrm{XZ}}
\end{array}\right\}=\left[\begin{array}{cc}
\cos \Psi_{\mathrm{S}} & -\sin \Psi_{\mathrm{S}} \\
\sin \Psi_{\mathrm{S}} & \cos \Psi_{\mathrm{S}}
\end{array}\right]\left\{\begin{array}{l}
\sigma_{\mathrm{yz}} \\
\sigma_{\mathrm{xz}}
\end{array}\right\} \equiv\left[\mathrm{T}_{\tau}\right]\left\{\begin{array}{l}
\sigma_{\mathrm{yz}} \\
\sigma_{\mathrm{xz}}
\end{array}\right\} \tag{16b}
\end{gather*}
$$

with

$$
\left[\mathrm{T}_{\sigma}\right]^{-1}=\left[\begin{array}{ccc}
\cos ^{2} \Psi_{\mathrm{S}} & \sin ^{2} \Psi_{\mathrm{S}} & -2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}  \tag{16c}\\
\sin ^{2} \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}} & 2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
\sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & -\sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}}-\sin ^{2} \Psi_{\mathrm{S}}
\end{array}\right]
$$

and

$$
\left[\mathrm{T}_{\tau}\right]^{-1}=\left[\begin{array}{cc}
\cos \Psi_{\mathrm{s}} & \sin \Psi_{\mathrm{s}}  \tag{16~d}\\
-\sin \Psi_{\mathrm{s}} & \cos \Psi_{\mathrm{s}}
\end{array}\right]
$$

Additionally,

$$
\begin{gather*}
\left\{\begin{array}{c}
\varepsilon_{\mathrm{XX}} \\
\varepsilon_{\mathrm{YY}} \\
\gamma_{\mathrm{XY}}
\end{array}\right\}=\left[\begin{array}{ccc}
\cos ^{2} \Psi_{\mathrm{S}} & \sin ^{2} \Psi_{\mathrm{S}} & \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
\sin ^{2} \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}} & \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
-2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & 2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}}-\sin ^{2} \Psi_{\mathrm{S}}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{\mathrm{xx}} \\
\varepsilon_{\mathrm{yy}} \\
\gamma_{\mathrm{xy}}
\end{array}\right\} \equiv\left[\mathrm{T}_{\varepsilon}\right]\left\{\begin{array}{c}
\varepsilon_{\mathrm{xx}} \\
\varepsilon_{\mathrm{yy}} \\
\gamma_{\mathrm{xy}}
\end{array}\right\}  \tag{17a}\\
\left\{\begin{array}{c}
\gamma_{\mathrm{YZ}} \\
\gamma_{\mathrm{xZ}}
\end{array}\right\}=\left[\mathrm{T}_{\tau}\right]\left\{\begin{array}{l}
\gamma_{\mathrm{yz}} \\
\gamma_{\mathrm{xz}}
\end{array}\right\} \tag{17b}
\end{gather*}
$$

with

$$
\left[\mathrm{T}_{\varepsilon}\right]^{-1}=\left[\begin{array}{ccc}
\cos ^{2} \Psi_{\mathrm{S}} & \sin ^{2} \Psi_{\mathrm{S}} & -\sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}  \tag{17c}\\
\sin ^{2} \Psi_{\mathrm{S}} & \cos ^{2} \Psi_{\mathrm{S}} & \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \\
2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} & -2 \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}-\sin ^{2} \Psi_{\mathrm{S}}
\end{array}\right]
$$

Based on the standard definitions of plate stress results, it follows that

$$
\left\{\begin{array}{l}
\boldsymbol{n}_{\mathrm{xX}}  \tag{18a}\\
\boldsymbol{n}_{\mathrm{yY}} \\
\boldsymbol{n}_{\mathrm{xY}}
\end{array}\right\}=\left[\mathrm{T}_{\sigma}\right]\left[\begin{array}{l}
\boldsymbol{n}_{\mathrm{xx}} \\
\boldsymbol{n}_{\mathrm{yy}} \\
\boldsymbol{n}_{\mathrm{xy}}
\end{array}\right\}
$$

$$
\begin{align*}
& \left\{\begin{array}{l}
\boldsymbol{m}_{\mathrm{xx}} \\
\boldsymbol{m}_{\mathrm{yY}} \\
\boldsymbol{m}_{\mathrm{xy}}
\end{array}\right\}=\left[\mathrm{T}_{\mathrm{o}}\right]\left\{\begin{array}{l}
\boldsymbol{m}_{\mathrm{xx}} \\
\boldsymbol{m}_{\mathrm{yy}} \\
\boldsymbol{m}_{\mathrm{xy}}
\end{array}\right\}  \tag{18b}\\
& \left\{\begin{array}{l}
\mathrm{Q}_{\mathrm{xz}} \\
\mathrm{Q}_{\mathrm{xz}}
\end{array}\right\}=\left[\mathrm{T}_{\tau}\right]\left\{\begin{array}{l}
\mathrm{Q}_{\mathrm{yz}} \\
\mathrm{Q}_{\mathrm{xz}}
\end{array}\right\} \tag{18c}
\end{align*}
$$

From equations (10) and the corresponding equations in the $x-y-z$ coordinate system, it follows from equations (17a) and (17b) that

$$
\begin{align*}
& \left\{\begin{array}{c}
\varepsilon_{\mathrm{XX}}^{\mathrm{o}} \\
\varepsilon_{\mathrm{YY}}^{\mathrm{o}} \\
\gamma_{\mathrm{XY}}^{\mathrm{o}}
\end{array}\right\}=\left[\mathrm{T}_{\varepsilon}\right]\left[\begin{array}{c}
\varepsilon_{\mathrm{xx}}^{\mathrm{o}} \\
\varepsilon_{\mathrm{yy}}^{\mathrm{o}} \\
\gamma_{\mathrm{xy}}^{\mathrm{o}}
\end{array}\right\}  \tag{19a}\\
& \left\{\begin{array}{c}
\kappa_{\mathrm{XX}}^{\mathrm{o}} \\
\kappa_{\mathrm{YY}}^{\mathrm{o}} \\
\kappa_{\mathrm{XY}}^{\mathrm{o}}
\end{array}\right\}=\left[\mathrm{T}_{\varepsilon}\right]\left[\begin{array}{c}
\kappa_{\mathrm{xx}}^{\mathrm{o}} \\
\kappa_{\mathrm{yy}}^{\mathrm{o}} \\
\kappa_{\mathrm{xy}}^{\mathrm{o}}
\end{array}\right\}  \tag{19b}\\
& \left\{\begin{array}{c}
\gamma_{\mathrm{YZ}}^{\mathrm{o}} \\
\gamma_{\mathrm{XZ}}^{\mathrm{o}}
\end{array}\right\}=\left[\mathrm{T}_{\tau}\right]\left\{\begin{array}{c}
\gamma_{\mathrm{yz}}^{\mathrm{o}} \\
\gamma_{\mathrm{xz}}^{\mathrm{o}}
\end{array}\right\} \tag{19c}
\end{align*}
$$

Now, using

$$
\begin{align*}
& \left\{\begin{array}{l}
\boldsymbol{n}_{\mathrm{xx}} \\
\boldsymbol{n}_{\mathrm{yr}} \\
\boldsymbol{n}_{\mathrm{xy}}
\end{array}\right\}=\left\{\begin{array}{l}
\boldsymbol{n}_{\mathrm{xx}}^{\text {plate }} \\
\boldsymbol{n}_{\mathrm{yP}}^{\text {plate }} \\
\boldsymbol{n}_{\mathrm{xy}}^{\text {plate }}
\end{array}\right\}+\left\{\begin{array}{l}
\boldsymbol{n}_{\mathrm{xx}}^{\text {stifferer }} \\
\boldsymbol{n}_{\mathrm{ys}}^{\text {suffener }} \\
\frac{1}{2} \boldsymbol{n}_{\mathrm{xy}}^{\text {stiffener }}
\end{array}\right\}  \tag{20a}\\
& \left\{\begin{array}{l}
\boldsymbol{m}_{\mathrm{xx}} \\
\boldsymbol{m}_{\mathrm{yx}} \\
\boldsymbol{m}_{\mathrm{xy}}
\end{array}\right\}=\left\{\begin{array}{l}
\boldsymbol{m}_{\mathrm{xx}}^{\text {plate }} \\
\boldsymbol{m}_{\mathrm{xy}}^{\text {plat }} \\
\boldsymbol{m}_{\mathrm{xy}}^{\text {plat }}
\end{array}\right\}+\left\{\begin{array}{l}
\boldsymbol{m}_{\mathrm{xx}}^{\text {stifferer }} \\
\boldsymbol{m}_{\mathrm{yx} \text { sifferer }}^{\text {stiff }} \\
\frac{1}{2} \boldsymbol{m}_{\mathrm{xy}}^{\text {stifferer }}
\end{array}\right\}  \tag{20b}\\
& \left\{\begin{array}{c}
Q_{y z} \\
Q_{x z}
\end{array}\right\}=\left\{\begin{array}{c}
Q_{y z}^{\text {plate }} \\
Q_{x z}^{\text {plate }}
\end{array}\right\}+\left\{\begin{array}{c}
Q_{y z}^{\text {stiffener }} \\
Q_{x z}^{\text {stiffener }}
\end{array}\right\} \tag{20c}
\end{align*}
$$

with equations (18) it follows that

Similarly,

$$
\begin{align*}
&\left\{\begin{array}{l}
\mathcal{M}_{\mathrm{xx}} \\
\mathcal{M}_{\mathrm{yy}} \\
\mathcal{M}_{\mathrm{xy}}
\end{array}\right\}=\left\{\begin{array}{l}
\mathcal{M}_{\mathrm{xx}}^{\text {plate }} \\
\mathcal{M}_{\mathrm{yxy}}^{\text {plate }} \\
\mathcal{M}_{\mathrm{xy}}^{\text {plate }}
\end{array}\right\}+\left[\mathrm{T}_{\mathrm{z}}\right]^{-1}\left\{\begin{array}{l}
\mathcal{M}_{\mathrm{xx}}^{\text {stiffener }} \\
\mathcal{M}_{\mathrm{ys}}^{\text {suffener }} \\
\frac{1}{2} \mathcal{M}_{\mathrm{xy}}^{\text {stiffener }}
\end{array}\right\}  \tag{21b}\\
&\left\{\begin{array}{c}
\mathrm{Q}_{\mathrm{yz}} \\
\mathrm{Q}_{\mathrm{xz}}
\end{array}\right\}=\left\{\begin{array}{c}
\mathrm{Q}_{\mathrm{yz}}^{\text {plate }} \\
\mathrm{Q}_{\mathrm{xz}}^{\text {plate }}
\end{array}\right\}+\left[\mathrm{T}_{\tau}\right]^{-1}\left\{\begin{array}{c}
\mathrm{Q}_{\mathrm{xz}}^{\text {stiffener }} \\
\mathrm{Q}_{\mathrm{xz}}^{\text {stiffener }}
\end{array}\right\} \tag{21c}
\end{align*}
$$

Substituting equations (19) into equations (15) and then substituting the results into equations (21) yields

$$
\begin{gather*}
\left\{\begin{array}{c}
\mathbb{U}_{\mathrm{xx}} \\
\mathbb{U}_{\mathrm{yy}} \\
\mathbb{U}_{\mathrm{xy}} \\
\hline \mathbb{M}_{\mathrm{xx}} \\
\mathbb{M}_{\mathrm{yy}} \\
\mathbb{M}_{\mathrm{xy}}
\end{array}\right\}=\left[\begin{array}{lll|lll}
\mathrm{A}_{11} & \mathrm{~A}_{12} & \mathrm{~A}_{16} & \mathrm{~B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} \\
\mathrm{~A}_{12} & \mathrm{~A}_{22} & \mathrm{~A}_{26} & \mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} \\
\mathrm{~A}_{16} & \mathrm{~A}_{26} & \mathrm{~A}_{66} & \mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66} \\
\hline \mathrm{~B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} & \mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} & \mathrm{D}_{12} & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66} & \mathrm{D}_{16} & \mathrm{D}_{26} & \mathrm{D}_{66}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{\mathrm{xx}}^{\mathrm{o}} \\
\varepsilon_{\mathrm{yy}}^{\mathrm{o}} \\
\gamma_{\mathrm{xy}}^{\mathrm{o}} \\
\hline \kappa_{\mathrm{xx}}^{\mathrm{o}} \\
\kappa_{\mathrm{yy}}^{\mathrm{o}} \\
\kappa_{\mathrm{xy}}^{\mathrm{o}}
\end{array}\right\}  \tag{22a}\\
\left.\left\{\begin{array}{l}
\mathrm{Q}_{\mathrm{yz}} \\
\mathrm{Q}_{\mathrm{xz}}
\end{array}\right\}=\left[\begin{array}{ll}
\mathrm{A}_{44} & \mathrm{~A}_{45} \\
\mathrm{~A}_{45} & \mathrm{~A}_{55}
\end{array}\right]\right)\left(\begin{array}{l}
\gamma_{\mathrm{yz}}^{\mathrm{o}} \\
\gamma_{\mathrm{xz}}^{\mathrm{o}}
\end{array}\right\} \tag{22b}
\end{gather*}
$$

where

$$
\begin{align*}
& {\left[\begin{array}{lll}
A_{11} & A_{12} & A_{16} \\
A_{12} & A_{22} & A_{26} \\
A_{16} & A_{26} & A_{66}
\end{array}\right]=\left[\begin{array}{lll}
A_{11}^{\text {plate }} & A_{12}^{\text {plate }} & A_{16}^{\text {plate }} \\
A_{12}^{\text {plate }} & A_{22}^{\text {plate }} & A_{26}^{\text {plate }} \\
A_{16}^{\text {plate }} & A_{26}^{\text {plate }} & A_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{lll}
A_{11}^{\text {stiffener }} & A_{12}^{\text {stiffener }} & A_{16}^{\text {stiffener }} \\
A_{12}^{\text {stiffener }} & A_{22}^{\text {stiffener }} & A_{26}^{\text {stiffener }} \\
A_{16}^{\text {stiffener }} & A_{26}^{\text {stiffener }} & A_{66}^{\text {stiffener }}
\end{array}\right]}  \tag{23a}\\
& {\left[\begin{array}{lll}
B_{11} & B_{12} & B_{16} \\
B_{12} & B_{22} & B_{26} \\
B_{16} & B_{26} & B_{66}
\end{array}\right]=\left[\begin{array}{lll}
B_{11}^{\text {plate }} & B_{12}^{\text {plate }} & B_{16}^{\text {plate }} \\
B_{12}^{\text {plate }} & B_{22}^{\text {plate }} & B_{26}^{\text {plate }} \\
B_{16}^{\text {plate }} & B_{26}^{\text {plate }} & B_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{lll}
B_{11}^{\text {stiffener }} & B_{12}^{\text {stiffener }} & B_{16}^{\text {stiffener }} \\
B_{12}^{\text {stiffener }} & B_{22}^{\text {stiffener }} & B_{26}^{\text {stiffener }} \\
B_{16}^{\text {stiffener }} & B_{26}^{\text {stiffener }} & B_{66}^{\text {stiffener }}
\end{array}\right]}  \tag{23b}\\
& {\left[\begin{array}{lll}
D_{11} & D_{12} & D_{16} \\
D_{12} & D_{22} & D_{26} \\
D_{16} & D_{26} & D_{66}
\end{array}\right]=\left[\begin{array}{lll}
D_{11}^{\text {plate }} & D_{12}^{\text {plate }} & D_{16}^{\text {plate }} \\
D_{12}^{\text {plate }} & D_{22}^{\text {plate }} & D_{26}^{\text {plate }} \\
D_{16}^{\text {plate }} & D_{26}^{\text {plate }} & D_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{lll}
D_{11}^{\text {stiffener }} & D_{12}^{\text {stiffener }} & D_{16}^{\text {stiffener }} \\
D_{12}^{\text {stiffener }} & D_{22}^{\text {stiffener }} & D_{26}^{\text {stiffener }} \\
D_{16}^{\text {stiffener }} & D_{26}^{\text {stiffener }} & D_{66}^{\text {stiffener }}
\end{array}\right]} \tag{23c}
\end{align*}
$$

$$
\left[\begin{array}{ll}
A_{44} & A_{45}  \tag{23d}\\
A_{45} & A_{55}
\end{array}\right]=\left[\begin{array}{ll}
A_{44}^{\text {plate }} & A_{45}^{\text {plate }} \\
A_{45}^{\text {plate }} & A_{55}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{ll}
A_{44}^{\text {stiffener }} & A_{45}^{\text {stiffener }} \\
A_{45}^{\text {stiffener }} & A_{55}^{\text {stiffener }}
\end{array}\right]
$$

with

$$
\begin{align*}
& {\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {stiffener }} & \mathrm{A}_{12}^{\text {stiffener }} & \mathrm{A}_{16}^{\text {stiffere }} \\
\mathrm{A}_{12}^{\text {stiffener }} & \mathrm{A}_{22}^{\text {stiffener }} & \mathrm{A}_{26}^{\text {stiffener }} \\
\mathrm{A}_{16}^{\text {stifferer }} & \mathrm{A}_{26}^{\text {stiffener }} & \mathrm{A}_{66}^{\text {stiffener }}
\end{array}\right]=\left[\mathrm{T}_{\mathrm{G}}\right]^{-1}\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{S}}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{\mathrm{k}_{\mathrm{Y}}^{s} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{4 \mathrm{~d}_{\mathrm{S}}}
\end{array}\right]\left[\mathrm{T}_{\varepsilon}\right]}  \tag{24a}\\
& {\left[\begin{array}{cccc}
\mathrm{B}_{11}^{\text {stiffener }} & \mathrm{B}_{12}^{\text {stiffener }} & \mathrm{B}_{16}^{\text {stiffener }} \\
\mathrm{B}_{12}^{\text {stiffener }} & \mathrm{B}_{22}^{\text {stiffener }} & \mathrm{B}_{26}^{\text {stiffener }} \\
\mathrm{B}_{16}^{\text {stiffener }} & \mathrm{B}_{26}^{\text {stiffener }} & \mathrm{B}_{66}^{\text {stiffener }}
\end{array}\right]=\left[\mathrm{T}_{\sigma}\right]^{-1}\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \bar{z}_{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}}}{4 \mathrm{~d}_{\mathrm{s}}}
\end{array}\right]\left[\mathrm{T}_{\varepsilon}\right]}  \tag{24b}\\
& {\left[\begin{array}{lll}
\mathrm{D}_{11}^{\text {stiffener }} & \mathrm{D}_{12}^{\text {stiffener }} & \mathrm{D}_{16}^{\text {stiffener }} \\
\mathrm{D}_{12}^{\text {stiffener }} & \mathrm{D}_{22}^{\text {stiffener }} & \mathrm{D}_{26}^{\text {stiffener }} \\
\mathrm{D}_{16}^{\text {stiffener }} & \mathrm{D}_{26}^{\text {stiffener }} & \mathrm{D}_{66}^{\text {stiffener }}
\end{array}\right]=\left[\mathrm{T}_{\sigma}\right]^{-1}\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{J}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & \frac{1}{4} \mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}
\end{array}\right]\left[\mathrm{T}_{\varepsilon}\right]}  \tag{24c}\\
& {\left[\begin{array}{cc}
\mathrm{A}_{44}^{\text {stiffener }} & \mathrm{A}_{45}^{\text {stiffener }} \\
\mathrm{A}_{45}^{\text {stiffener }} & \mathrm{A}_{55}^{\text {stiffener }}
\end{array}\right]=\left[\mathrm{T}_{\tau}\right]^{-1}\left[\begin{array}{cc}
0 & 0 \\
0 & \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{s}}}
\end{array}\right]\left[\mathrm{T}_{\tau}\right]} \tag{24d}
\end{align*}
$$

The constitutive terms with the superscript "plate" are the usual stiffnesses of the Reissner-Mindlin-type shear-deformation plate theory that are found in reference 139. The explicit expressions for the stiffnesses associated with the stiffeners are given by

$$
\begin{align*}
& \mathrm{A}_{11}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{S}}} \cos ^{2} \Psi_{\mathrm{S}}\left(\cos ^{2} \Psi_{\mathrm{S}}+\tau_{\mathrm{Y}}^{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\right)  \tag{25a}\\
& \mathrm{A}_{12}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{S}}} \sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(1-\tau_{\mathrm{Y}}^{\mathrm{S}}\right) \tag{25b}
\end{align*}
$$

$$
\begin{align*}
& A_{16}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin \Psi_{S} \cos \Psi_{S}\left(\cos ^{2} \Psi_{S}-\frac{\tau_{Y}^{S}}{2} \cos 2 \Psi_{S}\right)  \tag{25c}\\
& A_{22}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin ^{2} \Psi_{S}\left(\sin ^{2} \Psi_{S}+\tau_{Y}^{S} \cos ^{2} \Psi_{S}\right)  \tag{25~d}\\
& A_{26}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin \Psi_{S} \cos \Psi_{S}\left(\sin ^{2} \Psi_{S}+\frac{\tau_{Y}^{S}}{2} \cos 2 \Psi_{S}\right)  \tag{25e}\\
& A_{66}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}}\left(\sin ^{2} \Psi_{S} \cos ^{2} \Psi_{S}+\frac{\tau_{Y}^{S}}{4} \cos ^{2} 2 \Psi_{S}\right)  \tag{25f}\\
& B_{11}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \cos ^{2} \Psi_{S}\left(\bar{z}_{S} \cos ^{2} \Psi_{S}+\tau_{Y}^{S} \overline{\bar{z}}_{S} \sin ^{2} \Psi_{S}\right)  \tag{26a}\\
& B_{12}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin ^{2} \Psi_{S} \cos ^{2} \Psi_{S}\left(\bar{z}_{S}-\tau_{Y}^{S} \overline{\bar{z}}_{S}\right)  \tag{26b}\\
& B_{16}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin \Psi_{S} \cos \Psi_{S}\left(\bar{z}_{S} \cos ^{2} \Psi_{S}-\frac{\tau_{Y}^{S} \overline{\bar{z}}_{S}}{2} \cos 2 \Psi_{S}\right)  \tag{26c}\\
& B_{22}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin { }^{2} \Psi_{S}\left(\bar{z}_{S} \sin ^{2} \Psi_{S}+\tau_{Y}^{S} \overline{\bar{z}}_{S} \cos ^{2} \Psi_{S}\right)  \tag{26d}\\
& B_{26}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}} \sin \Psi_{S} \cos \Psi_{S}\left(\bar{z}_{S} \sin ^{2} \Psi_{S}+\frac{\tau_{Y}^{S} \overline{\bar{z}}_{S}}{2} \cos 2 \Psi_{S}\right)  \tag{26e}\\
& B_{66}^{\text {stiffener }}=\frac{E_{S} A_{S}}{d_{S}}\left(\bar{z}_{S} \sin ^{2} \Psi_{S} \cos ^{2} \Psi_{S}+\frac{\tau_{Y}^{S} \overline{\bar{z}}_{S}}{4} \cos ^{2} 2 \Psi_{S}\right)  \tag{26f}\\
& D_{11}^{\text {stiffener }}=\cos ^{2} \Psi_{S}\left(\frac{E_{S} I_{Y Y}^{S}}{d_{S}} \cos { }^{2} \Psi_{S}+\frac{G_{S} J_{S}}{d_{S}} \sin ^{2} \Psi_{S}\right)  \tag{27a}\\
& D_{12}^{\text {stiffener }}=\sin ^{2} \Psi_{S} \cos ^{2} \Psi_{S}\left(\frac{E_{S} I_{Y Y}^{S}}{d_{S}}-\frac{G_{S} J_{S}}{d_{S}}\right) \tag{27b}
\end{align*}
$$

$$
\begin{align*}
& \mathrm{D}_{16}^{\text {stiffener }}= \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\frac{\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \cos ^{2} \Psi_{\mathrm{S}}-\frac{1}{2} \frac{\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{s}}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{27c}\\
& \mathrm{D}_{22}^{\text {stiffener }}= \sin ^{2} \Psi_{\mathrm{S}}\left(\frac{\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \sin ^{2} \Psi_{\mathrm{S}}+\frac{\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{s}}} \cos ^{2} \Psi_{\mathrm{S}}\right)  \tag{27~d}\\
& \mathrm{D}_{26}^{\text {stiffener }}= \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\frac{\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \sin ^{2} \Psi_{\mathrm{S}}+\frac{1}{2} \frac{\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{s}}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{27e}\\
& \mathrm{D}_{66}^{\text {stiffener }}= \frac{\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}+\frac{1}{4} \frac{\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}}{\mathrm{~d}_{\mathrm{s}}} \cos ^{2} 2 \Psi_{\mathrm{S}}  \tag{27f}\\
& \mathrm{~A}_{44}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \sin { }^{2} \Psi_{\mathrm{s}}  \tag{28a}\\
& \mathrm{~A}_{45}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{s}}  \tag{28b}\\
& \mathrm{~A}_{55}^{\text {stiffener }}=\frac{\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \cos ^{2} \Psi_{\mathrm{s}} \tag{28c}
\end{align*}
$$

where

$$
\begin{equation*}
\tau_{\mathrm{Y}}^{\mathrm{S}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}}}{\mathrm{E}_{\mathrm{S}}} \tag{29a}
\end{equation*}
$$

is an inplane-shear-deformation parameter associated with the shear flexibility of the stiffeners in a direction parallel to the plate midplane, based on a first-order transverse-shear deformation beam theory, and

$$
\begin{equation*}
\tau_{\mathrm{z}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}} \tag{29b}
\end{equation*}
$$

is a corresponding transverse-shear-deformation parameter associated with the shear flexibility of the stiffeners in a direction perpendicular to the plate midplane. The effects of inplane-sheardeformation and transverse-shear-deformation of the stiffeners can be neglected in equations (25)-(28) by setting $\boldsymbol{\tau}_{\mathrm{Y}}^{\mathrm{s}}=0$ and $\boldsymbol{\tau}_{\mathrm{Z}}^{\mathrm{s}}=0$, respectively.

Expressions like those given by equations (25) and (27) have been given by Heki and Saka ${ }^{50,56}$ for homogeneous isotropic stiffeners with negligible inplane-shear stiffnesses and appear to be in agreement for the most part. Some discrepancies exist for the term associated with the twisting stiffness. However, the expressions for the stiffnesses associated with membrane anisotropy, equations (25c) and (25e), are in complete agreement with those of Heki and Saka. Expressions
like those given by equations (25) and (27) have also been given by Slinchenko and Verijenko ${ }^{129}$ for homogeneous isotropic stiffeners with negligible inplane-shear and torsional stiffnesses and are in complete agreement. Furthermore, expressions like those given by equations (25)-(27) have been given by Won ${ }^{106}$ for homogeneous isotropic beam members with rectangular cross-sections of equal depth and negligible transverse-shear stiffnesses. The expressions given by Won are for a pair of oblique stiffener families and include higher-order effects associated with the interaction of the plate wall with the stiffeners at the stiffener intersections, which are neglected in a firstapproximation analysis. When these higher-order effects are neglected, and only a single stiffener family considered, the expressions given by Won are in complete agreement with the corresponding expressions given herein. Pshenichnov ${ }^{112}$ and Sumec ${ }^{107}$ have also presented expressions like those given by equations (25) and (27) for homogeneous isotropic members with negligible transverse-shear stiffnesses and are in complete agreement.

## Analysis Applications

The equivalent-plate stiffnesses given by equations (25)-(28) represent the homogenization of a single family of unidirectional, equally spaced, identical stiffeners that are oriented at an angle $\Psi_{\mathrm{s}}$ with respect to the plate x -axis, as shown in figure 6. Inspection of the analysis reveals that the analysis is easily extend to plates stiffened with multiple families of stiffeners by simply adding the stiffness contributions of each family. Several examples of applying the analysis are presented subsequently for plates with the stiffener arrangements depicted in figures 14-18. In these figures, stiffeners aligned with the global plate x - and y -axes are referred to as stringers and ribs, respectively. Other stiffeners are referred to as diagonal braces or, simply, as diagonals. All stiffeners are eccentric with respect to the plate midplane, unless stated otherwise. The notation used for the material and section properties and orientation angle of each stiffener family in these examples is given in Tables 1-3. In these tables, the stiffener extensional modulus, shear modulus, eccentricities, moment of inertia, torsion constant, and transverse-shear correction factors refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam. Furthermore, quantities associated with the stringers, ribs, and diagonals are identified by the lower case subscripts or superscripts " s, " " r ," and " d ," respectively. Wherever two families of diagonals are involved, the quantities associated with the two families are identified by the subscripts or superscripts "d1," and "d2."

Orthogrid plate with doubly braced bays. Consider a laminated-composite plate that is eccentrically stiffened with the arrangement of stringers, ribs, and braces shown in figure 14a. The pockets, or bays, formed by the skin, stringers, and ribs are diagonally braced with two nonidentical families of stiffeners. The spacings of the ribs and stringers are denoted by $\mathrm{L}_{\mathrm{x}}$ and $\mathrm{L}_{y}$, respectively. The stiffness expressions are obtained from equations (23) and (25)-(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Table 1. The resulting equivalent-plate stiffnesses are given in Appendix B. For this general stiffener arrangement, the stiffnesses in Appendix $B$ include a broad range of anisotropies characterized by the $\mathrm{A}_{16}, \mathrm{~A}_{26}, \mathrm{~A}_{45}, \mathrm{D}_{16}, \mathrm{D}_{26}, \mathrm{~B}_{11}, \mathrm{~B}_{12}, \mathrm{~B}_{16}, \mathrm{~B}_{22}, \mathrm{~B}_{26}$, and $\mathrm{B}_{66}$ equivalent-plate constitutive terms appearing in equations (22). It is worth noting that by neglecting the contributions of the ribs in the stiffness expressions given in Appendix B, the resulting expressions will then correspond to the diamondshaped stiffener pattern shown in figure 15.

Several corresponding results have been published for stiffened plates and plate-like lattices with homogeneous, isotropic stiffeners. In particular, the stiffnesses given in Appendix B reduce to those given by Karmakar ${ }^{88}$ and by Gerhard et. al. ${ }^{118}$ (see pp. 57-75) for the special case of identical braces and members with negligible transverse-shear and torsional stiffnesses. Similarly, for the special case of no braces (orthogrids) and members with negligible transverse shear stiffnesses, the stiffnesses given in Appendix B reduce to those given by Block, Card, and Mikulas. ${ }^{38}$ Likewise, the membrane stiffnesses given in Appendix B can be obtained from the Heki-Saka ${ }^{50,56}$ equations that are similar to those given by equations (25), for the special case in which the stiffeners have negligible transverse-shear stiffnesses in the plane parallel to the plate. Expressions have also been given by Chen and Tsai ${ }^{119}$ that include orthogrids and grids with only diagonal braces as special cases. The equivalent membrane and out-of-plane bending and transverse-shearing stiffnesses given by Chen and Tsai are in complete agreement with the corresponding results given in Appendix B. However, inplane transverse-shearing stiffnesses are presented by Chen and Tsai that disagree with the corresponding stiffnesses given in Appendix B. This disagreement appears to be associated with the fact that the stiffnesses given by Chen and Tsai are derived by using a method that accounts for combined bending and shearing of the stiffeners in the plane parallel to the plate. This combined stiffener bending-shearing action is not included in the first-approximation analysis presented herein. Similarly, equivalent-plate stiffnesses are given in reference 81 for rectangular orthogrids with two identical diagonal braces per bay and homogeneous, isotropic stiffeners. The corresponding stiffnesses presented herein for this special case are only in agreement if the terms associated with shear deformation and torsion of the stiffeners are neglected. At least part of the discrepancies, particularly that associated with inplane shear deformation of the stiffeners, appears to be associated with the $1 / 2$ appearing in equations (11e) and (14a) being neglected in reference 81. It is important to point out that neglecting the $1 / 2$ appearing in equations (11e) and (14a) results in a lack of the symmetry in equations (15a) and (15b).

Bunakov and Protasov ${ }^{105}$ presented equivalent-continuum stiffnesses for the stiffener arrangement shown in figure 14a, but without stringers and ribs and with identical diagonals with a rectangular cross-section. These stiffnesses are based on a micropolar continuum model of deformation and include transverse-shear and bending stiffnesses of the beam members associated with deformations in a plane parallel to the plate midplane. When the inplane bending stiffnesses of the stiffeners and the micro-rotation normal to the plate midplane are neglected, the stiffnesses given in reference 105, which include inplane and out-of-plane transverse-shear stiffnesses of the beam members, are in complete agreement with the stiffnesses given in Appendix B . It is important to point out that the expressions for the stiffnesses $\mathrm{A}_{66}$ and $\mathrm{D}_{66}$ were obtained from the micropolar theory by noting that both of the asymmetric inplane shearing strain measures and the asymmetric twisting strain measures used in reference 105 reduce to one half the inplane shearing strain and one half the twisting strain, respectively, when the micro-rotations normal to the plate midplane are neglected. The stiffnesses $\mathrm{A}_{66}$ and $\mathrm{D}_{66}$ were then obtained by relating the average of the asymmetric stress resultants to the corresponding strain.

Orthogrid plate with singly braced bays. Equations (23) and (25)-(28) were also applied to a laminated-composite plate that is stiffened with eccentric stringers, ribs, and nonidentical diagonal braces, as shown in figure 16a. For this case, alternating bays, enclosed by stringers and ribs, are braced with a single diagonal stiffener, and the spacing of the ribs and stringers is denoted
by $\mathrm{L}_{\mathrm{x}}$ and $\mathrm{L}_{\mathrm{y}}$, respectively. The stiffness expressions are obtained from equations (23) and (25)(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Table 2. The resulting equivalent-plate stiffnesses are also given in Appendix B. For the special case of homogeneous, isotropic stiffeners, identical braces, and members with negligible inplane transverse-shear stiffnesses, the stiffnesses given in Appendix B reduce to those given by Reddy et. al. ${ }^{95}$ and by Chen and Tsai. ${ }^{119}$ However, the out-of-plane transverse-shear stiffnesses of Reddy et. al. do not agree with those in Appendix B or with those given by Chen and Tsai, and appear to be in error. Likewise, for the special case of square bays with identical braces and members with negligible inplane and out-of-plane transverse-shear and inplane bending stiffnesses, the stiffnesses given in Appendix B reduce to those given by Hefzy \& Nayfeh. ${ }^{90,99}$

Isosceles-triangle stiffener pattern. The analysis of this section was also applied to a plate stiffened with an eccentric grid that has pockets that are isosceles triangles, as shown in figure 17a. The notation used for the material and section properties and orientation angle of each stiffener family is given in Table 3, and the horizontal spacing of the triangles and the spacing of the stringers are denoted by $\mathrm{L}_{\mathrm{x}}$ and $\mathrm{L}_{\mathrm{y}}$, respectively. For this stiffening grid, the two families of diagonal beams are nonidentical and the stiffeners intersect at the vertices of the triangular pockets. The resulting equivalent-plate stiffnesses obtained by applying equations (23) and (25)(28) are given in Appendix C. Expressions are also given in Appendix C for the special case of pockets that are equilateral triangles and members with identical properties. This particular stiffener configuration is often referred to as an isogrid because of the isotropic nature of its equivalent-plate inplane and bending stiffnesses. Similarly, equivalent-plate stiffnesses are given in reference 81 for this special case with homogeneous, isotropic stiffeners that are in complete agreement with those presented herein, except for the stiffness contributions associated with inplane shear deformation and the twisting stiffness $\mathrm{D}_{66}$. The discrepancy also appears to be associated with the $1 / 2$ appearing in equations (11e) and (14a) being neglected in reference 81. The stiffnesses for this special case with homogeneous, isotropic stiffeners that have negligible transverse-shear stiffnesses are in complete agreement with the corresponding stiffnesses given by Hefzy \& Nayfeh. ${ }^{99}$

Kagome stiffener pattern. Equations (23) and (25)-(28) were also applied to a plate stiffened with a similar eccentric stiffening grid presented by Wodesenbet et.al. ${ }^{133}$ and shown in figure 18a. This type of stiffening configuration is sometimes referred to as a Kagome pattern. ${ }^{140,141}$ The notation used for the material and section properties and orientation angle of each stiffener family is the same as that given in Table 3. For this stiffener arrangement, the two families of diagonal beams are nonidentical and the horizontal stiffeners do not intersect the diagonal stiffeners at the triangle vertices. The resulting equivalent-plate stiffnesses are identical to those given in Appendix C for the isosceles-triangle stiffener pattern. For the special case in which the beam members are made of a homogeneous, isotropic material, have rectangular cross-sections, and negligible inplane transverse-shear and torsional stiffnesses, the stiffnesses given in Appendix C reduce to those given by Vasiliev et. al. ${ }^{131}$ In addition, for the case in which all stiffeners have the same properties and all stiffeners have negligible transverse-shear, bending, and torsional stiffnesses, the stiffnesses given in Appendix C reduce to those given by Heki ${ }^{50}$ and by Wodesenbet et.al. ${ }^{133}$ Moreover, the stiffnesses given in Appendix C reduce to those given by Wang et. al. ${ }^{138}$ for the special case of negligible transverse-shear and torsional stiffnesses.

## Basic-Cell Energy-Equivalence Method

In this method, a basic repeating cell of the stiffened plate, such as the cell shown in figure 14b, is identified. The criterion for selecting the basic cell used herein is that it be a simple unit that will generate a stiffened structure of a given species by translation over the plate midplane, without any overlapping. Each basic cell contains a finite number of stiffener members. Consider a single, arbitrary beam stiffener. Applying the kinematical equivalence described by equations (11), the beam strains are expressed in terms of the equivalent-plate strains, in the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates shown in figure 6, by

$$
\begin{equation*}
\left\{\varepsilon_{b}\right\}=[\mathrm{E}]\left\{\varepsilon_{P}\right\} \tag{30a}
\end{equation*}
$$

where

$$
\begin{align*}
& \left\{\varepsilon_{b}\right\}^{\mathbf{T}}=\left\{\begin{array}{llllll}
e_{\mathrm{XX}}^{\mathrm{o}} & \Gamma_{\mathrm{XY}}^{\circ} & \Gamma_{\mathrm{XZ}}^{\circ} & \chi_{\mathrm{Z}}^{\circ} & \chi_{\mathrm{Y}}^{\circ} & \tau^{\circ}
\end{array}\right\}  \tag{30b}\\
& \left\{\varepsilon_{P}\right\}^{\mathbf{T}}=\left\{\varepsilon_{\mathrm{XX}}^{\mathrm{o}} \varepsilon_{\mathrm{YY}}^{\mathrm{o}} \gamma_{\mathrm{XY}}^{\mathrm{o}} \kappa_{\mathrm{XX}}^{\mathrm{o}} \kappa_{\mathrm{YY}}^{\mathrm{o}} \kappa_{\mathrm{XY}}^{\mathrm{o}} \gamma_{\mathrm{YZ}}^{\mathrm{o}} \gamma_{\mathrm{XZ}}^{\mathrm{o}}\right\} \tag{30c}
\end{align*}
$$

and

$$
[\mathbf{E}]=\left[\begin{array}{ccc:ccc:cc}
1 & 0 & 0 & 0 & 0 & 0 & 0 & 0  \tag{30~d}\\
0 & 0 & \frac{1}{2} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & -\frac{1}{2} & 0 & 0
\end{array}\right]
$$

In these equations, the uppercase subscript, $P$, denotes reference to the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates. The matrix defined by equation (30d) is referred to herein as the strain-equivalence matrix. By using these equations, the strain energy of the beam, given by (A25) and (A26), is expressed as

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\frac{1}{2} \int_{\mathrm{L}_{\mathrm{s}}}\left\{\varepsilon_{P}\right\}^{\mathrm{T}}\left[\mathcal{C}_{P}\right]\left\{\varepsilon_{P}\right\}^{\mathrm{dX}} \tag{31}
\end{equation*}
$$

with

$$
\begin{equation*}
\left[\mathcal{C}_{P}\right]=[\mathrm{E}]^{\mathrm{T}}[\mathcal{C}][\mathrm{E}] \tag{32}
\end{equation*}
$$

and where $L_{s}$ is the beam-member length. Performing the matrix multiplication gives

$$
\left[\mathcal{U}_{P}\right]=\left[\begin{array}{ccc:ccc:cc}
\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} & 0 & 0 & \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\mathrm{z}}_{\mathrm{S}} & 0 & 0 & 0 & 0  \tag{33}\\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & \frac{1}{4} \mathrm{k}_{\mathrm{Y}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} & 0 & 0 & \frac{1}{4} \mathrm{k}_{\mathrm{Y}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{z}}_{\mathrm{S}} & 0 & 0 \\
\hdashline \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\mathrm{z}}_{\mathrm{S}} & 0 & 0 & \mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{S}} & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & \frac{1}{4} \mathrm{k}_{\mathrm{Y}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{z}}_{\mathrm{S}} & 0 & 0 & \frac{1}{4} \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} & 0 & -\frac{1}{2} \mathrm{k}_{\mathrm{Z}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{y}}_{\mathrm{S}} \\
\hdashline 0 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & -\frac{1}{2} \mathrm{k}_{\mathrm{Z}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\bar{y}}_{\mathrm{S}} & 0 & \mathrm{k}_{\mathrm{Z}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}
\end{array}\right]
$$

The elements of this matrix are based on the notation used in Appendix A for the effective engineering constants of a nonhomogeneous, specially orthotropic beam. In particular, the nonhomogeneous beam stiffener is assigned an effective axial modulus $\mathrm{E}_{\mathrm{s}}$, an effective shear modulus $\mathrm{G}_{\mathrm{s}}$, cross-sectional area $\mathrm{A}_{\mathrm{s}}$, effective moments of inertia $\mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}$ and $\mathrm{I}_{\mathrm{ZZ}}^{\mathrm{s}}$, effective product of inertia $\mathrm{I}_{\mathrm{YZ}}^{\mathrm{S}}$, and effective torsional constant $\mathrm{J}_{\mathrm{S}}$, in addition to the effective eccentricities $\overline{\mathrm{y}}_{\mathrm{S}}, \overline{\mathrm{z}}_{\mathrm{S}}$, $\overline{\bar{y}}_{\mathrm{s}}$ and $\overline{\bar{z}}_{\mathrm{s}}$. Effective shear correction factors for the beam are denoted by $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ and $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$.

Next, the plate strains in the (X, Y, Z) beam coordinates are defined in terms of the global plate $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates shown in figure 6 as follows

$$
\left\{\boldsymbol{\varepsilon}_{P}\right\}=\left[\begin{array}{c:c:c}
{\left[\begin{array}{ll}
\boldsymbol{T}_{\varepsilon}
\end{array}\right]} & {\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right]}  \tag{34a}\\
\hdashline\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right] & {\left[\boldsymbol{T}_{\varepsilon}\right.}
\end{array}\right]\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right] .\left[\boldsymbol{\varepsilon}_{p}\right\}
$$

with

$$
\begin{equation*}
\left\{\boldsymbol{\varepsilon}_{p}\right\}^{\mathbf{T}}=\left\{\boldsymbol{\varepsilon}_{\mathrm{xx}}^{\mathrm{o}} \boldsymbol{\varepsilon}_{\mathrm{yy}}^{\mathrm{o}} \boldsymbol{\gamma}_{\mathrm{xy}}^{\mathrm{o}} \boldsymbol{\kappa}_{\mathrm{xx}}^{\mathrm{o}} \boldsymbol{\kappa}_{\mathrm{yy}}^{\mathrm{o}} \boldsymbol{\kappa}_{\mathrm{xy}}^{\mathrm{o}} \gamma_{\mathrm{yz}}^{\mathrm{o}} \gamma_{\mathrm{xz}}^{\mathrm{o}}\right\} \tag{34b}
\end{equation*}
$$

and where the lowercase subscript, $p$, denotes reference to the $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates of the plate. The transformation sub-matrices appearing in equation (34a) are defined by equations (17). In addition,

$$
\left\{\boldsymbol{\varepsilon}_{P}\right\}^{\mathbf{T}}=\left\{\boldsymbol{\varepsilon}_{p}\right\}^{\mathbf{T}}\left[\begin{array}{c:c:c}
{\left[\begin{array}{l}
\mathbf{T}_{\varepsilon}
\end{array}\right]^{\mathbf{T}}} & {\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right]}  \tag{34c}\\
\left.\hdashline \begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right] & {\left[\mathbf{T}_{\varepsilon}\right]^{\mathbf{T}}} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right]} \\
\hdashline\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right] & {\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]} & {\left[\mathbf{T}_{\boldsymbol{\tau}}\right]^{\mathbf{T}}}
\end{array}\right]
$$

The beam strain energy defined by equation (31) is expressed in terms of the global plate coordinate system by

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\frac{1}{2} \int_{\mathrm{L}_{\mathrm{s}}}\left\{\varepsilon_{p}\right\}^{\mathrm{T}}\left[\mathcal{C}_{p}\right]\left\{\varepsilon_{p}\right\} \mathrm{dX} \tag{35}
\end{equation*}
$$

where $\mathrm{dX}=\mathrm{dX}(\mathrm{x}, \mathrm{y})$ and

$$
\left.\left.\left.\left[\begin{array}{c:c:c}
\boldsymbol{\mathcal { C }}_{p}
\end{array}\right]=\left[\begin{array}{l:l:l:l}
{\left[\begin{array}{ll}
\boldsymbol{T}_{\varepsilon}
\end{array}\right]^{\mathbf{T}}} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0 \\
0
\end{array}\right]} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right]}  \tag{36}\\
\hdashline\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right] & \left.\boldsymbol{T}_{\varepsilon}\right]^{\mathbf{T}} & {\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right]} \\
\hdashline\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right] & {\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]} & {\left[\boldsymbol{T}_{\tau}\right]^{\mathbf{T}}}
\end{array}\right]\left[\begin{array}{l}
\boldsymbol{T}_{\varepsilon} \\
{\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]}
\end{array}\right]\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right] ~\left[\begin{array}{lll}
0 & 0 & 0 \\
0 & 0 & 0 \\
0 & 0 & 0
\end{array}\right]\left[\begin{array}{l}
\boldsymbol{T}_{\varepsilon}
\end{array}\right]\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0 & 0
\end{array}\right] .\left[\begin{array}{ll}
0 & 0 \\
0 & 0
\end{array}\right]:\left[\begin{array}{ll}
0 & 0 \\
0 & 0 \\
0
\end{array}\right]: \boldsymbol{T}_{\tau}\right]\right] c\right]
$$

The explicit expressions for the elements of this matrix are given in Appendix D.
The basic presumption of this energy-based homogenization method is that the basic repetitive cell is small enough, compared to the overall structural dimensions, so that the strain-energy density of every beam member within it can be represented adequately by constant value. Based upon this discretization concept, the integrand of equation (35) is a constant and, as a result, the beam-member strain energy is given by

$$
\begin{equation*}
\boldsymbol{\varepsilon}_{\varepsilon}=\frac{\mathrm{L}_{\mathrm{S}}}{2}\left\{\boldsymbol{\varepsilon}_{p}\right\}^{\mathrm{T}}\left[\mathcal{C}_{p}\right]\left\{\boldsymbol{\varepsilon}_{p}\right\} \tag{37}
\end{equation*}
$$

The beam-member strain energy is now completely characterized by the plate strains and beam properties. The dependence on the strains is expressed functionally by

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\varepsilon_{\varepsilon}\left(\varepsilon_{x x}^{\circ}, \varepsilon_{y y}^{\circ}, \gamma_{x y}^{\circ}, \kappa_{x x}^{\circ}, \kappa_{y y}^{\circ}, \kappa_{x y}^{\circ}, \gamma_{x z}^{\circ}, \gamma_{y z}^{\circ}\right) \tag{38}
\end{equation*}
$$

The "average" two-dimensional strain-energy density $\hat{\mathcal{E}}_{\varepsilon}$ for the basic equivalent-plate cell, with area $\mathrm{A}_{\text {cell }}$, is given by

$$
\begin{equation*}
\hat{\varepsilon}_{\varepsilon}=\hat{\varepsilon}_{\varepsilon}^{\text {plate }}+\frac{1}{\mathrm{~A}_{\text {cell }}} \sum^{\text {members }} \varepsilon_{\varepsilon}=\hat{\varepsilon}_{\varepsilon}\left(\varepsilon_{x x}^{\circ}, \varepsilon_{y y}^{\circ}, \gamma_{x y}^{\circ}, \kappa_{x x}^{\circ}, \kappa_{y y}^{\circ}, \kappa_{x y}^{\circ}, \gamma_{x z}^{\circ}, \gamma_{y z}^{\circ}\right) \tag{39a}
\end{equation*}
$$

where

$$
\begin{align*}
2 \hat{\varepsilon}_{\varepsilon}^{\text {plate }}= & \mathcal{U}_{x x}^{\text {plate }} \varepsilon_{x x}^{\circ}+\mathcal{U}_{y y}^{\text {plate }} \varepsilon_{y y}^{\circ}+\mathcal{U}_{x y}^{\text {plate }} \gamma_{x y}^{\circ} \\
& \quad+M_{x x}^{\text {plate }} \kappa_{x x}^{\circ}+M_{y y}^{\text {plate }} \kappa_{y y}^{\circ}+M_{x y}^{\text {plate }} \kappa_{x y}^{\circ}+Q_{x z}^{\text {plate }} \gamma_{x z}^{\circ}+Q_{y z}^{\text {plate }} \gamma_{y z}^{\circ} \tag{39b}
\end{align*}
$$

This expression represents an equivalent pointwise function for the contribution of all beam members within the basic, repetitive cell to the equivalent-plate strain energy density, plus the contribution of the plate wall. The strain energy density in this expression is given in terms of all stiffener properties, stiffener orientations, and wall properties, in addition to the global plate strains. The next step in this method is to relate equation (39a) to the general form for an anisotropic plate, based on the first-order transverse-shear deformation theory presented herein. In particular, the strain-energy density of an anisotropic plate is given by

$$
\begin{equation*}
2 \hat{\varepsilon}_{\varepsilon}=\mathcal{M}_{\mathrm{xx}} \varepsilon_{\mathrm{xx}}^{\circ}+\mathcal{M}_{\mathrm{yy}} \varepsilon_{\mathrm{yy}}^{\circ}+\mathcal{M}_{\mathrm{xy}} \gamma_{\mathrm{xy}}^{\circ}+M_{\mathrm{xx}} \kappa_{\mathrm{xx}}^{\circ}+M_{\mathrm{yy}} \kappa_{\mathrm{yy}}^{\circ}+M_{\mathrm{xy}} \kappa_{\mathrm{xy}}^{\circ}+\mathrm{Q}_{\mathrm{xz}} \gamma_{\mathrm{xz}}^{\circ}+\mathrm{Q}_{\mathrm{yz}} \gamma_{\mathrm{yz}}^{\circ} \tag{40}
\end{equation*}
$$

By using the anisotropic-plate constitutive equations

$$
\left\{\begin{array}{l}
\boldsymbol{n}_{\mathrm{xx}}  \tag{41a}\\
\boldsymbol{n}_{\mathrm{yy}} \\
\boldsymbol{n}_{\mathrm{xy}} \\
\hline \boldsymbol{m}_{\mathrm{xx}} \\
\boldsymbol{m}_{\mathrm{yy}} \\
\boldsymbol{m}_{\mathrm{xy}}
\end{array}\right\}=\left[\begin{array}{lll|lll}
\mathrm{A}_{11} & \mathrm{~A}_{12} & \mathrm{~A}_{16} & \mathrm{~B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} \\
\mathrm{~A}_{12} & \mathrm{~A}_{22} & \mathrm{~A}_{26} & \mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} \\
\mathrm{~A}_{16} & \mathrm{~A}_{26} & \mathrm{~A}_{66} & \mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66} \\
\hline \mathrm{~B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} & \mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} & \mathrm{D}_{12} & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66} & \mathrm{D}_{16} & \mathrm{D}_{26} & \mathrm{D}_{66}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{\mathrm{xx}}^{\mathrm{o}} \\
\varepsilon_{\mathrm{yy}}^{\mathrm{o}} \\
\gamma_{\mathrm{xy}}^{\mathrm{o}} \\
\hline \kappa_{\mathrm{xx}}^{\mathrm{o}} \\
\kappa_{\mathrm{yy}}^{\mathrm{o}} \\
\kappa_{\mathrm{xy}}^{\mathrm{o}}
\end{array}\right\}
$$

and

$$
\left\{\begin{array}{l}
\mathrm{Q}_{\mathrm{yz}}  \tag{41b}\\
\mathrm{Q}_{\mathrm{xz}}
\end{array}\right\}=\left[\begin{array}{ll}
\mathrm{A}_{44} & \mathrm{~A}_{45} \\
\mathrm{~A}_{45} & \mathrm{~A}_{55}
\end{array}\right]\left\{\begin{array}{l}
\gamma_{\mathrm{yz}}^{\circ} \\
\gamma_{\mathrm{xz}}^{\circ}
\end{array}\right\}
$$

the strain energy density given by equation (40) becomes a quadratic function of the plate strains. Therefore, it follows that the symmetric constitutive matrices are given by

$$
\left[\begin{array}{ccc}
\mathrm{A}_{11} & \mathrm{~A}_{12} & \mathrm{~A}_{16}  \tag{42a}\\
\bullet & \mathrm{~A}_{22} & \mathrm{~A}_{26} \\
\text { symmetric } & \bullet & \mathrm{A}_{66}
\end{array}\right]=\left[\begin{array}{ccc}
\frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\circ} \partial \varepsilon_{\mathrm{xx}}^{\circ}} & \frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\circ} \partial \varepsilon_{\mathrm{yy}}^{\circ}} & \frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\circ} \partial \gamma_{\mathrm{xy}}^{\circ}} \\
\bullet & \frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\circ} \partial \varepsilon_{\mathrm{yy}}^{\circ}} & \frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\circ} \partial \gamma_{\mathrm{xy}}^{\circ}} \\
\text { symmetric } & \bullet & \frac{\partial^{2} \hat{\mathcal{E}}_{\varepsilon}}{\partial \gamma_{\mathrm{xy}}^{\circ} \partial \gamma_{\mathrm{xy}}^{\circ}}
\end{array}\right]
$$

$$
\begin{gather*}
{\left[\begin{array}{ccc}
\mathrm{B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} \\
\bullet & \mathrm{~B}_{22} & \mathrm{~B}_{26} \\
\text { symmetric } & \bullet & \mathrm{B}_{66}
\end{array}\right]=\left[\begin{array}{ccc}
\frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xx}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}} \\
\bullet & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}} \\
\text { symmetric } & \bullet & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \gamma_{\mathrm{xy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}}
\end{array}\right]}  \tag{42b}\\
{\left[\begin{array}{ccc}
\mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\bullet & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\text { symmetric } & \bullet & \mathrm{D}_{66}
\end{array}\right]=\left[\begin{array}{ccc}
\frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xx}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}} \\
\bullet & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}} \\
\text { symmetric } & \bullet & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \kappa_{\mathrm{xy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}}
\end{array}\right]}  \tag{42c}\\
{\left[\begin{array}{cc}
\mathrm{A}_{44} & \mathrm{~A}_{45} \\
\text { symmetric } & \mathrm{A}_{55}
\end{array}\right]=\left[\begin{array}{cc}
\frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \gamma_{\mathrm{yz}}^{\mathrm{o}} \partial \gamma_{\mathrm{yz}}^{\mathrm{o}}} & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \gamma_{\mathrm{yz}}^{\mathrm{o}} \partial \gamma_{\mathrm{xz}}^{\mathrm{o}}} \\
\text { symmetric } & \frac{\partial^{2} \hat{\boldsymbol{\varepsilon}}_{\varepsilon}}{\partial \gamma_{\mathrm{xz}}^{\mathrm{o}} \partial \gamma_{\mathrm{xz}}^{\mathrm{o}}}
\end{array}\right]} \tag{42d}
\end{gather*}
$$

Inspection of equation (39) indicates that the contributions of the stiffeners in the basic cell to the constitutive equations are given by

$$
\begin{align*}
{\left[\begin{array}{ccc}
\mathrm{A}_{11}^{\text {stiffener }} & \mathrm{A}_{12}^{\text {stiffener }} & \mathrm{A}_{16}^{\text {stiffener }} \\
\bullet & \mathrm{A}_{22}^{\text {stiffener }} & \mathrm{A}_{26}^{\text {stiffener }} \\
\text { symmetric } & \bullet & \mathrm{A}_{66}^{\text {stiffener }}
\end{array}\right] } & =\frac{1}{\mathrm{~A}_{\text {cell }}} \sum\left[\begin{array}{ccc}
\frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}}} & \frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \gamma_{\mathrm{xy}}^{\mathrm{o}}} \\
\bullet & \frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \gamma_{\mathrm{xy}}^{\mathrm{o}}} \\
\text { symmetric } & \bullet & \frac{\partial^{2} \boldsymbol{\varepsilon}_{\varepsilon}}{\partial \gamma_{\mathrm{xy}}^{\mathrm{o}} \partial \gamma_{\mathrm{xy}}^{\mathrm{o}}}
\end{array}\right]  \tag{43a}\\
& =\frac{1}{\mathrm{~A}_{\text {cell }}} \sum^{\text {members }}\left[\begin{array}{ccc}
\mathcal{C}_{11}^{p} & \mathcal{C}_{12}^{p} & \mathcal{C}_{13}^{p} \\
\bullet & \mathcal{C}_{22}^{p} & \mathcal{C}_{23}^{p} \\
\text { symmetric } & \bullet & \mathcal{C}_{33}^{p}
\end{array}\right]
\end{align*}
$$

$$
\begin{align*}
& {\left[\begin{array}{ccc}
\mathrm{B}_{11}^{\text {stiffener }} & \mathrm{B}_{12}^{\text {stiffener }} & \mathrm{B}_{16}^{\text {stiffener }} \\
\bullet & \mathrm{B}_{22}^{\text {stiffener }} & \mathrm{B}_{26}^{\text {stiffener }} \\
\text { symmetric } & \bullet & \mathrm{B}_{66}^{\text {stiffener }}
\end{array}\right]=\frac{1}{\mathrm{~A}_{\text {cell }}} \sum^{\frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xx}}^{\mathrm{o}}}} \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \varepsilon_{\mathrm{xx}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}}\left[\begin{array}{ccc}
\bullet & \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{yy}}^{\mathrm{o}}} & \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \varepsilon_{\mathrm{yy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}} \\
\text { symmetric } & \bullet & \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \gamma_{\mathrm{xy}}^{\mathrm{o}} \partial \kappa_{\mathrm{xy}}^{\mathrm{o}}}
\end{array}\right]}  \tag{43b}\\
& =\frac{1}{\mathrm{~A}_{\text {cell }}} \sum^{\text {members }} \mathrm{L}_{\mathrm{S}}\left[\begin{array}{ccc}
\mathcal{C}_{14}^{p} & \mathcal{C}_{15}^{p} & \mathcal{C}_{16}^{p} \\
\bullet & \mathcal{C}_{25}^{p} & \mathcal{C}_{26}^{p} \\
\text { symmetric } & \bullet & \mathcal{C}_{36}^{p}
\end{array}\right]
\end{align*}
$$

$$
\begin{align*}
& {\left[\begin{array}{ll}
\mathrm{A}_{44}^{\text {stiffener }} & \mathrm{A}_{45}^{\text {stiffener }} \\
\text { symmetric } & \mathrm{A}_{55}^{\text {stiffener }}
\end{array}\right]=\frac{1}{\mathrm{~A}_{\text {cell }}} \sum\left[\begin{array}{cc}
\frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \gamma_{\mathrm{yz}}^{\mathrm{o}} \partial \gamma_{\mathrm{yz}}^{\mathrm{o}}} & \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \gamma_{\mathrm{yz}}^{\mathrm{o}} \partial \gamma_{\mathrm{xz}}^{\mathrm{o}}} \\
\text { symmetric } & \frac{\partial^{2} \mathcal{E}_{\varepsilon}}{\partial \gamma_{\mathrm{xz}}^{\mathrm{o}} \partial \gamma_{\mathrm{xz}}^{\mathrm{o}}}
\end{array}\right]=\frac{1}{\mathrm{~A}_{\text {cell }}} \sum_{\mathrm{s}}^{\text {members }}\left[\begin{array}{cc}
\mathcal{e}_{77}^{p} & \mathcal{e}_{78}^{p} \\
\text { symmetric } & \mathcal{e}_{88}^{p}
\end{array}\right]} \tag{43d}
\end{align*}
$$

Using equations (43), the constitutive equations for the equivalent plate are given by equations (22) and (23).

## Analysis Application

Several examples of applying the basic-cell energy-equivalence method are presented subsequently for plates with the stiffener arrangements depicted in figures 14-24. In these figures, stiffeners aligned with the global plate x - and y -axes are referred to as stringers and ribs, respectively. Other stiffeners are referred to as diagonal braces or, simply, as diagonals. All stiffeners are eccentric with respect to the plate midplane, and each family of stiffeners has different properties unless stated otherwise. The notation used for the material and section
properties and orientation angle of each stiffener member of the basic cell used in these examples is given in Tables 4-9. In these tables, the member designation denotes numbers associated with the beginning and end of the members comprising a basic cell, as shown in figures 14b, 16b, 17b, 18b, 21b, and 23b. Also, the stiffener extensional modulus, shear modulus, eccentricity, moment of inertia, torsion constant, and transverse-shear correction factors, refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam. Quantities associated with the stringers, ribs, and diagonals are identified by the subscripts or superscripts "s," "r," and "d," respectively. Wherever two families of diagonals are involved, the quantities associated with the two families are identified by the subscripts or superscripts "d1," and "d2." For the examples presented subsequently, the Mathematica® computer program ${ }^{142}$ presented in Appendix E was used to obtain the equivalent-plate stiffnesses.

Orthogrid plate with doubly or singly braced bays. The basic-cell energy-equivalence method was applied to the orthogonally stiffened plates with diagonally braced bays shown in figures 14a and 16a. The basic cell for the stiffener grid in figure 14a is shown in figure 14b and consists of four beam members with the basic-cell beam-member attributes given in Table 4. The basic cell for the stiffener grid in figure 16a is shown in figure 16b and consists of six beam members with the basic-cell beam-member attributes given in Table 5. The ends of each beam member are indicated in figures 14 b and 16 b by the filled red circular symbols. For both stiffener grids, the rib and stringer spacings are denoted by $\mathrm{L}_{\mathrm{x}}$ and $\mathrm{L}_{\mathrm{y}}$, respectively, and the length of the diagonals is given by $L_{d}=\sqrt{L_{x}^{2}+L_{y}^{2}}$. The dashed rectangle shown in figures 14a and 14b indicates the perimeter of the basic repetitive cell and has the area $\mathrm{A}_{\text {cell }}=\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}$. Similarly, the shaded rectangle shown in figures 16a and 16b indicates the basic repetitive cell, with the area $\mathrm{A}_{\text {cell }}=4 \mathrm{~L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}$. Applying the analysis described in this section to these two basic cells yields the same equivalent plate stiffnesses given in Appendix B that were obtained by using the Direct Equilibrium-Compatibility Method presented herein.

Isosceles-triangle and Kagome stiffener patterns. The basic-cell energy-equivalence method was also applied to a plate stiffened with the stiffener arrangements shown in figures 17 and 18 . The basic cell for the grid in figure 17a is shown in figure 17b and consists of three stiffeners with the properties given in Table 6. Likewise, the basic cell for the Kagome grid in figure 18a is shown in figure 18b and consists of four beam members with the properties given in Table 7. The ends of each beam member are also indicated in figures 17b and 18b by the filled red circular symbols. For both stiffener grids, the horizontal spacing of the diagonals and the stringer spacing are denoted by $L_{x}$ and $L_{y}$, respectively. The dashed hexagon shown in figures 17a and 17b and the dashed rectangle shown in figures 18a and 18b indicates the perimeter of each basic repetitive cell and has the area $\mathrm{A}_{\text {cell }}=\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}$ and $2 \mathrm{~L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}$, respectively, and the length of the diagonals is given by $\mathrm{L}=\sqrt{\mathrm{L}_{\mathrm{x}}^{2}+\mathrm{L}_{\mathrm{y}}^{2}}$. The shaded region surrounding each cell perimeter indicates how the cell relates to the surrounding structure, for clarity. In addition, figures 19 and 20 indicate how the basic cells in figures 17b and 18b are translated to generate the stiffened-plate structure, respectively. Applying the analysis described in this section to the basic cells with the attributes given in Tables 6 and 7 also yields the same equivalent plate stiffnesses given in Appendix C that were obtained by using the Direct Equilibrium-Compatibility Method presented herein.

Hexagon-shaped stiffener pattern. Another stiffened plate considered in the present study is shown in figure 21, in which the plate wall is reinforced with a hexagonal grid of stiffeners from three families. The basic cell for this structure is shown in figure 21b and consists of five stiffeners with the basic-cell beam-member attributes given in Table 8. The ends of each member are indicated in the figure by the filled red circular symbols, and the length of the ribs is different from the length of the diagonals. The dashed hexagon shown in figures 21a and 21b indicates the perimeter of the basic repetitive cell and has the area $\mathrm{A}_{\text {cell }}=2 \mathrm{a}(\mathrm{b}+\mathrm{c})$. The shaded region surrounding the cell perimeter indicates how the cell relates to the surrounding structure. Figure 22 shows how the basic cell in figure 21b is translated to generate the stiffened-plate structure. Applying the analysis described in this section to the basic cell yields the equivalent plate stiffnesses given in Appendix F. Similar membrane stiffnesses have been given by Heki ${ }^{50}$ for a hexagonal stiffener arrangement in which all beam members forming a hexagon have the same length and are made of a homogeneous, isotropic material. The stiffnesses presented in Appendix F do not agree with those in reference 50. For the special case of homogeneous, isotropic members with the same length and identical properties and negligible inplane and out-of-plane transverse-shear stiffnesses, the stiffnesses given in Appendix F are in complete agreement with those given by Hefzy and Nayfeh. ${ }^{99}$ Similarly, equivalent-plate stiffnesses are given in reference 81 for the special case of a homogeneous, isotropic single-layer grid comprised of members with the same length and identical properties. The stiffnesses presented herein are in agreement with those in reference 81 for this special case, except for the stiffness contributions associated with inplane shear deformation. This discrepancy also appears to be associated with the 1/2 appearing in equations (11e) and (14a) being neglected in reference 81.

Star-shaped stiffener pattern. The analysis was also applied to a plate stiffened with the starshaped stiffener arrangement shown in figures 23. For this case, the star shapes are formed from two oppositely directed isosceles triangles with coincident centroids. The basic cell for this structure is shown in figure 23b and consists of twelve stiffeners from three families with the basic-cell beam-member attributes given in Table 9. The ends of each member are indicated in the figure by the filled red circular symbols. The dashed hexagon shown in figures 23a and 23b indicates the perimeter of the basic repetitive cell and has the area $A_{\text {cell }}=4 B H / 3$, where $B$ and $H$ are the base and height of either isosceles triangle forming the star shape. The shaded region surrounding the cell perimeter indicates how the cell relates to the surrounding structure. Figure 24 shows how the basic cell in figure 23b is translated to generate the stiffened-plate structure. Applying the analysis described in this section to the basic cell yields the equivalent plate stiffnesses given in Appendix G.

## Equivalent-Plate Stiffnesses for Sandwich Plates

Inspection of the analysis presented herein reveals that the stiffnesses given in Appendices B, $\mathrm{C}, \mathrm{F}$, and G can also be used to obtain the equivalent-plate stiffnesses for sandwich plates with two nonidentical anisotropic face plates, such as those shown in figures 25-27. This task is accomplished by using equations (23) based on two plate members, neither of which are located at $\mathrm{z}=0$. The stiffeners forming the core are presumed to be made of a homogeneous orthotropic or isotropic material. For convenience, the equivalent-plate reference plane is taken as the
midplane of the core layer formed by the stiffeners such that all core anisotropies associated with coupling between membrane and bending actions vanish. The contribution of the face plates to the equivalent-plate stiffnesses are obtained by applying the integral definitions of the plate stiffnesses, in accordance with figure 28. In particular, the stiffnesses of a face plate are given, with respect to the global plate $(\mathrm{x}, \mathrm{y}, \mathrm{z})$ coordinates shown in figure 28, by

$$
\left.\begin{array}{l}
{\left[\begin{array}{lll}
A_{11}^{\text {plate }} & A_{12}^{\text {plate }} & A_{16}^{\text {plate }} \\
A_{12}^{\text {plate }} & A_{22}^{\text {plate }} & A_{26}^{\text {plate }} \\
A_{16}^{\text {plate }} & A_{26}^{\text {plate }} & A_{66}^{\text {plate }}
\end{array}\right]=\int_{e-\frac{h}{2}}^{e+\frac{h}{2}}\left[\begin{array}{lll}
\bar{Q}_{11} & \bar{Q}_{12} & \bar{Q}_{16} \\
\bar{Q}_{12} & \bar{Q}_{22} & \bar{Q}_{26} \\
\bar{Q}_{16} \bar{Q}_{26} & \bar{Q}_{66}
\end{array}\right] d z} \\
{\left[\begin{array}{lll}
B_{11}^{\text {plate }} & B_{12}^{\text {plate }} & B_{16}^{\text {plate }} \\
B_{12}^{\text {plate }} & B_{22}^{\text {plate }} & B_{26}^{\text {plate }} \\
B_{16}^{\text {plate }} & B_{26}^{\text {plate }} & B_{66}^{\text {plate }}
\end{array}\right]=\int_{e-\frac{h}{2}}^{e+\frac{h}{2}}\left[\begin{array}{ll}
\bar{Q}_{11} & \bar{Q}_{12} \\
\bar{Q}_{12} & \bar{Q}_{22} \\
\bar{Q}_{16} & \bar{Q}_{26} \\
\bar{Q}_{26} & \bar{Q}_{66}
\end{array}\right] z d z} \\
{\left[\begin{array}{lll}
D_{11}^{\text {plate }} & D_{12}^{\text {plate }} & D_{16}^{\text {plate }} \\
D_{12}^{\text {plate }} & D_{22}^{\text {plate }} & D_{26}^{\text {plate }} \\
D_{16}^{\text {plate }} & D_{26}^{\text {plate }} & D_{66}^{\text {plate }}
\end{array}\right]=\int_{e-\frac{h}{2}}^{e+\frac{h}{2}}\left[\begin{array}{ll}
\bar{Q}_{11} & \bar{Q}_{12} \bar{Q}_{16} \\
\bar{Q}_{12} & \bar{Q}_{22} \\
\bar{Q}_{16} & \bar{Q}_{26} \\
\bar{Q}_{66}
\end{array}\right] z^{2} d z} \\
{\left[\begin{array}{l}
A_{44}^{\text {plate }} A_{45}^{\text {plate }} \\
A_{45}^{\text {plate }}
\end{array} A_{55}^{\text {plate }}\right.}
\end{array}\right]=K^{\text {plate }} \int_{e-\frac{h}{2}}^{e+\frac{h}{2}}\left[\begin{array}{l}
\bar{Q}_{44}  \tag{44d}\\
\bar{Q}_{45} \\
\bar{Q}_{45} \\
\bar{Q}_{55}
\end{array}\right] d z
$$

where $h$ is the face-plate thickness, $e$ is the face-plate eccentricity, $\bar{Q}_{i j}(z)$ are the transformed lamina stiffnesses of first-order shear-deformation laminated-plate theory (see reference 139), and $\mathrm{K}^{\text {plate }}$ is a transverse-shear correction factor. For the core, transverse-shear correction factors are used for the beam members. Next, the local ( $\mathrm{x}^{\prime}, \mathrm{y}^{\prime}, \mathrm{z}^{\prime}$ ) coordinates shown in figure 28 are used to obtain

$$
\begin{align*}
& {\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {plate }} & \mathrm{A}_{12}^{\text {plate }} & \mathrm{A}_{16}^{\text {plate }} \\
\mathrm{A}_{12}^{\text {plate }} & \mathrm{A}_{22}^{\text {plate }} & \mathrm{A}_{26}^{\text {plate }} \\
\mathrm{A}_{16}^{\text {plate }} & \mathrm{A}_{26}^{\text {plate }} & \mathrm{A}_{66}^{\text {plate }}
\end{array}\right]=\left[\begin{array}{lll}
\mathrm{A}_{11}^{, \text {plate }} & \mathrm{A}_{12}^{, \text {plate }} & \mathrm{A}_{16}^{, \text {plate }} \\
\mathrm{A}_{12}^{, \text {plate }} & \mathrm{A}_{22}^{, \text {plate }} & \mathrm{A}_{22}^{, \text {plate }} \\
\mathrm{A}_{12}^{, \text {plate }} & \mathrm{A}_{26}^{, \text {plate }} & \mathrm{A}_{166}^{, \text {plate }}
\end{array}\right]}  \tag{45a}\\
& {\left[\begin{array}{lll}
\mathbf{B}_{11}^{\text {plate }} & \mathbf{B}_{12}^{\text {plate }} & \mathbf{B}_{16}^{\text {plate }} \\
\mathbf{B}_{12}^{\text {plate }} & \mathbf{B}_{22}^{\text {plate }} & \mathbf{B}_{26}^{\text {plate }} \\
\mathbf{B}_{16}^{\text {plate }} & \mathbf{B}_{26}^{\text {plate }} & \mathbf{B}_{66}^{\text {plate }}
\end{array}\right]=\mathrm{e}\left[\begin{array}{lll}
\mathbf{A}_{11}^{\text {plate }} & \mathbf{A}_{12}^{\text {plate }} & \mathbf{A}_{16}^{\text {,plate }} \\
\mathbf{A}_{12}^{\text {plate }} & \mathbf{A}_{22}^{\text {plate }} & \mathbf{A}_{26}^{\text {plate }} \\
\mathbf{A}_{16}^{\text {plate }} & \mathbf{A}_{26}^{\text {plate }} & \mathbf{A}_{16}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{lll}
\mathbf{B}_{11}^{\prime \text { plate }} & \mathbf{B}_{12}^{\prime \text { plate }} & \mathbf{B}_{16}^{\prime \text { plate }} \\
\mathbf{B}_{12}^{\prime \text { plate }} & \mathbf{B}_{22}^{\prime \text { plate }} & \mathbf{B}_{26}^{\prime \text { plate }} \\
\mathbf{B}_{16}^{\prime \text { plate }} & \mathbf{B}_{26}^{\prime \text { plate }} & \mathbf{B}_{166}^{\prime \text { plate }}
\end{array}\right]} \tag{45b}
\end{align*}
$$

$$
\begin{align*}
& {\left[\begin{array}{ll}
\mathrm{A}_{44}^{\text {plate }} & \mathrm{A}_{45}^{\text {plate }} \\
\mathrm{A}_{45}^{\text {plate }} & \mathrm{A}_{55}^{\text {plate }}
\end{array}\right]=\left[\begin{array}{ll}
\mathrm{A}_{44}^{\prime \text { plate }} & \mathrm{A}_{45}^{\prime \text { plate }} \\
\mathrm{A}_{45}^{\prime \text { plate }} & \mathrm{A}_{55}^{\prime \text { plate }}
\end{array}\right]} \tag{45d}
\end{align*}
$$

where $z=z^{\prime}+e$ and

$$
\begin{align*}
& \left.\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {,plate }} & \mathrm{A}_{12}^{\text {,plate }} & \mathrm{A}_{16}^{\text {,plate }} \\
\mathrm{A}_{12}^{\text {plate }} & \mathrm{A}_{22}^{\text {plate }} & \mathrm{A}_{26}^{\text {plate }} \\
\mathrm{A}_{16}^{\text {plate }} & \mathrm{A}_{26}^{\text {plate }} & \mathrm{A}_{16}^{\text {plate }}
\end{array}\right]=\int_{-\frac{\mathrm{h}}{2}}^{+}\left[\begin{array}{l}
\mathrm{h} \\
\mathrm{~A}_{12}^{\text {plate }}
\end{array}\right]=\int_{\overline{\mathrm{Q}}_{11}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{12}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{16}\left(\mathrm{z}^{\prime}\right)}^{\overline{\mathrm{Q}}_{12}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{22}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{26}\left(\mathrm{z}^{\prime}\right)} \overline{\mathrm{Q}}_{16}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{26}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{66}\left(\mathrm{z}^{\prime}\right)\right] \mathrm{d} \mathrm{z}^{\prime}  \tag{46a}\\
& {\left[\begin{array}{ll}
B_{11}^{\text {plate }} & B_{12}^{\text {plate }} \\
B_{16}^{\text {plate }} \\
B_{12}^{\text {plate }} & B_{12}^{\text {plate }} \\
B_{26}^{\text {plate }} & B_{26}^{\text {plate }} \\
B_{12}^{\text {plate }} & B_{26}^{\text {plate }} \\
B_{16}^{\text {plate }}
\end{array}\right]=\int_{-\frac{h}{2}}^{+}\left[\begin{array}{l}
\text { plate } \\
B_{16}
\end{array}\right]\left[\begin{array}{l}
\bar{Q}_{11}\left(z^{\prime}\right) \bar{Q}_{12}\left(z^{\prime}\right) \bar{Q}_{16}\left(z^{\prime}\right) \\
\bar{Q}_{12}\left(z^{\prime}\right) \bar{Q}_{22}\left(z^{\prime}\right) \bar{Q}_{26}\left(z^{\prime}\right) \\
\bar{Q}_{16}\left(z^{\prime}\right) \bar{Q}_{26}\left(z^{\prime}\right) \bar{Q}_{66}\left(z^{\prime}\right)
\end{array}\right] z^{\prime} d z^{\prime}}  \tag{46b}\\
& {\left[\begin{array}{lll}
\mathrm{D}_{11}^{\text {plate }} & \mathrm{D}_{12}^{\text {plate }} & \mathrm{D}_{16}^{\text {plate }} \\
\mathrm{D}_{12}^{\prime \text { plate }} & \mathrm{D}_{22}^{\prime \text { plate }} & \mathrm{D}_{26}^{\prime \text { plate }} \\
\mathrm{D}_{16}^{\prime \text { plate }} & \mathrm{D}_{26}^{\prime \text { plate }} & \mathrm{D}_{26}^{\prime \text { plate }}
\end{array}\right]==\int_{-\frac{\mathrm{h}}{2}}^{+} \frac{\mathrm{h}}{2}\left[\begin{array}{l}
\overline{\mathrm{Q}}_{11}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{12}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{16}\left(\mathrm{z}^{\prime}\right) \\
\overline{\mathrm{Q}}_{12}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{22}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{26}\left(\mathrm{z}^{\prime}\right) \\
\overline{\mathrm{Q}}_{16}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{26}\left(\mathrm{z}^{\prime}\right) \overline{\mathrm{Q}}_{66}\left(\mathrm{z}^{\prime}\right)
\end{array}\right] \mathrm{z}^{\prime \prime^{2}} \mathrm{dz}^{\prime}}  \tag{46c}\\
& {\left[\begin{array}{ll}
\mathrm{A}^{\text {plate }} & \mathrm{A}^{\text {plate }} \\
\mathrm{A}^{\text {plata }} & \mathrm{A}^{\text {plate }} \\
\mathrm{A}^{\text {plate }} &
\end{array}\right]=\mathrm{K}^{\text {plate }} \int_{-\frac{\mathrm{h}}{2}}^{+\frac{\mathrm{h}}{2}}\left[\begin{array}{ll}
\overline{\mathrm{Q}}_{44}\left(\mathrm{z}^{\prime}\right) & \overline{\mathrm{Q}}_{45}\left(\mathrm{z}^{\prime}\right) \\
\overline{\mathrm{Q}}_{45}\left(\mathrm{z}^{\prime}\right) & \overline{\mathrm{Q}}_{55}\left(\mathrm{z}^{\prime}\right)
\end{array}\right] d \mathrm{z}^{\prime}} \tag{46~d}
\end{align*}
$$

Equations (46) represent the plate stiffnesses of a given face plate that are calculated in the usual way (see references 19 and 139) in which $\mathrm{z}^{\prime}=0$ represents the plate midplane. With these definitions, the equivalent-sandwich-plate stiffnesses are given by

$$
\begin{align*}
& {\left[\begin{array}{lll}
\mathrm{A}_{11} & \mathrm{~A}_{12} & \mathrm{~A}_{16} \\
\mathrm{~A}_{12} & \mathrm{~A}_{22} & \mathrm{~A}_{26} \\
\mathrm{~A}_{16} & \mathrm{~A}_{26} & \mathrm{~A}_{66}
\end{array}\right]=\left[\begin{array}{lll}
\mathrm{A}_{11}^{, \text {plate no. 1 }} & \mathrm{A}_{12}^{, \text {plate no. 1 }} & \mathrm{A}_{16}^{, \text {plate no. 1 }} \\
\mathrm{A}_{12}^{\text {plate no. 1 }} & \mathrm{A}_{22}^{\text {plate no. 1 }} & \mathrm{A}_{22}^{, \text {plate no. 1 }} \\
\mathrm{A}_{16}^{\text {plate no. 1 }} & \mathrm{A}_{26}^{, \text {plate no. 1 }} & \mathrm{A}_{166}^{, \text {plate no. 1 }} \\
& &
\end{array}\right]+} \\
& {\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {plate no. } 2} & \mathrm{~A}_{12}^{\text {plate no. } 2} & \mathrm{~A}_{16}^{\text {plate no. } 2} \\
\mathrm{~A}_{12}^{\text {plate no. } 2} & \mathrm{~A}_{22}^{\text {plate no. } 2} & \mathrm{~A}_{26}^{\text {plate no. } 2} \\
\mathrm{~A}_{16}^{\text {plate no. } 2} & \mathrm{~A}_{26}^{\prime \text { plate no. } 2} & \mathrm{~A}_{16}^{\prime \text { plata no. }} \\
& &
\end{array}\right]+\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {plat }} & \mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{16}^{\text {core }} \\
\mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{22}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} \\
\mathrm{A}_{16}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} & \mathrm{A}_{66}^{\text {core }}
\end{array}\right]}  \tag{47a}\\
& {\left[\begin{array}{lll}
B_{11} & B_{12} & B_{16} \\
B_{12} & B_{22} & B_{26} \\
B_{16} & B_{26} & B_{66}
\end{array}\right]=\left[\begin{array}{lll}
B_{11}^{, \text {plate no. 1 }} & B_{12}^{, \text {plate no. 1 }} & B_{16}^{, \text {plate no. 1 }} \\
B_{12}^{, \text {plate no. 1 }} & B_{22}^{, \text {plate no. 1 }} & B_{26}^{, \text {plate no. 1 }} \\
B_{12}^{, \text {plate no. 1 }} & B_{26}^{, \text {plate no. 1 }} & B_{16}^{, \text {plate no. 1 }}
\end{array}\right]+\left[\begin{array}{lll}
B_{11}^{, \text {plate no. 2 }} & B_{12}^{, \text {plate no. 2 }} & B_{16}^{, \text {plate no. 2 }} \\
B_{12}^{, \text {plate no. 2 }} & B_{22}^{, \text {plate no. 2 }} & B_{26}^{, \text {plate no. 2 }} \\
B_{12}^{, \text {plate no. 2 }} & B_{22}^{, \text {plate no. 2 }} & B_{26}^{, \text {plate no. 2 }}
\end{array}\right]} \\
& +\mathrm{e}^{\text {plate no. 1 }}\left[\begin{array}{lll}
\mathrm{A}_{11}^{, \text {plate no. 1 }} & \mathrm{A}_{12}^{, \text {plate no. 1 }} & \mathrm{A}_{16}^{, \text {plate no. 1 }} \\
\mathrm{A}_{12}^{\text {plate no. 1 }} & \mathrm{A}_{22}^{\text {plate no. 1 }} & \mathrm{A}_{26}^{\text {plate no. 1 }} \\
\mathrm{A}_{16}^{\text {plate no. 1 }} & \mathrm{A}_{26}^{\text {plate no. 1 }} & \mathrm{A}_{160}^{\text {plate no. 1 }}
\end{array}\right]+\mathrm{e}^{\text {plate no. 2 }}\left[\begin{array}{lll}
\mathrm{A}_{11}^{, \text {plate no. 2 }} & \mathrm{A}_{12}^{, \text {plate no. 2 }} & \mathrm{A}_{16}^{, \text {plate no. 2 }} \\
\mathrm{A}_{12}^{, \text {plate no. 2 }} & \mathrm{A}_{22}^{, \text {plate no. 2 }} & \mathrm{A}_{22}^{, \text {plate no. 2 }} \\
\mathrm{A}_{16}^{, \text {plate no. 2 }} & \mathrm{A}_{26}^{, \text {plate no. 2 }} & \mathrm{A}_{66}^{, \text {plate no. 2 }}
\end{array}\right]  \tag{47b}\\
& {\left[\begin{array}{lll}
\mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\mathrm{D}_{12} & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\mathrm{D}_{16} & \mathrm{D}_{26} & \mathrm{D}_{66}
\end{array}\right]=\left[\begin{array}{lll}
\mathrm{D}_{11}^{\prime p_{16}^{\text {plate no. 1 }}} \mathrm{D}_{12}^{\prime \text { plate no. 1 }} & \mathrm{D}_{16}^{\prime \text { plate no. 1 }} \\
\mathrm{D}_{12}^{\prime \text { plate no. 1 }} & \mathrm{D}_{22}^{\prime \text { plate no. 1 }} & \mathrm{D}_{26}^{\prime \text { plate no. 1 }} \\
\mathrm{D}_{12}^{\prime \text { plate no. 1 }} & \mathrm{D}_{26}^{\prime \text { plate no. 1 }} & \mathrm{D}_{66}^{\prime \text { plate no. 1 }}
\end{array}\right]+\left[\begin{array}{lll}
\mathrm{D}_{11}^{\prime \text { plate no. 2 }} & \mathrm{D}_{12}^{\prime \text { plate no. 2 }} & \mathrm{D}_{16}^{\prime \text { plate no. 2 }} \\
\mathrm{D}_{12}^{\prime \text { plate no. 2 }} & \mathrm{D}_{22}^{\text {plate no. 2 }} & \mathrm{D}_{26}^{\prime \text { plate no. 2 }} \\
\mathrm{D}_{12}^{\prime \text { plate no. 2 }} & \mathrm{D}_{26}^{\prime \text { plate no. 2 }} & \mathrm{D}_{26}^{\prime \text { plate no. 2 }}
\end{array}\right]} \\
& +\left(e^{\text {plate no. 1 }}\right)^{2}\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {plate no. 1 }} & \mathrm{A}_{12}^{\text {plate no. 1 }} & \mathrm{A}_{16}^{\text {plate no. 1 }} \\
\mathrm{A}_{12}^{\text {plate no. 1 }} & \mathrm{A}_{22}^{\text {plate no. 1 }} & \mathrm{A}_{26}^{\text {plate no. 1 }} \\
\mathrm{A}_{16}^{\text {plate no. 1 }} & \mathrm{A}_{26}^{\text {plate no. 1 }} & \mathrm{A}_{16}^{\text {plate no. 1 }}
\end{array}\right]+\left(e^{\text {plate no. 2 }}\right)^{2}\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {plate no. 2 }} & \mathrm{A}_{12}^{\text {plate no. 2 }} & \mathrm{A}_{16}^{\prime \text { plate no. 2 }} \\
\mathrm{A}_{12}^{\text {plate no. 2 }} & \mathrm{A}_{22}^{\text {plate no. 2 }} & \mathrm{A}_{26}^{\prime \text { plate no. 2 }} \\
\mathrm{A}_{16}^{\text {plate no. 2 }} & \mathrm{A}_{26}^{\prime \text { plate no. 2 }} & \mathrm{A}_{66}^{\prime \text { plate no. 2 }}
\end{array}\right] \\
& +2 e^{\text {plate no. } 1}\left[\begin{array}{lll}
\boldsymbol{B}_{11}^{p^{\text {plate no. } 1}} & \boldsymbol{B}_{12}^{p^{\text {plate no. } 1}} & \boldsymbol{B}_{16}^{p^{\text {plate no. } 1}} \\
\boldsymbol{B}_{12}^{\text {plate no. } 1} & \boldsymbol{B}_{22}^{\text {plate no. } 1} & \boldsymbol{B}_{26}^{\text {plate no. 1 }} \\
\boldsymbol{B}_{16}^{\text {plate no. 1 }} & \boldsymbol{B}_{26}^{\text {plate no. 1 }} & \boldsymbol{B}_{16}^{\text {plate no. 1 }}
\end{array}\right]+2 e^{\text {plate no. }}\left[\begin{array}{lll}
\boldsymbol{B}_{11}^{\text {plate no. 2 }} & \boldsymbol{B}_{12}^{\text {plate no. 2 }} & \boldsymbol{B}_{16}^{\text {plate no. 2 }} \\
\boldsymbol{B}_{12}^{\text {plate no. 2 }} & \boldsymbol{B}_{22}^{\text {plate no. 2 }} & \boldsymbol{B}_{26}^{\text {plate no. 2 }} \\
\boldsymbol{B}_{12}^{\text {plate no. 2 }} & \boldsymbol{B}_{26}^{\text {plate no. 2 }} & \boldsymbol{B}_{16}^{\text {plate no. 2 }}
\end{array}\right]  \tag{47c}\\
& +\left[\begin{array}{lll}
\mathrm{D}_{11}^{\text {core }} & \mathrm{D}_{12}^{\text {core }} & \mathrm{D}_{16}^{\text {core }} \\
\mathrm{D}_{12}^{\text {core }} & \mathrm{D}_{22}^{\text {core }} & \mathrm{D}_{26}^{\text {core }} \\
\mathrm{D}_{16}^{\text {core }} & \mathrm{D}_{26}^{\text {core }} & \mathrm{D}_{66}^{\text {core }}
\end{array}\right] \\
& {\left[\begin{array}{ll}
\mathrm{A}_{44} & \mathrm{~A}_{45} \\
\mathrm{~A}_{45} & \mathrm{~A}_{55}
\end{array}\right]=\left[\begin{array}{ll}
\mathrm{A}_{44}^{, \text {plate no. 1 }} & \mathrm{A}_{45}^{, \text {plate no. 1 }} \\
\mathrm{A}_{45}^{, \text {plate no. 1 }} & \mathrm{A}_{55}^{, \text {plate no. 1 }}
\end{array}\right]+\left[\begin{array}{ll}
\mathrm{A}_{44}^{, \text {plate no. 2 }} & \mathrm{A}_{45}^{, \text {plate no. 2 }} \\
\mathrm{A}_{45}^{, \text {plate no. 2 }} & \mathrm{A}_{55}^{, \text {plate no. 2 }}
\end{array}\right]+\left[\begin{array}{ll}
\mathrm{A}_{44}^{\text {core }} & \mathrm{A}_{45}^{\text {core }} \\
\mathrm{A}_{45}^{\text {core }} & \mathrm{A}_{55}^{\text {core }}
\end{array}\right]} \tag{47~d}
\end{align*}
$$

The analysis of the present study was applied to the sandwich plates with two nonidentical anisotropic face plates shown in figures 25-27. For these examples, the eccentricities of the face plates, plates no. 1 and 2, are given by $\mathrm{e}_{1}=-\frac{1}{2}\left(\mathrm{~h}_{1}+\mathrm{h}_{\mathrm{c}}\right)$ and $\mathrm{e}_{2}=\frac{1}{2}\left(\mathrm{~h}_{2}+\mathrm{h}_{\mathrm{c}}\right)$, with respect to the
midplane of the core, respectively, where $\mathrm{h}_{\mathrm{c}}$ is the depth of the core and $\mathrm{h}_{1}$ and $\mathrm{h}_{2}$ are the thicknesses of plates no. 1 and 2, respectively. The sandwich plate shown in figure 25 has a regular hexagon-cell core composed of two member types, each with a rectangular cross-section. One member type is aligned with the y -axis of the plate, as shown in figure 25, and is referred to herein as a rib. The other member type makes an angle with the x -axis and is referred to herein as a diagonal. The core has the same layout as the hexagonal stiffener grid shown in figure 21a and with the dimensions $\frac{\mathrm{a}}{\mathrm{L}}=\frac{\sqrt{3}}{2}, \frac{\mathrm{~b}}{\mathrm{~L}}=\frac{1}{2}$, and $\frac{\mathrm{c}}{\mathrm{L}}=1$. The geometrical properties of the face plates and the core are also shown in figure 25, and the section properties of the core are given in Appendix H. The core contributions to the equivalent-plate stiffnesses in equations (47) are given in Appendix H and are obtained by specializing the general stiffnesses given in Appendix F for a hexagonal stiffener arrangement. For the special case in which the face plates are made of the same isotropic material, the core is made of a second isotropic material, the thicknesses of the core members are identical ( $t_{s}=t_{d}=t$ ), the face plates have identical thicknesses ( $h_{1}=h_{2}=h$ ), and shear deformation is neglected, the stiffnesses in Appendix H reduce to those given by Kalamkarov ${ }^{110}$ (see p. 205), with the exception of the contribution of the torsional stiffnesses of the core members.

The sandwich plate shown in figure 26 has a regular "orthogrid" core with the same layout as the stiffening arrangement shown in figure 14a, but without the diagonal braces. The geometrical properties of the face plates and the core are shown figure 26, and the relationship of these properties to the orthogonal stiffeners is given in Table 4 and Appendix I. The core contributions to equations (47) are given in Appendix I and are obtained by specializing the general stiffnesses given in Appendix B. Expressions are also given in Appendix I for the special case in which the two face plates and the core are made of three different homogeneous orthotropic materials. When these expressions are further reduced for face plates with identical thicknesses ( $\mathrm{h}_{1}=\mathrm{h}_{2}$ ) and shear deformation is neglected, the stiffnesses reduce to those given by Kalamkarov ${ }^{110}$ (see pp. 200-201), with the exception of the torsional stiffnesses of the core members.

A sandwich plate with a star-shaped, or star-cell, core is shown in figure 26 which has the same layout as the stiffening arrangement shown in figure 23a. The relationship of the geometrical properties to the core stiffeners is given in Table 9 and Appendix J. Specializing the general stiffnesses in Appendix G yields the core contribution to equations (47) given in Appendix J. Expressions are also given in Appendix J for the special case in which the star shapes forming the core are composed of equilateral triangles with coincident centroids.

## Equivalent-Plate Thickness

The equivalent-plate thickness, $\mathrm{h}+\mathrm{h}_{\mathrm{s}}$, shown in figure 9, is often needed to perform auxiliary design computations. However, for the analysis presented herein, the results reveal that this thickness is not defined uniquely. For example, enforcing equivalence between the area of the stiffener and the area of the equivalent-stiffener layer gives the equivalent-stiffener layer thickness as

$$
\begin{equation*}
\mathrm{h}_{\mathrm{s}}=\frac{\mathrm{A}_{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \tag{48}
\end{equation*}
$$

In contrast, the stiffness-weighted first moment of stiffener area about the y -axis, defined by equation (A13e), is given by

$$
\begin{equation*}
\frac{1}{\mathrm{E}_{\mathrm{S}}} \iint_{\mathrm{A}_{\mathrm{S}}} \mathrm{E}_{\mathrm{X}} \mathrm{ZdYdZ}=\mathrm{A}_{\mathrm{S}} \overline{\mathrm{Z}}_{\mathrm{S}} \tag{49}
\end{equation*}
$$

Applying this equation to the equivalent-stiffener layer is generally complicated for an arbitrary nonhomogeneous stiffener. For the simpler case of a homogeneous stiffener, equation (49) gives the equivalence statement

$$
\begin{equation*}
\mathrm{h}_{\mathrm{s}}\left(\mathrm{~h}_{\mathrm{s}}+\mathrm{h}\right)=\frac{2 \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \tag{50}
\end{equation*}
$$

which is solved to obtain $\mathrm{h}_{\mathrm{s}}$. Likewise, the stiffness-weighted second moment of stiffener area about the y -axis, defined by equation (A13f), is given by

$$
\begin{equation*}
\frac{1}{\mathrm{E}_{\mathrm{S}}} \iint_{\mathrm{A}_{\mathrm{S}}} \mathrm{E}_{\mathrm{X}} \mathrm{Z}^{2} \mathrm{dYdZ}=\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}} \tag{51}
\end{equation*}
$$

Applying this equation to the equivalent-stiffener layer, for the simpler case of a homogeneous stiffener, gives

$$
\begin{equation*}
h_{s}^{3}+\frac{3 h}{2} h_{s}^{2}+\frac{3 h^{2}}{4} h_{s}=\frac{3}{d_{s}} I_{Y Y} \tag{52}
\end{equation*}
$$

which is solved to obtain $\mathrm{h}_{\mathrm{s}}$. Similarly, applying the formula from elasticity theory for torsion of a homogeneous, isotropic beam with a rectangular cross-section given in reference 144 (see p. 89) to the equivalent-stiffener layer gives the transcendental equation

$$
\begin{equation*}
\frac{\mathrm{h}_{\mathrm{s}}^{3} \mathrm{~d}_{\mathrm{s}}}{3}\left[1-\frac{64}{3 \pi^{5}} \frac{\mathrm{~h}_{\mathrm{s}}}{\mathrm{~d}_{\mathrm{s}}} \tanh \left(\frac{\pi \mathrm{~d}_{\mathrm{s}}}{2 \mathrm{~h}_{\mathrm{s}}}\right)\right]=\mathrm{J}_{\mathrm{s}} \tag{53}
\end{equation*}
$$

Thus, equations (48), (50), (52), and (53) give four different values for the thickness of the equivalent-stiffener layer, but other criteria based on equations (A13) exist. In particular, equation (48) results from equivalence based on membrane action, and equation (50) results from equivalence based on coupling between membrane and bending action. Equation (52) results from equivalence based on bending action, and equation (53) results from equivalence based on twisting action. The appropriate formula to use for $\mathrm{h}_{\mathrm{s}}$ should be based on the dominant physical characteristic response involved in a particular auxiliary computation.

## Concluding Remarks

A survey of studies conducted since 1914 on the use of equivalent-plate stiffnesses in modeling the overall, stiffness-critical response of stiffened plates and shells, and two detailed, comprehensive derivations of first-approximation equivalent-plate stiffnesses have been presented. The derivations are based on the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. The first derivation is based purely on static and kinematic equivalence between a stiffened plate and its homogenized equivalent. The second derivation is based on equivalence of the strain-energy density and is more amenable to complicated stiffener arrangements such as the hexagonal and star-shaped stiffening arrangements presented herein. In both derivations, the stiffener members are modelled as beams that are shear deformable within and transverse to the midplane of the plate, consistent with the classical continuum model of solid mechanics. In general, each stiffener is prismatic and may have a nonhomogeneous cross-section made from specially orthotropic materials. This general formulation allows the computation of equivalent-plate stiffnesses for stiffened panels such as those in which the stiffener caps are reinforced with high-strength, pultruded rods. Consistent with a first-approximation theory, inplane bending of the stiffeners and total compatibility between the plate skin and the stiffeners are neglected. Both methods presented herein have been shown to yield identical results.

Equivalent-plate stiffness expressions, and a corresponding symbolic manipulation computer program, have also presented for several different stiffener configurations. These expressions are very general and exhibit the full range of anisotropies permitted by the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. The expressions presented in the present study were also compared with available, previously published results. For the most part, the previously published results are for special cases of the general expressions presented herein. These previously published results and are almost in complete agreement with the corresponding results contained herein and plausible reasons for the discrepancies have been given. Analysis has also been presented that extends the use of the equivalent-plate stiffness expressions to sandwich plates with nonidentical, anisotropic face plates. In addition, several criteria for obtaining an equivalent-plate thickness for stiffened plates have been presented.

## References

1. Huber, M. T.: Die Grundlagen einer rationellen Berechnung der Kruezwise beweheten Eisenbetonplatten. Zeitschrift des Oesterreichischen Ingenieur und Architekten-Vereines, vol. 66, 1914, pp. 557-564.
2. Huber, M. T.: Die Theorie der Kreuzweise bewehrten Eisenbeton-Platte nebst Anwendungen auf mehrere bautechnisch wichtige Aufgaben uiber rechteckige Platten. Bauingenieur, vol. 4, 1923, pp. 354-360 and 392-395.
3. Huber, M. T.: Probleme der Statik Technisch Wichtiger Orthotroper Platten. Nakkadem Akadenji Nauk Technicznych Warszawa, Poland, 1929.
4. Flugge, W.: Die Stabilitat der Kreiszylinderschale. Ingenieur-Archiv, vol. 3, no. 5, 1932, pp. 463-506.
5. Heck, O. S.; and Ebner, H.: Methods and Formulas for Calculating the Strength of Plate and Shell Constructions as Used in Airplane Design. NACA TM 785, 1936.
6. Anon.: Some Investigations of the General Instability of Stiffened Metal Cylinders, I-Review of Theory and Bibliography. NACA TN 905, 1943.
7. Dale, F. A.; and Smith, R. C. T.: Grid Sandwich Panels in Compression. Report ACA-16, Australian Council for Aeronautics, April, 1945.
8. Smith, C. B.; Heebink, T. B.; and Norris, C. B.: The Effective Stiffness of a Stiffener Attached to a Flat Plywood Plate. Report No. 1557, U. S. Department of Agriculture, Forest Products Laboratory, September, 1946.
9. Van der Neut, A: The General Instability of Stiffened Cylindrical Shells under Axial Compression. Report S. 314, Nationaal Luchtvaartlaboratorium, 1947.
10. Pfluger, A.: Zum Beulproblcm der anisotropen Rechteckplatte. Ingenieur-Archiv, vol. 16, 1947, pp. 111-120.
11. Gomza, A.; and Seide, P.: Minimum-Weight Design of Simply Supported Transversely Stiffened Plates under Compression. NACA TN 1710, 1948.
12. Libove, C.; and Hubka, R. E.: Elastic Constants for Corrugated-Core Sandwich Plates. NACA TN 2289, 1951.
13. Libove, C. and Batdorf, S. B.: A General Small-Deflection Theory for Flat Sandwich Plates. NACA Rep. 899, 1948.
14. Reissner, E.: Small Bending and Stretching of Sandwich-Type Shells. NACA Rep. 975, 1950.
15. Stein, M.; and Mayers, J.: A Small-Deflection Theory for Curved Sandwich Plates. NACA Rep. 1008, 1951.
16. Benscoter, S. U.; and MacNeal, R. H.: Equivalent Plate Theory for a Straight Multicell Wing. NACA TN 2786, 1952.
17. Horvay, G.: Bending of Honeycombs and of Perforated Plates. Journal of Applied Mechanics, March, 1952, pp. 122-123.
18. Dow, N. F.; Libove, C.; and Hubka, R. E.: Formulas for the Elastic Constants of Plates with Integral Waffle-Like Stiffening. NACA Rep. 1195, 1953.
19. Jones, R. M.: Mechanics of Composite Materials. Second ed., Taylor \& Francis, 1999.
20. Crawford, R. F.; and Libove, C.: Shearing Effectiveness of Integral Stiffening. NACA TN 3443, 1955.
21. Hoppmann, W. H., II: Bending of Orthogonally Stiffened Plates. Journal of Applied Mechanics, June, 1955, pp. 267-271.
22. Hoppmann, W. H., II: Elastic Compliances of Orthogonally Stiffened Plates. Proceedings of the Society of Experimental Stress Analysis, vol. 14, no. 1, 1956, pp. 137-144.
23. Hoppmann, W. H., II; Huffington, N. J., Jr.; and Magness, L. S.: A Study of Orthogonally Stiffened Plates. Journal of Applied Mechanics, September, 1956, pp. 343-350.
24. Hoppmann, W. H., II and Magness, L. S.: Nodal Patterns of the Free Flexural Vibrations of Stiffened Plates. Journal of Applied Mechanics, December, 1957, pp. 526-530.
25. Huffington, N. J., Jr.: Theoretical Determination of Rigidity Properties of Orthogonally Stiffened Plates. Journal of Applied Mechanics, March, 1956, pp. 15-20.
26. Bodner, S. R.: General Instability of a Ring-Stiffened Circular Cylindrical Shell under Hydrostatic Pressure. Journal of Applied Mechanics, June, 1957, pp. 269-277.
27. Gerard, G.: Minimum Weight Analysis of Orthotropic Plates Under Compressive Loading. Journal of the Aeronautical Sciences, vol. 27, no. 1, 1960, pp. 21-26 and 64.
28. Baruch, M.; and Singer, J.: Effect of Eccentricity of Stiffeners on the General Instability of Stiffened Cylindrical Shells under Hydrostatic Pressure. Journal of Mechanical Engineering Science, vol. 5, no. 1, 1963, pp. 23-27.
29. Clifton, R. J.; Chang, J. C. L.; and Au, T.: Analysis of Orthotropic Plate Bridges. ASCE Journal of the Structural Division, vol. 89, no. ST5, 1963, pp.133-171.
30. Stroud, W. J.: Elastic Constants for Bending and Twisting of Corrugation-Stiffened Panels. NASA TR R-166, 1963.
31. Meyer, R. R.; and Bellefante, R. J.: Fabrication and Experimental Evaluation of Common Domes having Waffle-Like Stiffening, Part I - Program Development. Report SM-47742, Douglas Missile \& Space Systems Division, November, 1964.
32. Sewall, J. L.; Clary, R. R.; and Leadbetter, S. A.: An Experimental and Analytical Vibration Study of a Ring-Stiffened Cylindrical Shell Structure with Various Support Conditions. NASA TN D-2398, 1964.
33. Baruch, M.: Equilibrium and Stability Equations for Stiffened Shells. Sixth Annual Conference on Aviation and Astronautics, Tel Aviv and Haifa, Israel, February 24-25, 1964, pp. 117-124.
34. Hedgepeth, J. M.; and Hall, D. B.: Stability of Stiffened Cylinders. AIAA Journal, vol. 3, no. 12, 1965, pp. 2275-2286.
35. Crawford, R. F.: Effects of Asymmetric Stiffening on Buckling of Shells. Proceedings of the AIAA Second Annual Meeting, July 26-29, San Francisco, CA, 1965, pp. 1-21.
36. Meyer, R. R.: Orthotropic Rib-Stiffened Shells with Eccentricity, Including Buckling of an Axially Compressed Cylinder, Part I - Theory. Report No. SM-47832, Missile and Space Systems Division, Douglas Aircraft Company, Inc., 1965.
37. Mikulas, M. M., Jr. and McElman, J. A.: On Free Vibrations of Eccentrically Stiffened Cylindrical Shells and Flat Plates. NASA TN D-3010, 1965.
38. Block, D. L.; Card, M. F.; and Mikulas, M. M., Jr.: Buckling of Eccentrically Stiffened Orthotropic Cylinders. NASA TN D-2960, 1965.
39. Geier, B.: Das Beulverhalten versteifter Zylinderschalen-Teil I: Differentialgleichungen. Zeitschrift fur Flugwissenschaften, vol. 14, no. 7, 1966, pp. 306-323.
40. McElman, J. A.; Mikulas, M. M., Jr.; and Stein, M.: Static and Dynamic Effects of Eccentric Stiffening of Plates and Cylindrical Shells. AIAA Journal, vol. 4, no. 5, 1966, pp. 887-894.
41. Card, M. F.; and Jones, R. M.: Experimental and Theoretical Results for Buckling of Eccentrically Stiffened Cylinders. NASA TN D-3639, October, 1966.
42. Singer, J.; Baruch, M.; and Harari, O.: Inversion of the Eccentricity Effect in Stiffened Cylindrical Shells Buckling under External Pressure. Journal Mechanical Engineering Science, vol. 8, no. 4, 1966, pp. 363-373.
43. Stuhlman, C.; DeLuzio, A.; and Almroth, B.: Influence of Stiffener Eccentricity and End Moment on Stability of Cylinders in Compression. AIAA Journal, vol. 4, no. 5, 1966, pp. 872-877.
44. Geier, B.: Beullasten versteifter Kreiszylinderschalen. WGLR-Jahrbuch 1965, Friedrich Vieweg and Sohn GmbH, Braunschweig, 1966, pp. 440-447 (see also translation by the Aerospace Corporation, LRG-67-T-19, August, 1967).
45. Seggelke, P.; and Geier, B.: Das Beulverhalten versteifter Zylinderschalen-Teil II: Beullasten. Zeitschrift fur Flugwissenschaften, vol. 15, no. 12, 1967, pp. 477-490.
46. Meyer, R. R.: Buckling of $45^{\circ}$ Eccentric-Stiffened Waffle Cylinders. Journal of the Royal Aeronautical Society, vol. 71, pp. 516-520, 1967.
47. Simitses, G. J.: A Note on the General Instability of Eccentrically Stiffened Cylinders. Journal of Aircraft, vol. 4, no. 5, 1967, pp. 473-475.
48. Sundara Raja Iyengar, K. T.; and Narayana Iyengar, R.: Determination of the Orthotropic Plate Parameters of Stiffened Plates and Grillages in Free Vibrations. Applied Scientific Research, vol. 17, 1967, pp. 422-438.
49. Jones, R. M.: Buckling of Circular Cylindrical Shells with Multiple Orthotropic Layers and Eccentric Stiffeners. AIAA Journal, vol. 6, no. 12, 1968, pp. 2301-2305.
50. Heki, K.: On the Effective Rigidities of Lattice Plates. Recent Researches of Structural Mechanics, Contributions in Honour of the 60th Birthday of Prof. Y. Tsuboi, H. Tanaka and S. Kawamata, eds., Uno Shoten, Tokyo, 1968, pp. 31-46.
51. Jones, R. M.: Errata: 'Buckling of Circular Cylindrical Shells with Multiple Orthotropic Layers and Eccentric Stiffeners.' AIAA Journal, vol. 7, no. 10, 1969, pp. 2048.
52. Soong, T.-C.: Buckling of Cylindrical Shells with Eccentric Spiral-Type Stiffeners. AIAA Journal, vol. 7, no. 10, 1969, pp. 65-72.
53. Meyer, R. R.: Comments on "Buckling of Cylindrical Shells with Eccentric Spiral-Type Stiffeners." AIAA Journal, vol. 7, no. 10, 1969, p. 2047.
54. Soong, T.-C.: Reply by Author to R. R. Meyer. AIAA Journal, vol. 7, no. 10, 1969, pp. 20472048.
55. Flower, W. R.; and Schmidt, L. C.: Analysis of Space Truss as Equivalent Plate. ASCE Journal of the Structural Division, vol. 97, no. ST12, 1971, pp. 2777-2789.
56. Heki, K.; and Saka, T.: Stress Analysis of Lattice Plates as Anisotropic Continuum Plates. IASS Pacific Symposium - Part II on Tension Structures and Space Frames, Tokyo and Kyoto, October 17-23, 1971, pp. 7-7-1 to 7-7-12.
57. Kao Ding Chiu: Stability of Orthotropic Stiffened Composite Plates. ASCE Journal of the Engineering Mechanics Division, vol. 98, no. EM5, 1972, pp. 1253-1271.
58. Cusens, A. R.; Zeidan, M. A.; and Pama, R. P.: Elastic Rigidity of Ribbed Plates. Building Science, vol. 7, 1972, pp. 23-32.
59. Rehfield, L. W.: Design of Stiffened Cylinders to Resist Axial Compression. Journal of Spacecraft \& Rockets, vol. 10, no. 5, 1973, pp. 346-349.
60. Patnaik, S.; and Sankaran, G. V.: Vibration of Initially Stressed Stiffened Circular Cylinders and Panels. Journal of Sound and Vibration, vol. 31, no. 3, 1973, pp. 369-382.
61. Lind, N. C.: Buckling of Longitudinally Stiffened Sheets. ASCE Journal of the Structural Division, vol. 99, no. ST7, 1973, pp.1686-1691.
62. Sun, C. T.; and Yang, T. Y.: A Continuum Approach Toward Dynamics of Gridworks. Journal of Applied Mechanics, vol. 40, March, 1973, pp. 186-192.
63. Nishino, F.; Pama, R. P.; and Lee, S.-L.: Orthotropic Plates with Eccentric Stiffeners. International Association of Bridge Structural Engineering, vol. 34, no. 2, 1974, pp. 117-129.
64. Dobyns, A.; Avery, J.; Blaisdell, R.; and Figge, I. E.: Advanced Composite Lattice Structure for Improved Structural Integrity. Proceedings of the AIAA/ASME/SAE 15th Structures, Structural Dynamics, and Materials Conference, 1974, AIAA paper 74-357.
65. Rosen, A.; and Singer, J.: Vibrations of Axially Loaded Stiffened Cylindrical Shells. Journal of Sound and Vibration, vol. 34, no. 3, 1974, pp. 357-378.
66. Kalev, I. and Baruch, M.: General Elastic Buckling of Eccentrically Stiffened Plates under Load Combinations. Israel Journal of Technology, vol. 13, 1975, pp. 31-38.
67. Hasegawa, A.; Akiyama, H.; and Nishino, F.: Analysis of Plates with Single-Sided Stiffeners. Proceedings of the Japan Society of Civil Engineers, vol. 240, 1975, pp. 23-34.
68. Rhodes, M. D.; and Mikulas, M. M., Jr.: Composite Lattice Structure. NASA TM X-72771, 1975.
69. Rosen, A.; and Singer, J.: Vibrations and Buckling of Axially Loaded Stiffened Cylindrical Shells with Elastic Restraints. International Journal of Solids \& Structures, vol. 12, 1976, pp. 577-588.
70. Heard, W. L., Jr.; Anderson, M. S.; and Slysh, P.: An Engineering Procedure for Calculating Compressive Strength of Isogrid Cylindrical Shells with Buckled Skin. NASA TN D-8239, 1976.
71. Sobel, L. H.; and Agarwal, B. L.: Buckling of Eccentrically Stringer-Stiffened Cylindrical Panels Under Axial Compression. Computers \& Structures, vol. 6, 1976, pp. 193-198.
72. Richards, D. M.: Optimum Design of Stiffened Shear Webs with Supplementary Skin Stabilization. International Journal of Solids and Structures, vol. 12, 1976, pp. 791-802.
73. Srinivasan, R. S.; and Ramachandran, S. V.: Linear and Nonlinear Analysis of Stiffened Plates. International Journal of Solids and Structures, vol. 13, 1977, pp. 897-912.
74. Agarwal, B. L.; and Sobel, L. H.: Weight Comparisons of Optimized Stiffened, Unstiffened, and Sandwich Cylindrical Shells. Journal of Aircraft, vol. 14, no. 10, 1977, pp. 1000-1008.
75. Elgaaly, M.: Correlation Between the Buckling of Uniformly Stiffened and Isotropic Plates. International Colloquium on Stability of Structures under Static and Dynamic Loads, Washington, D. C., May 17-19, 1977, pp. 422-434.
76. Prathap, G.; and Varadan, T. K.: Large Amplitude Flexural Vibration of Stiffened Plates. Journal of Sound and Vibration, vol. 57, no. 4, 1978, pp. 583-593.
77. Rossow, M. P.; and Ibrahimkhail, A. K.: Constraint Method Analysis of Stiffened Plates. Computers \& Structures, vol. 8, 1978, pp. 51-60.
78.Weller, T.: Combined Stiffening and In-Plane Boundary Conditions Effects on the Buckling of Circular Cylindrical Stiffened Shells. Computers \& Structures, vol. 9, 1978, pp. 1-16.
78. Noor, A. K.; Anderson, M. S.; and Greene, W. H.: Continuum Models for Beam- and Platelike Lattice Structures. AIAA Journal, vol. 16, no. 12, 1978, pp. 1219-1228.
79. Karmakar, R.: Buckling of Waffle Cylinders. Aeronautical Journal, vol. 83, July, 1979, pp. 274-278.
80. Nemeth, M. P.: Continuum Models for Repetitive Lattices Structures with Rigid Joints. M.S. Thesis, The George Washington University, 1979.
81. Ko, W. L.: Elastic Constants for Superplastically Formed/Diffusion-Bonded Sandwich Structures. Proceedings of the AIAA/ASME/AHS 20th Structures, Structural Dynamics, and Materials Conference, 1979, AIAA paper 79-0756.
82. Ko, W. L.: Elastic Constants for Superplastically Formed/Diffusion-Bonded Sandwich Structures. AIAA Journal, vol. 18, no. 8, 1980, pp. 986-987.
83. Ko, W. L.: Elastic Stability of Superplastically Formed/Diffusion-Bonded Orthogonally Corrugated Core Sandwich Plates. Proceedings of the AIAA/ASME/AHS 21st Structures, Structural Dynamics, and Materials Conference, 1980, AIAA paper 80-0683.
84. Karmakar, R.: Axially Compressed Optimum Cylinder-Comparison of Stiffener Configurations. Journal of Spacecraft and Rockets, vol. 17, no. 5, 1980, pp. 477-479.
85. Rao, S. S.; and Reddy, E. S.: Optimum Design of Stiffened Cylindrical Shells with Natural Frequency Constraints. Computers \& Structures, vol. 12, 1980, pp. 211-219.
86. Yen, S.-W.: Buckling of Cylindrical Shells with Spiral Stiffeners under Uniform Compression and Torsion. Computers \& Structures, vol. 11, 1980, pp. 587-595.
87. Karmakar, R.: Effect of Stiffener Eccentricity in Axially Compressed Waffle Cylinders. AIAA Journal, vol. 19, no. 6, 1981, pp. 828-829.
88. Weller, T.: Combined Effects of In-Plane Boundary Conditions and Stiffening on Buckling of Eccentrically Stringer-Stiffened Cylindrical Panels. Computers \& Structures, vol. 14, no. 5-6, 1981, pp. 427-442.
89. Nayfeh, A. H.; and Hefzy, M. S.: Effective Constitutive Relations for Large Repetitive FrameLike Structures. International Journal of Solids and Structures, vol. 18, no. 11, 1982, pp. 975-987.
90. Nayfeh, A. H.; Hefzy, M. S.; and Hartle, M. S.: Effective Constitutive Relations for the Microstructure of Periodic Frames. AIAA Paper No. 83-1006, 1983.
91. Sheinman, I.; Shaw, D.; and Simitses, G. J.: Nonlinear Analysis of Axially-Loaded Laminated Cylindrical Shells. Computers \& Structures, vol. 16, no. 1-4, 1983, pp. 131-137.
92. Ellinas, C. P., and Croll, J. G. A.: Experimental and Theoretical Correlations for Elastic Buckling of Axially Compressed Stringer Stiffened Cylinders. Journal of Strain Analysis, vol. 18, no. 1, 1983, pp. 41-67.
93. Simitses, G. J.; Shaw, D.; and Sheinman, I.: Stability of Cylindrical Shells, by Various Nonlinear Shell Theories. Z. Angew. Math. u. Mech., vol. 65, no. 3, 1985, pp. 159-166.
94. Reddy, A. D.; Valisetty, R. R.; and Rehfield, L. W.: Continuous Filament Wound Composite Concepts for Aircraft Fuselage Structures. Journal of Aircraft, vol. 22, no. 3, 1985, 249-255.
95. Srinivasan, R. S.; and Thiruvenkatachari, V.: Static and Dynamic Analysis of Stiffened Plates. Computers \& Structures, vol. 21, no. 3, 1985, pp. 395-403.
96. Kolpakov, A. G.: Determination of the Average Characteristics of Elastic Frameworks. Prikladnaya Matematika i Mekhanika, vol. 49, no. 6, 1985, pp. 739-745.
97. Kollar, L.; and Hegedus, I.: Analysis and Design of Space Frames by the Continuum Method. Developments in Civil Engineering, vol. 10, Elsevier, 1985.
98. Hefzy, M. S.; and Nayfeh, A. H.: Shear Deformation Plate Continua of Large Double Layered Space Structures. International Journal of Solids and Structures, vol. 22, no. 12, 1986, pp. 1455-1469.
99. Tamma, K. K.; and Saw, K. C.: Reduced Modeling and Analysis of Large Repetitive Space Structures via Continuum/Discrete Concepts. Computers \& Structures, vol. 25, no. 3, 1987, pp. 321-333.
100. Noor, A. K.: Continuum Modeling for Repetitive Lattice Structures. Applied Mechanics Reviews, vol. 41, no. 7, 1988, pp. 285-296.
101. Deb, A.; and Booton, M.: Finite Element Models for Stiffened Plates under Transverse Loading. Computers \& Structures, vol. 28, no. 3, 1988, pp. 361-372.
102. Boot, J. C.; and Moore, D. B.: Stiffened Plates Subject to Transverse Loading. International Journal of Solids and Structures, vol. 4, no. 1, 1988, pp. 89-104.
103. Srinivasan, R. S.; and Krishnan, P. A.: Dynamic Analysis of Stiffened Conical Shell Panels. Computers \& Structures, vol. 33, no. 3, 1989, pp. 831-837.
104. Bunakov, V. A.; and Protasov, V. D.: Cylindrical Reticular Composite Shells. Mechanics of Composite Materials, vol. 25, no. 6, 1989, pp. 759-766.
105. Won, C. J.: Stiffened Plates with Arbitrary Oblique Stiffeners. International Journal of Solids and Structures, vol. 26, 1990, pp. 779-799.
106. Sumec, J.: Regular Lattice Plates and Shells. Developments in Civil Engineering, vol. 33, Elsevier, 1990.
107. Ko, W. L.; and Jackson, R. H.: Compressive Buckling Analysis of Hat-Stiffened Panel. NASA TM 4310, 1991.
108. Guo, M.; and Harik, I. E.: Stability of Eccentrically Stiffened Plates. Thin-Walled Structures, vol. 14, 1992, pp. 1-20.
109. Kalamkarov, A. L.: Composite and Reinforced Elements of Construction. John Wiley \& Sons, 1992.
110. Luo, S.; Suhling, J. C.; Considine, J. M.; and Laufenberg, T. L.: The Bending Stiffnesses of Corrugated Board. Mechanics of Cellulosic Materials, R. W. Perkins, ed., AMD-vol. 145/ MD-vol. 36, ASME, 1992, pp. 15-26.
111. Pshenichnov, G. I.: A Theory of Latticed Plates and Shells. Series on Advances in Mathematics for Applied Sciences-vol. 5, World Scientific, New Jersey, 1993.
112. Lee, U.: Dynamic Continuum Plate Representations of large Thin Lattice Structures. AIAA Journal, vol. 31, no. 9, 1993, pp. 1734-1736.
113. Gantes, C.; Connor, J. J.; and Logcher, R. D.: Equivalent Continuum Model for Deployable Flat Lattice Structures. Journal of Aerospace Engineering, vol. 7, no. 1, 1994, pp. 72-91.
114. Zarutskii, V. A.: Approximate Formulas for Stability Analysis of Ribbed Cylindrical Shells. International Applied Mechanics, vol. 31, no. 9, 1995, pp. 732-737.
115. Jaunky, N.; Knight, N. F., Jr.; and Ambur, D. R.: Formulation of an Improved Smeared Stiffener Theory for Buckling Analysis of Grid-Stiffened Composite Panels. NASA TM 110162, 1995.
116. Jaunky, N.; Knight, N. F., Jr.; and Ambur, D. R.: Formulation of an Improved Smeared Stiffener Theory for Buckling Analysis of Grid-Stiffened Composite Panels. Composites: Part B, vol. 27B, 1996, pp. 519-526.
117. Gerhard, C. S.; Gurdal, Z.; and Kapania, R. K.: Finite Element Analysis of Geodesically Stiffened Cylindrical Composite Shells Using a Layerwise Theory-Final Report. NASA CR200288, 1996.
118. Chen, H.-J.; and Tsai, S. W.: Analysis and Optimum Design of Composite Grid Structures. Journal of Composite Materials, vol. 30, no. 4, 1996, pp. 503-534.
119. Mecitoglu, Z.: Vibration Characteristics of a Stiffened Conical Shell. Journal of Sound and Vibration, vol. 197, no. 2, 1996, pp. 191-206.
120. Andrianov, I. V.; Kholod, E. G.; and Olevsky, V. I.: Approximate Non-Linear Boundary Value Problems of Reinforced Shell Dynamics. Journal of Sound and Vibration, vol. 194, no. 3, 1996, pp. 369-387.
121. Huybrechts, S.; and Tsai, W. S.: Analysis and Behavior of Grid Structures. Composites Science and Technology, vol. 56, 1996, pp. 1001-1015.
122. Shen, H.-S.: Thermomechanical Postbuckling of Stiffened Laminated Cylindrical Shell. Journal of Engineering Mechanics, vol. 123, no. 5, 1997, pp. 433-443.
123. Bedair, O. K.: Analysis of Stiffened Plates under Lateral Loading Using Sequential Quadratic Programming (SQP). Computers \& Structures, vol. 62, no. 1, 1997, pp. 63-80.
124. Bedair, O. K.: A Contribution to the Stability of Stiffened Plates Under Uniform Compression. Computers \& Structures, vol. 66, no. 5, 1998, pp. 535-570.
125. Librescu, L.; and Souza, M. A.: Nonlinear Dynamics of Stiffened Flat Panels under Thermomechanical Loads. Journal of Aerospace Engineering, vol. 13, no. 3, 2000, pp. 78-84.
126. Kim, B.; and Christensen, R. M.: Basic Two-Dimensional Core Types for Sandwich Structures. International Journal of Mechanical Sciences, vol. 42, 2000, pp. 657-676.
127. Paik, J. K.; Thayamballi, A. K.; and Kim, B. J.: Large Deflection Orthotropic Plate Approach to Develop Ultimate Strength Formulations for Stiffened Panels under Combined Biaxial Compression/Tension and Lateral Pressure. Thin-Walled Structures, vol. 39, 2001, pp. 215-246.
128. Slinchenko, D.; and Verijenko, V. E.: Structural analysis of Composite Lattice Shells of Revolution on the Basis of Smearing Stiffness. Composite Structures, vol. 54, 2001, pp. 341-348.
129. Kidane, S.: Buckling Analysis of Grid Stiffened Composite Structures. M.S. Thesis, Louisiana State University and Agricultural and Mechanical College, 2002.
130. Vasiliev, V. V.; Barynin, V. A.; and Rasin, A. F.: Anisogrid Lattice Structures - Survey of Development and Application. Composite Structures, vol. 54, 2001, pp. 361-370.
131. Hohe, J.; and Becker, W.: Effective Stress-Strain Relations for Two-Dimensional Cellular Sandwich Cores: Homogenization, Material Models, and Properties. Applied Mechanics Reviews, vol. 55, no. 1, 2002, pp. 61-87.
132. Wodesenbet, E.; Kidane, Samuel; Pang, Su-Seng: Optimization for Buckling Loads of Grid Stiffened Composite Panels. Composite Structures, vol. 60, 2003, pp. 159-169.
133. Kidane, S.; Li, G.; Helms, J.; Pang, S-S., and Woldesenbet, E: Buckling Load Analysis of Grid Stiffened Composite Cylinders. Composites: Part B, vol. 34, 2003, pp. 1-9.
134. Byklum, E.; Steen, E.; and Amdahl, Jorgen: A Semi-Analytical Model for Global Buckling and Postbuckling Analysis of Stiffened Panels. Thin-Walled Structures, vol. 42, 2004, pp. 701-717.
135. Mazur-Sniady, K.; Wozniak, Cz.; and Wierbicki, E.: On the Modeling of Dynamic Problems for Plates with a Periodic Structure. Archive of Applied Mechanics, vol. 74, 2004, pp. 179-190.
136. Hughes, O. F.; Ghosh, B.; and Chen, Y.: Improved Prediction of Simultaneous Local and Overall Buckling of Stiffened Panels. Thin-Walled Structures, vol. 42, 2004, pp. 827-856.
137. Wang, X.; Liang, C.; Han, M.; Yeh, K.; and Wang, G.: Nonlinear Dynamical Behavior of Shallow Cylindrical Reticulated Shells. Applied Mathematics and Mechanics, vol. 28, no. 2, 2007, pp. 151-156.
138. Reddy, J. N.: Mechanics of Laminated Composite Plates - Theory and Analysis. CRC Press, 1997.
139. Wang, A.-J.; and McDowell, D. L.: Yield Surfaces of Various Periodic Metal Honeycombs at Intermediate Relative Density. International Journal of Plasticity, vol. 21, 2005, pp. 285-320.
140. Fan, H; Fang, D.; and Jin, F.: Mechanical Properties of Lattice Grid Composites. Acta Mechanica Sinica, vol. 24, 2008, pp. 409-418.
141. Wolfram Mathematica, Software Package, Ver. 6.0.1.0, Wolfram Research, Champaign, IL, 1988-2007.
142. Leknitskii, S. G.: Theory of Elasticity of an Anisotropic Body. Mir Publishers, Moscow, 1981.
143. Wang, C. - T.: Applied Elasticity. McGraw-Hill Book Company, 1953.
144. Allen, D. H.; and Haisler, W. E.: Introduction to Aerospace Structural Analysis. John Wiley \& Sons, 1985.

Table 1. Stiffener attributes for an eccentric, orthogonal stiffening grid with two diagonal braces per bay (see figure 14)
| Stiffener family | Spacing, $\mathrm{d}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{L}_{\mathrm{y}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |
| Ribs | $\mathrm{L}_{\mathrm{x}}$ | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{r}}$ |
| Diagonals \#1 | $\frac{\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\frac{\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 1. Concluded
| Stiffener family | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}$ | Torsion constant, $\mathrm{J}_{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| Ribs | $\mathrm{I}_{\mathrm{r}}$ | $\mathrm{J}_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| Diagonals \#1 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $k_{\mathrm{Y}}^{{ }^{\text {d1 }}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
L_{d}=\sqrt{L_{x}^{2}+L_{y}^{2}}
$$

Table 2. Stiffener attributes for an eccentric, orthogonal stiffening grid with one diagonal brace per bay (see figure 16)
| Stiffener family | Spacing, $\mathrm{d}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{L}_{\mathrm{y}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |
| Ribs | $\mathrm{L}_{\mathrm{x}}$ | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{r}}$ |
| Diagonals \#1 | $\frac{2 \mathrm{~L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\bar{Z}}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\frac{2 \mathrm{~L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 2. Concluded
| Stiffener family | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}$ | Torsion constant, $\mathrm{J}_{\mathrm{S}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| Ribs | $\mathrm{I}_{\mathrm{r}}$ | $\mathrm{J}_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| Diagonals \#1 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{{ }^{\mathrm{d1}}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
L_{d}=\sqrt{L_{x}^{2}+L_{y}^{2}}
$$

Table 3. Stiffener attributes for an eccentric, isosceles-triangle stiffener pattern (see figure 17)
| Stiffener family | Spacing, $\mathrm{d}_{\mathrm{s}}$ | Angle, $\Psi_{s}$, degrees | $\cos \Psi_{\mathrm{s}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{S}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{L}_{\mathrm{y}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |
| Diagonals \#1 | $\frac{\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\frac{\mathrm{L}_{\mathrm{x}} \mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $180-\Phi$ | $-\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{d} 2}$ |


Table 3. Concluded
| Stiffener family | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, $\mathrm{J}_{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Stringers | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| Diagonals \#1 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{1}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| Diagonals \#2 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}{ }^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


Table 4. Basic-cell beam-member attributes for an eccentric, orthogonal stiffener pattern with two diagonal braces per bay (see figure 14b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{Z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2}, 0$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2}, 0$ | $\mathrm{L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |
| 3-4 | $0,-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $0, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | $\mathrm{L}_{\mathrm{y}}$ | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{r}}$ |
| 5-6 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | $\mathrm{L}_{\mathrm{d}}$ | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 7-8 | $\frac{\mathrm{L}_{\mathrm{x}}}{2},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $-\frac{\mathrm{L}_{\mathrm{x}}}{2}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | $\mathrm{L}_{\mathrm{d}}$ | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 4. Concluded
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, J $_{\text {s }}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 3-4 | $\mathrm{I}_{\mathrm{r}}$ | $\mathrm{J}_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| 5-6 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 7-8 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
L_{d}=\sqrt{L_{x}^{2}+L_{y}^{2}}
$$

Table 5. Basic-cell beam-member attributes for an eccentric, orthogonal stiffener pattern with one diagonal brace per bay (see figure 16b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{s}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | ${ }^{-} \mathrm{L}_{\mathrm{x}}, 0$ | $\mathrm{L}_{x}, 0$ | $2 \mathrm{~L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 3-4 | $0,-\mathrm{L}_{\mathrm{y}}$ | $0, \mathrm{~L}_{\mathrm{y}}$ | $2 \mathrm{~L}_{\mathrm{y}}$ | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{r}}$ |
| 5-6 | $-\mathrm{L}_{\mathrm{x}},-\mathrm{L}_{\mathrm{y}}$ | $\mathrm{L}_{x}, \mathrm{~L}_{y}$ | $2 \mathrm{~L}_{\mathrm{d}}$ | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 5-7 | $-\mathrm{L}_{\mathrm{x}},-\mathrm{L}_{\mathrm{y}}$ | $\mathrm{L}_{x},-\mathrm{L}_{y}$ | $2 \mathrm{~L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 5-8 | $-\mathrm{L}_{\mathrm{x}},-\mathrm{L}_{\mathrm{y}}$ | $-\mathrm{L}_{\mathrm{x}}, \mathrm{L}_{\mathrm{y}}$ | $2 \mathrm{~L}_{\mathrm{y}}$ | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{r}}$ |
| 7-8 | $\mathrm{L}_{\mathrm{x}},-\mathrm{L}_{\mathrm{y}}$ | $-\mathrm{L}_{\mathrm{x}}, \mathrm{L}_{\mathrm{y}}$ | $2 \mathrm{~L}_{\mathrm{d}}$ | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{\mathrm{L}_{\mathrm{d}}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}_{\mathrm{d}}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 5. Concluded
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, $\mathrm{J}_{\mathrm{S}}$ | Shear correction <br> factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction <br> factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, <br> $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 3-4 | Ir | J $_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\text {z }}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| 5-6 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d1}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 5-7 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 5-8 | $\mathrm{I}_{\mathrm{r}}$ | $\mathrm{J}_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| 7-8 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}{ }^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
L_{d}=\sqrt{L_{x}^{2}+L_{y}^{2}} \text { and } A_{\text {cell }}=4 L_{x} L_{y}
$$

Table 6. Basic-cell beam-member attributes for a plate stiffened with an eccentric, isoscelestriangle stiffener pattern (see figure 17b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{s}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{S}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2}, 0$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2}, 0$ | $\mathrm{L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 3-4 | $-\frac{\mathrm{L}_{\mathrm{x}}}{4},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $\frac{\mathrm{L}_{\mathrm{x}}}{4}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | L | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{d} 1}$ |
| 5-6 | $\frac{\mathrm{L}_{\mathrm{x}}}{4},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $-\frac{\mathrm{L}_{\mathrm{x}}}{4}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | L | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 6. Continued
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}$ | Torsion constant, J $_{\text {s }}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 3-4 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{1}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 5-6 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
\mathrm{L}=\sqrt{\mathrm{L}_{\mathrm{x}}^{2}+\mathrm{L}_{\mathrm{y}}^{2}}
$$

Table 7. Basic-cell beam-member attributes for a plate stiffened with an eccentric Kagome stiffener pattern (see figure 18b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{s}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{S}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2},-\frac{\mathrm{L}_{\mathrm{y}}}{2}$ | $\mathrm{L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 3-4 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2}, \frac{\mathrm{~L}_{\mathrm{y}}}{2}$ | $\mathrm{L}_{\mathrm{x}}$ | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 5-6 | $-\frac{\mathrm{L}_{\mathrm{x}}}{2},-\mathrm{L}_{\mathrm{y}}$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2}, \mathrm{~L}_{\mathrm{y}}$ | L | $\Phi$ | $\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{d} 1}$ |
| 7-8 | $\frac{\mathrm{L}_{\mathrm{x}}}{2},-\mathrm{L}_{\mathrm{y}}$ | $-\frac{\mathrm{L}_{\mathrm{x}}}{2}, \mathrm{~L}_{\mathrm{y}}$ | L | 180 - Ф | $-\frac{\mathrm{L}_{\mathrm{x}}}{2 \mathrm{~L}}$ | $\frac{\mathrm{L}_{\mathrm{y}}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{d} 2}$ |


Table 7. Continued
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, $\mathrm{J}_{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-2 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 3-4 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 5-6 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d1}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 7-8 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}{ }^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
\mathrm{L}=\sqrt{\mathrm{L}_{\mathrm{x}}^{2}+\mathrm{L}_{\mathrm{y}}^{2}}
$$

Table 8. Basic-cell-member attributes for a plate stiffened with an eccentric, hexagonal stiffener pattern (see figure 21b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{S}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2-1 | $0,-\frac{\mathrm{c}}{2}$ | $\frac{\mathrm{a}}{2},-\frac{\mathrm{b}+\mathrm{c}}{2}$ | $\frac{\mathrm{L}}{2}$ | $-\Phi$ | $\frac{\mathrm{a}}{\mathrm{L}}$ | $-\frac{\mathrm{b}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |
| 2-3 | $0,-\frac{\mathrm{c}}{2}$ | $-\frac{\mathrm{a}}{2},-\frac{\mathrm{b}+\mathrm{c}}{2}$ | $\frac{L}{2}$ | -180+ Ф | $-\frac{\mathrm{a}}{\mathrm{L}}$ | $-\frac{\mathrm{b}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 2-5 | $0,-\frac{\mathrm{c}}{2}$ | $0, \frac{\mathrm{c}}{2}$ | c | 90 | 0 | 1 | $\mathrm{A}_{\mathrm{r}}$ | $\overline{\mathrm{z}}_{\mathrm{r}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{r}}$ |
| 5-4 | $0, \frac{\mathrm{c}}{2}$ | $\frac{\mathrm{a}}{2}, \frac{\mathrm{~b}+\mathrm{c}}{2}$ | $\frac{\mathrm{L}}{2}$ | $\Phi$ | $\frac{\mathrm{a}}{\mathrm{L}}$ | $\frac{\mathrm{b}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 5-6 | $0, \frac{\mathrm{c}}{2}$ | $-\frac{\mathrm{a}}{2}, \frac{\mathrm{~b}+\mathrm{c}}{2}$ | $\frac{\mathrm{L}}{2}$ | 180 - Ф | $-\frac{\mathrm{a}}{\mathrm{L}}$ | $\frac{\mathrm{b}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |


Table 8. Continued
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, J $_{\text {S }}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, $\mathrm{G}_{\mathrm{s}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2-1 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |
| 2-3 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{{ }^{\mathrm{d1}}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 2-5 | $\mathrm{I}_{\mathrm{r}}$ | $\mathrm{J}_{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}}$ | $\mathrm{E}_{\mathrm{r}}$ | $\mathrm{G}_{\mathrm{r}}$ |
| 5-4 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{{ }^{\mathrm{d1}}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 5-6 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}{ }^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |


$$
\mathrm{L}=\sqrt{\mathrm{a}^{2}+\mathrm{b}^{2}}
$$

Table 9. Basic-cell-member attributes for a plate stiffened with an eccentric, star-shaped stiffener pattern (see figure 23b)
| Member designation | Starting coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Ending coordinates, ( $\mathrm{x}, \mathrm{y}$ ) | Length, $\mathrm{L}_{\mathrm{s}}$ | Angle, $\Psi_{\mathrm{s}}$, degrees | $\cos \Psi_{\mathrm{S}}$ | $\sin \Psi_{\mathrm{s}}$ | Area, $\mathrm{A}_{\mathrm{s}}$ | Effective eccentricity, $\overline{\mathrm{z}}_{\mathrm{S}}$ | Effective eccentricity, $\overline{\overline{\mathrm{Z}}}_{\mathrm{S}}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-12 | $\frac{\mathrm{B}}{3}, 0$ | $\frac{\mathrm{B}}{2},-\frac{\mathrm{H}}{3}$ | L/3 | - Ф | $\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $-\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{Z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |
| 1-2 | $\frac{\mathrm{B}}{3}, 0$ | $\frac{\mathrm{B}}{2}, \frac{\mathrm{H}}{3}$ | L/3 | $\Phi$ | $\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 3-2 | $\frac{\mathrm{B}}{6}, \frac{\mathrm{H}}{3}$ | $\frac{\mathrm{B}}{2}, \frac{\mathrm{H}}{3}$ | B/3 | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 3-4 | $\frac{\mathrm{B}}{6}, \frac{\mathrm{H}}{3}$ | $0, \frac{2 \mathrm{H}}{3}$ | L/3 | $180-\Phi$ | $-\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{Z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |
| 5-4 | $-\frac{\mathrm{B}}{6}, \frac{\mathrm{H}}{3}$ | $0, \frac{2 \mathrm{H}}{3}$ | L/3 | $\Phi$ | $\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 5-6 | $-\frac{\mathrm{B}}{6}, \frac{\mathrm{H}}{3}$ | $-\frac{\mathrm{B}}{2}, \frac{\mathrm{H}}{3}$ | B/3 | 180 | -1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |
| 7-6 | $-\frac{\mathrm{B}}{3}, 0$ | $-\frac{\mathrm{B}}{2}, \frac{\mathrm{H}}{3}$ | L/3 | $180-\Phi$ | $-\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{d} 2}$ |
| 7-8 | $-\frac{\mathrm{B}}{3}, 0$ | $-\frac{\mathrm{B}}{2},-\frac{\mathrm{H}}{3}$ | L/3 | $180+\Phi$ | $-\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $-\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 9-8 | $-\frac{\mathrm{B}}{6},-\frac{\mathrm{H}}{3}$ | $-\frac{\mathrm{B}}{2},-\frac{\mathrm{H}}{3}$ | B/3 | 180 | 0 | 1 | A ${ }_{\mathrm{s}}$ | $\overline{\mathrm{Z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{z}}}_{\mathrm{s}}$ |
| 9-10 | $-\frac{\mathrm{B}}{6},-\frac{\mathrm{H}}{3}$ | $0,-\frac{2 \mathrm{H}}{3}$ | L/3 | $-\Phi$ | $\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $-\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 2}$ | $\overline{\mathrm{z}}_{\mathrm{d} 2}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 2}$ |
| 11-10 | $\frac{\mathrm{B}}{6},-\frac{\mathrm{H}}{3}$ | $0,-\frac{2 \mathrm{H}}{3}$ | L/3 | $180+\Phi$ | $-\frac{\mathrm{B}}{2 \mathrm{~L}}$ | $-\frac{\mathrm{H}}{\mathrm{L}}$ | $\mathrm{A}_{\mathrm{d} 1}$ | $\overline{\mathrm{z}}_{\mathrm{d} 1}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{d} 1}$ |
| 11-12 | $\frac{\mathrm{B}}{6},-\frac{\mathrm{H}}{3}$ | $\frac{\mathrm{B}}{2},-\frac{\mathrm{H}}{3}$ | B/3 | 0 | 1 | 0 | $\mathrm{A}_{\mathrm{s}}$ | $\overline{\mathrm{z}}_{\mathrm{s}}$ | $\overline{\overline{\mathrm{Z}}}_{\mathrm{s}}$ |


Table 9. Concluded
| Member designation | Effective moment of inertia, $\mathrm{I}_{\mathrm{YY}}^{\mathrm{S}}$ | Torsion constant, $\mathrm{J}_{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | Shear correction factor, $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | Effective modulus, $\mathrm{E}_{\mathrm{s}}$ | Effective shear modulus, G $_{\text {s }}$ |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1-12 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 2}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |
| 1-2 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{{ }^{\mathrm{d1}}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 3-2 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 3-4 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d}^{2}}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |
| 5-4 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{{ }^{\mathrm{d1}}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 5-6 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 7-6 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d}_{2}}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |
| 7-8 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 9-8 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |
| 9-10 | $\mathrm{I}_{\mathrm{d} 2}$ | $\mathrm{J}_{\mathrm{d} 2}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}_{2}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d}^{2}}$ | $\mathrm{E}_{\mathrm{d} 2}$ | $\mathrm{G}_{\mathrm{d} 2}$ |
| 11-10 | $\mathrm{I}_{\mathrm{d} 1}$ | $\mathrm{J}_{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{d} 1}$ | $\mathrm{E}_{\mathrm{d} 1}$ | $\mathrm{G}_{\mathrm{d} 1}$ |
| 11-12 | $\mathrm{I}_{\mathrm{s}}$ | $\mathrm{J}_{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}$ | $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}}$ | $\mathrm{E}_{\mathrm{s}}$ | $\mathrm{G}_{\mathrm{s}}$ |


![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-074.jpg?height=2083&width=1495&top_left_y=234&top_left_x=317)
Figure 1. Space Shuttle and external tank structure.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-075.jpg?height=1866&width=1641&top_left_y=431&top_left_x=244)
Figure 2. Densely stiffened orthogrid cylinder.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-076.jpg?height=1791&width=1624&top_left_y=281&top_left_x=259)
Figure 3. Isogrid-stiffened cylinders.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-077.jpg?height=1789&width=1178&top_left_y=287&top_left_x=363)
(b) Family of beams within a "small" rectangular plate region

Figure 4. Unidirectionally stiffened plate geometry.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-078.jpg?height=433&width=1514&top_left_y=352&top_left_x=313)
Figure 5. Cross-section A-A of a uniformly stiffened panel shown in figure 4b.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-078.jpg?height=1022&width=1468&top_left_y=1155&top_left_x=365)
Figure 6. Plate and stiffener coordinate systems.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-079.jpg?height=407&width=1361&top_left_y=339&top_left_x=399)
Figure 7. Examples of a nonhomogeneous stiffener cross-section.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-079.jpg?height=590&width=983&top_left_y=1024&top_left_x=627)
Figure 8. Repetitive stiffened-panel element and coordinate systems.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-079.jpg?height=398&width=952&top_left_y=1929&top_left_x=623)
Figure 9. Equivalent-plate wall.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-080.jpg?height=1022&width=1488&top_left_y=414&top_left_x=315)
Figure 10. Beam stresses at an arbitrary cross-section.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-081.jpg?height=1262&width=1472&top_left_y=339&top_left_x=363)
Figure 11. Beam force and moment resultants at an arbitrary cross-section.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-082.jpg?height=723&width=1179&top_left_y=317&top_left_x=416)
Figure 12. Stiffener beam forces and moments acting on cross-section of repetitive stiffened-panel element.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-082.jpg?height=699&width=1305&top_left_y=1514&top_left_x=386)
Figure 13. Plate stress resultants acting on cross-section of equivalent stiffened-panel wall.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-083.jpg?height=2051&width=1445&top_left_y=300&top_left_x=380)
Figure 14. Orthogonal stiffener pattern with two diagonal braces per bay and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-084.jpg?height=936&width=1404&top_left_y=446&top_left_x=414)
Figure 15. Diamond-shaped stiffener pattern.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-085.jpg?height=2058&width=1459&top_left_y=295&top_left_x=369)
Figure 16. Orthogonal stiffener pattern with one diagonal brace per bay and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-086.jpg?height=2029&width=1432&top_left_y=315&top_left_x=401)
Figure 17. Isosceles-triangle stiffener pattern and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-087.jpg?height=2031&width=1393&top_left_y=294&top_left_x=401)
Figure 18. Kagome stiffener pattern and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-088.jpg?height=957&width=996&top_left_y=277&top_left_x=558)
Figure 19. Generation of an isosceles-triangle stiffener pattern obtained by translating the basic cell defined in figure 17.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-088.jpg?height=836&width=708&top_left_y=1521&top_left_x=715)
Figure 20. Generation of a Kagome stiffener pattern obtained by translating the basic cell defined in figure 18.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-089.jpg?height=2065&width=1425&top_left_y=294&top_left_x=369)
Figure 21. Hexagon-shaped stiffener pattern and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-090.jpg?height=766&width=867&top_left_y=676&top_left_x=614)
Figure 22. Generation of a hexagonal stiffener pattern obtained by translating the basic cell defined in figure 21.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-091.jpg?height=2132&width=1307&top_left_y=279&top_left_x=470)
Figure 23. Isosceles-star-shaped stiffener pattern and basic cell.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-092.jpg?height=1181&width=1131&top_left_y=369&top_left_x=457)
Figure 24. Generation of an isosceles-star-shaped stiffener pattern obtained by translating the basic cell defined in figure 23.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-093.jpg?height=1571&width=1467&top_left_y=365&top_left_x=317)
(b) Plate cross-section

Figure 25. Sandwich plate with nonidentical anisotropic face plates and a hexagon-cell core.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-094.jpg?height=1591&width=1380&top_left_y=517&top_left_x=369)
Figure 26. Sandwich plate with nonidentical anisotropic face plates and an orthogrid core.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-095.jpg?height=1898&width=1565&top_left_y=333&top_left_x=294)
Figure 27. Sandwich plate with nonidentical anisotropic face plates and a star-cell core.

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-096.jpg?height=553&width=1389&top_left_y=423&top_left_x=360)
Figure 28. Arbitrary face plate of a sandwich plate.

## Appendix A <br> Equations of First-Order Transverse-Shear Deformation Beam Theory

Let ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) denote the coordinates of the material particles forming a beam stiffener, with respect to the noncentroidal coordinate system shown in figure 6. The displacement of any material particle in the beam is given by the X -, Y -, and Z -components $\mathrm{U}(\mathrm{X}, \mathrm{Y}, \mathrm{Z}), \mathrm{V}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})$, and W(X, Y, Z), respectively. Consistent with Euler-Bernoulli and Timoshenko's first-order transverse-shear-deformation beam theories, these displacement components are expressed as

$$
\begin{gather*}
\mathrm{U}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\mathrm{u}(\mathrm{X})-\mathrm{Y} \varphi_{\mathrm{Z}}(\mathrm{X})+\mathrm{Z} \varphi_{\mathrm{Y}}(\mathrm{X})  \tag{A1a}\\
\mathrm{V}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\mathrm{v}(\mathrm{X})-\mathrm{Z} \varphi_{\mathrm{X}}(\mathrm{X})  \tag{A1b}\\
\mathrm{W}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\mathrm{W}(\mathrm{X})+\mathrm{Y} \varphi_{\mathrm{X}}(\mathrm{X}) \tag{A1c}
\end{gather*}
$$

where $\mathrm{u}(\mathrm{X}), \mathrm{v}(\mathrm{X})$, and $\mathrm{w}(\mathrm{X})$ are the displacements of the corresponding point on the beam stiffener reference axis, and $\varphi_{X}(X), \varphi_{Y}(X)$, and $\varphi_{Z}(X)$ are the dextral rotations of the beam cross-section about the X -, Y -, and Z -axes, respectively. For these kinematics, the cross-sectional planes are presumed to be planes of elastic symmetry; that is, the beam material is, at most, monoclinic with respect to the longitudinal $X$ axis (see Lekhnitskii, ${ }^{143}$ p. 271 and p. 293). The effects of crosssectional warping restraint associated with torsion of noncircular cross-sections are neglected in these kinematic equations and each cross section is presumed to warp in an identical manner. Substituting these displacement expressions into the linear strain-displacement relations for a three-dimensional elastic solid gives

$$
\begin{gather*}
\varepsilon_{\mathrm{XX}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\mathrm{e}_{\mathrm{XX}}^{\mathrm{o}}(\mathrm{X})+\mathrm{Y} \chi_{\mathrm{Z}}^{\mathrm{o}}(\mathrm{X})+\mathrm{Z} \chi_{\mathrm{Y}}^{\mathrm{o}}(\mathrm{X})  \tag{A2a}\\
\varepsilon_{\mathrm{YY}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\varepsilon_{\mathrm{ZZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\gamma_{\mathrm{YZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=0  \tag{A2b}\\
\gamma_{\mathrm{XY}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\Gamma_{\mathrm{XY}}^{\mathrm{o}}(\mathrm{X})-\mathrm{Z} \boldsymbol{\tau}^{\mathrm{o}}(\mathrm{X})  \tag{A2c}\\
\gamma_{\mathrm{XZ}}(\mathrm{X}, \mathrm{Y}, \mathrm{Z})=\Gamma_{\mathrm{XZ}}^{\mathrm{o}}(\mathrm{X})+\mathrm{Y} \boldsymbol{\tau}^{\mathrm{o}}(\mathrm{X}) \tag{A2d}
\end{gather*}
$$

where

$$
\begin{gather*}
\mathrm{e}_{\mathrm{XX}}^{\mathrm{o}}(\mathrm{X})=\frac{\partial \mathrm{u}}{\partial \mathrm{X}}  \tag{A3a}\\
\Gamma_{\mathrm{XY}}^{\mathrm{o}}(\mathrm{X})=\frac{\partial \mathrm{V}}{\partial \mathrm{X}}-\varphi_{\mathrm{Z}}  \tag{A3b}\\
\Gamma_{\mathrm{XZ}}^{\mathrm{o}}(\mathrm{X})=\frac{\partial \mathrm{W}}{\partial \mathrm{X}}+\varphi_{\mathrm{Y}} \tag{A3c}
\end{gather*}
$$

$$
\begin{align*}
& \tau^{\circ}(X)=\frac{\partial \varphi_{X}}{\partial X}  \tag{A3d}\\
& \chi_{Y}^{\circ}(X)=\frac{\partial \varphi_{Y}}{\partial X}  \tag{A3e}\\
& \chi_{Z}^{\circ}(X)=-\frac{\partial \varphi_{Z}}{\partial X} \tag{A3f}
\end{align*}
$$

The symbol $\boldsymbol{\tau}^{\circ}(\mathrm{X})$ represents the change in twist of the beam, associated with torsion. The symbols $\chi_{\mathrm{Y}}^{\circ}(\mathrm{X})$ and $\chi_{\mathrm{Z}}^{\circ}(\mathrm{X})$ represent the changes in curvature in the $\mathrm{X}-\mathrm{Z}$ and $\mathrm{X}-\mathrm{Y}$ planes, respectively. The symbols $\Gamma_{\mathrm{XY}}^{\circ}(\mathrm{X})$ and $\Gamma_{\mathrm{XZ}}^{\circ}(\mathrm{X})$ represent the transverse shear deformations in the $\mathrm{X}-\mathrm{Y}$ and $\mathrm{X}-\mathrm{Z}$ planes, respectively. In first-order shear-deformation beam theory, the set $\mathrm{u}(\mathrm{X})$, $\mathrm{V}(\mathrm{X}), \mathrm{W}(\mathrm{X}), \varphi_{\mathrm{X}}(\mathrm{X}), \varphi_{\mathrm{Y}}(\mathrm{X})$, and $\varphi_{\mathrm{Z}}(\mathrm{X})$ are the primary unknowns. In classical Euler-Bernoulli beam theory, the transverse shear deformations are presumed negligible, which yields

$$
\begin{gather*}
\varphi_{\mathrm{Y}}=-\frac{\partial \mathrm{W}}{\partial \mathrm{X}}  \tag{A4a}\\
\varphi_{\mathrm{Z}}=\frac{\partial \mathrm{V}}{\partial \mathrm{X}} \tag{A4b}
\end{gather*}
$$

and eliminates two of the unknowns. In addition, equations (A3e) and (A3f) yield

$$
\begin{align*}
& \chi_{\mathrm{Y}}^{\mathrm{o}}(\mathrm{X})=-\frac{\partial^{2} \mathrm{~W}}{\partial \mathrm{X}^{2}}  \tag{A4c}\\
& \chi_{\mathrm{Z}}^{\mathrm{o}}(\mathrm{X})=-\frac{\partial^{2} \mathrm{~V}}{\partial \mathrm{X}^{2}} \tag{A4d}
\end{align*}
$$

In the Euler-Bernoulli and first-order shear-deformation beam theories, all stresses are presumed to be negligible except $\sigma_{\mathrm{XX}}, \sigma_{\mathrm{XY}}$, and $\sigma_{\mathrm{XZ}}$. These stresses are shown in figure 10. The corresponding resultant internal forces are defined, with respect to the ( $\mathrm{X}, \mathrm{Y}, \mathrm{Z}$ ) coordinates, as

$$
\begin{align*}
& \mathrm{P}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}} \sigma_{\mathrm{XX}} \mathrm{dY} \mathrm{dZ}  \tag{A5a}\\
& \mathrm{~V}_{\mathrm{Y}}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}} \sigma_{\mathrm{XY}} \mathrm{dYdZ}  \tag{A5b}\\
& \mathrm{~V}_{\mathrm{Z}}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}} \sigma_{\mathrm{XZ}} \mathrm{dYdZ} \tag{A5c}
\end{align*}
$$

$$
\begin{gather*}
\mathrm{T}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}}\left(\mathrm{Y} \sigma_{\mathrm{XZ}}-\mathrm{Z} \sigma_{\mathrm{XY}}\right) \mathrm{dY} \mathrm{dZ}  \tag{A5d}\\
\mathrm{M}_{\mathrm{Y}}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}} \mathrm{Z} \sigma_{\mathrm{XX}} \mathrm{dYdZ}  \tag{A5e}\\
\mathrm{M}_{\mathrm{Z}}(\mathrm{X})=\iint_{\mathrm{A}_{\mathrm{S}}} \mathrm{Y} \sigma_{\mathrm{XX}} \mathrm{dY} \mathrm{dZ} \tag{A5f}
\end{gather*}
$$

where $A_{s}$ denotes the cross-sectional area of the beam stiffener. For these definitions, the corresponding positive valued moments are shown in figure 11.

The constitutive equations for a homogeneous, isotropic beam are obtained by substituting the beams strains and stresses into the constitutive equations for a general three-dimensional body. The result is

$$
\begin{align*}
& \sigma_{\mathrm{XX}}=\mathrm{E} \varepsilon_{\mathrm{XX}}  \tag{A6a}\\
& \sigma_{\mathrm{XY}}=\mathrm{G} \gamma_{\mathrm{XY}}  \tag{A6b}\\
& \sigma_{\mathrm{XZ}}=\mathrm{G} \gamma_{\mathrm{XZ}} \tag{A6c}
\end{align*}
$$

where E and G denote Young's extensional modulus and the shear modulus, respectively. Substituting equations (A2) into (A6), and then substituting the results into equations (A5) gives

$$
\begin{gather*}
\mathrm{P}=\mathrm{EA}_{\mathrm{S}}\left(\mathrm{e}_{\mathrm{XX}}^{\circ}+\overline{\mathrm{Y}} \chi_{\mathrm{Z}}^{\circ}+\overline{\mathrm{Z}} \chi_{\mathrm{Y}}^{\circ}\right)  \tag{A7a}\\
\mathrm{V}_{\mathrm{Y}}=\mathrm{k}_{\mathrm{Y}} \mathrm{GA}_{\mathrm{S}}\left(\Gamma_{\mathrm{XY}}^{\circ}-\overline{\mathrm{Z}} \tau^{\circ}\right)  \tag{A7b}\\
\mathrm{V}_{\mathrm{Z}}=\mathrm{k}_{\mathrm{Z}} \mathrm{GA}_{\mathrm{S}}\left(\Gamma_{\mathrm{XZ}}^{\circ}+\overline{\mathrm{Y}} \tau^{\circ}\right)  \tag{A7c}\\
\mathrm{T}=\mathrm{GA}_{\mathrm{S}}\left[\mathrm{k}_{\mathrm{Z}} \overline{\mathrm{Y}} \Gamma_{\mathrm{XZ}}^{\circ}-\mathrm{k}_{\mathrm{Y}} \overline{\mathrm{Z}} \Gamma_{\mathrm{XY}}^{\circ}\right]+\mathrm{GI}_{\mathrm{p}} \tau^{\circ}  \tag{A7d}\\
\mathrm{M}_{\mathrm{Y}}=\mathrm{EA}_{\mathrm{S}} \overline{\mathrm{Z}} \mathrm{e}_{\mathrm{XX}}^{\circ}+\mathrm{EI}_{\mathrm{YZ}} \chi_{\mathrm{Z}}^{\circ}+\mathrm{EI}_{\mathrm{YY}} \chi_{\mathrm{Y}}^{\circ}  \tag{A7e}\\
\mathrm{M}_{\mathrm{Z}}=\mathrm{EA}_{\mathrm{S}} \overline{\mathrm{Y}} \mathrm{e}_{\mathrm{XX}}^{\circ}+\mathrm{EI}_{\mathrm{ZZ}} \chi_{\mathrm{Z}}^{\circ}+\mathrm{EI}_{\mathrm{YZ}} \chi_{\mathrm{Y}}^{\circ} \tag{A7f}
\end{gather*}
$$

where $(\overline{\mathrm{Y}}, \overline{\mathrm{Z}})$ are the coordinates of the cross-section centroid, $\mathrm{k}_{\mathrm{Y}}$ and $\mathrm{k}_{\mathrm{Z}}$ are transverse-shear correction factors, and it is noted that

$$
\begin{align*}
& \iint_{A_{S}} Y d Y d Z=A_{S} \bar{Y}  \tag{A8a}\\
& \iint_{A_{S}} Z d Y d Z=A_{S} \bar{Z}  \tag{A8b}\\
& \iint_{A_{S}} Z^{2} d Y d Z \equiv I_{Y Y}  \tag{A8c}\\
& \iint_{A_{S}} Y^{2} d Y d Z \equiv I_{Z Z}  \tag{A8d}\\
& \iint_{A_{S}} Y Z d Y d Z \equiv I_{Y Z}  \tag{A8e}\\
& \iint_{A_{S}}\left(Y^{2}+Z^{2}\right) d Y d Z=I_{P} \tag{A8f}
\end{align*}
$$

The symbols $I_{Y Y}$ and $I_{Z Z}$ represent the area moments of inertia with respect to the noncentroidal $(X, Y, Z)$ coordinate system, and $I_{Y Z}$ denotes the corresponding product of inertia. The symbol $I_{P}$ denotes the polar moment of inertia, with respect to the origin of the coordinate system. To account for torsion of noncircular cross-sections, based on the St. Venant Theory of Torsion, equation (A7d) is expressed as

$$
\begin{equation*}
\mathrm{T}=\mathrm{GA}_{\mathrm{s}}\left[\mathrm{k}_{\mathrm{Z}} \overline{\mathrm{Y}} \Gamma_{\mathrm{XZ}}^{\mathrm{o}}-\mathrm{k}_{\mathrm{Y}} \overline{\mathrm{Z}} \Gamma_{\mathrm{XY}}^{\mathrm{o}}\right]+\mathrm{GJ} \tau^{\mathrm{o}} \tag{A9}
\end{equation*}
$$

where $\mathbf{J}$ is the torsion constant of elasticity theory. ${ }^{144}$
A set of constitutive equations for nonhomogeneous beams, similar to equations (A7) and to those given by Allen and Haisler ${ }^{145}$ (see pp. 171-187), are obtained as follows. First, the beam materials are presumed to be, at most, specially orthotropic with respect to the beam coordinate system. The material constitutive equations are given by

$$
\left\{\begin{array}{c}
\varepsilon_{\mathrm{XX}}  \tag{A10}\\
\varepsilon_{\mathrm{YY}} \\
\varepsilon_{\mathrm{ZZ}} \\
\gamma_{\mathrm{YZ}} \\
\gamma_{\mathrm{XZ}} \\
\gamma_{\mathrm{XY}}
\end{array}\right\}=\left[\begin{array}{cccccc}
\frac{1}{\mathrm{E}_{\mathrm{X}}} & -\frac{v_{\mathrm{YX}}}{\mathrm{E}_{\mathrm{Y}}} & -\frac{v_{\mathrm{ZX}}}{\mathrm{E}_{\mathrm{Z}}} & 0 & 0 & 0 \\
-\frac{v_{\mathrm{XY}}}{\mathrm{E}_{\mathrm{X}}} & \frac{1}{\mathrm{E}_{\mathrm{Y}}} & -\frac{v_{\mathrm{ZY}}}{\mathrm{E}_{\mathrm{Z}}} & 0 & 0 & 0 \\
-\frac{v_{\mathrm{XZ}}}{\mathrm{E}_{\mathrm{X}}} & -\frac{v_{\mathrm{YZ}}}{\mathrm{E}_{\mathrm{Y}}} & \frac{1}{\mathrm{E}_{\mathrm{Z}}} & 0 & 0 & 0 \\
0 & 0 & 0 & \frac{1}{\mathrm{G}_{\mathrm{YZ}}} & 0 & 0 \\
0 & 0 & 0 & 0 & \frac{1}{\mathrm{G}_{\mathrm{XZ}}} & 0 \\
0 & 0 & 0 & 0 & 0 & \frac{1}{\mathrm{G}_{\mathrm{XY}}}
\end{array}\right]\left\{\begin{array}{c}
\sigma_{\mathrm{XX}} \\
\sigma_{\mathrm{YY}} \\
\sigma_{\mathrm{ZZ}} \\
\sigma_{\mathrm{YZ}} \\
\sigma_{\mathrm{XZ}} \\
\sigma_{\mathrm{XY}}
\end{array}\right\}
$$

where $\mathrm{E}_{\mathrm{X}}, \mathrm{E}_{\mathrm{Y}}$, and $\mathrm{E}_{\mathrm{Z}}$ are the principal Young's moduli; $v_{\mathrm{XY}}, v_{\mathrm{XZ}}$, and $v_{\mathrm{YZ}}$ are the major Poisson's ratios; $v_{Y X}, v_{Z X}$, and $v_{Z Y}$ are the minor Poisson's ratios; and $\mathrm{G}_{X Y}, \mathrm{G}_{Y Z}$, and $\mathrm{G}_{X Z}$ are the principal shear moduli. For a nonhomogeneous cross-section, these material parameters are functions of the Y and Z cross-sectional coordinates. Based on equations (A2) and the presumption that $\sigma_{\mathrm{YY}}, \sigma_{\mathrm{ZZ}}$, and $\sigma_{Y Z}$ are negligible, equation (A10) reduces to

$$
\left\{\begin{array}{c}
\varepsilon_{\mathrm{XX}}  \tag{A11a}\\
0 \\
0 \\
0 \\
\gamma_{\mathrm{XZ}} \\
\gamma_{\mathrm{XY}}
\end{array}\right\}=\left[\begin{array}{cccccc}
\frac{1}{\mathrm{E}_{\mathrm{X}}} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & \frac{1}{\mathrm{G}_{\mathrm{XZ}}} & 0 \\
0 & 0 & 0 & 0 & 0 & \frac{1}{\mathrm{G}_{\mathrm{XY}}}
\end{array}\right]\left\{\begin{array}{c}
\sigma_{\mathrm{XX}} \\
0 \\
0 \\
0 \\
\sigma_{\mathrm{XZ}} \\
\sigma_{\mathrm{XY}}
\end{array}\right\}
$$

or

$$
\left\{\begin{array}{c}
\sigma_{\mathrm{XX}}  \tag{A11b}\\
0 \\
0 \\
0 \\
\sigma_{\mathrm{XZ}} \\
\sigma_{\mathrm{XY}}
\end{array}\right\}=\left[\begin{array}{cccccc}
\mathrm{E}_{\mathrm{X}} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & \mathrm{G}_{\mathrm{XZ}} & 0 \\
0 & 0 & 0 & 0 & 0 & \mathrm{G}_{\mathrm{XY}}
\end{array}\right]\left\{\begin{array}{c}
\varepsilon_{\mathrm{XX}} \\
0 \\
0 \\
0 \\
\gamma_{\mathrm{XZ}} \\
\gamma_{\mathrm{XY}}
\end{array}\right\}
$$

Substituting equations (A2) into (A11), and then substituting the results into equations (A5) gives

$$
\begin{equation*}
P(x)=\iint_{A_{S}} E_{X} d Y d Z e_{X X}^{o}+\iint_{A_{S}} E_{X} Y d Y d Z \chi_{Z}^{o}+\iint_{A_{S}} E_{X} Z d Y d Z \chi_{Y}^{o} \tag{A12a}
\end{equation*}
$$

$$
\begin{gather*}
V_{Y}(X)=\iint_{A_{S}} G_{X Y} d Y d Z \Gamma_{X Y}^{o}-\iint_{A_{S}} G_{X Y} Z d Y d Z \tau^{o}  \tag{A12b}\\
V_{Z}(X)=\iint_{A_{S}} G_{X Z} d Y d Z \Gamma_{X Z}^{o}+\iint_{A_{S}} G_{X Z} Y d Y d Z \tau^{o}  \tag{A12c}\\
T(X)=\iint_{A_{S}} G_{X Z} Y d Y d Z \Gamma_{X Z}^{o}-\iint_{A_{S}} G_{X Y} Z d Y d Z \Gamma_{X Y}^{o}+  \tag{A12~d}\\
M_{Y}(X)=\iint_{A_{S}} E_{X} Z d Y d Z e_{X X}^{o}+\iint_{A_{S}} E_{X} Y Z d Y d Z \chi_{Z}^{o}+\iint_{A_{S}}^{o} E_{X} Z^{2} d Y d Z \chi_{Y}^{o} \\
M_{Z}(X)=\iint_{A_{S}} E_{X} Y d Y d Z e_{X X}^{o}+\iint_{A_{S}}^{o} E_{X} Y^{2} d Y d Z \chi_{Z}^{o}+\iint_{A_{S}}^{o} E_{X} Y Z d Y d Z \chi_{Y}^{o} \tag{A12e}
\end{gather*}
$$

By defining the effective quantities

$$
\begin{align*}
& E_{S}=\frac{1}{A_{S}} \iint_{A_{S}} E_{X} d Y d Z  \tag{A13a}\\
& G_{X Z}^{s}=\frac{1}{A_{S}} \iint_{A_{S}} G_{X Z} d Y d Z  \tag{A13b}\\
& G_{X Y}^{s}=\frac{1}{A_{S}} \iint_{A_{S}} G_{X Y} d Y d Z  \tag{A13c}\\
& \bar{y}_{S}=\frac{\iint_{A_{S}} E_{X} Y d Y d Z}{A_{S} E_{S}}  \tag{A13d}\\
& \bar{Z}_{S}=\frac{\iint_{A_{S}} E_{X} Z d Y d Z}{A_{S} E_{S}}  \tag{A13e}\\
& I_{Y Y}^{s}=\frac{\iint_{A_{S}} E_{X} Z^{2} d Y d Z}{E_{S}} \tag{A13f}
\end{align*}
$$

$$
\begin{align*}
I_{Z Z}^{S} & =\frac{\iint_{A_{S}} E_{X} Y^{2} d Y d Z}{E_{S}}  \tag{A13g}\\
I_{Y Z}^{S} & =\frac{\iint_{A_{S}} E_{X} Y Z d Y d Z}{E_{S}}  \tag{A13h}\\
I_{P}^{S} & =\frac{\iint_{A}\left(Y^{2} G_{X Z}+Z^{2} G_{X Y}\right) d Y d Z}{\sqrt{G_{X Z}^{S} G_{X Y}^{S}}}  \tag{A13i}\\
\overline{\bar{y}}_{s} & =\frac{\iint_{A_{s}} G_{X Z} Y d Y d Z}{A_{S} G_{X Z}^{S}}  \tag{A13j}\\
\overline{\bar{Z}}_{S} & =\frac{\iint_{A_{S}} G_{X Y} Z d Y d Z}{A_{S} G_{X Y}^{S}} \tag{A13k}
\end{align*}
$$

equations (A12) are expressed as

$$
\begin{gather*}
P=E_{S} A_{S}\left(e_{X X}^{o}+\bar{y}_{S} \chi_{Z}^{o}+\bar{z}_{S} \chi_{Y}^{o}\right)  \tag{A14a}\\
V_{Y}=k_{Y} G_{X Y}^{s} A_{S}\left(\Gamma_{X Y}^{o}-\overline{\bar{z}}_{S} \tau^{o}\right)  \tag{A14b}\\
V_{Z}=k_{Z} G_{X Z}^{s} A_{S}\left(\Gamma_{X Z}^{o}+\overline{\bar{y}}_{S} \tau^{o}\right)  \tag{A14c}\\
T=k_{Z} G_{X Z}^{s} A_{S} \overline{\bar{y}}_{S} \Gamma_{X Z}^{o}-k_{Y} G_{X Y}^{s} A_{S} \overline{\bar{z}}_{S} \Gamma_{X Y}^{o}+\sqrt{G_{X Z}^{S} G_{X Y}^{S}} I_{P}^{s} \tau^{o}  \tag{A14d}\\
M_{Y}=E_{S} A_{S} \bar{z}_{S} e_{X X}^{o}+E_{S} I_{Y Z}^{s} \chi_{Z}^{o}+E_{S} I_{Y Y}^{s} \chi_{Y}^{o}  \tag{A14e}\\
M_{Z}=E_{S} A_{S} \bar{y}_{S} e_{X X}^{o}+E_{S} I_{Z Z}^{s} \chi_{Z}^{o}+E_{S} I_{Y Z}^{s} \chi_{Y}^{o} \tag{A14f}
\end{gather*}
$$

where $E_{S}$ is the effective extensional modulus of the nonhomogeneous beam stiffener; $G_{x z}^{s}$ and
$\mathrm{G}_{\mathrm{XY}}^{\mathrm{s}}$ are effective shear moduli; $\overline{\mathrm{y}}_{\mathrm{S}}, \overline{\mathrm{z}}_{\mathrm{S}}, \overline{\overline{\mathrm{y}}}_{\mathrm{S}}$, and $\overline{\overline{\mathrm{z}}}_{\mathrm{S}}$ are stiffness-weighted first moments of area; $I_{Y Y}^{s}$ and $I_{Z Z}^{s}$ are effective, stiffness-weighted moments of inertia; $I_{Y Z}^{s}$ is the corresponding stiffness-weighted product of inertia; and $\mathrm{I}_{\mathrm{p}}^{\mathrm{s}}$ is a stiffness-weighted polar moment of inertia. It is noteworthy to indicate that for homogeneous orthotropic materials with the principal axes aligned with the beam axes $\mathrm{E}_{\mathrm{s}}=\mathrm{E}_{\mathrm{X}}, \mathrm{G}_{\mathrm{XZ}}^{\mathrm{s}}=\mathrm{G}_{\mathrm{XZ}}, \mathrm{G}_{\mathrm{XY}}^{\mathrm{s}}=\mathrm{G}_{\mathrm{XY}}, \overline{\overline{\mathrm{y}}}_{\mathrm{s}}=\overline{\mathrm{y}}_{\mathrm{s}}=\overline{\mathrm{Y}}, \overline{\overline{\mathrm{z}}}_{\mathrm{s}}=\overline{\mathrm{z}}_{\mathrm{s}}=\overline{\mathrm{Z}}, \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}=\mathrm{I}_{\mathrm{YY}}, \mathrm{I}_{\mathrm{ZZ}}^{\mathrm{s}}=\mathrm{I}_{\mathrm{ZZ}}$, $I_{Y Z}^{s}=I_{Y Z}$, and $I_{P}^{s}=G_{X Z} I_{Z Z}+G_{X Y} I_{Y Y}$. To account for torsion of noncircular cross-sections based on the St. Venant Theory of Torsion, equation (A14d) is expressed as

$$
\begin{equation*}
\mathrm{T}=\mathrm{k}_{\mathrm{Z}} \mathrm{G}_{\mathrm{XZ}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\bar{y}}_{\mathrm{s}} \Gamma_{\mathrm{XZ}}^{\mathrm{o}}-\mathrm{k}_{\mathrm{Y}} \mathrm{G}_{\mathrm{XY}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}} \Gamma_{\mathrm{XY}}^{\mathrm{o}}+\mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}} \tau^{\mathrm{o}} \tag{A15a}
\end{equation*}
$$

where $\mathrm{J}_{\mathrm{S}}$ is an effective torsion constant that based on elasticity theory, and generally depends on the material composition in addition to the cross-section geometry, and

$$
\begin{equation*}
G_{s} \equiv \sqrt{G_{X Z}^{s} G_{X Y}^{s}} \tag{A15b}
\end{equation*}
$$

For a stiffener with a rectangular cross-section of height $\frac{k}{}$ and thickness $t$, made of a homogeneous orthotropic material, Leknitskii ${ }^{143}$ gives an expression for the torsional stiffness that is equivalent to

$$
\begin{equation*}
\mathrm{J}_{\mathrm{S}}=\left(\frac{\mathrm{G}_{\mathrm{XZ}}}{\mathrm{G}_{\mathrm{XY}}}\right)^{\frac{1}{2}} \frac{t^{3} h}{3}\left\{1-\frac{96}{\pi^{5}} \frac{t}{h}\left(\frac{\mathrm{G}_{\mathrm{XZ}}}{\mathrm{G}_{\mathrm{XY}}}\right)^{\frac{1}{2}} \sum_{\mathrm{p}=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{\mathrm{p}}}{\mathrm{p}^{5}} \tanh \left(\frac{\mathrm{p} \pi h}{2 t}\left(\frac{\mathrm{G}_{\mathrm{XY}}}{\mathrm{G}_{\mathrm{XZ}}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{A16}
\end{equation*}
$$

The strain energy of a beam is obtained from the general definition given by the theory of elasticity; that is,

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\frac{1}{2} \iiint_{\mathrm{V}_{\mathrm{S}}}\left(\sigma_{\mathrm{XX}} \varepsilon_{\mathrm{XX}}+\sigma_{\mathrm{YY}} \varepsilon_{\mathrm{YY}}+\sigma_{\mathrm{ZZ}} \varepsilon_{\mathrm{ZZ}}+\sigma_{\mathrm{XY}} \gamma_{\mathrm{XY}}+\sigma_{\mathrm{XZ}} \gamma_{\mathrm{XZ}}+\sigma_{\mathrm{YZ}} \gamma_{\mathrm{YZ}}\right) \mathrm{dXdYdZ} \tag{A17}
\end{equation*}
$$

where $V_{s}$ denotes the volume of the material particles forming the beam stiffener. For the prismatic beams considered herein, the volume is the product of the cross-sectional area $A_{s}$ and the length $\mathrm{L}_{\mathrm{s}}$. Using equations (A2) and (A5) with (A17) gives the beam strain energy as

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\frac{1}{2} \int_{\mathrm{L}_{\mathrm{s}}}\left(\mathrm{Pe}_{\mathrm{XX}}^{\mathrm{o}}+\mathrm{M}_{\mathrm{Z}} \chi_{\mathrm{Z}}^{\mathrm{o}}+\mathrm{M}_{\mathrm{Y}} \chi_{\mathrm{Y}}^{\mathrm{o}}+\mathrm{V}_{\mathrm{Y}} \Gamma_{\mathrm{XY}}^{\mathrm{o}}+\mathrm{V}_{\mathrm{Z}} \Gamma_{\mathrm{XZ}}^{\mathrm{o}}+\mathrm{T} \tau^{\mathrm{o}}\right) \mathrm{dX} \tag{A18}
\end{equation*}
$$

For the analysis presented herein, it is convenient to define a vector of beam forces and moments by

$$
\{\mathcal{F}\}^{T}=\left\{\begin{array}{lllll}
P & V_{Y} & V_{Z} & M_{Z} & M_{Y} \tag{A19}
\end{array} \mathrm{~T}\right\}
$$

and strains by

$$
\left\{\varepsilon_{b}\right\}^{\mathbf{T}}=\left\{\begin{array}{llllll}
\mathrm{e}_{\mathrm{XX}}^{\circ} & \Gamma_{\mathrm{XY}}^{\circ} & \Gamma_{\mathrm{XZ}}^{\circ} & \chi_{\mathrm{Z}}^{\circ} & \chi_{\mathrm{Y}}^{\circ} & \tau^{\circ} \tag{A20}
\end{array}\right\}
$$

where the superscript " $\mathbf{T}$ " denotes matrix transposition. Then, equations (A7) and (A9) yield

$$
\begin{equation*}
\{\nmid\}=[\mathcal{C}]\left\{\varepsilon_{b}\right\} \tag{A21}
\end{equation*}
$$

where

$$
[\mathcal{C}]=\left[\begin{array}{cccccc}
\mathrm{EA}_{\mathrm{s}} & 0 & 0 & \mathrm{EA}_{\mathrm{s}} \overline{\mathrm{Y}} & \mathrm{EA}_{\mathrm{s}} \overline{\mathrm{Z}} & 0  \tag{A22}\\
\bullet & \mathrm{k}_{\mathrm{Y}} \mathrm{GA}_{\mathrm{s}} & 0 & 0 & 0 & -\mathrm{k}_{\mathrm{Y}} \mathrm{G} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{Z}} \\
\bullet & \bullet & \mathrm{k}_{\mathrm{Z}} \mathrm{GA}_{\mathrm{s}} & 0 & 0 & \mathrm{k}_{\mathrm{Z}} \mathrm{GA}_{\mathrm{s}} \overline{\mathrm{Y}} \\
\bullet & \bullet & \bullet & \mathrm{EI}_{\mathrm{ZZ}} & \mathrm{EI}_{\mathrm{YZ}} & 0 \\
\bullet & \bullet & \bullet & \bullet & \mathrm{EI}_{\mathrm{YY}} & 0 \\
\text { symmetric } & \bullet & \bullet & \bullet & \bullet & \mathrm{GJ}
\end{array}\right]
$$

is the constitutive matrix for a homogeneous beam made of isotropic material. For a heterogeneous beam made of, at most, specially orthotropic materials, equations (A14) and (A15) yield

$$
[\mathcal{C}]=\left[\begin{array}{cccccc}
\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{y}}_{\mathrm{s}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}} & 0  \tag{A23}\\
\bullet & \mathrm{k}_{\mathrm{Y}} \mathrm{G}_{\mathrm{YY}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & 0 & -\mathrm{k}_{\mathrm{Y}} \mathrm{G}_{\mathrm{XY}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{s}} \\
\bullet & \bullet & \mathrm{k}_{\mathrm{Z}} \mathrm{G}_{\mathrm{XZ}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & \mathrm{k}_{\mathrm{Z}} \mathrm{G}_{\mathrm{XZ}}^{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{s}} \\
\bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{ZZ}}^{\mathrm{s}} & \mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YZ}}^{\mathrm{s}} & 0 \\
\bullet & \bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{S}}^{\mathrm{s}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} & 0 \\
\text { symmetric } & \bullet & \bullet & \bullet & \bullet & \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{s}}
\end{array}\right]
$$

To obtain a matrix equation similar in form to equation (A22), it is convenient to introduce the stiffness-weight shear correction factors

$$
\begin{align*}
& k_{Y}^{s}=k_{Y} \sqrt{\frac{G_{X Y}^{s}}{G_{X Z}^{s}}}  \tag{A24a}\\
& k_{z}^{s}=k_{z} \sqrt{\frac{G_{X Z}^{s}}{G_{X Y}^{s}}} \tag{A24b}
\end{align*}
$$

such that equation (A23) becomes

$$
[\boldsymbol{C}]=\left[\begin{array}{cccccc}
\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{y}}_{\mathrm{s}} \mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}} & 0  \tag{A25}\\
\bullet & \mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & 0 & -\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{s}} \\
\bullet & \bullet & \mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} & 0 & 0 & \mathrm{k}_{\mathrm{z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{s}} \\
\bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{s}} \mathrm{I}_{\mathrm{ZZ}}^{\mathrm{s}} & \mathrm{E}_{\mathrm{s}} \mathrm{I}_{\mathrm{YZ}}^{\mathrm{s}} & 0 \\
\bullet & \bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{s}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} & 0 \\
\text { symmetric } & \bullet & \bullet & \bullet & \bullet & \mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}
\end{array}\right]
$$

Note that for a homogeneous beam, equation (A25) has the same structure as equation (A22). By using equations (A11) - (A15), the strain energy is expressed as

$$
\begin{equation*}
\varepsilon_{\varepsilon}=\frac{1}{2} \int_{\mathrm{L}_{\mathrm{s}}}\{\mathcal{7}\}^{\mathrm{T}}\left\{\varepsilon_{b}\right\} \mathrm{dX}=\frac{1}{2} \int_{\mathrm{L}_{\mathrm{s}}}\left\{\varepsilon_{b}\right\}^{\mathrm{T}}[\mathcal{C}]\left\{\varepsilon_{b}\right\} \mathrm{dX} \tag{A26}
\end{equation*}
$$

In equation (A25), ( $\mathrm{X}, \overline{\mathrm{y}}_{\mathrm{s}}, \overline{\mathrm{z}}_{\mathrm{s}}$ ) define the coordinates of a stiffness-weighted centroidal axis, shown in figures 6 and 11, which is coincident with the centroidal axis for prismatic beams with homogeneous cross sections. By defining the stiffness-weighted-centroidal coordinates $(\xi, \eta, \zeta)$ shown in figures 10 and 11, the effective quantities defined by equations (A13) yield

$$
\begin{align*}
& E_{S}=\frac{1}{A_{S}} \iint_{A_{S}} E_{X} d \eta d \zeta  \tag{A27a}\\
& G_{X Z}^{s}=\frac{1}{A_{S}} \iint_{A_{S}} G_{X Z} d \eta d \zeta  \tag{A27b}\\
& G_{X Y}^{s}=\frac{1}{A_{S}} \iint_{A_{S}} G_{X Y} d \eta d \zeta  \tag{A27c}\\
& \bar{\eta}_{S}=\frac{\iint_{A_{S}} E_{X} \eta d \eta d \zeta}{A_{S} E_{S}}=0  \tag{A27d}\\
& \bar{\xi}_{S}=\frac{\iint_{A_{S}} E_{X} \zeta d \eta d \zeta}{A_{S} E_{S}}=0 \tag{A27e}
\end{align*}
$$

$$
\begin{gather*}
\mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}=\mathrm{I}_{\eta \eta}^{\mathrm{s}}+\mathrm{A}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}}^{2}  \tag{A27f}\\
\mathrm{I}_{\mathrm{ZZ}}^{\mathrm{s}}=\mathrm{I}_{\zeta \zeta}^{\mathrm{s}}+\mathrm{A}_{\mathrm{s}} \overline{\mathrm{y}}_{\mathrm{s}}^{2}  \tag{A27g}\\
\mathrm{I}_{\mathrm{YZ}}^{\mathrm{s}}=\mathrm{I}_{\eta \zeta}^{\mathrm{s}}+\mathrm{A}_{\mathrm{s}} \overline{\mathrm{y}}_{\mathrm{s}} \overline{\mathrm{z}}_{\mathrm{s}}  \tag{A27h}\\
\overline{\overline{\mathrm{y}}}_{\mathrm{s}}=\overline{\bar{\eta}}_{\mathrm{s}}+\overline{\mathrm{y}}_{\mathrm{s}}  \tag{A27j}\\
\overline{\overline{\mathrm{z}}}_{\mathrm{s}}=\overline{\bar{\zeta}}_{\mathrm{s}}+\overline{\mathrm{z}}_{\mathrm{s}} \tag{A27k}
\end{gather*}
$$

with the stiffness-weighted-centroidal moments and product of inertia

$$
\begin{align*}
I_{\eta \eta}^{s} & =\frac{\iint_{A_{s}} E_{x} \zeta^{2} d \eta d \zeta}{E_{s}}  \tag{A28a}\\
I_{\zeta \xi}^{s} & =\frac{\iint_{A_{s}} E_{x} \eta^{2} d \eta d \zeta}{E_{s}}  \tag{A28b}\\
I_{\eta \zeta}^{s} & =\frac{\iint_{A_{s}} E_{x} \eta \zeta d \eta d \zeta}{E_{s}} \tag{A28c}
\end{align*}
$$

and the shear-stiffness-weighted first moments of area

$$
\begin{align*}
\bar{\xi}_{S} & =\frac{\iint_{A_{S}} G_{X Y} \zeta d \eta d \zeta}{A_{S} G_{X Y}^{S}}  \tag{A29a}\\
\overline{\bar{\eta}}_{S} & =\frac{\iint_{A_{S}} G_{X Z} \eta d \eta d \zeta}{A_{S} G_{X Z}^{S}} \tag{A29b}
\end{align*}
$$

For beams with homogeneous cross sections, the shear-stiffness-weighted first moments of area vanish and the stiffness-weighted-centroidal moments and product of inertia become the corresponding centroidal moments and product of inertia.

## Appendix B <br> Equivalent-Plate Stiffnesses for a Plate Reinforced with Eccentric Stringers, Ribs, and Diagonal Braces

The expressions presented in this appendix are for a general laminated-composite plate that is stiffened with stringers, ribs, and diagonal braces, as shown in figure 14 or figure 16. The stringers and ribs are eccentric with respect to the plate midplane and the pockets formed by the skin, stringers, and ribs are diagonally braced with two nonidentical families of eccentric stiffeners. The notation used for the material and section properties and orientation angle of each stiffener family is given in Tables 1 and 2 for the stiffener arrangements shown in figures 14 and 16 , respectively. In particular, the subscripts and superscripts " s " and " r " refer to quantities associated with the stringers and ribs, respectively. The subscripts and superscripts "d1" and "d2" refer to quantities associated with the two nonidentical families of diagonals. The stiffness expressions are obtained from equations (23) and (25)-(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Tables 1 and 2. The resulting equivalent-plate stiffnesses are given as follows where $n=1$ and $1 / 2$ for the stiffener arrangements shown in figures 14 and 16, respectively. In the expressions that follow, the stiffener extensional modulus, shear modulus, eccentricity, moment of inertia, torsion constant, and transverse-shear correction factors refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam. In addition, the length of the diagonal stiffeners is given by $\mathrm{L}_{\mathrm{d}}=\sqrt{\mathrm{L}_{\mathrm{x}}^{2}+\mathrm{L}_{\mathrm{y}}^{2}}$.

$$
\begin{align*}
& A_{11}=A_{11}^{\text {plate }}+\frac{E_{s} A_{s}}{L_{y}}+\frac{\boldsymbol{u} L_{x}^{3}}{L_{d}^{3} L_{y}}\left[E_{d 1} A_{d 1}\left(1+\tau_{Y}^{d 1} \frac{L_{y}^{2}}{L_{x}^{2}}\right)+E_{d 2} A_{d 2}\left(1+\tau_{Y}^{d 2} \frac{L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{B1}\\
& A_{12}=A_{12}^{\text {plate }}+\frac{\boldsymbol{u} L_{x} L_{y}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(1-\tau_{Y}^{d 1}\right)+E_{d 2} A_{d 2}\left(1-\tau_{Y}^{d 2}\right)\right]  \tag{B2}\\
& A_{16}=A_{16}^{\text {plate }}+\frac{\boldsymbol{u} L_{x}^{2}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(1-\frac{\tau_{Y}^{d 1}}{2}\left[1-\frac{L_{y}^{2}}{L_{x}^{2}}\right]\right)-E_{d 2} A_{d 2}\left(1-\frac{\tau_{Y}^{d 2}}{2}\left[1-\frac{L_{y}^{2}}{L_{x}^{2}}\right]\right)\right]  \tag{B3}\\
& A_{22}=A_{22}^{\text {plate }}+\frac{E_{r} A_{r}}{L_{x}}+\frac{\boldsymbol{u} L_{y}^{3}}{L_{d}^{3} L_{x}}\left[E_{d 1} A_{d 1}\left(1+\tau_{Y}^{d 1} \frac{L_{x}^{2}}{L_{y}^{2}}\right)+E_{d 2} A_{d 2}\left(1+\tau_{Y}^{d 2} \frac{L_{x}^{2}}{L_{y}^{2}}\right)\right]  \tag{B4}\\
& A_{26}=A_{26}^{\text {plate }}+\frac{\boldsymbol{u} L_{y}^{2}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(1-\frac{\tau_{Y}^{d 1}}{2}\left[1-\frac{L_{x}^{2}}{L_{y}^{2}}\right]\right)-E_{d 2} A_{d 2}\left(1-\frac{\tau_{Y}^{d 2}}{2}\left[1-\frac{L_{x}^{2}}{L_{y}^{2}}\right]\right)\right] \tag{B5}
\end{align*}
$$

$$
\begin{align*}
& A_{66}=A_{66}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{Y}^{s}}{4 L_{y}}+\frac{E_{r} A_{r} \tau_{Y}^{r}}{4 L_{x}}+  \tag{B6}\\
& \frac{\boldsymbol{u} L_{x} L_{y}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{4}\left[\frac{L_{x}}{L_{y}}-\frac{L_{y}}{L_{x}}\right]^{2}\right)+E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{4}\left[\frac{L_{x}}{L_{y}}-\frac{L_{y}}{L_{x}}\right]^{2}\right)\right] \\
& B_{11}=B_{11}^{\text {plate }}+\frac{E_{s} A_{s} \bar{z}_{s}}{L_{y}}+\frac{\boldsymbol{u} L_{x}^{3}}{L_{d}^{3} L_{y}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1} \frac{L_{y}^{2}}{L_{x}^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2} \frac{L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{B7}\\
& B_{12}=B_{12}^{\text {plate }}+\frac{\boldsymbol{u} L_{x} L_{y}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}-\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}-\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}\right)\right]  \tag{B8}\\
& B_{16}=B_{16}^{\text {plate }}+\frac{\boldsymbol{u} L_{x}^{2}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}-\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{2}\left(1-\frac{L_{y}^{2}}{L_{x}^{2}}\right)\right)-E_{d 2} A_{d 2}\left(\bar{z}_{d 2}-\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left(1-\frac{L_{y}^{2}}{L_{x}^{2}}\right)\right)\right]  \tag{B9}\\
& B_{22}=B_{22}^{\text {plate }}+\frac{E_{r} A_{r} \bar{Z}_{r}}{L_{x}}+\frac{\boldsymbol{u} L_{y}^{3}}{L_{d}^{3} L_{x}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1} \frac{L_{x}^{2}}{L_{y}^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2} \frac{L_{x}^{2}}{L_{y}^{2}}\right)\right]  \tag{B10}\\
& B_{26}=B_{26}^{\text {plate }}+\frac{\boldsymbol{u} L_{y}^{2}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}-\frac{\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1}}{2}\left(1-\frac{L_{x}^{2}}{L_{y}^{2}}\right)\right)-E_{d 2} A_{d 2}\left(\bar{z}_{d 2}-\frac{\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2}}{2}\left(1-\frac{L_{x}^{2}}{L_{y}^{2}}\right)\right)\right]  \tag{B11}\\
& B_{66}=B_{66}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{Y}^{s} \overline{\bar{Z}}_{s}}{4 L_{y}}+\frac{E_{r} A_{r} \tau_{Y}^{r} \overline{\bar{Z}}_{r}}{4 L_{x}}+  \tag{B12}\\
& \frac{\boldsymbol{u} L_{x} L_{y}}{L_{d}^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1}}{4}\left[\frac{L_{x}}{L_{y}}-\frac{L_{y}}{L_{x}}\right]^{2}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2}}{4}\left[\frac{L_{x}}{L_{y}}-\frac{L_{y}}{L_{x}}\right]^{2}\right)\right] \\
& \quad D_{11}=D_{11}^{\text {plate }}+\frac{E_{s} I_{s}}{L_{y}}+\frac{\boldsymbol{u} L_{x}^{3}}{L_{d}^{3} L_{y}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{L_{y}^{2}}{L_{x}^{2}}\right]  \tag{B13}\\
& \quad D_{12}=D_{12}^{\text {plate }}+\frac{\boldsymbol{u} L_{x} L_{y}}{L_{d}^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}-G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right] \tag{B14}
\end{align*}
$$

$$
\begin{gather*}
D_{16}=D_{16}^{\text {plate }}+\boldsymbol{u} \frac{L_{x}^{2}}{L_{d}^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{G_{d 2} J_{d 2}-G_{d 1} J_{d 1}}{2}\left(1-\frac{L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{B15}\\
D_{22}=D_{22}^{\text {plate }}+\frac{E_{r} I_{r}}{L_{x}}+\frac{\boldsymbol{n} L_{y}^{3}}{L_{x} L_{d}^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{L_{x}^{2}}{L_{y}^{2}}\right]  \tag{B16}\\
D_{26}=D_{26}^{\text {plate }}+\boldsymbol{n} \frac{L_{y}^{2}}{L_{d}^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{G_{d 1} J_{d 1}-G_{d 2} J_{d 2}}{2}\left(\frac{L_{x}^{2}}{L_{y}^{2}}-1\right)\right]  \tag{B17}\\
D_{66}=D_{66}^{\text {plate }}+\frac{1}{4}\left(\frac{G_{s} J_{s}}{L_{y}}+\frac{G_{r} J_{r}}{L_{x}}\right)+\frac{\boldsymbol{n} L_{x} L_{y}}{L_{d}^{3}}\left(E_{d 1} I_{d 1}+E_{d 2} I_{d 2}\right)+  \tag{B18}\\
A_{44}=A_{44}^{\text {plate }}+\frac{E_{r} A_{r} \tau_{Z}^{r}}{L_{x}}+\frac{\boldsymbol{n} L_{y}}{L_{x} L_{d}}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{Z}^{d 2}\right) \\
A_{45}=A_{45}^{\text {plate }}+\boldsymbol{n}\left(\frac{E_{d 1} A_{d 1} \tau_{z}^{d 1}-E_{d 2} A_{d 2} \tau_{z}^{d 2}}{4 L_{d}^{3}}\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right)\left(\frac{L_{x}}{L_{y}}-\frac{L_{y}}{L_{x}}\right)^{2}\right.  \tag{B19}\\
L_{d}=A_{55}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{Z}^{s}}{L_{y}}+\frac{\boldsymbol{n} L_{x}}{L_{y} L_{d}}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{z}^{d 2}\right) \tag{B20}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Y}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}}  \tag{B22}\\
& \tau_{\mathrm{Y}}^{\mathrm{r}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}}}{\mathrm{E}_{\mathrm{r}}}  \tag{B23}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{B24}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{B25}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Z}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}}  \tag{B26}\\
& \tau_{\mathrm{Z}}^{\mathrm{r}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}}}{\mathrm{E}_{\mathrm{r}}}  \tag{B27}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{B28}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{B29}
\end{align*}
$$

Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear deformation. For the special case of no diagonal braces, the stiffnesses reduce to

$$
\begin{align*}
& {\left[\begin{array}{lll}
A_{11} & A_{12} & A_{16} \\
A_{12} & A_{22} & A_{26} \\
A_{16} & A_{26} & A_{66}
\end{array}\right]=\left[\begin{array}{ccc}
A_{11}^{\text {plate }} & A_{12}^{\text {plate }} & A_{16}^{\text {plate }} \\
A_{12}^{\text {plate }} & A_{22}^{\text {plate }} & A_{26}^{\text {plate }} \\
A_{16}^{\text {plate }} & A_{26}^{\text {plate }} & A_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{ccc}
\frac{E_{s} A_{s}}{L_{y}} & 0 & 0 \\
0 & \frac{E_{r} A_{r}}{L_{x}} & 0 \\
0 & 0 & \frac{E_{s} A_{s} \tau_{Y}^{s}}{4 L_{y}}+\frac{E_{r} A_{r} \tau_{Y}^{r}}{4 L_{x}}
\end{array}\right]}  \tag{B30}\\
& {\left[\begin{array}{lll}
\mathrm{B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} \\
\mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} \\
\mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66}
\end{array}\right]=\left[\begin{array}{lll}
\mathrm{B}_{11}^{\text {plate }} & \mathrm{B}_{12}^{\text {plate }} & \mathrm{B}_{16}^{\text {plate }} \\
\mathrm{B}_{12}^{\text {plate }} & \mathrm{B}_{22}^{\text {plate }} & \mathrm{B}_{26}^{\text {plate }} \\
\mathrm{B}_{16}^{\text {plate }} & \mathrm{B}_{26}^{\text {plate }} & \mathrm{B}_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}} \overline{\mathrm{z}}_{\mathrm{s}} & 0 & 0 \\
0 & \frac{\mathrm{E}_{\mathrm{r}} \mathrm{~A}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}} \overline{\mathrm{Z}}_{\mathrm{r}} & 0 \\
0 & 0 & \frac{\mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Y}}^{\mathrm{s}}}{4 \mathrm{~L}_{\mathrm{y}}} \overline{\mathrm{z}}_{\mathrm{s}}+\frac{\mathrm{E}_{\mathrm{r}} \mathrm{~A}_{\mathrm{r}} \tau_{\mathrm{Y}}^{\mathrm{r}}}{4 \mathrm{~L}_{\mathrm{x}}} \overline{\mathrm{z}}_{\mathrm{r}}
\end{array}\right]}  \tag{B31}\\
& {\left[\begin{array}{lll}
\mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\mathrm{D}_{12} & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\mathrm{D}_{16} & \mathrm{D}_{26} & \mathrm{D}_{66}
\end{array}\right]=\left[\begin{array}{lll}
\mathrm{D}_{11}^{\text {plate }} & \mathrm{D}_{12}^{\text {plate }} & \mathrm{D}_{16}^{\text {plate }} \\
\mathrm{D}_{12}^{\text {plate }} & \mathrm{D}_{22}^{\text {plate }} & \mathrm{D}_{26}^{\text {plate }} \\
\mathrm{D}_{16}^{\text {plate }} & \mathrm{D}_{26}^{\text {plate }} & \mathrm{D}_{66}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{s}} \mathrm{I}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}} & 0 & 0 \\
0 & \frac{\mathrm{E}_{\mathrm{r}} \mathrm{I}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}} & 0 \\
0 & 0 & \frac{1}{4}\left(\frac{\mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}}+\frac{\mathrm{G}_{\mathrm{r}} \mathrm{~J}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}}\right)
\end{array}\right]}  \tag{B32}\\
& {\left[\begin{array}{ll}
A_{44} & A_{45} \\
A_{45} & A_{55}
\end{array}\right]=\left[\begin{array}{ll}
A_{44}^{\text {plate }} & A_{45}^{\text {plate }} \\
A_{45}^{\text {plate }} & A_{55}^{\text {plate }}
\end{array}\right]+\left[\begin{array}{cc}
\frac{E_{r} A_{r} \tau_{Z}^{r}}{L_{x}} & 0 \\
0 & \frac{E_{s} A_{s} \tau_{Z}^{s}}{L_{y}}
\end{array}\right]} \tag{B33}
\end{align*}
$$

## Appendix C <br> Equivalent-Plate Stiffnesses for a Plate Reinforced with an Isosceles-Triangle or Kagome Grid Stiffener Arrangement

The expressions presented in this appendix are for a general laminated-composite plate that is stiffened with stringers and two nonidentical families of diagonal braces, as shown in figure 17 or figure 18. The stringers and diagonal braces are eccentric with respect to the plate midplane and the pockets formed by the skin and stiffeners shown in figure 17 are isosceles triangles. The pockets shown in figure 18 for the Kagome grid are isosceles triangles and hexagons. The notation used for the material and section properties and orientation angle of each stiffener family is given in Table 3 for both stiffener arrangements. In particular, the subscripts and superscripts "s" refer to quantities associated with the stringers, and the subscripts and superscripts "d1" and "d2" refer to quantities associated with the two nonidentical families of diagonals. The stiffness expressions presented subsequently are obtained from equations (23) and (25)-(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Table 3. In the expressions that follow, the stiffener extensional modulus, shear modulus, eccentricity, moment of inertia, torsion constant, and transverse-shear correction factors refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam. In addition, the length of the diagonal stiffeners is given by $\mathrm{L}=\sqrt{\mathrm{L}_{\mathrm{x}}^{2}+\mathrm{L}_{\mathrm{y}}^{2}}$.

$$
\begin{gather*}
A_{11}=A_{11}^{\text {plate }}+\frac{E_{s} A_{s}}{L_{y}}+\frac{L_{x}^{3}}{16 L^{3} L_{y}}\left[E_{d 1} A_{d 1}\left(1+4 \tau_{Y}^{d 1} \frac{L_{y}^{2}}{L_{x}^{2}}\right)+E_{d 2} A_{d 2}\left(1+4 \tau_{Y}^{d 2} \frac{L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{C1}\\
A_{12}=A_{12}^{\text {plate }}+\frac{L_{x} L_{y}}{4 L^{3}}\left[E_{d 1} A_{d 1}\left(1-\tau_{Y}^{d 1}\right)+E_{d 2} A_{d 2}\left(1-\tau_{Y}^{d 2}\right)\right]  \tag{C2}\\
A_{16}=A_{16}^{\text {plate }}+\frac{L_{x}^{2}}{8 L^{3}}\left(E_{d 1} A_{d 1}\left[1-\frac{\tau_{Y}^{d 1}}{2}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]-E_{d 2} A_{d 2}\left[1-\frac{\tau_{Y}^{d 2}}{2}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]\right\}  \tag{C3}\\
A_{22}=A_{22}^{\text {plate }}+\frac{L_{y}^{3}}{L^{3} L_{x}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{4} \frac{L_{x}^{2}}{L_{y}^{2}}\right)+E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{4} \frac{L_{x}^{2}}{L_{y}^{2}}\right)\right]  \tag{C4}\\
A_{26}=A_{26}^{\text {plate }}+\frac{L_{y}^{2}}{2 L^{3}}\left\{E_{d 1} A_{d 1}\left[1-\frac{\tau_{Y}^{d 1}}{2}\left(1-\frac{L_{x}^{2}}{4 L_{y}^{2}}\right)\right]-E_{d 2} A_{d 2}\left[1-\frac{\tau_{Y}^{d 2}}{2}\left(1-\frac{L_{x}^{2}}{4 L_{y}^{2}}\right)\right]\right\}  \tag{C5}\\
A_{66}^{\text {stiffener }}=\frac{E_{s} A_{s} \tau_{Y}^{s}}{4 L_{y}}+\frac{L_{x} L_{y}}{4 L^{3}}\left\{E_{d 1} A_{d 1}\left[1+\tau_{Y}^{d 1} \frac{L_{x}^{2}}{16 L_{y}^{2}}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)^{2}\right]+E_{d 2} A_{d 2}\left[1+\tau_{Y}^{d 2} \frac{L_{x}^{2}}{16 L_{y}^{2}}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)^{2}\right]\right\} \tag{C6}
\end{gather*}
$$

$$
\begin{gather*}
B_{11}=B_{11}^{\text {plate }}+\frac{E_{s} A_{s} \bar{z}_{s}}{L_{y}}+\frac{L_{x}^{3}}{16 L^{3} L_{y}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+4 \tau_{Y}^{d 1} \overline{\bar{z}}_{d 1} \frac{L_{y}^{2}}{L_{x}^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+4 \tau_{Y}^{d 2} \overline{\bar{z}}_{d 2} \frac{L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{C7}\\
B_{12}=B_{12}^{\text {plate }}+\frac{L_{x} L_{y}}{4 L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}-\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}-\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}\right)\right]  \tag{C8}\\
B_{16}=B_{16}^{\text {plate }}+\frac{L_{x}^{2}}{8 L^{3}}\left\{E_{d 1} A_{d 1}\left[\bar{z}_{d 1}-\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{2}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]-E_{d 2} A_{d 2}\left[\bar{z}_{d 2}-\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]\right\}  \tag{C9}\\
B_{22}=B_{22}^{\text {plate }}+\frac{L_{y}^{3}}{L^{3} L_{x}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{4} \frac{L_{x}^{2}}{L_{y}^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{4} \frac{L_{x}^{2}}{L_{y}^{2}}\right)\right]  \tag{C10}\\
B_{26}=B_{26}^{\text {plate }}+\frac{L_{y}^{2}}{2 L^{3}}\left\{E_{d 1} A_{d 1}\left[\bar{z}_{d 1}-\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{2}\left(1-\frac{L_{x}^{2}}{4 L_{y}^{2}}\right)\right]-E_{d 2} A_{d 2}\left[\bar{z}_{d 2}-\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left(1-\frac{L_{x}^{2}}{4 L_{y}^{2}}\right)\right]\right\}  \tag{C11}\\
B_{66}=B_{66}^{\text {plate }}+\frac{E_{s} A \tau_{s} \tau_{Y}^{s}}{4 L_{y}} \overline{\bar{z}}_{s}+  \tag{C12}\\
\frac{L_{x} L_{y}}{4 L^{3}}\left\{E_{d 1} A_{d 1}\left[\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1} \frac{L_{x}^{2}}{16 L_{y}^{2}}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)^{2}\right]+E_{d 2} A_{d 2}\left[\bar{z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2} \frac{L_{x}^{2}}{16 L_{y}^{2}}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]\right\} \\
D_{11}=D_{11}^{\text {plate }}+\frac{E_{s} I_{s}}{L_{y}}+\frac{L_{x}^{3}}{16 L_{y} L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{4 L_{y}^{2}}{L_{x}^{2}}\right]  \tag{C13}\\
D_{12}=D_{12}^{\text {plate }}+\frac{L_{x} L_{y}}{4 L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}-G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right]  \tag{C14}\\
D_{16}=D_{16}^{\text {plate }}+\frac{L_{x}^{2}}{8 L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 2} J_{d 2}-G_{d 1} J_{d 1}\right)\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)\right]  \tag{C15}\\
D_{22}=D_{22}^{\text {plate }}+\frac{L_{y}^{3}}{L^{3} L_{x}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{L_{x}^{2}}{4 L_{y}^{2}}\right] \tag{C16}
\end{gather*}
$$

$$
\begin{gather*}
D_{26}=D_{26}^{\text {plate }}+\frac{L_{y}^{2}}{2 L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 2} J_{d 2}-G_{d 1} J_{d 1}\right)\left(1-\frac{L_{x}^{2}}{4 L_{y}^{2}}\right)\right]  \tag{C17}\\
D_{66}=D_{66}^{\text {plate }}+\frac{G_{s} J_{s}}{4 L_{y}}+\frac{L_{x} L_{y}}{4 L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{L_{x}^{2}}{16 L_{y}^{2}}\left(1-\frac{4 L_{y}^{2}}{L_{x}^{2}}\right)^{2}\right]  \tag{C18}\\
A_{44}=A_{44}^{\text {plate }}+\frac{L_{y}}{L L_{x}}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{z}^{d 2}\right)  \tag{C19}\\
A_{45}=A_{45}^{\text {plate }}+\frac{1}{2 L}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}-E_{d 2} A_{d 2} \tau_{z}^{d 2}\right)  \tag{C20}\\
A_{55}=A_{55}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{z}^{s}}{L_{y}}+\frac{L_{x}}{4 L L_{y}}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{z}^{d 2}\right) \tag{C21}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Y}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}}  \tag{C22}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{C23}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{C24}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Z}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}}  \tag{C25}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{C26}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{C27}
\end{align*}
$$

Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear deformation.

For the special case in which the triangle-shaped pockets enclosed by the stiffeners form equilateral triangles and the properties of all stiffeners are identical, $L_{x}=L$ and $L_{y}=\frac{\sqrt{3} L}{2}$ and the stiffnesses reduce to

$$
\begin{gather*}
{\left[\begin{array}{lll}
A_{11} & A_{12} & A_{16} \\
A_{12} & A_{22} & A_{26} \\
A_{16} & A_{26} & A_{66}
\end{array}\right]=\left[\begin{array}{ll}
A_{11}^{\text {plate }} & A_{12}^{\text {plate }} \\
A_{12}^{\text {plate }} & A_{16}^{\text {plate }} \\
A_{16}^{\text {plate }} & A_{26}^{\text {plate }} \\
A_{26}^{\text {plate }} & A_{66}^{\text {plate }}
\end{array}\right]+\frac{\sqrt{3} E_{\mathrm{s}} A_{\mathrm{s}}}{4 L}\left[\begin{array}{ccc}
3+\tau_{\mathrm{Y}}^{\mathrm{s}} & 1-\tau_{\mathrm{Y}}^{\mathrm{s}} & 0 \\
1-\tau_{\mathrm{Y}}^{\mathrm{s}} & 3+\tau_{\mathrm{Y}}^{\mathrm{s}} & 0 \\
0 & 0 & 1+\tau_{\mathrm{Y}}^{\mathrm{s}}
\end{array}\right]}  \tag{C28}\\
{\left[\begin{array}{lll}
B_{11} & B_{12} & B_{16} \\
B_{12} & B_{22} & B_{26} \\
B_{16} & B_{26} & B_{66}
\end{array}\right]=\left[\begin{array}{lll}
B_{11}^{\text {plate }} & B_{12}^{\text {plate }} & B_{16}^{\text {plate }} \\
B_{12}^{\text {plate }} & B_{22}^{\text {plate }} & B_{26}^{\text {plate }} \\
B_{16}^{\text {plate }} & B_{26}^{\text {plate }} & B_{66}^{\text {plate }}
\end{array}\right]+\frac{\sqrt{3} E_{\mathrm{s}} A_{\mathrm{s}}}{4 L}\left[\begin{array}{ccc}
3 \bar{z}_{\mathrm{s}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}} & \bar{z}_{\mathrm{s}}-\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}} & 0 \\
\bar{z}_{\mathrm{s}}-\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}} & 3 \bar{z}_{\mathrm{s}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}} & 0 \\
0 & 0 & \bar{z}_{\mathrm{s}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{s}}
\end{array}\right]}  \tag{C29}\\
{\left[\begin{array}{lll}
D_{11} & D_{12} & D_{16} \\
D_{12} & D_{22} & D_{26} \\
D_{16} & D_{26} & D_{66}
\end{array}\right]=\left[\begin{array}{ll}
D_{11}^{\text {plate }} & D_{12}^{\text {plate }} D_{16}^{\text {plate }} \\
D_{12}^{\text {plate }} & D_{22}^{\text {plate }} D_{26}^{\text {plate }} \\
D_{16}^{\text {plate }} & D_{26}^{\text {plate }} \\
D_{66}^{\text {plate }}
\end{array}\right]+\frac{\sqrt{3} E_{\mathrm{s}} I_{\mathrm{s}}}{4 L}\left[\begin{array}{ccc}
3+\frac{G_{\mathrm{s}} J_{\mathrm{s}}}{E_{\mathrm{s}} I_{\mathrm{s}}} & 1-\frac{G_{\mathrm{s}} J_{\mathrm{s}}}{E_{\mathrm{s}} I_{\mathrm{s}}} & 0 \\
1-\frac{G_{\mathrm{s}} J_{\mathrm{s}}}{E_{\mathrm{s}} I_{\mathrm{s}}} & 3+\frac{G_{\mathrm{s}} J_{\mathrm{s}}}{E_{\mathrm{s}} I_{\mathrm{s}}} & 0 \\
0 & 0 & 1+\frac{G_{\mathrm{s}} J_{\mathrm{s}}}{E_{\mathrm{s}} I_{\mathrm{s}}}
\end{array}\right]}  \tag{C30}\\
{\left[\begin{array}{l}
A_{44} \\
A_{45}
\end{array}\right]=\left[\begin{array}{ll}
A_{44}^{\text {plate }} & A_{45}^{\text {plate }} \\
A_{45}^{\text {plate }} & A_{55}^{\text {plate }}
\end{array}\right]+\frac{\sqrt{3} E_{\mathrm{s}} A_{\mathrm{s}} \tau_{\mathrm{z}}^{\mathrm{s}}}{L}\left[\begin{array}{ll}
1 & 0 \\
0 & 1
\end{array}\right]} \tag{C31}
\end{gather*}
$$

## Appendix D <br> Beam-Member Stiffness Coefficients

In the present study, it was found to be convenient to express equation (A25) as

$$
[\mathcal{C}]=\left[\begin{array}{cccccc}
\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} & 0 & 0 & \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\mathrm{y}}_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\mathrm{z}}_{\mathrm{S}} & 0  \tag{D1}\\
\bullet & \tau_{\mathrm{Y}}^{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} & 0 & 0 & 0 & -\tau_{\mathrm{Y}}^{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \\
\bullet & \bullet & \tau_{\mathrm{Z}}^{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} & 0 & 0 & \tau_{\mathrm{Z}}^{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \overline{\overline{\mathrm{y}}}_{\mathrm{S}} \\
\bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{ZZ}}^{\mathrm{S}} & \mathrm{E}_{\mathrm{S}}^{\mathrm{S}} \mathrm{I}_{\mathrm{YZ}}^{\mathrm{S}} & 0 \\
\bullet & \bullet & \bullet & \bullet & \mathrm{E}_{\mathrm{S}}^{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{S}} & 0 \\
\text { symmetric } & \bullet & \bullet & \bullet & \bullet & \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}
\end{array}\right]
$$

such that equation (36) yields the following nonzero elements of the symmetric matrix $\left[\mathscr{C}_{p}\right]$ :

$$
\begin{gather*}
\mathcal{C}_{11}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(\cos ^{2} \Psi_{\mathrm{S}}+\tau_{\mathrm{Y}}^{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\right)  \tag{D2}\\
\mathcal{C}_{12}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(1-\tau_{\mathrm{Y}}^{\mathrm{S}}\right)  \tag{D3}\\
\mathcal{C}_{13}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\cos ^{2} \Psi_{\mathrm{S}}-\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D4}\\
\mathcal{C}_{14}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\right)  \tag{D5}\\
\mathcal{C}_{15}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}}-\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}}\right)  \tag{D6}\\
\mathcal{C}_{16}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}} \cos ^{2} \Psi_{\mathrm{S}}-\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D7}\\
\mathcal{C}_{22}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\left(\sin ^{2} \Psi_{\mathrm{S}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \cos ^{2} \Psi_{\mathrm{S}}\right)  \tag{D8}\\
\mathcal{C}_{23}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\sin ^{2} \Psi_{\mathrm{S}}+\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D9}\\
\mathcal{C}_{24}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}}-\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}}\right) \tag{D10}
\end{gather*}
$$

$$
\begin{gather*}
\mathcal{C}_{25}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}+\tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\right)  \tag{D11}\\
\mathcal{C}_{26}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}+\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\bar{z}}_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D12}\\
\mathcal{C}_{33}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}\left(\sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}+\frac{1}{4} \tau_{\mathrm{Y}}^{\mathrm{s}} \cos ^{2} 2 \Psi_{\mathrm{S}}\right)  \tag{D13}\\
\mathcal{C}_{34}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}-\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D14}\\
\mathcal{C}_{35}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}+\frac{1}{2} \tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D15}\\
\mathcal{C}_{36}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}}\left(\overline{\mathrm{z}}_{\mathrm{S}} \sin { }^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}+\frac{1}{4} \tau_{\mathrm{Y}}^{\mathrm{s}} \overline{\overline{\mathrm{z}}}_{\mathrm{S}} \cos { }^{2} 2 \Psi_{\mathrm{S}}\right)  \tag{D16}\\
\mathcal{C}_{45}^{p}=\cos ^{2} \Psi_{\mathrm{S}}\left(\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} \cos ^{2} \Psi_{\mathrm{S}}+\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} \sin ^{2} \Psi_{\mathrm{S}}\right)  \tag{D17}\\
\mathcal{C}_{46}^{p}=\sin \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}\left(\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}-\mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}\right)  \tag{D18}\\
\mathcal{C}_{47}^{p}=\sin ^{2} \Psi_{\mathrm{S}} \cos ^{2} \Psi_{\mathrm{S}}-\frac{1}{2} \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{S}}  \tag{D19}\\
\mathcal{C}_{48}^{p}=\cos ^{2} \Psi_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{S}}  \tag{D20}\\
\mathcal{C}_{55}^{p}=\sin ^{2} \Psi_{\mathrm{S}}\left(\cos ^{2} \Psi_{\mathrm{S}} \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}}+\sin ^{2} \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}}\right)  \tag{D21}\\
\mathcal{C}_{56}^{p}=\sin \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}}\left(\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} \sin { }^{2} \Psi_{\mathrm{S}}+\frac{1}{2} \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}}\right)  \tag{D22}\\
\mathcal{C}_{57}^{p}=-\sin ^{2} \Psi_{\mathrm{S}} \cos \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{S}}  \tag{D23}\\
\mathcal{C}_{58}^{p}=-\cos ^{2} \Psi_{\mathrm{S}} \sin \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{S}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\overline{\mathrm{y}}}_{\mathrm{S}}  \tag{D24}\\
\mathcal{C}_{66}^{p}=\mathrm{E}_{\mathrm{S}} \mathrm{I}_{\mathrm{YY}}^{\mathrm{s}} \sin ^{2} \Psi_{\mathrm{S}} \cos { }^{2} \Psi_{\mathrm{S}}+\frac{1}{4} \mathrm{G}_{\mathrm{S}} \mathrm{~J}_{\mathrm{S}} \cos { }^{2} 2 \Psi_{\mathrm{S}} \tag{D25}
\end{gather*}
$$

$$
\begin{gather*}
\mathcal{C}_{67}^{p}=-\frac{1}{2} \sin \Psi_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\bar{y}}_{\mathrm{s}}  \tag{D27}\\
\mathcal{C}_{68}^{p}=-\frac{1}{2} \cos \Psi_{\mathrm{S}} \cos 2 \Psi_{\mathrm{S}} \mathrm{E}_{\mathrm{S}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}} \overline{\bar{y}}_{\mathrm{s}}  \tag{D28}\\
\mathcal{C}_{77}^{p}=\sin ^{2} \Psi_{\mathrm{s}} \mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}}  \tag{D29}\\
\mathcal{C}_{78}^{p}=\sin \Psi_{\mathrm{s}} \cos \Psi_{\mathrm{s}} \mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}}  \tag{D30}\\
\mathcal{C}_{88}^{p}=\cos ^{2} \Psi_{\mathrm{s}} \mathrm{E}_{\mathrm{s}} \mathrm{~A}_{\mathrm{s}} \tau_{\mathrm{Z}}^{\mathrm{s}} \tag{D31}
\end{gather*}
$$

where

$$
\begin{equation*}
\tau_{\mathrm{Y}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{S}}}{\mathrm{E}_{\mathrm{S}}} \tag{D32}
\end{equation*}
$$

is an inplane-shear-deformation parameter and

$$
\begin{equation*}
\tau_{\mathrm{Z}}^{\mathrm{S}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{S}} \mathrm{G}_{\mathrm{S}}}{\mathrm{E}_{\mathrm{S}}} \tag{D33}
\end{equation*}
$$

is a transverse-shear-deformation parameter. Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear deformation.

## Appendix E

## Mathematica ${ }^{\circledR}$ Program for the Basic-Cell Energy-Equivalence Method

The computer program ${ }^{142}$ used in the present study to determine the contribution of the stiffeners to the equivalent-continuum plate stiffnesses, based on the basic-cell energy-equivalence method described herein, is presented subsequently. The input used in this program for the orthogonal stiffener arrangement with diagonal braces shown in figure 14 is given in Table 4 and the output is presented in Appendix B, where $\boldsymbol{n}=1$. IGRID = 1 corresponds to the special case in which the stiffening grid has no diagonal braces and the stringers are generally different from the ribs (see figure 14a). In contrast, IGRID = 2 corresponds to the general case in which the stiffening grid has two nonidentical families of diagonal braces in addition to the stringers and ribs. For IGRID = 3, all diagonal braces are identical. Similarly, the input used in the program for the orthogonal stiffener arrangement with diagonal braces shown in figure 16 is given in Table 5 and the output is presented in Appendix B, where $\boldsymbol{n}=1 / 2$. IGRID = 4 corresponds to the general case in which the stiffening grid has two nonidentical families of diagonal braces in addition to the stringers and ribs. For IGRID $=5$, all diagonal braces are identical.

The input used in this program for the isosceles-triangle stiffener arrangement shown in figure 17 is given in Table 6 and the output is presented in Appendix C. IGRID $=6$ corresponds to the general case in which the stiffening grid has two nonidentical families of diagonal braces that are different from the stringers (see figure 17a). IGRID $=7$ corresponds to the special case of an equilateral-triangle grid with identical braces and stringers. Similarly, the input used in this program for the Kagome stiffener arrangement, with two nonidentical families of diagonal braces that are different from the stringers, shown in figure 18 (IGRID $=8$ ) is given in Table 7 and the output was found to be identical to that presented in Appendix C for the isosceles-triangle stiffener arrangement.

The input used in the program for the hexagon-shaped stiffener arrangement shown in figure 21 is given in Table 8 and the output is presented in Appendix F. IGRID = 9 corresponds to the general case in which one pair of opposite sides have a different length and different properties than the remaining sides, and the properties of each family of diagonal members are different. IGRID = 10 corresponds to the special case of an equilateral hexagon-shaped stiffener arrangement with identical side lengths and identical diagonal members.

The input used in the program for the star-shaped stiffener arrangement shown in figure 23 is given in Table 9 and the output is presented in Appendix G. IGRID = 11 corresponds to the general case in which the star shape is made from identical isosceles triangles with coincident centroids, and the two families of diagonal members have different properties. IGRID = 12 corresponds to the special case in which the star shape is made from identical equilateral triangles with coincident centroids, and with identical diagonal members.

IGRID = 13 corresponds to the hexagon-shaped core of the stiffened plate shown in figure 25. For this case, the core is made of isosceles hexagons formed by beams with rectangular cross sections, and is centered on plane $\mathrm{z}=0$, as shown in figure 25 . The basic cell for this case is identical to that shown in figure 21b. Likewise, IGRID = 14 is for the special case in which the
core is made of isotropic beams with the same length. The output for these cases is presented in Appendix H.

IGRID $=15$ corresponds to the star-shaped core of the stiffened plate shown in figure 27. For this case, the core is made of isosceles-star shapes formed by beams with rectangular cross sections, and is centered on plane $\mathrm{z}=0$, as shown in figure 27. The basic cell for this case is identical to that shown in figure 23b. Likewise, IGRID = 16 is for the special case in which the core is made of isotropic beams with the same length. The output for these cases is presented in Appendix J.

In the computer program listing that follows, the user-defined input is given by the single red line that indicates a selection for the IGRID variable. The program is then executed by using the "evaluate notebook" Mathematica ${ }^{\circledR}$ command. For each of the stiffener arrangements defined by IGRID, the $(\mathrm{x}, \mathrm{y})$ coordinates of the starting point and ending point of members forming a given basic cell are arranged in row vectors, in ascending order. For example, the starting and ending points, or nodes, of the members in the basic cell shown in figure 14b correspond to the filled red circles and are numbered from 1 to 8 . The corresponding row vectors for the coordinates of the nodes, specified in ascending order from 1 to 8, are

$$
\left.\begin{array}{rlrrlrr}
\mathrm{x}=\{-\mathrm{Lx} / 2, & \mathrm{Lx} / 2, & 0, & 0, & -\mathrm{Lx} / 2, & \mathrm{Lx} / 2, & \mathrm{Lx} / 2, \\
\mathrm{y}= & 0, \mathrm{Lx} / 2\} \\
\mathrm{y}= & 0, & -\mathrm{Ly} / 2, & \mathrm{Ly} / 2, & -\mathrm{Ly} / 2, & \mathrm{Ly} / 2, & -\mathrm{Ly} / 2, \\
\mathrm{Oy} / 2
\end{array}\right\}
$$

Next, the starting and ending node number and the geometric and material properties of each beam member forming a given basic cell are specified in a table. For example, the table for the basic cell shown in figure 14b is given by

```
PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
    {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,Ly},
    {5,6,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld},
    {7,8,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld}}
```

Each row in this table corresponds to one beam member of the basic cell shown in figure 14b. The nomenclature follows that given in Table 4 and Appendix D.

Upon forming the geometry and material properties of the specified basic cell, the strain energy of each member in the basic cell is computed by using equation (37) and then summed and divided by the area of the basic cell, as indicated by equation (39a). To obtain this equivalent-continuum strain-energy density, $\cos \Psi_{\mathrm{S}}$ and $\sin \Psi_{\mathrm{S}}$ for each beam member in the basic cell are computed by using the nodal coordinates the length of each member. This calculation enables formation of the transformation matrix given by equation (34a). Then the beam constitutive matrix given by equation (D1) is formed, the strain-equivalence matrix given by equation (30d) is formed, and the calculations indicated by equations (32) and (36) are performed. It is important to note that the matrix elements of equation (D1) are the effective, noncentroidal values. All the calculations are completed within a "DO LOOP" that corresponds to the summation symbol in equation (39a). Upon forming the equivalent-continuum strain-energy density, the contributions of the stiffeners to the equivalent-plate stiffnesses are calculated following equations (43). The code that performs
these calculations is given as follows.

```
(**************************************************************************)
(* LIST OF STIFFENER ARRANGEMENTS *)
(* *)
(* IGRID=1 Orthogonal Grid of ribs and stringers *)
(* Orthogonal Grid of ribs and stringers with two *)
(* nonidentical braces per bay *)
(* Orthogonal Grid of ribs and stringers with two *)
(* identical braces per bay *)
(* Orthogonal Grid of ribs and stringers with nonidentical *)
(* braces and one brace per bay *)
(* Orthogonal Grid of ribs and stringers with identical *)
(* braces and one brace per bay *)
(* 6 Isosceles-Triangle Grid with nonidentical diagonals *)
(* Equilateral-Triangle Grid with identical members *)
(* 8 KAGOME Grid depicted in figure 18 with *)
(* nonidentical diagonals *)
(* Isosceles-Hexagon Grid with nonidentical diagonals *)
(* 10 Equilateral-Hexagon Grid with identical diagonals *)
(* 11 Isosceles-star-cell Grid with nonidentical diagonals *)
(* Equilateral-star-cell Grid with identical diagonals *)
(* 13 Isosceles-Hexagon Core made of rectangular-cross-section *)
(* beams and with identical diagonals *)
(* Equilateral-Hexagon Core made of rectangular-cross-section *)
(* isotropic beams *)
(* 15 Isosceles-star-cell Core with identical diagonals *)
(* 16 Equilateral-star-cell Core with identical isotropic members*)
(*************************************************************************)
IGRID = 3; (* SELECT GRID-STIFFENER ARRANGEMENT *)
If[IGRID == 1, {
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 2, CellArea = Lx Ly,
        x = {-Lx/2, Lx/2, 0, 0},
        y = { 0, 0, -Ly/2, Ly/2},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,Ly} } }];
If[IGRID == 2, {
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 4, CellArea = Lx Ly,
        x = {-Lx/2, Lx/2, 0, 0, -Lx/2, Lx/2, Lx/2, -Lx/2},
        y = { 0, 0, -Ly/2, Ly/2, -Ly/2, Ly/2, -Ly/2, Ly/2},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,Ly},
            {5,6,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld},
            {7,8,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld} } }];
If[IGRID==3,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 4,CellArea=Lx Ly,
        x={-Lx/2, Lx/2, 0, 0, -Lx/2, Lx/2, Lx/2, -Lx/2},
        y={ 0, 0, -Ly/2, Ly/2, -Ly/2, Ly/2, -Ly/2, Ly/2},
```

```
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,Ly},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld},
            {7,8,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld} } }];
If[IGRID==4,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 6,CellArea = 4Lx Ly,
        x={-Lx, Lx, 0, 0, -Lx, Lx, Lx, -Lx},
        y={ 0, 0, -Ly, Ly, -Ly, Ly, -Ly, Ly},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,2Lx},
            {5,7, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, 2Lx },
            {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,2Ly},
            {5,8,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,2Ly},
            {5,6,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,2Ld},
            {7,8,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,2Ld} } }];
If[IGRID==5,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=6,CellArea=4Lx Ly,
        x={-Lx, Lx, 0, 0, -Lx, Lx, Lx, -Lx},
        y={ 0, 0, -Ly, Ly, -Ly, Ly, -Ly, Ly},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,2Lx},
            {5,7, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, 2Lx },
            {3,4,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,2Ly},
            {5,8,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,2Ly},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,2Ld},
            {7,8,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,2Ld} } }];
If[IGRID==6,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=3,CellArea=Lx Ly,
        x={-Lx/2, Lx/2, -Lx/4, Lx/4, Lx/4, -Lx/4},
        y={ 0, 0, -Ly/2, Ly/2, -Ly/2, Ly/2},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld},
            {5,6,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld} } }];
If[IGRID==7,{
    (* SET PROPERTY EQUALITIES FOR IDENTICAL MEMBERS AND SPECIAL CASE CRITERIA *)
        Lx=L,Ly=Sqrt[3]/2 L,Ld=L,Ad=As,Ed=Es,Gd=Gs,Jd=Js,
        YBd=YBs,Y2Bd=Y2Bs,ZBd=ZBs,Z2Bd=Z2Bs,IYd=IYs,IZd=IZs,IYZd=IYZs,
        TauYd=TauYs,TauZd=TauZs,
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=3,CellArea=Lx Ly,
        x={-Lx/2, Lx/2, -Lx/4, Lx/4, Lx/4, -Lx/4},
        y={ 0, 0, -Ly/2, Ly/2, -Ly/2, Ly/2},
```

```
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={ {1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld} } }];
If[IGRID==8,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=4,CellArea=2 Lx Ly,
        x={-Lx/2, Lx/2, -Lx/2, Lx/2, -Lx/2, Lx/2, Lx/2, -Lx/2},
        y={-Ly/2, -Ly/2, Ly/2, Ly/2, -Ly, Ly, -Ly, Ly},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={ {1,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,Lx},
            {3,4, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, Lx },
            {5,6,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,2L},
            {7,8,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,2L} } }];
If[IGRID==9,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=5,CellArea=2*a*(b+c),
        x={ 0, 0/2, -a/2, 0/2, 0, -a/2},
        y = \{ - ( b + c ) / 2 , ~ - c / 2 , ~ - ( b + c ) / 2 , ~ ( b + c ) / 2 , ~ c / 2 , ~ ( b + c ) / 2 \} ,
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{2,1,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,L/2},
            {2,3,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,L/2},
            {2,5,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,C},
            {5,4,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,L/2},
            {5,6,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,L/2} } }];
If[ IGRID==10,{
    (* SET PROPERTY EQUALITIES FOR IDENTICAL MEMBERS AND SPECIAL CASE CRITERIA *)
        a=Sqrt[3]/2 L,b=L/2,C=L,
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers =5,CellArea = 2*a*(b+c),
        x={ 0, 0/2, -a/2, a/2, 0, -a/2},
```

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-123.jpg?height=33&width=836&top_left_y=1800&top_left_x=335)

```
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{2,1,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,3,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,5,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,C},
            {5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2} } }];
If[ IGRID==11,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 12, CellArea = 4 B H/3,
        x={B/3, B/2, B/6, 0, -B/6, -B/2, -B/3, -B/2, -B/6, 0, B/6, B/2},
        y={ 0, H/3, H/3, 2 H/3, H/3, H/3, 0, -H/3, -H/3, -2 H/3, -H/3, -H/3},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,12,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld/3},
```

```
            {1,2,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld/3},
            {3,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {3,4,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld/3},
            {5,4,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld/3},
            {5,6,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {7,6,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2,Ld/3},
            {7,8,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld/3},
            {9,8,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {9,10,Ed2,Ad2,YBd2,Y2Bd2,ZBd2,Z2Bd2,IYd2,IZd2,IYZd2,Gd2,TauYd2,TauZd2,Jd2, Ld/3},
            {11,10,Ed1,Ad1,YBd1,Y2Bd1,ZBd1,Z2Bd1,IYd1,IZd1,IYZd1,Gd1,TauYd1,TauZd1,Jd1,Ld/3},
            {11,12,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3} } }];
If[IGRID==12,{
        H=Sqrt[3] L/2,B= L,Ld=L,
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 12,CellArea = 4 B H/3,
        x={B/3, B/2, B/6, 0, -B/6, -B/2, -B/3, -B/2, -B/6, 0, B/6, B/2},
        y={ 0, H/3, H/3, 2 H/3, H/3, H/3, 0, -H/3, -H/3, -2 H/3, -H/3, -H/3},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        PROPS={{1,12,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {1,2,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {3,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {3,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {5,6, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, B/3 ,
            {7,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {7,8,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {9,8,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {9,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd, Ld/3},
            {11,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {11,12,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3} } }];
If[IGRID==13,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers =5,CellArea = 2*a*(b+c),
        x={ 0, a/2, -a/2, a/2, 0, -a/2},
        y={-(b+c)/2, -c/2, -(b+c)/2, (b+c)/2, c/2, (b+c)/2},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        Ad=hc td,
        Ar=hc tr,
        ZBd=0,
        Z2Bd=0,
        ZBr=0,
        Z2Br=0,
        IYd=hc^3 td/12,
        IZd=td^3 hc/12,
        IYZd=0,
        IYr = hc^3 tr/12,
        IZr=tr^3 hc/12,
        IYZr=0,
        PROPS={{2,1,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,3,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,5,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,C},
            {5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2} } }];
If[IGRID==14,{
        a=Sqrt[3]/2 L,b=L/2,C=L,
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers=5,CellArea=2*a*(b+c),
```

```
        x={ 0, a/2, -a/2, a/2, 0, -a/2},
        y = \{ - ( b + c ) / 2 , - c / 2 , - ( b + c ) / 2 , ( b + c ) / 2 , ~ c / 2 , ( b + c ) / 2 \} ,
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        Ad=hc td,
        Ar=hc tr,
        ZBd=0,
        Z2Bd=0,
        ZBr=0,
        Z2Br=0,
        IYd=hc^3 td/12,
        IZd=td^3 hc/12,
        IYZd=0,
        IYr=hc^3 tr/12,
        IZr=tr^3 hc/12,
        IYZr=0,
        Ed=EE,Er=EE,Gd=G,Gr=G,TauYd=k G/EE, TauYr=k G/EE,TauZd=k G/EE,TauZr=k G/EE,
        Jd=td^3 hc/3(1-Kd),Jr=tr^3 hc/3(1-Kr),
        PROPS={{2,1,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,3,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {2,5,Er,Ar,YBr,Y2Br,ZBr,Z2Br,IYr,IZr,IYZr,Gr,TauYr,TauZr,Jr,C},
            {5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2},
            {5,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,L/2} } }];
If[IGRID==15,{
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 12, CellArea = 4 B H/3,
        x={B/3, B/2, B/6, 0, -B/6, -B/2, -B/3, -B/2, -B/6, 0, B/6, B/2},
        y={ 0, H/3, H/3, 2 H/3, H/3, H/3, 0, -H/3, -H/3, -2 H/3, -H/3, -H/3},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        As = ts hc,Ad = td hc,IYs = ts hc^3/12,IYd = td hc^3/12,
        ZBd=0,ZBs=0,Z2Bd=0,Z2Bs=0,Js=ts^3 hc/3(1-Ks),Jd=td^3 hc/3(1-Kd),
        PROPS={{1,12,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {1,2,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {3,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {3,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {5,6, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, B/3 ,
            {7,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {7,8,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {9,8, Es, As, YBs, Y2Bs, ZBs, Z2Bs, IYs, IZs, IYZs, Gs, TauYs, TauZs, Js, B/3 },
            {9,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd, Ld/3},
            {11,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {11,12,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3} } }];
If[IGRID==16,{
        B=L,H=Sqrt[3] L/2,
    (* DEFINE THE NUMBER OF MEMBERS, THE AREA OF THE BASIC CELL, AND *)
    (* THE SEQUENTIAL GLOBAL (x, y) NODAL COORDINATES AS ROW VECTORS *)
        NMembers = 12,CellArea = 4 B H/3,
        x={B/3, B/2, B/6, 0, -B/6, -B/2, -B/3, -B/2, -B/6, 0, B/6, B/2},
        y={ 0, H/3, H/3, 2 H/3, H/3, H/3, 0, -H/3, -H/3, -2 H/3, -H/3,-H/3},
    (* DEFINE A TABLE OF BEAM-MEMBER BEGINNING AND ENDING NODES AND *)
    (* PROPERTIES FOR THE BASIC CELL *)
        Ld=L,
        As = t hc,Ad = t hc,IYs = t hc^3/12,IYd = t hc^3/12,
        ZBd=0,ZBs=0,Z2Bd=0,Z2Bs=0,Js = t^3 hc/3 (1-KK),Jd = t^3 hc/3 (1-KK),
        Es=EE,Ed=EE,Gs=G,Gd=G,TauYd=k G/EE, TauYs=k G/EE,TauZd=k G/EE,TauZs=k G/EE,
        PROPS={{1,12,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {1,2,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
            {3,2,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
            {3,4, Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
```

```
{5,4,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
{5,6,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
{7,6,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
{7,8,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
{9,8,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3},
{9,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd, Ld/3},
{11,10,Ed,Ad,YBd,Y2Bd,ZBd,Z2Bd,IYd,IZd,IYZd,Gd,TauYd,TauZd,Jd,Ld/3},
{11,12,Es,As,YBs,Y2Bs,ZBs,Z2Bs,IYs,IZs,IYZs,Gs,TauYs,TauZs,Js,B/3} } }];
```

```
(*************************************************************************)
(* BEGIN A DO-LOOP THAT COMPUTES THE STRAIN ENERGY CONTRIBUTION OF EACH *)
(* BEAM MEMBER TO THE STRAIN ENERGY OF THE EQUIVALENT CONTINUUM *)
(* *)
(* THE CURRENT BEAM MEMBER IN THE LOOP IS IDENTIED BY THE INDEX K *)
(*************************************************************************)
(* INITIALIZE THE STRAIN-ENERGY OF THE EQUIVALENT CONTINUUM *)
StrainEnergy = 0;
Do[
(* COMPUTE GLOBAL COORDINATES OF THE CURRENT BEAM MEMBER IJ *)
    xI = x[[ PROPS[[K, 1]] ]];
    xJ = x[[ PROPS[[K, 2]] ]];
    yI = y[[ PROPS[[K, 1]] ]];
    yJ = y[[ PROPS[[K, 2]] ]];
(* COMPUTE THE LENGTH OF THE CURRENT BEAM MEMBER *)
    LengthIJ = PROPS[[K, 16]];
(* COMPUTE m = COS(psi) and n = SIN(psi) FOR THE CURRENT BEAM MEMBER *)
    m = (xJ - xI)/LengthIJ;
    n = (yJ - yI)/LengthIJ;
(* COMPUTE THE PROPERTIES OF THE CURRENT BEAM MEMBER *)
EX=PROPS[[K,3]];
A=PROPS[[K,4]];
Ybar=PROPS[[K,5]];
Y2bar=PROPS[[K,6]];
Zbar=PROPS[[K,7]];
Z2bar=PROPS[[K,8]];
IYY=PROPS[[K,9]];
IZZ=PROPS[[K,10]];
IYZ=PROPS[[K,11]];
G=PROPS[[K,12]];
TauY=PROPS[[K,13]];
TauZ=PROPS[[K,14]];
J=PROPS[[K,15]];
(* COMPUTE THE STIFFNESS MATRIX FOR THE CURRENT BEAM MEMBER; see equation (D1) *)
C11 = EX A;
C14 = EX A Ybar;
C15 = EX A Zbar;
C22 = EX A TauY;
C26 = -EX A TauY Z2bar;
C33 = EX A TauZ;
C36 = EX A TauZ Y2bar;
C44 = EX IZZ;
C45 = EX IYZ;
C55 = EX IYY;
C66 = G J;
    Cmatrix = { { C11, 0, 0, C14, C15, 0},
        { 0, C22, 0, 0, C26},
        { 0, 0, C33, 0, 0, C36},
        {C14, 0, 0, C44, C45, 0},
        {C15, 0, 0, C45, C55, 0},
        { 0, C26, C36, 0, 0, C66} };
```

```
(* COMPUTE THE TRANSFORMED STIFFNESS MATRIX FOR THE CURRENT BEAM MEMBER; see equations (30)-(36) *)
Ematrix = { { 1, 0, 0, 0, 0, 0, 0, 0},
                    { 0, 0, 1/2, 0, 0, 0, 0, 0},
```

![](https://cdn.mathpix.com/cropped/b3ae0505-0ab3-497f-b5e0-d185accedd45-127.jpg?height=33&width=523&top_left_y=408&top_left_x=468)

```
                    {0, 0, 0, 0, 0, 0, 0, 0},
                    { 0, 0, 0, 1, 0, 0, 0, 0},
                    {0, 0, 0, 0, 0, -1/2, 0, 0} };
CPmatrix = Transpose[Ematrix].Cmatrix.Ematrix;
    Transformationmatrix = {
            { m^2, m*n, 0, 0, 0, 0, 0},
            { n^2, m*2, 0, 0, 0, 0},
            {-2*m*n, 2*m*n, m^2-n^2, 0, 0, 0, 0},
            { 0, 0, m^2, m^2, m*n, 0, 0},
            {0, 0, -2*m*n, 2*m*n, m^2-n^2, 0, 0},
            { 0, 0, 0, 0, m, -n},
            { 0, 0, 0, 0, n, m} };
    Cpmatrix = Transpose[Transformationmatrix].CPmatrix.Transformationmatrix;
(* COMPUTE STRAIN ENERGY CONTRIBUTION OF THE CURRENT BEAM MEMBER; see equation (37) *)
    StrainList = {epxx, epyy, gamxy, kapxx, kapyy, kapxy, gamyz, gamxz};
    MemberStrainEnergy = LengthIJ/2 StrainList.Cpmatrix.StrainList;
(* ADD THE STRAIN-ENERGY CONTRIBUTION OF THE CURRENT BEAM MEMBER TO THE *)
(* CONTINUUM STRAIN ENERGY; see equation (39a) *)
        StrainEnergy = StrainEnergy + MemberStrainEnergy,
                (* CLOSE DO-LOOP *) {K, 1, NMembers } ]
(* COMPUTE THE TOTAL STRAIN ENERGY DENSITY OF THE EQUIVALENT CONTINNUM; see equation (39a) *)
        StrainEnergyDensity = StrainEnergy/CellArea;
(* COMPUTE THE A-MATRIX OF FIRST-ORDER TRANSVERSE-SHEAR DEFORMATION PLATE THEORY; see equation (43a) *)
Print["Astiffener11 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, epxx] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener12 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, epyy] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener16 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, gamxy] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener22 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epyy, epyy] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener26 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epyy, gamxy] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener66 = ", FullSimplify[Factor[ D[StrainEnergyDensity, gamxy, gamxy] ] ] ];
Print[" "]; Print[" "]; Print[" "];
(* COMPUTE THE B-MATRIX OF FIRST-ORDER TRANSVERSE-SHEAR DEFORMATION PLATE THEORY; see equation (43b) *)
Print["Bstiffener11 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, kapxx] ] ] ];
Print[" "]; Print[" "];
Print["Bstiffener12 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, kapyy] ] ] ];
Print[" "]; Print[" "];
Print["Bstiffener16 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epxx, kapxy] ] ] ];
Print[" "]; Print[" "];
```

```
Print["Bstiffener22 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epyy, kapyy] ] ] ];
Print[" "]; Print[" "];
Print["Bstiffener26 = ", FullSimplify[Factor[ D[StrainEnergyDensity, epyy, kapxy] ] ] ];
Print[" "]; Print[" "];
Print["Bstiffener66 = ", FullSimplify[Factor[ D[StrainEnergyDensity, gamxy, kapxy] ] ] ];
Print[" "]; Print[" "]; Print[" "];
(* COMPUTE THE D-MATRIX OF FIRST-ORDER TRANSVERSE-SHEAR DEFORMATION PLATE THEORY; see equation (43c) *)
Print["Dstiffener11 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapxx, kapxx] ] ] ];
Print[" "]; Print[" "];
Print["Dstiffener12 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapxx, kapyy] ] ] ];
Print[" "]; Print[" "];
Print["Dstiffener16 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapxx, kapxy] ] ] ];
Print[" "]; Print[" "];
Print["Dstiffener22 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapyy, kapyy] ] ] ];
Print[" "]; Print[" "];
Print["Dstiffener26 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapyy, kapxy] ] ] ];
Print[" "]; Print[" "];
Print["Dstiffener66 = ", FullSimplify[Factor[ D[StrainEnergyDensity, kapxy, kapxy] ] ] ];
Print[" "]; Print[" "]; Print[" "];
(* COMPUTE THE TRANSVERSE-SHEAR STIFFNESS MATRIX OF FIRST-ORDER TRANSVERSE-SHEAR DEFORMATION PLATE
    THEORY; see equation (43d) *)
Print["Astiffener44 = ", FullSimplify[Factor[ D[StrainEnergyDensity, gamyz, gamyz] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener45 = ", FullSimplify[Factor[ D[StrainEnergyDensity, gamyz, gamxz] ] ] ];
Print[" "]; Print[" "];
Print["Astiffener55 = ", FullSimplify[Factor[ D[StrainEnergyDensity, gamxz, gamxz] ] ] ];
Print[" "]; Print[" "]; Print[" "];
(* RE-INITIALIZE MATHEMATICA *)
    Remove["Globalˋ*"];
(* CHANGE INPUT AND SELECT "EVALUATE NOTEBOOK" UNDER THE EVALUATION MENU ON THE MATHEMATICA WINDOW HEADER *)
```


## Appendix F <br> Equivalent-Plate Stiffnesses for a Plate Reinforced with a Hexagon-Shaped Stiffener Arrangement

The expressions presented in this appendix are for a general laminated-composite plate that is stiffened with ribs and two nonidentical families of diagonal braces, as shown in figure 21. The ribs and diagonals are eccentric with respect to the plate midplane and the pockets formed by the skin and stiffeners shown in figure 21 are isosceles hexagons; that is, the two pairs of diagonal members have the same length, which is generally different from the length of the two identical ribs. The notation used for the material and section properties and the orientation angle of each stiffener family is given in Table 8. In this table and the expressions that follow, the subscript and superscript " r " refers to the ribs and the subscripts and superscripts "d1" and "d2" refer to the two nonidentical families of diagonals. The stiffness expressions presented subsequently are obtained from equations (23) and (25)-(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Table 8. In the expressions that follow, the stiffener extensional modulus, shear modulus, eccentricity, moment of inertia, torsion constant, and the transverseshear correction factors refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam.

$$
\begin{align*}
A_{11} & =A_{11}^{\text {plate }}+\frac{a^{3}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(1+\tau_{Y}^{d 1} \frac{b^{2}}{a^{2}}\right)+E_{d 2} A_{d 2}\left(1+\tau_{Y}^{d 2} \frac{b^{2}}{a^{2}}\right)\right]  \tag{F1}\\
A_{12} & =A_{12}^{\text {plate }}+\frac{a b^{2}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(1-\tau_{Y}^{d 1}\right)+E_{d 2} A_{d 2}\left(1-\tau_{Y}^{d 2}\right)\right]  \tag{F2}\\
A_{16} & =A_{16}^{\text {plate }}+\frac{a^{2} b}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Z}^{d 1}}{2}\left[\frac{b^{2}}{a^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{2}\left[\frac{b^{2}}{a^{2}}-1\right]\right)\right]  \tag{F3}\\
A_{22} & =A_{22}^{\text {plate }}+\frac{E_{r} A_{r} c}{2 a(b+c)}+\frac{b^{4}}{2 a(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(1+\tau_{Y}^{d 1} \frac{a^{2}}{b^{2}}\right)+E_{d 2} A_{d 2}\left(1+\tau_{Y}^{d 2} \frac{a^{2}}{b^{2}}\right)\right]  \tag{F4}\\
A_{26} & =A_{26}^{\text {plate }}+\frac{b^{3}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{2}\left[\frac{a^{2}}{b^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{2}\left[\frac{a^{2}}{b^{2}}-1\right]\right)\right] \tag{F5}
\end{align*}
$$

$$
\begin{align*}
& \mathrm{A}_{66}=\mathrm{A}_{66}^{\text {plate }}+\frac{\mathrm{E}_{\mathrm{r}} \mathrm{~A}_{\mathrm{r}} \tau_{\mathrm{Y}}^{\mathrm{r}} \mathrm{c}}{8 \mathrm{a}(\mathrm{~b}+\mathrm{c})}+  \tag{F6}\\
& \frac{a b^{2}}{2(b+c) L^{3}}\left\{E_{d 1} A_{d 1}\left[1+\frac{\tau_{Y}^{d 1}}{4}\left(\frac{a^{2}-b^{2}}{a b}\right)^{2}\right]+E_{d 2} A_{d 2}\left[1+\frac{\tau_{Y}^{d 2}}{4}\left(\frac{a^{2}-b^{2}}{a b}\right)^{2}\right]\right\} \\
& B_{11}=B_{11}^{\text {plate }}+\frac{a^{3}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1} \frac{b^{2}}{a^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2} \frac{b^{2}}{a^{2}}\right)\right]  \tag{F7}\\
& B_{12}=B_{12}^{\text {plate }}+\frac{a b^{2}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1} \bar{Z}_{d 1}\left(1-\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1}\right)+E_{d 2} A_{d 2} \bar{Z}_{d 2}\left(1-\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2}\right)\right]  \tag{F8}\\
& B_{16}=B_{16}^{\text {plate }}+\frac{a^{2} b}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1}}{2}\left[\frac{b^{2}}{a^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(\bar{Z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2}}{2}\left[\frac{b^{2}}{a^{2}}-1\right]\right)\right]  \tag{F9}\\
& \mathrm{B}_{22}=\mathrm{B}_{22}^{\text {plate }}+\frac{\mathrm{E}_{\mathrm{r}} \mathrm{~A}_{\mathrm{r}} \mathrm{c} \overline{\mathrm{z}}_{\mathrm{r}}}{2 \mathrm{a}(\mathrm{~b}+\mathrm{c})}+ \\
& \frac{b^{4}}{2 a(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1} \frac{a^{2}}{b^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{Z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2} \frac{a^{2}}{b^{2}}\right)\right]  \tag{F10}\\
& B_{26}=B_{26}^{\text {plate }}+\frac{b^{3}}{2(b+c) L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d l} \overline{\bar{z}}_{d 1}}{2}\left[\frac{a^{2}}{b^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left[\frac{a^{2}}{b^{2}}-1\right]\right)\right]  \tag{F11}\\
& B_{66}=B_{66}^{\text {plate }}+\frac{E_{r} A_{r} c}{8 a(b+c)} \tau_{Y}^{r} \overline{\bar{Z}}_{r}+  \tag{F12}\\
& \frac{a b^{2}}{2(b+c) L^{3}}\left\{E_{d 1} A_{d 1}\left[\bar{Z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{Z}}_{d 1}}{4}\left(\frac{a^{2}-b^{2}}{a b}\right)^{2}\right]+E_{d 2} A_{d 2}\left[\bar{Z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{Z}}_{d 2}}{4}\left(\frac{a^{2}-b^{2}}{a b}\right)^{2}\right]\right\} \\
& D_{11}=D_{11}^{\text {plate }}+\frac{a^{3}}{2(b+c) L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{b^{2}}{a^{2}}\right] \tag{F13}
\end{align*}
$$

$$
\begin{gather*}
D_{12}=D_{12}^{\text {plate }}+\frac{a b^{2}}{2(b+c) L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}-G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right]  \tag{F14}\\
D_{16}=D_{16}^{\text {plate }}+\frac{a^{2} b}{2(b+c) L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right)\left(\frac{b^{2}}{a^{2}}-1\right)\right]  \tag{F15}\\
D_{22}=D_{22}^{\text {plate }}+\frac{E_{r} I_{r} c}{2 a(b+c)}+\frac{b^{4}}{2 a(b+c) L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{a^{2}}{b^{2}}\right]  \tag{F16}\\
D_{26}=D_{26}^{\text {plate }}+\frac{b^{3}}{2(b+c) L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right)\left(\frac{a^{2}}{b^{2}}-1\right)\right]  \tag{F17}\\
D_{66}=D_{66}^{\text {plate }}+\frac{c G_{r} J_{r}}{8 a(b+c)}+\frac{a b^{2}}{2(b+c) L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right)\left(\frac{a^{2}-b^{2}}{2 a b}\right)^{2}\right]  \tag{F18}\\
A_{44}=A_{44}^{\text {plate }}+\frac{\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{Z}^{d 2}\right) b^{2}+E_{r} A_{r} \tau_{Y}^{r} c L}{2 a(b+c) L}  \tag{F19}\\
A_{45}=A_{45}^{\text {plate }}+\frac{\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}-E_{d 2} A_{d 2} \tau_{z}^{d 2}\right) b}{2(b+c) L}  \tag{F20}\\
A_{55}=A_{55}^{\text {plate }}+\frac{\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{Z}^{d 2}\right) a}{2(b+c) L} \tag{F21}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Y}}^{\mathrm{r}} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}}}{\mathrm{E}_{\mathrm{r}}}  \tag{F22}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{F23}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Y}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{F24}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Z}}^{\mathrm{r}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}}}{\mathrm{E}_{\mathrm{r}}}  \tag{F25}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 1} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 1} \mathrm{G}_{\mathrm{d} 1}}{\mathrm{E}_{\mathrm{d} 1}}  \tag{F26}\\
& \tau_{\mathrm{Z}}^{\mathrm{d} 2} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d} 2} \mathrm{G}_{\mathrm{d} 2}}{\mathrm{E}_{\mathrm{d} 2}} \tag{F27}
\end{align*}
$$

Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear deformation.

For the special case in which all stiffeners have the same length, $a=\frac{\sqrt{3} \mathrm{~L}}{2}, b=\mathrm{L} / 2$, and $\mathrm{c}=\mathrm{L}$. For this simplification and for identical families of diagonals, the stiffnesses reduce to

$$
\begin{gather*}
A_{11}=A_{11}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(1+\frac{\tau_{Y}^{d}}{3}\right)  \tag{F22}\\
A_{12}=A_{12}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{12 L}\left(1-\tau_{Y}^{d}\right)  \tag{F23}\\
A_{16}=A_{16}^{\text {plate }}  \tag{F24}\\
A_{22}=A_{22}^{\text {plate }}+\frac{\sqrt{3}}{36 L}\left[8 E_{r} A_{r}+E_{d} A_{d}\left(1+3 \tau_{Y}^{d}\right)\right]  \tag{F25}\\
A_{26}=A_{26}^{\text {plate }}  \tag{F26}\\
A_{66}=A_{66}^{\text {plate }}+\frac{\sqrt{3}}{12 L}\left[\frac{2 E_{r} A_{r} \tau_{Y}^{r}}{3}+E_{d} A_{d}\left(1+\frac{\tau_{Y}^{d}}{3}\right)\right]  \tag{F27}\\
B_{11}=B_{11}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(\bar{z}_{d}+\frac{\tau_{Y}^{d} \overline{\bar{Z}}_{d}}{3}\right)  \tag{F28}\\
B_{12}=B_{12}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{12 L}\left(\bar{Z}_{d}-\tau_{Y}^{d} \overline{\bar{Z}}_{d}\right) \tag{F29}
\end{gather*}
$$

$$
\begin{gather*}
B_{16}=B_{16}^{\text {plate }}  \tag{F30}\\
B_{22}=B_{22}^{\text {plate }}+\frac{\sqrt{3}}{36 L}\left[8 E_{r} A_{r} \bar{Z}_{r}+E_{d} A_{d} \bar{Z}_{d}\left(\bar{Z}_{d}+3 \tau_{Y}^{d} \overline{\bar{Z}}_{d}\right)\right]  \tag{F31}\\
B_{26}=B_{26}^{\text {plate }}  \tag{F32}\\
B_{66}=B_{66}^{\text {plate }}+\frac{\sqrt{3}}{12 L}\left[\frac{2 E_{r} A_{r} \tau_{Y}^{r} \overline{\bar{Z}}_{r}}{3}+E_{d} A_{d}\left(\bar{Z}_{d}+\frac{\tau_{Y}^{d} \overline{\bar{Z}}_{d}}{3}\right)\right]  \tag{F33}\\
D_{11}=D_{11}^{\text {plate }}+\frac{\sqrt{3}}{4 L}\left(E_{d} I_{d}+\frac{G_{d} J_{d}}{3}\right)  \tag{F34}\\
D_{12}=D_{12}^{\text {plate }}+\frac{\sqrt{3}}{12 L}\left(E_{d} I_{d}-G_{d} J_{d}\right)  \tag{F35}\\
D_{16}=D_{16}^{\text {plate }}  \tag{F36}\\
D_{22}=D_{22}^{\text {plate }}+\frac{\sqrt{3}}{36 L}\left(8 E_{r} I_{r}+E_{d} I_{d}+3 G_{d} J_{d}\right)  \tag{F37}\\
D_{26}=D_{26}^{\text {plate }}  \tag{F38}\\
D_{66}=D_{66}^{\text {plate }}+\frac{\sqrt{3}}{36 L}\left(3 E_{d} I_{d}+2 G_{r} J_{r}+G_{d} J_{d}\right)  \tag{F39}\\
A_{44}=A_{44}^{\text {plate }}+\frac{\sqrt{3}}{9 L}\left(E_{d} A_{d} \tau_{Z}^{d}+2 E_{r} A_{r} \tau_{Z}^{r}\right)  \tag{F40}\\
A_{45}=A_{45}^{\text {plate }}  \tag{F41}\\
A_{55}=A_{55}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d} \tau_{Z}^{d}}{3 L} \tag{F42}
\end{gather*}
$$

where the subscript and superscript "d" indicates the properties of the diagonal stiffeners.

## Appendix G <br> Equivalent-Plate Stiffnesses for a Plate Reinforced with a Star-Cell-Shaped Stiffener Arrangement

The expressions presented in this appendix are for a general laminated-composite plate that is stiffened with stringers and two nonidentical families of diagonal braces, as shown in figure 23. The stringers and diagonals are eccentric with respect to the plate midplane and the pockets formed by the skin and stiffeners shown in figure 23 are star shapes, formed by isosceles triangles, and isosceles hexagons. The two pairs of diagonal members have the same length, which is generally different from the length of the two identical stringers. The notation used for the material and section properties and orientation angle of each stiffener family is given in Table 9. The stiffness expressions presented subsequently are obtained from equations (23) and (25)-(28) by applying equations (25)-(28) to each family of stiffeners with the attributes given in Table 9. In the expressions that follow, the stiffener extensional modulus, shear modulus, eccentricity, moment of inertia, torsion constant, and transverse-shear correction factors refer to the corresponding effective quantities defined in Appendix A for a nonhomogeneous, specially orthotropic beam. The subscript and superscript "s" refers to the stringers and the subscripts and superscripts "d1" and "d2" refer to the two nonidentical families of diagonals.

$$
\begin{gather*}
A_{11}=A_{11}^{\text {plate }}+\frac{E_{s} A_{s}}{H}+\frac{B^{3}}{16 H L^{3}}\left[E_{d 1} A_{d 1}\left(1+4 \tau_{Y}^{d 1} \frac{H^{2}}{B^{2}}\right)+E_{d 2} A_{d 2}\left(1+4 \tau_{Y}^{d 2} \frac{H^{2}}{B^{2}}\right)\right]  \tag{G1}\\
A_{12}=A_{12}^{\text {plate }}+\frac{B H}{4 L^{3}}\left[E_{d 1} A_{d 1}\left(1-\tau_{Y}^{d 1}\right)+E_{d 2} A_{d 2}\left(1-\tau_{Y}^{d 2}\right)\right]  \tag{G2}\\
A_{16}=A_{16}^{\text {plate }}+\frac{B^{2}}{8 L^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{2}\left[\frac{4 H^{2}}{B^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{2}\left[\frac{4 H^{2}}{B^{2}}-1\right]\right)\right]  \tag{G3}\\
A_{22}=A_{22}^{\text {plate }}+\frac{H^{3}}{B L^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{4} \frac{B^{2}}{H^{2}}\right)+E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{4} \frac{B^{2}}{H^{2}}\right)\right]  \tag{G4}\\
A_{26}=A_{26}^{\text {plate }}+\frac{H^{2}}{2 L^{3}}\left[E_{d 1} A_{d 1}\left(1+\frac{\tau_{Y}^{d 1}}{2}\left[\frac{B^{2}}{4 H^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(1+\frac{\tau_{Y}^{d 2}}{2}\left[\frac{B^{2}}{4 H^{2}}-1\right]\right)\right]  \tag{G5}\\
A_{66}=A_{66}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{Y}^{s}}{4 H}+\frac{B H}{4 L^{3}}\left(E_{d 1} A_{d 1}\left[1+\tau_{Y}^{d 1}\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\right]+E_{d 2} A_{d 2}\left[1+\tau_{Y}^{d 2}\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\right]\right) \tag{G6}
\end{gather*}
$$

$$
\begin{gather*}
B_{11}=B_{11}^{\text {plate }}+\frac{E_{s} A_{s} \bar{z}_{s}}{H}+\frac{B^{3}}{16 H L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+4 \tau_{Y}^{d 1} \overline{\bar{z}}_{d 1} \frac{H^{2}}{B^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+4 \tau_{Y}^{d 2} \overline{\bar{z}}_{d 2} \frac{H^{2}}{B^{2}}\right)\right]  \tag{G7}\\
B_{12}=B_{12}^{\text {plate }}+\frac{B H}{4 L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}-\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}-\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}\right)\right]  \tag{G8}\\
B_{16}=B_{16}^{\text {plate }}+\frac{B^{2}}{8 L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{2}\left[\frac{4 H^{2}}{B^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left[\frac{4 H^{2}}{B^{2}}-1\right]\right)\right]  \tag{G9}\\
B_{22}=B_{22}^{\text {plate }}+\frac{H^{3}}{B L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{4} \frac{B^{2}}{H^{2}}\right)+E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{4} \frac{B^{2}}{H^{2}}\right)\right]  \tag{G10}\\
B_{26}=B_{26}^{\text {plate }}+\frac{H^{2}}{2 L^{3}}\left[E_{d 1} A_{d 1}\left(\bar{z}_{d 1}+\frac{\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}}{2}\left[\frac{B^{2}}{4 H^{2}}-1\right]\right)-E_{d 2} A_{d 2}\left(\bar{z}_{d 2}+\frac{\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}}{2}\left[\frac{B^{2}}{4 H^{2}}-1\right]\right)\right]  \tag{G11}\\
B_{66}=B_{66}^{\text {plate }}+\frac{E_{s} A_{s} \tau_{Y}^{s} \overline{\bar{z}}_{s}}{4 H}+ \\
\frac{B H}{4 L^{3}}\left(E_{d 1} A_{d 1}\left[\bar{z}_{d 1}+\tau_{Y}^{d 1} \overline{\bar{z}}_{d 1}\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\right]+E_{d 2} A_{d 2}\left[\bar{z}_{d 2}+\tau_{Y}^{d 2} \overline{\bar{z}}_{d 2}\left(\frac{B}{4 H}-\frac{H}{B}\right)\right]\right\}  \tag{G12}\\
D_{11}=D_{11}^{D^{p l a t e}}+\frac{E_{s} I_{s}}{H}+\frac{B^{3}}{16 H L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\frac{4 H^{2}}{B^{2}}\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right)\right]  \tag{G13}\\
D_{12}=D_{12}^{\text {plate }}+\frac{B H}{4 L^{3}}\left(E_{d 1} I_{d 1}+E_{d 2} I_{d 2}-G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right)  \tag{G14}\\
D_{16}=D_{16}^{\text {plate }}+\frac{B^{2}}{8 L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right)\left[\frac{4 H^{2}}{B^{2}}-1\right]\right]  \tag{G15}\\
D_{22}=D_{22}^{\text {plate }}+\frac{H^{3}}{B L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right) \frac{B^{2}}{4 H^{2}}\right] \tag{G16}
\end{gather*}
$$

$$
\begin{gather*}
D_{26}=D_{26}^{\text {plate }}+\frac{H^{2}}{2 L^{3}}\left[E_{d 1} I_{d 1}-E_{d 2} I_{d 2}+\frac{1}{2}\left(G_{d 1} J_{d 1}-G_{d 2} J_{d 2}\right)\left[\frac{B^{2}}{4 H^{2}}-1\right]\right]  \tag{G17}\\
D_{66}=D_{66}^{\text {plate }}+\frac{G_{s} J_{s}}{4 H}+\frac{B H}{4 L^{3}}\left[E_{d 1} I_{d 1}+E_{d 2} I_{d 2}+\left(G_{d 1} J_{d 1}+G_{d 2} J_{d 2}\right)\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\right]  \tag{G18}\\
A_{44}=A_{44}^{\text {plate }}+\frac{H}{B L}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{z}^{d 2}\right)  \tag{G19}\\
A_{45}=A_{45}^{\text {plate }}+\frac{1}{2 L}\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}-E_{d 2} A_{d 2} \tau_{z}^{d 2}\right)  \tag{G20}\\
A_{55}=A_{55}^{\text {plate }}+\frac{4 E_{s} A_{s} \tau_{z}^{s} L+\left(E_{d 1} A_{d 1} \tau_{z}^{d 1}+E_{d 2} A_{d 2} \tau_{z}^{d 2}\right) B}{4 H L} \tag{G21}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Y}}^{\mathrm{s}} \equiv \frac{k_{\mathrm{Y}}^{\mathrm{s}} G_{\mathrm{s}}}{E_{\mathrm{s}}}  \tag{G22}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 1} \equiv \frac{k_{\mathrm{Y}}^{\mathrm{d} 1} G_{\mathrm{d} 1}}{E_{\mathrm{d} 1}}  \tag{G23}\\
& \tau_{\mathrm{Y}}^{\mathrm{d} 2} \equiv \frac{k_{\mathrm{Y}}^{\mathrm{d} 2} G_{\mathrm{d} 2}}{E_{\mathrm{d} 2}} \tag{G24}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Z}}^{\mathrm{s}} \equiv \frac{k_{\mathrm{Z}}^{\mathrm{s}} G_{\mathrm{s}}}{E_{\mathrm{s}}}  \tag{G25}\\
& \tau_{\mathrm{z}}^{\mathrm{d} 1} \equiv \frac{k_{\mathrm{z}}^{\mathrm{d} 1} G_{\mathrm{d} 1}}{E_{\mathrm{d} 1}}  \tag{G26}\\
& \tau_{\mathrm{z}}^{\mathrm{d} 2} \equiv \frac{k_{\mathrm{z}}^{\mathrm{d} 2} G_{\mathrm{d} 2}}{E_{\mathrm{d} 2}} \tag{G27}
\end{align*}
$$

Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear
deformation.
For the special case of equilateral-star cells with identical diagonals $B=L$ and $H=\frac{\sqrt{3}}{2} L$ and the stiffnesses reduce to

$$
\begin{gather*}
A_{11}=A_{11}^{\text {plate }}+\frac{2 \sqrt{3} E_{s} A_{s}}{3 L}+\frac{\sqrt{3} E_{d} A_{d}}{12 L}\left(1+3 \tau_{Y}^{d}\right)  \tag{G28}\\
A_{12}=A_{12}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(1-\tau_{Y}^{d}\right)  \tag{G29}\\
A_{16}=A_{16}^{\text {plate }}  \tag{G30}\\
A_{22}=A_{22}^{\text {plate }}+\frac{3 \sqrt{3} E_{d} A_{d}}{4 L}\left(1+\frac{\tau_{Y}^{d}}{3}\right)  \tag{G31}\\
A_{26}=A_{26}^{\text {plate }}  \tag{G32}\\
A_{66}=A_{66}^{\text {plate }}+\frac{\sqrt{3} E_{s} A_{s} \tau_{Y}^{s}}{6 L}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(1+\frac{\tau_{Y}^{d}}{3}\right)  \tag{G33}\\
B_{11}=B_{11}^{\text {plate }}+\frac{2 \sqrt{3} E_{s} A_{s} \bar{z}_{s}}{3 L}+\frac{\sqrt{3} E_{d} A_{d}}{12 L}\left(\bar{z}_{d}+3 \tau_{Y}^{d} \overline{\bar{Z}}_{d}\right)  \tag{G34}\\
B_{12}=B_{12}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(\bar{z}_{d}-\tau_{Y}^{d} \overline{\bar{Z}}_{d}\right)  \tag{G35}\\
B_{16}=B_{16}^{\text {plate }}  \tag{G36}\\
B_{22}=B_{22}^{\text {plate }}+\frac{3 \sqrt{3} E_{d} A_{d}}{4 L}\left(\bar{z}_{d}+\frac{\tau_{Y}^{d} \overline{\bar{Z}}_{d}}{3}\right)  \tag{G37}\\
B_{26}=B_{26}^{\text {plate }}  \tag{G38}\\
B_{66}=B_{66}^{\text {plate }}+\frac{\sqrt{3} E_{s} A_{s} \tau_{Y}^{s} \overline{\bar{Z}}_{s}}{6 L}+\frac{\sqrt{3} E_{d} A_{d}}{4 L}\left(\bar{z}_{d}+\frac{\tau_{Y}^{d} \overline{\bar{Z}}_{d}}{3}\right) \tag{G39}
\end{gather*}
$$

$$
\begin{gather*}
D_{11}=D_{11}^{\text {plate }}+\frac{2 \sqrt{3} E_{s} I_{s}}{3 L}+\frac{\sqrt{3}}{12 L}\left(E_{d} I_{d}+3 G_{d} J_{d}\right)  \tag{G40}\\
D_{12}=D_{12}^{\text {plate }}+\frac{\sqrt{3}}{4 L}\left(E_{d} I_{d}-G_{d} J_{d}\right)  \tag{G41}\\
D_{16}=D_{16}^{\text {plate }}  \tag{G42}\\
D_{22}=D_{22}^{\text {plate }}+\frac{3 \sqrt{3}}{4 L}\left(E_{d} I_{d}+\frac{G_{d} J_{d}}{3}\right)  \tag{G43}\\
D_{26}=D_{26}^{\text {plate }}  \tag{G44}\\
D_{66}=D_{66}^{\text {plate }}+\frac{\sqrt{3} G_{s} J_{s}}{6 L}+\frac{\sqrt{3}}{4 L}\left(E_{d} I_{d}+\frac{G_{d} J_{d}}{3}\right)  \tag{G45}\\
A_{44}=A_{44}^{\text {plate }}+\frac{\sqrt{3} E_{d} A_{d} \tau_{Z}^{d}}{L}  \tag{G46}\\
A_{45}=A_{45}^{\text {plate }}  \tag{G47}\\
A_{55}=A_{55}^{\text {plate }}+\frac{\sqrt{3}}{3 L}\left(2 E_{s} A_{s} \tau_{Z}^{s}+E_{d} A_{d} \tau_{Z}^{d}\right) \tag{G48}
\end{gather*}
$$

where the subscript and superscript "d" indicates the properties of the diagonal stiffeners.

## Appendix H <br> Equivalent-Plate Stiffnesses for a Hexagon-Cell-Core Sandwich Plate

The equivalent-plate stiffnesses for a sandwich plate composed of two different, anisotropic, laminated-composite face plates and the hexagon-cell core, made of a homogeneous orthotropic material, shown in figure 25 are presented in this appendix. The thicknesses of the bottom face plate (plate no. 1), the top face plate (plate no. 2), and the core are denoted by $\mathrm{h}_{1}, \mathrm{~h}_{2}$, and $\mathrm{h}_{\mathrm{c}}$, respectively. The plate reference plane is located at the midplane of the core and the eccentricities of face plates no. 1 and no. 2 are given by $e_{1}=-\frac{1}{2}\left(h_{1}+h_{c}\right)$ and $e_{2}=\frac{1}{2}\left(h_{2}+h_{c}\right)$, respectively. The core is composed of two member types. One member type is aligned with the $y$-axis of the plate, as shown in figures 21 and 25, and is referred to herein as a rib. The other member type makes an angle $\Phi$ with the x-axis and is referred to herein as a diagonal. Member attributes associated with the ribs and diagonals are indicated subsequently with the subscripts or superscripts " r " and " d ," respectively.

For a hexagon-core stiffener arrangement with each member made of a homogeneous orthotropic material, the effective moduli given by equations (A13a)-(A13c) reduce to the corresponding principal moduli of the orthotropic material, where the principal orthotropicmaterial axes are coincident with the $\mathrm{X}, \mathrm{Y}$, and Z beam coordinate axes shown in figure 6. Thus, the symbols $\mathrm{E}_{\mathrm{r}}$ and $\mathrm{E}_{\mathrm{d}}$ denote the extensional modulus $\mathrm{E}_{\mathrm{X}}$ and the symbols $\mathrm{G}_{\mathrm{r}}$ and $\mathrm{G}_{\mathrm{d}}$ denote the mean principal shear moduli $\sqrt{\mathrm{G}_{\mathrm{xz}} \mathrm{G}_{\mathrm{xY}}}$ of the ribs and diagonals, respectively. Similarly, the stiffness-weighted eccentricities $\bar{z}_{r}, \bar{z}_{d}, \overline{\bar{z}}_{r}$, and $\overline{\bar{z}}_{d}$ vanish for homogeneous stiffeners centered on the plate reference plane. Moreover, the stiffness-weighted moments of inertia reduce to the corresponding second moments of area and the stiffness-weighted product of inertia vanishes for the rectangular stiffener cross sections. The cross-sectional areas of the core members are given by $A_{r}=h_{c} t_{r}$ and $A_{d}=h_{c} t_{d}$, where $t_{r}$ is the rib thickness and $t_{d}$ is the diagonal thickness. The moments of inertia associated with out-of-plane bending are given by $\mathrm{I}_{\mathrm{r}}=\frac{\mathrm{h}_{\mathrm{c}}^{3} \mathrm{t}_{\mathrm{r}}}{12}$ for the ribs and $I_{d}=\frac{h_{c}^{3} t_{d}}{12}$ for the diagonals. The planar geometric dimensions of the core, as shown in figure 21 and 25, are given by the symbols $\mathrm{a}, \mathrm{b}, \mathrm{c}$, and L . The symbols $\mathrm{G}_{\mathrm{r}} \mathrm{J}_{\mathrm{r}}$ and $\mathrm{G}_{\mathrm{d}} \mathrm{J}_{\mathrm{d}}$ are the torsional stiffnesses of the ribs and diagonals, respectively. For a rib with a rectangular cross-section made of a homogeneous orthotropic material, equation (A16) yields

$$
\begin{equation*}
G_{r} J_{r}=G_{X Z} \frac{t_{r}^{3}}{3} h_{c}\left\{1-\frac{96}{\pi^{5}} h_{c}\left(\frac{G_{X Z}}{G_{X Y}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{r}}\left(\frac{G_{X Y}}{G_{X Z}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{H1}
\end{equation*}
$$

and for a diagonal

$$
\begin{equation*}
G_{d} J_{d}=G_{X Z} \frac{t_{r}^{3} h_{c}}{3}\left\{1-\frac{96}{\pi^{5}} \frac{t_{d}}{h_{c}}\left(\frac{G_{X Z}}{G_{X Y}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{d}}\left(\frac{G_{X Y}}{G_{X Z}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{H2}
\end{equation*}
$$

Likewise, the symbols $k_{z}^{r}$ and $k_{z}^{d}$ denote the stiffness-weighted transverse-shear correction factor $k_{Z} \sqrt{\frac{G_{X Z}}{G_{X Y}}}$ of the ribs and diagonals, respectively, and $k_{Y}^{r}$ and $k_{Y}^{d}$ denote the stiffnessweighted inplane-shear correction factor $\mathrm{k}_{\mathrm{Y}} \sqrt{\frac{\mathrm{G}_{\mathrm{XY}}}{\mathrm{G}_{\mathrm{XZ}}}}$ of the ribs and diagonals, respectively.

For the notation just given, the equivalent-plate-stiffness contributions of the core to equations (47) are given by

$$
\begin{gather*}
A_{11}^{\text {core }}=\frac{E_{d} h_{c} t_{d} a^{3}}{(b+c) L^{3}}\left(1+\tau_{Y}^{d} \frac{b^{2}}{a^{2}}\right)  \tag{H3}\\
A_{12}^{\text {core }}=\frac{E_{d} h_{c} t_{d} a b^{2}}{(b+c) L^{3}}\left(1-\tau_{Y}^{d} G_{d}\right)  \tag{H4}\\
A_{16}^{\text {core }}=0  \tag{H5}\\
A_{22}^{\text {core }}=\frac{h_{c}}{a(b+c)}\left[\frac{E_{r} t_{r} c}{2}+\frac{E_{d} t_{d} b^{4}}{L^{3}}\left(1+\tau_{Y}^{d} \frac{a^{2}}{b^{2}}\right)\right]  \tag{H6}\\
A_{66}^{\text {core }}=\frac{h_{c}}{a(b+c)}\left\{\frac{E_{r} t_{r} \tau_{Y}^{r} c}{8}+\frac{E_{d} t_{d} a^{2} b^{2}}{L^{3}}\left[1+\frac{\tau_{Y}^{d}}{4}\left(\frac{a^{2}-b^{2}}{a b}\right)^{2}\right]\right\}  \tag{H7}\\
D_{11}^{\text {core }}=\frac{a^{3}}{(b+c) L^{3}}\left[\frac{E_{d} h_{c}^{3} t_{d}}{12}+\frac{G_{d} J_{d} b^{2}}{a^{2}}\right]  \tag{H8}\\
D_{12}^{\text {core }}=\frac{a b^{2}}{(b+c) L^{3}}\left[\frac{E_{d} h_{c}^{3} t_{d}}{12}-G_{d} J_{d}\right] \tag{H9}
\end{gather*}
$$

$$
\begin{gather*}
D_{16}^{\text {core }}=0  \tag{H11}\\
D_{22}^{\text {core }}=\frac{c}{a(b+c)}\left[\frac{E_{r} h_{c}^{3} t_{r}}{24}+\frac{b^{4}}{c L^{3}}\left(\frac{E_{d} h_{c}^{3} t_{d}}{12}+G_{d} J_{d} \frac{a^{2}}{b^{2}}\right)\right]  \tag{H12}\\
D_{26}^{\text {core }}=0  \tag{H13}\\
D_{66}^{\text {core }}=\frac{a b^{2}}{(b+c) L^{3}}\left[\frac{E_{d} h_{c}^{3} t_{d}}{12}+\frac{G_{r} J_{r} L^{3} c}{8 a^{2} b^{2}}+\frac{G_{d} J_{d}}{4 a^{2} b^{2}}\left(a^{2}-b^{2}\right)^{2}\right]  \tag{H14}\\
A_{44}^{\text {core }}=\frac{h_{c}}{2 a(b+c) L}\left[2 E_{d} t_{d} \tau_{z}^{d} b^{2}+E_{r} t_{r} \tau_{z}^{r} c L\right]  \tag{H15}\\
A_{45}^{\text {core }}=0  \tag{H16}\\
A_{55}^{\text {core }}=\frac{E_{d} h_{c} t_{d} \tau_{z}^{d} a}{(b+c) L} \tag{H17}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{Y}^{r} \equiv \frac{k_{Y}^{r} G_{r}}{E_{r}}  \tag{H18}\\
& \tau_{Y}^{d} \equiv \frac{k_{Y}^{d} G_{d}}{E_{d}} \tag{H19}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{Z}^{r} \equiv \frac{k_{Z}^{r} G_{r}}{E_{r}}  \tag{H20}\\
& \tau_{Z}^{d} \equiv \frac{k_{Z}^{d} G_{d}}{E_{d}} \tag{H21}
\end{align*}
$$

Setting these shear-deformation parameters equal to zero eliminates the effects of stiffener shear deformation. The overall stiffnesses of the sandwich plate are obtained by substituting equations (H3)-(H17) into equations (47).

For the special case of a homogeneous, isotropic core comprised of hexagons with all sides having length L , the angle $\Phi$ shown in figure 21b is 30 degrees, $\mathrm{a}=\frac{\sqrt{3} \mathrm{~L}}{2}, \mathrm{~b}=\mathrm{L} / 2$, and $\mathrm{c}=\mathrm{L}$. In addition, $\mathrm{E}_{\mathrm{r}}=\mathrm{E}_{\mathrm{d}}=\mathrm{E}$ and $\mathrm{G}_{\mathrm{r}}=\mathrm{G}_{\mathrm{d}}=\mathrm{G}$, where E and G are the extensional and shear moduli of an isotropic material, and $\mathrm{k}_{\mathrm{Y}}^{\mathrm{r}}=\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}}=\mathrm{k}_{\mathrm{Z}}^{\mathrm{r}}=\mathrm{k}_{\mathrm{Z}}^{\mathrm{d}}=\mathrm{k}$. For this case, equations (H1) and (H2) are expressed as

$$
\begin{align*}
\mathrm{G}_{\mathrm{r}} \mathrm{~J}_{\mathrm{r}} & =\frac{\mathrm{Gt}_{\mathrm{r}}^{3} \mathrm{~h}_{\mathrm{c}}}{3}\left(1-\mathrm{K}_{\mathrm{r}}\right)  \tag{H22}\\
\mathrm{G}_{\mathrm{d}} \mathrm{~J}_{\mathrm{d}} & =\frac{\mathrm{Gt}_{\mathrm{d}}^{3} \mathrm{~h}_{\mathrm{c}}}{3}\left(1-\mathrm{K}_{\mathrm{d}}\right) \tag{H23}
\end{align*}
$$

where

$$
\begin{align*}
& K_{r}=\frac{96}{\pi^{5}} \frac{t_{r}}{h_{c}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{r}}\right)\right]  \tag{H24}\\
& K_{d}=\frac{96}{\pi^{5}} \frac{t_{d}}{h_{c}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{d}}\right)\right] \tag{H25}
\end{align*}
$$

The equivalent-plate core stiffnesses reduce to

$$
\begin{gather*}
{\left[\begin{array}{llc}
A_{11}^{\text {core }} & A_{12}^{\text {core }} & A_{16}^{\text {core }} \\
A_{12}^{\text {core }} & A_{22}^{\text {core }} & A_{26}^{\text {core }} \\
A_{16}^{\text {ocre }} & A_{26}^{\text {core }} & A_{66}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} h_{\mathrm{c}} t_{\mathrm{d}} E}{12 L}\left[\begin{array}{ccc}
3+\frac{k G}{E} & 1-\frac{k G}{E} & 0 \\
1-\frac{k G}{E} & \frac{1}{3}\left(1+8 \frac{t_{\mathrm{r}}}{t_{\mathrm{d}}}+\frac{3 k G}{E}\right) & 0 \\
0 & 0 & 1+\frac{k G}{3 E}\left[1+2 \frac{t_{\mathrm{r}}}{t_{\mathrm{d}}}\right]
\end{array}\right]}  \tag{H26}\\
{\left[\begin{array}{l}
D_{11}^{\text {core }} D_{12}^{\text {core }} D_{16}^{\text {core }} \\
D_{12}^{\text {core }} D_{22}^{\text {core }} D_{26}^{\text {core }} \\
D_{16}^{\text {core }} D_{26}^{\text {core }} D_{66}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} h_{\mathrm{c} t_{\mathrm{d}}}^{3} E}{144 L}\left[\begin{array}{ccc}
3+\frac{4 G}{E} \frac{t}{\mathrm{~d}}_{\mathrm{c}}^{2} & \left(1-K_{\mathrm{d}}\right) & 1-\frac{4 G}{E} \frac{t_{\mathrm{d}}^{2}}{h_{\mathrm{c}}^{2}}\left(1-K_{\mathrm{d}}\right) \\
1-\frac{4 G}{E} \frac{t_{\mathrm{d}}^{2}}{h_{\mathrm{c}}^{2}}\left(1-K_{\mathrm{d}}\right) & \frac{1}{3}\left(1+8 \frac{t_{\mathrm{r}}}{t_{\mathrm{d}}}+\frac{12 G}{E} \frac{t_{\mathrm{d}}^{2}}{h_{\mathrm{d}}^{2}}\left(1-K_{\mathrm{d}}\right)\right) & 0 \\
0 & 0 & 1+\frac{4 G}{3 E} \frac{t_{\mathrm{d}}^{2}}{h_{\mathrm{c}}^{2}}\left[\frac{2 t_{\mathrm{r}}^{3}}{t_{\mathrm{d}}^{3}}\left(1-K_{\mathrm{r}}\right)+1-K_{\mathrm{d}}\right.
\end{array}\right]}  \tag{H27}\\
{\left[\begin{array}{l}
A_{44}^{\text {core }} A_{45}^{\text {core }} \\
A_{45}^{\text {core }} A_{55}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} k G h_{\mathrm{c}} t_{\mathrm{d}}}{9 L}\left[\begin{array}{cc}
1+2 \frac{t_{\mathrm{r}}}{t_{\mathrm{d}}} & 0 \\
0 & 3
\end{array}\right]} \tag{H28}
\end{gather*}
$$

## Appendix I <br> Equivalent-Plate Stiffnesses for an Orthogrid-Core Sandwich Plate

The equivalent-plate stiffnesses for a sandwich plate composed of two different, anisotropic, laminated-composite face plates and the orthogrid core with homogeneous, orthotropic members shown in figure 26 are presented in this appendix. The thicknesses of the bottom face plate (plate no. 1), the top face plate (plate no. 2), and the core are denoted by $\mathrm{h}_{1}, \mathrm{~h}_{2}$, and $\mathrm{h}_{\mathrm{c}}$, respectively. The plate reference plane is located at the midplane of the core and the eccentricities of face plates no. 1 and no. 2 are given by $e_{1}=-\frac{1}{2}\left(h_{1}+h_{c}\right)$ and $e_{2}=\frac{1}{2}\left(h_{2}+h_{c}\right)$, respectively. The stringer and rib elements of the core are aligned with the x - and y -axes of the plate shown in figure 26, respectively. Member attributes associated with the ribs and stringers are indicated subsequently with the subscripts or superscripts " r " and " s ," respectively.

For an orthogrid core with each member made of a homogeneous orthotropic material, the effective moduli given by equations (A13a)-(A13c) reduce to the corresponding principal moduli of the orthotropic material, where the principal orthotropic-material axes are coincident with the $\mathrm{X}, \mathrm{Y}$, and Z beam coordinate axes shown in figure 6. Thus, the symbols $\mathrm{E}_{\mathrm{r}}$ and $\mathrm{E}_{\mathrm{s}}$ denote the extensional modulus $\mathrm{E}_{\mathrm{X}}$ and the symbols $\mathrm{G}_{\mathrm{r}}$ and $\mathrm{G}_{\mathrm{s}}$ denote the mean principal shear moduli $\sqrt{\mathrm{G}_{\mathrm{XZ}} \mathrm{G}_{\mathrm{XY}}}$ of the ribs and stringers, respectively. Similarly, the stiffness-weighted first moments of area $\bar{z}_{\mathrm{r}}, \bar{z}_{\mathrm{s}}, \overline{\bar{z}}_{\mathrm{r}}$, and $\overline{\bar{z}}_{\mathrm{s}}$ vanish for homogeneous stiffeners centered on the plate reference plane. Moreover, the stiffness-weighted moments of inertia reduce to the corresponding second moments of area and the stiffness-weighted product of inertia vanishes for the rectangular stiffener cross sections. The cross-sectional areas of the stringers and ribs are given by $\mathrm{A}_{\mathrm{s}}=\mathrm{h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}$ and $A_{r}=h_{c} t_{r}$, respectively, where $t_{s}$ is the stringer thickness and $t_{r}$ is the rib thickness. The moments of inertia associated with out-of-plane bending are given by $I_{s}=\frac{h_{c}^{3} t_{s}}{12}$ for the stringers and $I_{r}=\frac{h_{\mathrm{c}}^{3} t_{\mathrm{r}}}{12}$ for the ribs. The symbols $L_{y}$ and $L_{x}$ denote the spacing of the stringers and ribs, respectively, as shown in figure 26. The symbols $\mathrm{G}_{\mathrm{s}} \mathrm{J}_{\mathrm{s}}$ and $\mathrm{G}_{\mathrm{r}} \mathrm{J}_{\mathrm{r}}$ are the torsional stiffnesses of the stringers and ribs, respectively. For a rib with a rectangular cross-section made of a homogeneous orthotropic material, equation (A16) yields

$$
\begin{equation*}
G_{r} J_{r}=G_{X Z} \frac{t_{r}^{3} h_{c}}{3}\left\{1-\frac{96}{\pi^{5} h_{c}} t_{r}\left(\frac{G_{X Z}}{G_{X Y}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{r}}\left(\frac{G_{X Y}}{G_{X Z}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{I1}
\end{equation*}
$$

and for a stringer

$$
\begin{equation*}
G_{s} J_{s}=G_{X Z} \frac{t_{s}^{3} h_{c}}{3}\left\{1-\frac{96}{\pi^{5}} \frac{t_{s}}{h_{c}}\left(\frac{G_{X Z}}{G_{X Y}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{s}}\left(\frac{G_{X Y}}{G_{X Z}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{I2}
\end{equation*}
$$

Likewise, the symbols $k_{z}^{s}$ and $k_{z}^{r}$ denote the stiffness-weighted transverse-shear correction factor $k_{Z} \sqrt{\frac{G_{X Z}}{G_{X Y}}}$ of the stringers and ribs, respectively, and $k_{Y}^{s}$ and $k_{Y}^{r}$ denote the stiffnessweighted inplane-shear correction factor $k_{Y} \sqrt{\frac{G_{X Y}}{G_{X Z}}}$ of the stringers and ribs, respectively.

Based on the notation just given, the equivalent-plate-stiffness contributions of the core are

$$
\begin{gather*}
{\left[\begin{array}{ccc}
\mathrm{A}_{11}^{\text {core }} & \mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{16}^{\text {core }} \\
\mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{22}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} \\
\mathrm{A}_{16}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} & \mathrm{A}_{66}^{\text {core }}
\end{array}\right]=\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{s}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}} & 0 & 0 \\
0 & \frac{\mathrm{E}_{\mathrm{r}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}} & 0 \\
0 & 0 & \frac{\mathrm{k}_{\mathrm{Y}}^{s} \mathrm{G}_{\mathrm{s}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}}{4 \mathrm{~L}_{\mathrm{y}}}+\frac{\mathrm{k}_{\mathrm{Y}}^{r} \mathrm{G}_{\mathrm{r}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{r}}}{4 \mathrm{~L}_{\mathrm{x}}}
\end{array}\right]}  \tag{I3}\\
{\left[\begin{array}{l}
\mathrm{D}_{11}^{\text {core }} \mathrm{D}_{12}^{\text {core }} \mathrm{D}_{16}^{\text {core }} \\
\mathrm{D}_{12}^{\text {core }} \mathrm{D}_{20}^{\text {core }} \mathrm{D}_{26}^{\text {core }} \\
\mathrm{D}_{16}^{\text {core }} \mathrm{D}_{26}^{\text {core }} \mathrm{D}_{66}^{\text {core }}
\end{array}\right]=\left[\begin{array}{ccc}
\frac{\mathrm{E}_{\mathrm{s}} \mathrm{~h}_{\mathrm{c}}^{3} \mathrm{t}_{\mathrm{s}}}{12 \mathrm{~L}_{\mathrm{y}}} & 0 & 0 \\
0 & \frac{\mathrm{E}_{\mathrm{r}} \mathrm{~h}_{\mathrm{c}}^{3} \mathrm{t}_{\mathrm{r}}}{12 \mathrm{~L}_{\mathrm{x}}} & 0 \\
0 & 0 & \frac{1}{4}\left(\frac{\mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}}+\frac{\mathrm{G}_{\mathrm{r}} \mathrm{~J}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}}\right)
\end{array}\right]}  \tag{I4}\\
{\left[\begin{array}{l}
\mathrm{A}_{44}^{\text {core }} \mathrm{A}_{45}^{\text {core }} \\
\mathrm{A}_{45}^{\text {core }} \mathrm{A}_{55}^{\text {core }}
\end{array}\right]=\left[\begin{array}{cc}
\frac{\mathrm{k}_{\mathrm{z}}^{r} \mathrm{G}_{\mathrm{r}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}} & 0 \\
0 & \frac{\mathrm{k}_{\mathrm{z}}^{\mathrm{c}} \mathrm{G}_{\mathrm{s}} \mathrm{~h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}}
\end{array}\right]} \tag{I5}
\end{gather*}
$$

As a special case, consider a sandwich plate with face sheets and a core are made from three different homogeneous, specially orthotropic materials. The core is made from a monolithic piece of orthotropic material. The face plates are relatively thin and, as a result, the transverse-shearing deformations of the face plates are presumed to be negligible. For this case, the principal material coordinate frames are taken to be identical to the structural coordinate frame shown in figure 26. The orthotropic-material properties are denoted by the extensional moduli $\mathrm{E}_{\mathrm{x}}$ and $\mathrm{E}_{\mathrm{y}}$; the shear
moduli $\mathrm{G}_{\mathrm{xy}}, \mathrm{G}_{\mathrm{xz}}$, and $\mathrm{G}_{\mathrm{yz}}$; and the Poisson's ratios $v_{\mathrm{xy}}$, and $v_{\mathrm{yx}}$. In addition, superscripts are applied to these material-property designations to indicate their association with a given face plate or the core. For the stringer elements of the core, which are aligned with the x -axis; $\mathrm{E}_{\mathrm{s}} \rightarrow \mathrm{E}_{\mathrm{x}}^{\text {core }}$, $\mathrm{k}_{\mathrm{y}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \rightarrow \mathrm{k}_{\mathrm{y}}^{\text {core }} \mathrm{G}_{\mathrm{xy}}^{\text {core }}$, and $\mathrm{k}_{\mathrm{z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}} \rightarrow \mathrm{k}_{\mathrm{z}}^{\text {core }} \mathrm{G}_{\mathrm{xz}}^{\text {core }}$. For the rib elements of the core, which are aligned with the y-axis; $\mathrm{E}_{\mathrm{r}} \rightarrow \mathrm{E}_{\mathrm{y}}^{\text {core }}, \mathrm{k}_{\mathrm{y}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}} \rightarrow \mathrm{k}_{\mathrm{x}}^{\text {core }} \mathrm{G}_{\mathrm{xy}}^{\text {core }}$, and $\mathrm{k}_{\mathrm{z}}^{\mathrm{r}} \mathrm{G}_{\mathrm{r}} \rightarrow \mathrm{k}_{\mathrm{z}}^{\text {core }} \mathrm{G}_{\mathrm{yz}}^{\text {core }}$. For a stiffener with a rectangular cross-section made of a homogeneous orthotropic material, equations (I1) and (I2) give

$$
\begin{align*}
& \mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}=\mathrm{G}_{\mathrm{xz}}^{\operatorname{core}} \frac{\mathrm{t}_{\mathrm{s}}^{3} \mathrm{~h}_{\mathrm{c}}}{3}\left(1-\mathrm{K}_{\mathrm{s}}\right)  \tag{I6}\\
& \mathrm{G}_{\mathrm{r}} \mathrm{~J}_{\mathrm{r}}=\mathrm{G}_{\mathrm{yz}}^{\operatorname{core}} \frac{\mathrm{t}_{\mathrm{r}}^{3}}{3} \mathrm{~h}_{\mathrm{c}}\left(1-\mathrm{K}_{\mathrm{r}}\right) \tag{I7}
\end{align*}
$$

where

$$
\begin{align*}
& K_{s}=\frac{96}{\pi^{5}} \frac{t_{s}}{h_{c}}\left(\frac{G_{x z}^{\text {core }}}{G_{x y}^{\text {core }}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{s}}\left(\frac{G_{x y}^{\text {core }}}{G_{x z}^{\text {core }}}\right)^{\frac{1}{2}}\right)\right]  \tag{I8}\\
& K_{r}=\frac{96}{\pi^{5}} \frac{t_{r}}{h_{c}}\left(\frac{G_{y z}^{\text {core }}}{G_{x y}^{\text {core }}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{r}}\left(\frac{G_{x y}^{\text {core }}}{G_{y z}^{\text {core }}}\right)^{\frac{1}{2}}\right)\right] \tag{I9}
\end{align*}
$$

Using this information with equations (I3) - (I5) and (47) gives

$$
\begin{gather*}
{\left[\begin{array}{lll}
A_{11} & A_{12} & A_{16} \\
A_{12} & A_{22} & A_{26} \\
A_{16} & A_{26} & A_{66}
\end{array}\right]=h_{1}\left[\begin{array}{ccc}
\frac{E_{x}}{1-v_{x y} v_{y x}} \frac{v_{x y} E_{y}}{1-v_{x y} v_{y x}} & 0 \\
\frac{v_{y x} E_{x}}{1-v_{x y} v_{y x}} \frac{E_{y}}{1-v_{x y} v_{y x}} & 0 \\
0 & 0 & G_{x y}
\end{array}\right]^{\text {plate no. } 1}+h_{2}\left[\begin{array}{cc}
\frac{E_{x}}{1-v_{x y} v_{y x}} \frac{v_{x y} E_{y}}{1-v_{x y} v_{y x}} & 0 \\
\frac{v_{y x} E_{x}}{1-v_{x y} v_{y x}} \frac{E_{y}}{1-v_{x y} v_{y x}} & 0 \\
0 & 0
\end{array}\right]_{\mathrm{xy}}^{\text {plate no. } 2}} \\
+\left[\begin{array}{ccc}
\frac{E_{x}^{\text {core }} h_{c} t_{s}}{L_{y}} & 0 & 0 \\
0 & \frac{E_{y}^{\text {core }} h_{c} t_{r}}{L_{x}} & 0 \\
0 & 0 & \frac{k_{y}^{\text {core }} G_{x y}^{\text {core }} h_{c} t_{s}}{4 L_{y}}+\frac{k_{x}^{\text {core }} G_{x y}^{\text {core }} h_{c} t_{r}}{4 L_{x}}
\end{array}\right] \tag{I10}
\end{gather*}
$$

$$
\begin{align*}
& {\left[\begin{array}{ccc}
\mathrm{B}_{11} & \mathrm{~B}_{12} & \mathrm{~B}_{16} \\
\mathrm{~B}_{12} & \mathrm{~B}_{22} & \mathrm{~B}_{26} \\
\mathrm{~B}_{16} & \mathrm{~B}_{26} & \mathrm{~B}_{66}
\end{array}\right]=-\frac{1}{2}\left(\mathrm{~h}_{1}+\mathrm{h}_{\mathrm{c}}\right) \mathrm{h}_{1}\left[\begin{array}{cc}
\frac{\mathrm{E}_{\mathrm{x}}}{1-v_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} \frac{v_{\mathrm{xy}} \mathrm{E}_{\mathrm{y}}}{1-\boldsymbol{v}_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} & 0 \\
\frac{\boldsymbol{v}_{\mathrm{yx}} \mathrm{E}_{\mathrm{x}}}{1-\boldsymbol{v}_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} \frac{\mathrm{E}_{\mathrm{y}}}{1-\boldsymbol{v}_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} & 0 \\
0 & 0
\end{array} \mathrm{G}_{\mathrm{xy}}\right]^{\text {plate no. } 1}}  \tag{I11}\\
& +\frac{1}{2}\left(h_{2}+h_{c}\right) h_{2}\left[\begin{array}{cc}
\frac{E_{x}}{1-v_{x y} v_{y x}} \frac{v_{x y} E_{y}}{1-v_{x y} v_{y x}} & 0 \\
\frac{v_{y x} E_{x}}{1-v_{x y} v_{y x}} \frac{E_{y}}{1-v_{x y} v_{y x}} & 0 \\
0 & 0
\end{array} G_{x y}^{\text {plate no. } 2}\right. \\
& {\left[\begin{array}{lll}
\mathrm{D}_{11} & \mathrm{D}_{12} & \mathrm{D}_{16} \\
\mathrm{D}_{12} & \mathrm{D}_{22} & \mathrm{D}_{26} \\
\mathrm{D}_{16} & \mathrm{D}_{26} & \mathrm{D}_{66}
\end{array}\right]=\frac{1}{12}\left(4 \mathrm{~h}_{1}^{2}+6 \mathrm{~h}_{1} \mathrm{~h}_{\mathrm{c}}+3 \mathrm{~h}_{\mathrm{c}}^{2}\right)\left[\begin{array}{cc}
\frac{\mathrm{E}_{\mathrm{x}}}{1-\mathrm{v}_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} \frac{v_{\mathrm{xy}} \mathrm{E}_{\mathrm{y}}}{1-v_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} & 0 \\
\frac{v_{\mathrm{yx}} \mathrm{E}_{\mathrm{x}}}{1-v_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} \frac{\mathrm{E}_{\mathrm{y}}}{1-v_{\mathrm{xy}} \boldsymbol{v}_{\mathrm{yx}}} & 0 \\
0 & 0
\end{array} \mathrm{G}_{\mathrm{xy}}\right]^{\text {plate no. } 1}} \\
& +\frac{1}{12}\left(4 h_{2}^{2}+6 h_{2} h_{c}+3 h_{c}^{2}\right)\left[\begin{array}{cc}
\frac{E_{x}}{1-v_{x y} v_{y x}} \frac{v_{x y} E_{y}}{1-v_{x y} v_{y x}} & 0 \\
\frac{v_{y x} E_{x}}{1-v_{x y} v_{y x}} \frac{E_{y}}{1-v_{x y} v_{y x}} & 0 \\
0 & 0
\end{array} G_{x y}\right]^{\text {plate no. 2 }}  \tag{I12}\\
& +\left[\begin{array}{ccc}
\frac{E_{x}^{\text {core }} h_{c}^{3} t_{s}}{12 L_{y}} & 0 & 0 \\
0 & \frac{E_{y}^{\text {core }} h_{c}^{3} t_{r}}{12 L_{x}} & 0 \\
0 & 0 & \frac{h_{c}}{12}\left(\frac{G_{x z}^{\text {core }} t_{s}^{3}\left(1-K_{s}\right)}{L_{y}}+\frac{G_{y z}^{\text {core }} t_{r}^{3}\left(1-K_{r}\right)}{L_{x}}\right)
\end{array}\right] \\
& {\left[\begin{array}{ll}
\mathrm{A}_{44} & \mathrm{~A}_{45} \\
\mathrm{~A}_{45} & \mathrm{~A}_{55}
\end{array}\right]=\left[\begin{array}{cc}
\frac{\mathrm{k}_{\mathrm{z}}^{\text {core }} \mathrm{G}_{\mathrm{yz}}^{\text {core }} \mathrm{h}_{\mathrm{c}} \mathrm{t}_{\mathrm{r}}}{\mathrm{~L}_{\mathrm{x}}} & 0 \\
0 & \frac{\mathrm{k}_{\mathrm{z}}^{\text {core }} \mathrm{G}_{\mathrm{xz}}^{\text {core }} \mathrm{h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}}{\mathrm{~L}_{\mathrm{y}}}
\end{array}\right]} \tag{I13}
\end{align*}
$$

## Appendix J <br> Equivalent-Plate Stiffnesses for a Star-Cell-Core Sandwich Plate

The equivalent-plate stiffnesses for a sandwich plate composed of two nonidentical, anisotropic, laminated-composite face plates and the isosceles-star-cell core made of a homogeneous orthotropic material shown in figure 27 are presented in this appendix. The thicknesses of the bottom face plate (plate no. 1), the top face plate (plate no. 2), and the core are denoted by $\mathrm{h}_{1}, \mathrm{~h}_{2}$, and $\mathrm{h}_{\mathrm{c}}$, respectively. The plate reference plane is located at the midplane of the core and the eccentricities of face plates no. 1 and no. 2 are given by $e_{1}=-\frac{1}{2}\left(h_{1}+h_{c}\right)$ and $e_{2}=\frac{1}{2}\left(h_{2}+h_{c}\right)$, respectively. The core is composed of two member types. One member type is aligned with the x -axis of the plate, as shown in figures 23 and 27 , and is referred to herein as a stringer member. The other member type makes an angle $\Phi$ with the x -axis and is referred to herein as a diagonal. Member attributes associated with the stringers and diagonals are indicated subsequently with the subscripts or superscripts "s" and "d," respectively.

For an isosceles-star-cell core with each member made of a homogeneous orthotropic material, the effective moduli given by equations (A13a)-(A13c) reduce to the corresponding principal moduli of the orthotropic material, where the principal orthotropic-material axes are coincident with the $\mathrm{X}, \mathrm{Y}$, and Z beam coordinate axes shown in figure 6. Thus, the symbols $\mathrm{E}_{\mathrm{s}}$ and $\mathrm{E}_{\mathrm{d}}$ denote the extensional modulus $\mathrm{E}_{\mathrm{X}}$ and the symbols $\mathrm{G}_{\mathrm{s}}$ and $\mathrm{G}_{\mathrm{d}}$ denote the mean principal shear moduli $\sqrt{\mathbf{G}_{\mathrm{xZ}} \mathbf{G}_{\mathrm{xY}}}$ of the stringers and diagonals, respectively. Similarly, the stiffness-weighted first moments of area $\bar{z}_{s}, \bar{z}_{d}, \overline{\bar{z}}_{s}$, and $\overline{\bar{z}}_{d}$ vanish for homogeneous stiffeners centered on the plate reference plane. Moreover, the stiffness-weighted moments of inertia reduce to the corresponding second moments of area and the stiffness-weighted product of inertia vanishes for the rectangular stiffener cross sections. The cross-sectional areas of the core members are given by $\mathrm{A}_{\mathrm{s}}=\mathrm{h}_{\mathrm{c}} \mathrm{t}_{\mathrm{s}}$ and $A_{d}=h_{c} t_{d}$, where $t_{s}$ is the stringer thickness and $t_{d}$ is the diagonal thickness. The moments of inertia associated with out-of-plane bending are given by $I_{s}=\frac{h_{c}^{3} t_{s}}{12}$ for the stringers and $I_{d}=\frac{h_{c}^{3} t_{d}}{12}$ for the diagonals. The planar geometric dimensions of the core, as shown in figure 23 and 27, are given by the symbols B and H, where B and H are the base and height, respectively, of either isosceles triangle forming the star shape. The symbols $\mathrm{G}_{\mathrm{s}} \mathrm{J}_{\mathrm{s}}$ and $\mathrm{G}_{\mathrm{d}} \mathrm{J}_{\mathrm{d}}$ are the torsional stiffnesses of the stringers and diagonals, respectively. For a stringer with a rectangular cross-section made of a homogeneous orthotropic material, equation (A16) yields

$$
\begin{equation*}
\mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}=\mathrm{G}_{\mathrm{XZ}} \frac{\mathrm{t}_{\mathrm{s}}^{3}}{3} \mathrm{~h}_{\mathrm{c}}\left\{1-\frac{96}{\pi^{5} \mathrm{~h}_{\mathrm{c}}}\left(\frac{\mathrm{G}_{\mathrm{XZ}}}{\mathrm{G}_{\mathrm{XY}}}\right)^{\frac{1}{2}} \sum_{\mathrm{p}=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{\mathrm{p}}}{\mathrm{p}^{5}} \tanh \left(\frac{\mathrm{p} \pi \mathrm{~h}_{\mathrm{c}}}{2 \mathrm{t}_{\mathrm{s}}}\left(\frac{\mathrm{G}_{\mathrm{XY}}}{\mathrm{G}_{\mathrm{XZ}}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{J1}
\end{equation*}
$$

and for a diagonal

$$
\begin{equation*}
G_{d} J_{d}=G_{X Z} \frac{t_{r}^{3} h_{c}}{3}\left\{1-\frac{96}{\pi^{5}} \frac{t_{d}}{h_{c}}\left(\frac{G_{X Z}}{G_{X Y}}\right)^{\frac{1}{2}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t_{d}}\left(\frac{G_{X Y}}{G_{X Z}}\right)^{\frac{1}{2}}\right)\right]\right\} \tag{J2}
\end{equation*}
$$

Likewise, the symbols $k_{z}^{s}$ and $k_{z}^{d}$ denote the stiffness-weighted transverse-shear correction factor $\mathrm{k}_{Z} \sqrt{\frac{\mathrm{G}_{X Z}}{\mathrm{G}_{X Y}}}$ of the stringers and diagonals, respectively, and $\mathrm{k}_{Y}^{s}$ and $\mathrm{k}_{Y}^{d}$ denote the stiffness-weighted inplane-shear correction factor $\mathrm{k}_{\mathrm{Y}} \sqrt{\frac{\mathrm{G}_{\mathrm{XY}}}{\mathrm{G}_{\mathrm{XZ}}}}$ of the stringers and diagonals, respectively.

Based on the notation just given, the equivalent-plate-stiffnesses contributions of the core are

$$
\begin{gather*}
A_{11}^{\text {core }}=\frac{E_{s} h_{c} t_{s}}{H}+\frac{E_{d} h_{c} t_{d} B^{3}}{8 H L}\left(1+4 \tau_{Y}^{d} \frac{H^{2}}{B^{2}}\right)  \tag{J3}\\
A_{12}^{\text {core }}=\frac{E_{d} h_{c} t_{d} B H}{2 L^{3}}\left(1-\tau_{Y}^{d}\right)  \tag{J4}\\
A_{16}^{\text {core }}=0  \tag{J5}\\
A_{22}^{\text {core }}=\frac{2 E_{d} h_{c} t_{d} H^{3}}{B L^{3}}\left(1+\frac{\tau_{Y}^{d} B^{2}}{4 H^{2}}\right)  \tag{J6}\\
A_{66}^{\text {core }}=\frac{E_{s} \tau_{Y}^{s} h_{c} t_{s}}{4 H}+\frac{E_{d} h_{c} t_{d} B H}{2 L^{3}}\left[1+\tau_{Y}^{d}\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\right]  \tag{J7}\\
D_{11}^{\text {core }}=\frac{h_{c}^{3} t_{s}}{12 H}\left\{E_{s}+\frac{E_{d}}{8} \frac{t_{d}}{t_{s}} \frac{B^{3}}{L^{3}}\left[1+\frac{16 G_{d}}{E_{d}} \frac{t_{d}^{2}}{h_{c}^{2}} \frac{H^{2}}{B^{2}}\left(1-K_{d}\right)\right]\right\}  \tag{J8}\\
D_{12}^{\text {core }}=\frac{E_{d} h_{c}^{3} t_{d} B H}{24 L^{3}}\left[1-\frac{4 G_{d}}{E_{d}} \frac{t_{d}^{2}}{h_{c}^{2}}\left(1-K_{d}\right)\right]  \tag{J9}\\
D_{16}^{\text {core }}=0 \tag{J10}
\end{gather*}
$$

$$
\begin{gather*}
D_{22}^{\text {core }}=\frac{E_{d} h_{c}^{3} t_{d} H^{3}}{6 B L}\left[1+\frac{G_{d}}{E_{d}} \frac{t_{d}^{2}}{h_{c}^{2}} \frac{B^{2}}{H^{2}}\left(1-K_{d}\right)\right]  \tag{J12}\\
D_{26}^{\text {core }}=0  \tag{J13}\\
D_{66}^{\text {core }}=\frac{G_{s} t_{s}^{3} h_{c}}{12 H}\left(1-K_{s}\right)+\frac{E_{d} h_{c}^{3} t_{d} B H}{24 L^{3}}\left[1+\frac{4 G_{d}}{E_{d}} \frac{t_{d}^{2}}{h_{c}^{2}}\left(\frac{B}{4 H}-\frac{H}{B}\right)^{2}\left(1-K_{d}\right)\right]  \tag{J14}\\
A_{44}^{\text {core }}=\frac{2 \tau_{z}^{d} E_{d} h_{c} t_{d} H}{B L}  \tag{J15}\\
A_{45}^{\text {core }}=0  \tag{J16}\\
A_{55}^{\text {core }}=\frac{h_{c} t_{s}}{2 H}\left(2 \tau_{z}^{s} E_{s}+\tau_{z}^{d} E_{d} \frac{t_{d}}{t_{s}} \frac{B}{L}\right) \tag{J17}
\end{gather*}
$$

where the inplane-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Y}}^{\mathrm{s}} \equiv \frac{k_{\mathrm{Y}}^{\mathrm{s}} G_{\mathrm{s}}}{E_{\mathrm{s}}}  \tag{J18}\\
& \tau_{\mathrm{Y}}^{\mathrm{d}} \equiv \frac{k_{\mathrm{Y}}^{\mathrm{d}} G_{\mathrm{d}}}{E_{\mathrm{d}}} \tag{J19}
\end{align*}
$$

and the transverse-shear-deformation parameters are defined as

$$
\begin{align*}
& \tau_{\mathrm{Z}}^{\mathrm{s}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}} \mathrm{G}_{\mathrm{s}}}{\mathrm{E}_{\mathrm{s}}}  \tag{J20}\\
& \tau_{\mathrm{Z}}^{\mathrm{d}} \equiv \frac{\mathrm{k}_{\mathrm{Z}}^{\mathrm{d}} \mathrm{G}_{\mathrm{d}}}{\mathrm{E}_{\mathrm{d}}} \tag{J21}
\end{align*}
$$

The overall stiffnesses of the sandwich plate are obtained by substituting equations (J3)-(J17) into equations (47).

For the special case of an isotropic star-cell core comprised of triangles with all sides having length $L$ and thicknesses $t_{s}=t_{d}=t$, the angle $\Phi$ shown in figure 23b is 60 degrees, $H=\frac{\sqrt{3} L}{2}$, and $\mathrm{B}=\mathrm{L}$. In addition $\mathrm{E}_{\mathrm{s}}=\mathrm{E}_{\mathrm{d}}=\mathrm{E}$ and $\mathrm{G}_{\mathrm{s}}=\mathrm{G}_{\mathrm{d}}=\mathrm{G}$, where E and G are the extensional and shear
moduli of an isotropic material, and $\mathrm{k}_{\mathrm{Y}}^{\mathrm{s}}=\mathrm{k}_{\mathrm{Y}}^{\mathrm{d}}=\mathrm{k}_{\mathrm{Z}}^{\mathrm{s}}=\mathrm{k}_{\mathrm{Z}}^{\mathrm{d}}=\mathrm{k}$. For this case, equations (J1) and (J2) are expressed as

$$
\begin{equation*}
\mathrm{G}_{\mathrm{s}} \mathrm{~J}_{\mathrm{s}}=\mathrm{G}_{\mathrm{d}} \mathrm{~J}_{\mathrm{d}}=\frac{\mathrm{Gt}^{3} \mathrm{~h}_{\mathrm{c}}}{3}(1-\mathrm{K}) \tag{J22}
\end{equation*}
$$

where

$$
\begin{equation*}
K=\frac{96}{\pi^{5}} \frac{t}{h_{c}} \sum_{p=1,2,3, \ldots}^{\infty}\left[\frac{1-(-1)^{p}}{p^{5}} \tanh \left(\frac{p \pi h_{c}}{2 t}\right)\right] \tag{J23}
\end{equation*}
$$

Thus, the equivalent-plate core-stiffness contributions become

$$
\begin{gather*}
{\left[\begin{array}{lll}
\mathrm{A}_{11}^{\text {core }} & \mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{16}^{\text {core }} \\
\mathrm{A}_{12}^{\text {core }} & \mathrm{A}_{22}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} \\
\mathrm{A}_{16}^{\text {core }} & \mathrm{A}_{26}^{\text {core }} & \mathrm{A}_{66}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} \mathrm{~h}_{\mathrm{c}} \mathrm{t} \mathrm{E}}{4 \mathrm{~L}}\left[\begin{array}{ccc}
3+\frac{\mathrm{kG}}{\mathrm{E}} & 1-\frac{\mathrm{kG}}{\mathrm{E}} & 0 \\
1-\frac{\mathrm{kG}}{\mathrm{E}} & 3+\frac{\mathrm{kG}}{\mathrm{E}} & 0 \\
0 & 0 & 1+\frac{\mathrm{kG}}{\mathrm{E}}
\end{array}\right]}  \tag{J24}\\
{\left[\begin{array}{l}
\mathrm{D}_{11}^{\text {core }} \mathrm{D}_{12}^{\text {core }} \mathrm{D}_{16}^{\text {core }} \\
\mathrm{D}_{12}^{\text {core }} \mathrm{D}_{22}^{\text {core }} \mathrm{D}_{26}^{\text {core }} \\
\mathrm{D}_{16}^{\text {core }} \mathrm{D}_{26}^{\text {core }} \mathrm{D}_{66}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} \mathrm{~h}_{\mathrm{c}}^{3} \mathrm{t} \mathrm{E}}{48 \mathrm{~L}}\left[\begin{array}{ccc}
3+\frac{4 \mathrm{G} \mathrm{t}^{2}}{\mathrm{E}} \mathrm{~h}_{\mathrm{c}}^{2}(1-\mathrm{K}) & 1-\frac{4 \mathrm{G}}{\mathrm{E}} \mathrm{t}^{2} \\
1-\frac{4 \mathrm{G}}{\mathrm{~h}_{\mathrm{c}}^{2}}(1-\mathrm{K}) & 0 \\
\mathrm{~h}_{\mathrm{c}}^{2} & 3+\frac{4 \mathrm{G}}{\mathrm{c}^{2}} \frac{\mathrm{t}^{2}}{\mathrm{~h}_{\mathrm{c}}^{2}}(1-\mathrm{K}) & 0 \\
0 & 0 & 1+\frac{4 \mathrm{G}}{\mathrm{~h}_{\mathrm{c}}^{2}}(1-\mathrm{K})
\end{array}\right]}  \tag{J25}\\
{\left[\begin{array}{l}
\mathrm{A}_{44}^{\text {core }} \mathrm{A}_{45}^{\text {core }} \\
\mathrm{A}_{45}^{\text {core }} \mathrm{A}_{55}^{\text {core }}
\end{array}\right]=\frac{\sqrt{3} \mathrm{kGh} \mathrm{t}}{\mathrm{~L}}\left[\begin{array}{cc}
1 & 0 \\
0 & 1
\end{array}\right]} \tag{J26}
\end{gather*}
$$

| REPORT DOCUMENTATION PAGE <br> Form Approved OMB No. 0704-0188 |  |  |
| :--- | :--- | :--- |
| The public reporting burden for this collection of information is estimated to average 1 hour per response, including the time for reviewing instructions, searching existing data sources, gathering and maintaining the data needed, and completing and reviewing the collection of information. Send comments regarding this burden estimate or any other aspect of this collection of information, including suggestions for reducing this burden, to Department of Defense, Washington Headquarters Services, Directorate for Information Operations and Reports (0704-0188), 1215 Jefferson Davis Highway, Suite 1204, Arlington, VA 22202-4302. Respondents should be aware that notwithstanding any other provision of law, no person shall be subject to any penalty for failing to comply with a collection of information if it does not display a currently valid OMB control number. <br> PLEASE DO NOT RETURN YOUR FORM TO THE ABOVE ADDRESS. |  |  |
| 1. REPORT DATE (DD-MM-YYYY) <br> 01-01-2011 |  | 3. DATES COVERED (From - To) |
| 4. TITLE AND SUBTITLE <br> A Treatise on Equivalent-Plate Stiffnesses for Stiffened <br> Laminated-Composite Plates and Plate-Like Lattices |  | 5b. GRANT NUMBER |
|  |  |  |
|  |  | 5c. PROGRAM ELEMENT NUMBER |
| 6. AUTHOR(S) <br> Nemeth, Michael P. |  | 5d. PROJECT NUMBER |
|  |  | 5e. TASK NUMBER |
|  |  | 136905.02.04.04.16.06 |
| 7. PERFORMING ORGANIZATION NAME(S) AND ADDRESS(ES) <br> NASA Langley Research Center <br> Hampton, VA 23681-2199 |  | 8. PERFORMING ORGANIZATION REPORT NUMBER <br> L-19728 |
| 9. SPONSORING/MONITORING AGENCY NAME(S) AND ADDRESS(ES) <br> National Aeronautics and Space Administration <br> Washington, DC 20546-0001 |  | 10. SPONSOR/MONITOR'S ACRONYM(S) <br> NASA |
|  |  | 11. SPONSOR/MONITOR'S REPORT NUMBER(S) <br> NASA/TP-2011-216882 |
| 12. DISTRIBUTION/AVAILABILITY STATEMENT <br> Unclassified - Unlimited <br> Subject Category 39 <br> Availability: NASA CASI (443) 757-5802 |  |  |
| 13. SUPPLEMENTARY NOTES |  |  |
| 14. ABSTRACT <br> A survey of studies conducted since 1914 on the use of equivalent-plate stiffnesses in modeling the overall, stiffness-critical response of stiffened plates and shells is presented. Two detailed, comprehensive derivations of first-approximation equivalent-plate stiffnesses are also presented that are based on the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. <br> Equivalent-plate stiffness expressions, and a corresponding symbolic manipulation computer program, are also presented for several different stiffener configurations. These expressions are very general and exhibit the full range of anisotropies permitted by the Reissner-Mindlin-type, first-order transverse-shear deformation theory for anisotropic plates. The expressions presented in the present study were also compared with available, previously published results. For the most part, the previously published results are for special cases of the general expressions presented herein and are almost in complete agreement. Analysis is also presented that extends the use of the equivalent-plate stiffness expressions to sandwich plates. |  |  |
| 15. SUBJECT TERMS <br> Homogenization; Equivalent-plate stiffnesses; Structural design; Single-layer grids; Lattices |  |  |
| 17. LIMITATION OF ABSTRACT | 18. NUMBER OF PAGES | STI Help Desk (email: help@sti.nasa.gov) |
|  |  |  |
|  |  | 19b. TELEPHONE NUMBER (Include area code) |
| U | 151 |  |

