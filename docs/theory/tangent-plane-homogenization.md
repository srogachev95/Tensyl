# Tangent-Plane Homogenization

Tangent-plane homogenization computes a local equivalent wall law for a
repeating stiffened cell that is treated as flat in the local tangent plane.
Curvature is not part of the first local cell stiffness assembly.

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
- $\mathbf T_m$ maps wall generalized strain into member beam strain.

The equivalent tangent is:

$$
\mathbf C_\text{wall}
=
\mathbf C_\text{skin}
+
\sum_m \Delta\mathbf C_m.
$$

The energy method is Tensyl's reference homogenizer because the assembled member
contribution is symmetric by construction and works for graph-like canonical
cells. Direct equilibrium-compatibility formulas are available for supported
straight stiffener-family cases and are tested against the energy path.

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
