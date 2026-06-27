# Level 1 Homogenization

Level 1 computes a local tangent-plane equivalent wall law for a repeating
stiffened cell. It follows Tensyl's core rule: homogenization computes a local
constitutive law, while shell geometry remains a separate embedding layer.

The implementation is anchored in Nemeth's first-approximation
equivalent-plate formulation, where stiffener-member strain energy is expressed
in terms of generalized plate strains and divided by the basic-cell area
[Nemeth 2011].

## Scope

The current implementation supports:

- centroidal beam-section stiffnesses;
- straight beam members with length, angle, eccentricity, and multiplicity;
- graph cells via `CellNode`, `CellEdge`, and `graph_unit_cell`;
- canonical unit cells with a skin `LinearABDWall`;
- the energy-equivalence homogenizer as the reference method;
- direct equilibrium-compatibility homogenization for straight stiffener
  families;
- unidirectional, orthogrid, braced orthogrid, isosceles-triangle, Kagome,
  hexagonal, and star-cell constructors;
- sandwich-core constructors with explicit face-sheet reference-surface offsets;
- diagnostics and validity reports.

It does not recover local stresses, model stiffener intersections, solve
cell-scale finite-element RVEs, or add curvature to the local homogenizer.

## Beam Sections And Members

`BeamSection` stores member-local stiffnesses:

$$
EA,\quad EI_y,\quad EI_z,\quad GJ,\quad kGA_y,\quad kGA_z .
$$

`EA` is axial stiffness, `EIy` is out-of-plane bending stiffness, `EIz` is
in-plane bending stiffness, and `GJ` is torsional stiffness. The optional shear
stiffnesses `kGAy` and `kGAz` contribute in-plane stiffener shear and transverse
stiffener shear. If either is omitted, that shear contribution is zero and the
assumption is recorded in the homogenization result.

`BeamMember.eccentricity` is positive from the wall reference surface along the
positive normal `Frame2D.n`. With member-local \(X\) along the stiffener and
\(Z\) equal to the wall normal, the implemented first-approximation beam strain
map is:

$$
\epsilon_X = \epsilon_{XX}^0 + z_s\kappa_{XX},
$$

$$
\Gamma_{XY} = \frac{1}{2}\left(\gamma_{XY}^0-z_s\kappa_{XY}\right),
$$

$$
\Gamma_{XZ} = \gamma_{XZ}^0,
\qquad
\chi_Z = \kappa_{YY},
\qquad
\chi_Y = \kappa_{XX},
\qquad
\tau = -\frac{1}{2}\kappa_{XY}.
$$

The one-half factors follow the first-approximation shear and twist averaging
used in Nemeth's beam-cell energy method [Nemeth 2011].

## Graph And Canonical Cells

`graph_unit_cell` converts a local tangent-plane graph into `BeamMember`
objects by computing each edge length and orientation from its endpoint
coordinates. Node indices are zero-based. The resulting cell still uses the
same energy-equivalence equation as every other canonical cell.

Named constructors are convenience layers over the same member-density model:

- `braced_orthogrid_cell` supports crossed diagonal braces and an alternating
  single-brace case. The single-brace case keeps both diagonal orientations but
  assigns each half the crossed-brace density, matching Nemeth's \(n=1/2\)
  convention for singly braced bays [Nemeth 2011].
- `isosceles_triangle_grid_cell` and `kagome_cell` use the same family-density
  reduction for matching inputs, consistent with Nemeth's Appendix C statement
  that the Kagome output is identical to the isosceles-triangle output under the
  listed assumptions [Nemeth 2011].
- `hexagonal_grid_cell` and `star_cell` follow the basic-cell layouts used in
  Nemeth's Appendix E program. `regular_hexagonal_grid_cell` and
  `equilateral_star_cell` provide identical-member special cases.

These constructors do not model joint details, local stress recovery, or
finite-width intersection effects. They only define member energy contributions
for the first-approximation equivalent wall.

## Reference Surfaces And Sandwich Faces

`shift_reference_surface(wall, offset)` expresses a `LinearABDWall` about a new
reference surface. The signed `offset` is measured from the wall's current
reference surface to the new one along `Frame2D.n`.

For a new reference surface offset by \(d\), membrane strain at the old surface
is:

$$
\boldsymbol\epsilon_\text{old}
= \boldsymbol\epsilon_\text{new} - d\boldsymbol\kappa .
$$

Tensyl applies that strain transformation to the full wall tangent. This makes
face-sheet superposition explicit for sandwich cells: shift each face sheet to
the sandwich reference plane, superpose the shifted face laws with
`superpose_linear_abd_walls`, then add the core members through the ordinary
energy homogenizer.

## Energy Homogenizer

For a cell with area \(A_\text{cell}\), each member contributes:

$$
\Delta\mathbf C_m =
\frac{\mu_m L_m}{A_\text{cell}}
\mathbf T_m^T\mathbf K_m\mathbf T_m ,
$$

where \(\mu_m\) is member multiplicity, \(L_m\) is member length,
\(\mathbf K_m\) is the member stiffness matrix, and \(\mathbf T_m\) maps the
global generalized wall strain vector into member beam strains.

The equivalent wall tangent is:

$$
\mathbf C_\text{wall}
=
\mathbf C_\text{skin}
+
\sum_m \Delta\mathbf C_m .
$$

The result is returned as a `LinearABDWall`, so transverse-shear coupling to
membrane or bending terms is still outside the current public law.

Example:

```python
from tensyl import BeamSection, EnergyHomogenizer, IsotropicMaterial
from tensyl import isotropic_plate, orthogrid_cell

skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)
section = BeamSection(
    EA=1.2e6,
    EIy=50.0,
    EIz=30.0,
    GJ=20.0,
    kGAy=4.0e5,
    kGAz=3.0e5,
)

cell = orthogrid_cell(
    skin=skin,
    stringer_section=section,
    rib_section=section,
    stringer_spacing=0.25,
    rib_spacing=0.40,
    stringer_eccentricity=0.012,
    rib_eccentricity=0.009,
)

result = EnergyHomogenizer().compute(cell)
wall = result.law
```

## Direct Family Homogenizer

`DirectECHomogenizer` uses the same member contribution but replaces
\(L_m/A_\text{cell}\) with the family length density:

$$
\frac{\mu}{d},
$$

where \(d\) is family spacing. It is therefore limited to continuous straight
stiffener families and is tested against the energy method for matching
canonical cells.

## Validity Reports

`ValidityContext` can provide:

- characteristic stiffener height \(h_s\);
- pitch \(p\);
- minimum geometry radius \(R_\text{min}\);
- response length \(L_\text{response}\).

The default warning thresholds are:

$$
\frac{h_s}{R_\text{min}}\ge 0.05,
\qquad
\frac{p}{R_\text{min}}\ge 0.05,
\qquad
\frac{p}{L_\text{response}}\ge 0.05.
$$

The result also reports a membrane-bending coupling ratio:

$$
\frac{\|\mathbf B\|_F}{\sqrt{\|\mathbf A\|_F\|\mathbf D\|_F}},
$$

with a default warning threshold of `0.10`.

These warnings do not make a law invalid by themselves. They mark cases where
the analyst should review whether a local tangent-plane equivalent wall is
appropriate for the intended structural response.
