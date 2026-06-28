# FEM Solver Handoff

Tensyl computes an equivalent wall law. A finite-element solver consumes that law
through whatever shell-section machinery it provides. Sometimes that machinery is
a reduced orthotropic material. Sometimes it is a preintegrated shell stiffness.
Sometimes it is a dialect-specific card that needs a careful audit before anyone
lets it near a margin.

This page describes practical handoff routes for NASTRAN, ANSYS, and Abaqus. It
does not make Tensyl a solver-deck writer. Use the YAML or JSON artifact from
[External Workflows](external-workflows.md) as the traceable source, then translate
the checked stiffness into the target solver input.

## Before Solver Input

Tensyl's local generalized strain order is:

$$
\boldsymbol\eta =
\begin{bmatrix}
\epsilon_{11}^0 &
\epsilon_{22}^0 &
\gamma_{12}^0 &
\kappa_{11} &
\kappa_{22} &
\kappa_{12} &
\gamma_{13}^0 &
\gamma_{23}^0
\end{bmatrix}^T.
$$

The matching resultants are:

$$
\mathbf r =
\begin{bmatrix}
N_{11} &
N_{22} &
N_{12} &
M_{11} &
M_{22} &
M_{12} &
Q_{13} &
Q_{23}
\end{bmatrix}^T.
$$

For solvers that take a six-by-six shell section stiffness, the part to hand off
is:

$$
\mathbf K_{ABD} =
\begin{bmatrix}
\mathbf A & \mathbf B \\
\mathbf B & \mathbf D
\end{bmatrix}
$$

with row and column order:

$$
(11,\ 22,\ 12,\ k11,\ k22,\ k12).
$$

The transverse-shear block is separate:

$$
\mathbf A_s =
\begin{bmatrix}
A_{s11} & A_{s12} \\
A_{s12} & A_{s22}
\end{bmatrix}.
$$

Keep these checks explicit:

- Use one unit system. `A` and `As` have force/length units, `B` has force units,
  and `D` has force-length units.
- Align local solver material axes with Tensyl's `e1` and `e2`. For the built-in
  `Cylinder`, `e1` is axial and `e2` is circumferential.
- Match the reference surface. Moving the solver section offset without shifting
  the ABD law changes `B`.
- Preserve the engineering shear and engineering twist convention. Quiet
  factor-of-two errors are unusually good at looking respectable.
- Review `result.validity.warnings` before export. A solver will not know whether
  a stiffener pitch is too large for the homogenization assumption.

## Reduced Orthotropic Properties

The simplest route is to convert the membrane block to equivalent orthotropic
plane-stress constants and let the solver build a conventional shell section.
This is useful for preliminary modal, static, or sizing models when the wall is
nearly uncoupled.

Choose an effective shell thickness `t_eff`. Then form:

$$
\mathbf Q_\mathrm{eff} = \frac{\mathbf A}{t_\mathrm{eff}},
\qquad
\mathbf S_\mathrm{eff} = \mathbf Q_\mathrm{eff}^{-1}.
$$

For local axes aligned with the orthotropic axes:

$$
E_1 = \frac{1}{S_{11}},
\quad
E_2 = \frac{1}{S_{22}},
\quad
G_{12} = \frac{1}{S_{66}},
\quad
\nu_{12} = -\frac{S_{12}}{S_{11}},
\quad
\nu_{21} = -\frac{S_{12}}{S_{22}}.
$$

Use this route only when the terms it discards are intentionally negligible:

- membrane-bending coupling `B`;
- off-axis membrane coupling `A16` and `A26`;
- off-axis bending coupling `D16` and `D26`;
- transverse shear details if the chosen shell element computes them from the
  material and thickness.

This preserves the chosen membrane compliance. It does not generally preserve
the bending block, eccentric stiffener coupling, or transverse-shear stiffness.
If those are carrying the physics, use a richer workflow.

```python
import numpy as np


def equivalent_orthotropic_from_A(stiffness, t_eff):
    """Return membrane-equivalent plane-stress constants in Tensyl's units."""

    q_eff = stiffness.A / t_eff
    s_eff = np.linalg.inv(q_eff)
    return {
        "E1": 1.0 / s_eff[0, 0],
        "E2": 1.0 / s_eff[1, 1],
        "G12": 1.0 / s_eff[2, 2],
        "nu12": -s_eff[0, 1] / s_eff[0, 0],
        "nu21": -s_eff[0, 1] / s_eff[1, 1],
    }
```

## NASTRAN

NASTRAN is a family name more than a single interface. MSC Nastran, NX Nastran,
Autodesk Nastran, OptiStruct, and pyNastran-supported decks share familiar bulk
data cards, but full shell-section stiffness support is not equally portable.
Treat the target solver manual and a patch test as part of the data handoff.

### Simple Route: `MAT8` And `PSHELL`

For an uncoupled equivalent orthotropic wall:

1. Convert `A/t_eff` to `E1`, `E2`, `G12`, and `nu12`.
2. Define a `MAT8` with those in-plane constants.
3. Define a `PSHELL` with thickness `t_eff`, using the `MAT8` as the membrane and
   bending material.
4. Use element material-angle fields or coordinate systems so material direction
   1 matches Tensyl `e1`.

This is the most portable route. It is also the most approximate route.

```text
$ Illustrative only: field layout and defaults vary by dialect.
MAT8, 101, E1, E2, NU12, G12, G1Z, G2Z, RHO
PSHELL, 201, 101, T_EFF, 101
```

Use `PCOMP` or `PCOMPG` instead when the equivalent wall is better represented as
a laminate stack and you want the solver to integrate ply stiffnesses. An
unsymmetric laminate can produce membrane-bending coupling, but it is still a
laminate model, not an arbitrary ABD matrix fit.

### Higher Fidelity: `PSHELL` Material References

The `PSHELL` card has separate material references for membrane, bending,
transverse shear, and membrane-bending coupling in common NASTRAN-style card
sets. pyNastran's public card reference, for example, exposes `MID1`, `MID2`,
`MID3`, and `MID4`, where `MID4` is the membrane-bending coupling material and
`MID3` is transverse shear.

That structure is tempting for Tensyl because `A`, `B`, `D`, and `As` are also
separate blocks. Do not assume it is a direct arbitrary-ABD interface without
verification. In many workflows the material cards and `PSHELL` thickness fields
still imply solver-specific scaling. The safe workflow is:

1. Determine from the target NASTRAN manual whether `MAT2`/`MAT8` plus `MID1` to
   `MID4` can represent the exact block you need.
2. Account for all thickness and inertia scale factors, including `12I/T**3` and
   transverse-shear factors.
3. Print or recover the element section stiffness from the solver when possible.
4. Run a one-element patch model with imposed membrane strains and curvatures,
   then compare recovered resultants with `K_ABD @ eta`.

If the target dialect cannot reproduce the full `A/B/D` matrix within tolerance,
keep the NASTRAN model reduced and document the approximation.

## ANSYS

ANSYS Mechanical APDL has a direct preintegrated shell-section path. The current
command reference lists `SECTYPE,,GENS` as a preintegrated general shell section
and identifies `SSPA`, `SSPB`, `SSPD`, and `SSPE` as the follow-on commands for
membrane, coupling, bending, and transverse shear. The command
field layouts are:

| Tensyl block | ANSYS command | Field order |
| --- | --- | --- |
| `A` | `SSPA` | `A11, A21, A31, A22, A32, A33, T` |
| `B` | `SSPB` | `B11, B21, B31, B22, B32, B33, T, B12, B13, B23` |
| `D` | `SSPD` | `D11, D21, D31, D22, D32, D33, T` |
| `As` | `SSPE` | `E11, E21, E22, T` |

The first six fields are the lower symmetric part of each three-by-three block:
`11`, `21`, `31`, `22`, `32`, `33`. For Tensyl's symmetric `B`, omit the optional
upper `B12`, `B13`, and `B23` fields unless the solver workflow specifically asks
for them.

```text
! Illustrative APDL fragment.
SECTYPE, 10, GENS, , TENSYL_WALL
SSPA, A11, A12, A16, A22, A26, A66, T_REF
SSPB, B11, B12, B16, B22, B26, B66, T_REF
SSPD, D11, D12, D16, D22, D26, D66, T_REF
SSPE, AS11, AS12, AS22, T_REF
SECNUM, 10
```

Use `T_REF` as the nominal section thickness required by the solver command
syntax and stress-output workflow. The preintegrated stiffness terms still need
to be entered with their actual integrated units.

For a reduced workflow, define an orthotropic material with `MP`/`TB` data and a
normal shell section thickness. That route is easier to inspect in Mechanical,
but it inherits the same limitations as the reduced-property method above.

## Abaqus

Abaqus has two relevant routes:

- material-based shell sections for reduced orthotropic workflows;
- direct general shell sections for full linear section stiffness.

For the direct route, omit `MATERIAL`, `COMPOSITE`, and `USER` on
`*SHELL GENERAL SECTION`. Abaqus then reads the symmetric half of the six-by-six
section stiffness matrix, 21 entries total, eight entries on each of the first
two lines and five on the third line. Abaqus also accepts an
`ORIENTATION` parameter, which should align section direction 1 with Tensyl
`e1`.

Pack:

$$
\mathbf K =
\begin{bmatrix}
A_{11} & A_{12} & A_{16} & B_{11} & B_{12} & B_{16} \\
A_{12} & A_{22} & A_{26} & B_{12} & B_{22} & B_{26} \\
A_{16} & A_{26} & A_{66} & B_{16} & B_{26} & B_{66} \\
B_{11} & B_{12} & B_{16} & D_{11} & D_{12} & D_{16} \\
B_{12} & B_{22} & B_{26} & D_{12} & D_{22} & D_{26} \\
B_{16} & B_{26} & B_{66} & D_{16} & D_{26} & D_{66}
\end{bmatrix}.
$$

The data order is:

```text
K11, K12, K22, K13, K23, K33, K14, K24,
K34, K44, K15, K25, K35, K45, K55, K16,
K26, K36, K46, K56, K66
```

An illustrative input fragment:

```text
*SHELL GENERAL SECTION, ELSET=wall, ORIENTATION=tensyl_axes, DENSITY=rho_area
A11, A12, A22, A16, A26, A66, B11, B12
B16, D11, B12, B22, B26, D12, D22, B16
B26, B66, D16, D26, D66
*TRANSVERSE SHEAR STIFFNESS
AS11, AS22, AS12
```

The transverse shear line is separate. Abaqus documents
`*TRANSVERSE SHEAR STIFFNESS` as a shell-compatible option with first-direction
stiffness, second-direction stiffness, and coupling term fields.

For a reduced workflow, define an engineering-constants material and use
`*SHELL SECTION` or a material-based `*SHELL GENERAL SECTION`. That is convenient
when `B = 0` and the wall behaves like a conventional orthotropic shell. It is
not a substitute for the direct 21-entry stiffness when the stiffeners introduce
important eccentricity coupling.

## Patch Check

Before using a translated stiffness in a production model, run a one-element
check in the target solver:

1. Use one shell element with the intended section, orientation, offset, and
   units.
2. Impose a pure `epsilon11`, `epsilon22`, `gamma12`, `kappa11`, `kappa22`, and
   `kappa12` case, one at a time if the solver setup allows it.
3. Compare solver-reported section forces and moments with:

   $$\mathbf r_{ABD} = \mathbf K_{ABD}\boldsymbol\eta_{ABD}.$$

4. For transverse shear flexible elements, apply independent shear checks against
   `As`.

The patch check is not busywork. It is how you catch axis swaps, offset mistakes,
solver-specific scaling, and the occasional perfectly formatted wrong number.

Next: [SP-8007 Data Handoff](sp8007-data-handoff.md).

## References

- Abaqus 2024, `*SHELL GENERAL SECTION`, direct stiffness data lines and
  orientation parameter:
  <https://docs.software.vt.edu/abaqusv2024/English/SIMACAEKEYRefMap/simakey-r-shellgeneralsection.htm>.
- Abaqus 2024, `*TRANSVERSE SHEAR STIFFNESS`:
  <https://docs.software.vt.edu/abaqusv2024/English/SIMACAEKEYRefMap/simakey-r-transverseshearstiffness.htm>.
- ANSYS 2024 R2 command reference, `SECTYPE`, shell section considerations for
  `GENS`:
  <https://ansyshelp.ansys.com/public/Views/Secured/corp/v242/en/ans_cmd/Hlp_C_SECTYPE.html>.
- ANSYS command reference mirror, `SSPA`, `SSPB`, `SSPD`, and `SSPE` command
  field layouts:
  <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_SSPA.html>,
  <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_SSPB.html>,
  <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_SSPD.html>,
  and
  <https://www.mm.bme.hu/~gyebro/files/ans_help_v182/ans_cmd/Hlp_C_SSPE.html>.
- pyNastran shell property reference, `PSHELL` fields and material references:
  <https://pynastran-git.readthedocs.io/en/latest/reference/bdf/cards/properties/pyNastran.bdf.cards.properties.shell.html>.
