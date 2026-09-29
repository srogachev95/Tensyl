# Homogenization and Results

After defining the skin and ribs, `EnergyHomogenizer().compute(cell)` returns the
plate stiffness, mass, modeling assumptions, and a report for the chosen response
scales. The [walkthrough](../getting-started/use-the-result.md) applies a load to
that result and recovers individual rib forces.

## Reading the Result

| Attribute | Use |
| --- | --- |
| `result.stiffness` | Solve loads and strains; read stiffness blocks and areal mass |
| `result.coefficients` | Read named entries such as `A11`, `B12`, and `D66` |
| `result.assumptions` | Read the member and section choices used in the calculation |
| `result.diagnostics` | Inspect rank, energy positivity, and neutral-surface offset |
| `result.validity` | Read scale ratios, coupling ratios, and warning codes |

`result.stiffness.validity` carries the same report. Saving the result also
preserves the assumptions and diagnostics. Use `print(result.summary())` for a
labeled display of all four blocks and the report.

## Reading the Blocks

`A` is membrane stiffness, `B` is membrane–bending coupling, `D` is bending
stiffness, and `As` is transverse shear stiffness. The
[plate relation](../theory/equivalent-stiffness.md) defines component order and
units. Compare entries in the same axes and at the same reference surface.

## Panel Mass

Panel mass per area includes the skin and all represented ribs:

$$
m_\text{panel} = m_\text{skin} + \frac{1}{A_\text{cell}}
\sum_{\text{members}} n_k\,L_k\,\mu_k ,
$$

where $n_k$ is the member multiplicity, $L_k$ its length inside the cell, and
$\mu_k$ its `BeamSection.mass_per_length`. Thin-wall sections fill in
$\mu_k = \rho A$ whenever their material has a density.


Supply material density or `BeamSection.mass_per_length` for every contribution.
When any contribution is unknown, `areal_mass` is `None` and the assumptions
record the missing mass. In SI, skin areal mass is kg/m² and rib mass per length
is kg/m.

## Diagnostics

`positive_semidefinite`, `minimum_eigenvalue`, and `rank` describe the assembled
energy operator. Rank eight means all eight generalized deformation modes have
resolved stiffness at the numerical tolerance. The report flags rank deficiency
or negative-energy modes; malformed inputs raise typed homogenization errors.

`neutral_surface_offset` gives the common shift that minimizes residual coupling
across the membrane modes. The
[modeling guide](../theory/validity.md#coupling-that-a-reference-shift-cannot-remove)
defines that diagnostic and its warning threshold.

The stored tangent is symmetric. Assembly checks floating-point residuals with
a scale-aware tolerance and projects roundoff differences onto exact symmetry.
Material asymmetry raises an error. Rank and energy checks are similarly scaled
so changing consistent units does not change the numerical judgment.

## Strains and Member Loads

Use `stiffness.strains(loads)` to solve the complete coupled relation, then
`member_loads(cell, strain)` to recover the rib forces. The
[executable load example](../getting-started/use-the-result.md) shows both calls.
A singular stiffness has no unique strain solution and raises `ValueError`.

Each returned `MemberLoads` corresponds to one entry in `cell.members`, with its
index and label. Its force and moment are for **one physical rib** under the
prescribed panel strain. Multiplicity and represented length enter the smeared
stiffness, while the recovered force uses the rib section directly.

In the member's local axes, the five work-conjugate strain measures and loads
are

$$
\begin{aligned}
N &= EA(\epsilon_{11}' + z_a\kappa_{11}'),\\
V_y &= kGA_y(\gamma_{12}' + z_s\kappa_{12}')/2,\\
V_z &= kGA_z\gamma_{13}',\\
M_y &= EI_y\kappa_{11}',\\
T &= -GJ\kappa_{12}'/2.
\end{aligned}
$$

Primes mean strain components expressed in the member axes. The positive
member direction follows `angle_rad`, its transverse in-plane direction makes
a right-handed frame with `+n`, and the eccentricities point along `+n`.
Positive axial force extends the rib. Moment and torque signs follow their
conjugate curvature and twist measures above; do not substitute an external
beam solver's end-force sign convention without a transformation. The factors
of one-half and negative twist sign come from the
[Nemeth member map](../theory/tangent-plane-homogenization.md).


The quantities are affine beam resultants. Omitted `kGAy` or `kGAz` gives zero
for that member shear force, matching the homogenization setup.

## Comparing ABD Stiffnesses

Compare the four blocks, mass, and reports after
[matching axes and reference surfaces](../theory/conventions.md). For a compact
inspection, `repr(stiffness)` gives the frame, mass, `A11`, `D11`, and warning
count. `summary(units=..., precision=...)` gives a report suitable for a log.
The labels describe your chosen units.

<span id="stiffener-families"></span>
[Independent families](rib-patterns.md#independent-families) provide another way
to build the cell. [Parameter sweeps](external-workflows.md#parameter-sweeps)
compare multiple designs in named output columns.

## Thermal Loading of a Stiffened Cell

For the aluminum cell in the [family example](rib-patterns.md), add the skin's
thermal resultants and the members' uniform axial expansion:

```python
--8<-- "docs/examples/scripts/panel_workflows.py:cell-thermal"
```

Each member contributes, per kelvin,

$$\mathbf r_{T,m}=\frac{\mu_mL_m}{A_\mathrm{cell}}\mathbf T_m^T
[EA\alpha,0,0,0,0]^T.$$

This follows by expanding its axial energy
$\tfrac12EA(\epsilon_m-\alpha\Delta T)^2$. The member map supplies the angle
projection and eccentric moment. All expansion coefficients must be explicit;
isotropic section helpers inherit `alpha` from their material.

The example's uniform aluminum panel expands freely with zero net rib axial
force to roundoff. `member_loads` evaluates the mechanical strain contribution,
so subtract `EA * alpha * delta_temperature` to obtain the net axial force.
For the plate-level thermal sign and combined mechanical loads, see
[temperature changes](materials-and-laminates.md#uniform-temperature-changes).
Keep the thermal object alongside the mechanical stiffness in an export.
