# Tangent-Plane Homogenization

Tangent-plane homogenization computes a local equivalent ABD stiffness for a
repeating stiffened cell that is treated as flat in the local tangent plane.
The cell is assembled in the local `e1`-`e2` plane. Surface curvature is handled
later by geometry embedding and validity checks, not by the first local cell
stiffness assembly.

For a cell with area $A_\text{cell}$, a beam member contributes:

$$
\Delta\mathbf C_m =
\frac{\mu_m L_m}{A_\text{cell}}
\mathbf T_m^T\mathbf K_m\mathbf T_m.
$$

Here:

- $\mu_m$ is multiplicity;
- $L_m$ is member length;
- $\mathbf K_m$ is the member stiffness matrix;
- $\mathbf T_m$ is the *member strain map*: it projects the stiffness's generalized
  strain onto each member's beam strain. This map is the hinge of the whole
  method, and it is referenced by name in the diagnostics below.

The equivalent tangent is:

$$
\mathbf C_\text{stiffness}
=
\mathbf C_\text{skin}
+
\sum_m \Delta\mathbf C_m.
$$

The energy method is Tensyl's reference homogenizer because the assembled
member contribution is symmetric by construction and works for graph-like
canonical cells. Direct equilibrium-compatibility formulas are available for
supported straight stiffener-family cases and are tested against the energy
path.

This follows the equivalent-plate idea used by Nemeth for stiffened laminated
plates and plate-like lattices. Tensyl treats those formulas as mechanics
guidance and keeps the energy path as the executable reference.

## Inputs

- `skin` is an `ABDStiffness` for the unstiffened skin or laminate.
- `BeamSection` supplies centroidal beam stiffness products. Tensyl does not
  currently compute those values from cross-section dimensions.
- `BeamMember` supplies member length, angle, eccentricity, and multiplicity
  inside a finite canonical cell.
- `StiffenerFamily` supplies angle, spacing, eccentricity, and multiplicity for
  the direct equilibrium-compatibility path.
- `CanonicalUnitCell.area` is the tangent-plane area represented by one
  repeated cell.

## Beam Section Quantities

`BeamSection` stores centroidal member-local stiffnesses:

| Quantity | Meaning | Common units, US customary |
| --- | --- | --- |
| `EA` | axial stiffness | `lbf` |
| `EIy` | bending stiffness about member-local `y` | `lbf*in^2` |
| `EIz` | bending stiffness about member-local `z` | `lbf*in^2` |
| `GJ` | torsional stiffness | `lbf*in^2` |
| `kGAy` | in-plane shear stiffness | `lbf` |
| `kGAz` | transverse shear stiffness | `lbf` |

Omitted shear stiffnesses contribute zero in the current homogenizer and are
recorded as assumptions in the result.

`BeamSection` asks for stiffness products (`EA`, `EIy`, `EIz`, `GJ`, `kGAy`,
`kGAz`) because the current homogenizer consumes centroidal beam stiffnesses.
Section-property calculation from raw cross-section geometry is outside the
current API.

## Diagnostics

The homogenizer returns `HomogenizationResult`, not just an ABD stiffness. The result
records:

- symmetry, positive-semidefinite status, rank, member count, and cell area;
- assumptions attached to the member strain map and section inputs;
- a `ValidityReport` with scale-separation ratios and warning codes.

!!! note "Two methods agreeing is necessary, not sufficient"
    Energy-vs-direct agreement is a good sign, but it is not proof. Both paths
    share the same member strain map, so they can agree and still be wrong
    together. For high-consequence use, you still need independent literature,
    test, or finite-element evidence.

## Limits

The first homogenizer is a tangent-plane model. It does not model local joints,
fasteners, stiffener crippling, curved stiffener geodesics, or full shell
equilibrium. Use geometry validity ratios such as `h_over_R`, `p_over_R`, and
`p_over_L_response` to decide whether the local flat-cell assumption is
reasonable for the intended response mode.
