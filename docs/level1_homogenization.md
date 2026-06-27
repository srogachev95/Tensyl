# Level 1 Homogenization

Level 1 computes a local tangent-plane equivalent wall law for a repeating
stiffened cell. It follows Tensyl's core rule: homogenization computes a local
constitutive law, while shell geometry remains a separate embedding layer.

The implementation is anchored in Nemeth's first-approximation
equivalent-plate formulation, where stiffener-member strain energy is expressed
in terms of generalized plate strains and divided by the basic-cell area
[Nemeth 2011].

## Scope

The Phase 2 implementation supports:

- centroidal beam-section stiffnesses;
- straight beam members with length, angle, eccentricity, and multiplicity;
- canonical unit cells with a skin `LinearABDWall`;
- the energy-equivalence homogenizer as the reference method;
- direct equilibrium-compatibility homogenization for straight stiffener
  families;
- unidirectional, orthogrid, and equilateral-isogrid constructors;
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
membrane or bending terms is still outside the Phase 2 public law.

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
