# FEM Solver Handoff

Tensyl computes an equivalent ABD stiffness. A finite-element solver consumes
that stiffness through whatever shell-section machinery it provides. Sometimes
that machinery is a reduced orthotropic material. Sometimes it is a
preintegrated shell stiffness. Sometimes it is a solver-specific section option
that benefits from a quick patch check before it joins the serious model.

This page describes practical handoff routes for NX Nastran, ANSYS, and Abaqus.
A YAML or JSON artifact from [External Workflows](external-workflows.md) is still
a useful traceability record: it keeps the stiffness, units, validity warnings,
and assumptions together while the solver input gets the particular syntax it
needs.

## Before Solver Input

Tensyl's canonical generalized strain and resultant order is defined in
[Equivalent-Stiffness Mechanics](../theory/equivalent-stiffness.md). Treat that
ordering as part of the data contract, not as a formatting preference.

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
  the ABD stiffness changes `B`.
- Preserve the engineering shear and engineering twist convention.
- Review `result.validity.warnings` before export. The solver sees stiffness
  numbers; the validity context has to travel with the model.

When a solver card, spreadsheet, or hand equation wants scalar terms, use the
named coefficient view instead of indexing matrices throughout the export code:

```python
coefficients = result.coefficients

print(coefficients.A11, coefficients.B12, coefficients.D66, coefficients.As22)
```

## Reduced Orthotropic Properties

The simplest route is to convert the membrane block to equivalent orthotropic
plane-stress constants and let the solver build a conventional shell section.
This is useful for preliminary modal, static, or sizing models when the ABD
stiffness is nearly uncoupled.

Choose an effective shell thickness `t_eff`. In this context, `t_eff` is the
thickness that the downstream shell property will use with the reduced material
constants. It is the bookkeeping thickness for the solver handoff, not something
Tensyl can discover from the ABD matrix alone.

The reduction forms:

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

!!! note "What the reduced route keeps"
    This preserves the chosen membrane compliance. It does not generally
    preserve the bending block, eccentric stiffener coupling, or transverse-shear
    stiffness. If those are carrying the physics, use a richer workflow.

Use the reduced route when the terms it discards are intentionally negligible:

- membrane-bending coupling `B`;
- off-axis membrane coupling `A16` and `A26`;
- off-axis bending coupling `D16` and `D26`;
- transverse shear details if the chosen shell element computes them from the
  material and thickness.

```python
props = result.reduced_orthotropic_properties(t_eff=0.080)

print(props.E1, props.E2, props.G12, props.nu12)
print(props.warnings)
```

Common `t_eff` choices are:

- the physical skin or laminate thickness when the model is skin-dominated;
- the total smeared structural depth for a coarse stiffened-shell study;
- a project-defined shell property thickness chosen to match mass, stress-output,
  or legacy model conventions.

Changing `t_eff` changes the reported `E1`, `E2`, and `G12`, but the membrane
reduction stays consistent because `A = Q_eff * t_eff`. Just keep a record of
which thickness the reduction used.

## NX Nastran

For NX Nastran, the most common handoff is through ordinary Bulk Data shell
properties and materials. The examples below use NX Nastran-style `MAT8`,
`PSHELL`, and laminate-property workflows. Check the installed Siemens NX Nastran
Quick Reference Guide for the exact field definitions used by your solver
release.

### Simple Route: `MAT8` and `PSHELL`

For an uncoupled equivalent orthotropic stiffness:

1. Use `result.reduced_orthotropic_properties(t_eff=...)` to obtain `E1`, `E2`,
   `G12`, and `nu12`.
2. Define a `MAT8` with those in-plane constants.
3. Define a `PSHELL` with thickness `t_eff`, using the `MAT8` as the membrane and
   bending material.
4. Use element material-angle fields or coordinate systems so material direction
   1 matches Tensyl `e1`.

This route is easy to inspect and works well when the equivalent stiffness is
close to a conventional orthotropic shell.

```text
$ Illustrative NX Nastran-style Bulk Data fragment.
MAT8, 101, E1, E2, NU12, G12, G1Z, G2Z, RHO
PSHELL, 201, 101, T_EFF, 101
```

Use `PCOMP` or `PCOMPG` instead when the equivalent stiffness is better
represented as a laminate stack and you want the solver to integrate ply
stiffnesses. An unsymmetric laminate can produce membrane-bending coupling, but
it is still a laminate model, not an arbitrary ABD matrix fit.

!!! note "Good first model"
    `MAT8` plus `PSHELL` is a useful first model when membrane behavior is the
    main target. It is not meant to preserve every term of a general stiffened
    ABD matrix.

### Higher Fidelity: `PSHELL` Material References

The `PSHELL` card has separate material references for membrane, bending,
transverse shear, and membrane-bending coupling through `MID1`, `MID2`, `MID3`,
and `MID4`. That lines up nicely with the way Tensyl reports `A`, `D`, `As`, and
`B`, but the card fields still carry NX Nastran's shell-property scaling rules.

Use this path when you have verified the mapping for the NX Nastran solution
sequence and element family you plan to use:

1. Decide whether `MAT2` or `MAT8` is the right material card for each block.
2. Account for `PSHELL` thickness and bending-inertia factors, including
   `12I/T**3`, and any transverse-shear factors.
3. Print or recover the element section stiffness from NX Nastran when that
   output is available.
4. Run a one-element patch model with imposed membrane strains and curvatures,
   then compare recovered resultants with `K_ABD @ eta`.

!!! warning "Verify the section stiffness"
    `MID1` through `MID4` can be a useful high-fidelity path, but it is not a
    universal "paste the ABD matrix here" slot. If the recovered section
    stiffness does not match the Tensyl matrix within the tolerance needed for
    the analysis, keep the NX Nastran model reduced and document the
    approximation.

## ANSYS

ANSYS Mechanical APDL has a direct preintegrated shell-section path. The current
command reference lists `SECTYPE,,GENS` as a preintegrated general shell section
and identifies `SSPA`, `SSPB`, `SSPD`, and `SSPE` as the follow-on commands for
membrane, coupling, bending, and transverse shear. The command
field layouts are:

| Tensyl block | ANSYS command | Field order |
| --- | --- | --- |
| `A` | `SSPA` | `A11, A12, A16, A22, A26, A66, T` |
| `B` | `SSPB` | `B11, B12, B16, B22, B26, B66, T` |
| `D` | `SSPD` | `D11, D12, D16, D22, D26, D66, T` |
| `As` | `SSPE` | `As11, As12, As22, T` |

The first six stiffness fields are the lower symmetric half of each
three-by-three block, taken column by column: `(1,1)`, `(2,1)`, `(6,1)`,
`(2,2)`, `(6,2)`, `(6,6)`, written here with Tensyl's engineering index `6` for
the in-plane shear/twist component. `SSPB` also accepts three optional
off-diagonal fields for a non-symmetric coupling block; Tensyl's `B` is
symmetric, so those repeat the lower terms and can be omitted unless the solver
workflow specifically asks for them.

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
*SHELL GENERAL SECTION, ELSET=panel, ORIENTATION=tensyl_axes, DENSITY=rho_area
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
when `B = 0` and the ABD stiffness behaves like a conventional orthotropic
shell. It is not a substitute for the direct 21-entry stiffness when stiffener
eccentricity coupling matters.

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

!!! tip "Small model, large leverage"
    The patch check catches axis swaps, offset mistakes, solver-specific scaling,
    and the occasional perfectly formatted wrong number. A single element is
    cheap; a bad coordinate system can get expensive.

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
- Siemens NX Nastran Quick Reference Guide, `MAT8`, `PSHELL`, `PCOMP`, `PCOMPG`,
  and `MAT2` Bulk Data entries. Use the guide installed with the NX Nastran
  release being used for analysis.
- pyNastran shell property reference, `PSHELL` fields and material references
  as an accessible cross-check for common NASTRAN Bulk Data names:
  <https://pynastran-git.readthedocs.io/en/latest/reference/bdf/cards/properties/pyNastran.bdf.cards.properties.shell.html>.
