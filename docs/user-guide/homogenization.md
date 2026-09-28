# Homogenization and Results

`EnergyHomogenizer` turns a repeating skin-and-stiffener cell into one equivalent
ABD stiffness. This is Tensyl's reference calculation.

```python
from tensyl import EnergyHomogenizer

result = EnergyHomogenizer().compute(cell)
stiffness = result.stiffness
```

`result.stiffness` is an `ABDStiffness`. The same validity report is attached to
`stiffness.validity`, so warnings travel with the ABD stiffness when it is passed
to later workflow steps.

Keep the result object rather than extracting only its matrix. It carries the
stiffness and the information needed to judge the calculation:

- `result.stiffness.A`, `B`, `D`, and `As` are the stiffness blocks;
- `result.diagnostics` reports numerical checks such as symmetry, rank, and
  positive-semidefinite status;
- `result.assumptions` records modeling assumptions;
- `result.validity.warnings` reports scale-separation and coupling warnings.
- `result.validity.coupling_ratios["B_residual"]` measures coupling after the
  best common reference shift. It drives the coupling warning and is unchanged
  by rotating the axes or shifting the reference surface.
- `result.diagnostics["neutral_surface_offset"]` gives that shift along `+n`
  in the model's length units. See the [derivation](../theory/validity.md).

## Stiffener Families

Some panels are easier to describe family by family than as a drawn repeat
cell: stringers every 6 in, rings every 20 in, and a set of diagonals at 30
degrees whose spacing shares no common box with either. Build those with
`stiffener_family_cell` and homogenize them the same way:

```python
import math

from tensyl import BeamSection, IsotropicMaterial, StiffenerFamily, isotropic_plate
from tensyl import EnergyHomogenizer, stiffener_family_cell

skin = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33), thickness=0.08)
stringer = BeamSection(EA=3.2e5, EIy=2.4e3, EIz=6.5e2, GJ=4.0e2)

cell = stiffener_family_cell(
    skin=skin,
    families=(
        StiffenerFamily(section=stringer, spacing=6.0, angle_rad=0.0, axial_eccentricity=0.3),
        StiffenerFamily(
            section=stringer, spacing=20.0, angle_rad=0.5 * math.pi, axial_eccentricity=0.3
        ),
    ),
)
result = EnergyHomogenizer().compute(cell)
```

Each family adds `multiplicity / spacing` of member length per unit panel area,
so the families never need to fit one repeat box. The cell has no drawable
geometry for the same reason.

Earlier releases had a separate `DirectECHomogenizer` for this input. It ran
the same member strain map through the same assembly, so its agreement with the
energy path checked nothing, and it has been folded into this one path. The
test suite now checks family stiffnesses against the classical smeared-stiffener
formulas written out term by term, which is an independent check of the
assembly.

## Reading the Result

`HomogenizationResult` is the main object to inspect after computing a stiffened
ABD stiffness.

```python
from tensyl import (
    BeamSection,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)

skin = isotropic_plate(
    IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
    thickness=0.080,
)
section = BeamSection(
    EA=3.2e6,
    EIy=2.4e4,
    EIz=6.5e3,
    GJ=4.0e3,
    kGAy=1.1e6,
    kGAz=0.9e6,
)
cell = orthogrid_cell(
    skin=skin,
    e1_section=section,
    e2_section=section,
    e1_pitch=8.0,
    e2_pitch=6.0,
    e1_axial_eccentricity=0.45,
    e2_axial_eccentricity=0.45,
)

result = EnergyHomogenizer().compute(
    cell,
    validity_context=ValidityContext(
        characteristic_height=0.50,
        pitch=8.0,
        min_radius=120.0,
        response_length=80.0,
    ),
)

print(result.stiffness.A)
print(result.stiffness.B)
print(result.stiffness.D)
print(result.stiffness.As)
print(result.diagnostics)
print(result.assumptions)
print(result.validity.warnings)
```

When pitch is omitted from `ValidityContext`, the homogenizer uses the longest
cell repeat vector, or the largest spacing supplied to `stiffener_family_cell`.
It preserves every scale the caller supplies. For a curved surface, use
`ValidityContext.from_surface_point(point, characteristic_height=...,
response_length=...)` to include local curvature.

| Warning kind | What it tells you |
| --- | --- |
| `validity_context_missing` | No scale context could be supplied or inferred. |
| `*_unavailable` | That check did not run because an input is missing. |
| `*_exceeds_threshold` | A computed ratio reached its threshold. |

The [validity limits](../theory/validity.md) explain the remaining affine
deformation assumption. It can overestimate stiffness in patterns that soften
by bending and rearranging within a cell, even when pitch is small.

Selected output, rounded:

| Item | Value |
| --- | --- |
| `A11`, `A22`, `A66` | `1.485e6`, `1.352e6`, `3.990e5` `lbf/in` |
| `B11`, `B22`, `B66` | `2.400e5`, `1.800e5`, `3.609e4` `lbf` |
| `D11`, `D22`, `D66` | `1.125e5`, `8.451e4`, `1.670e4` `lbf*in` |
| `As11`, `As22` | `4.157e5`, `3.782e5` `lbf/in` |
| diagnostics | positive-semidefinite, rank `8` |
| warnings | `p_over_R_exceeds_threshold`, `p_over_L_response_exceeds_threshold`, `membrane_bending_coupling_exceeds_threshold` |

For SI inputs the same blocks have units `N/m`, `N`, `N*m`, and `N/m`,
respectively. Tensyl preserves whichever system you feed it (see
[Units and Consistency](units-and-consistency.md)); it never converts.

## Reading the Blocks

- `A` describes stretching and in-plane shear.
- `B` describes coupling between stretching and bending.
- `D` describes bending and twisting.
- `As` describes transverse shear.

For an energy-based linear model, the stiffness matrix should be symmetric and
should not contain a negative-stiffness mode. A rank-deficient result means the
modeled skin and members do not resist at least one kind of deformation. Tensyl
returns that result with a warning so the unsupported mode can be reviewed.

`stiffness.validity == result.validity` means the warnings stay attached when the
ABD stiffness is passed to a geometry field, serialization workflow, or
downstream adapter.

## Panel Mass

A stiffened panel weighs more than its skin, often a good deal more, so the
homogenized `areal_mass` counts both. Tensyl adds each member's mass per unit
length, spread over the repeat area, to the skin's areal mass:

$$
m_\text{panel} = m_\text{skin} + \frac{1}{A_\text{cell}}
\sum_{\text{members}} n_k\,L_k\,\mu_k ,
$$

where $n_k$ is the member multiplicity, $L_k$ its length inside the cell, and
$\mu_k$ its `BeamSection.mass_per_length`. Thin-wall sections fill in
$\mu_k = \rho A$ whenever their material has a density.

If the skin or any member section has no mass, the result reports
`areal_mass=None` and says so in `result.assumptions`. A skin-only number would
look like an answer while understating the panel, so Tensyl leaves the field
empty instead.

## Diagnostics

Homogenization results include:

- `diagnostics["positive_semidefinite"]` and `diagnostics["minimum_eigenvalue"]`;
- `diagnostics["rank"]`;
- member and cell metadata where available.

Symmetry is not on the list because it is not a finding: every tangent is
projected onto exact symmetry when it is built, and a material asymmetry raises
instead of being reported. A check that cannot fail tells you nothing.

Malformed or unsupported inputs raise typed homogenization exceptions. Finite
rank-deficient assemblies are returned with diagnostics and warnings so the
caller can decide whether the mechanism is acceptable.

The energy assembly is a floating-point sum, so mathematically identical block
entries can differ in their last few bits when stiffnesses are large. Tensyl
checks those residuals against a dimensionless, scale-aware roundoff limit and
projects qualifying `A`, `B`, `D`, and `As` blocks onto exact symmetry. A
material asymmetry or coupling term outside the supported
ABD-plus-transverse-shear form raises `HomogenizationNumericalError`; it is not
silently discarded. Rank and positive-semidefinite diagnostics use the same
scale-aware principle, which keeps them independent of the chosen consistent
unit system.

!!! note "A clean diagnostics report is a floor, not a finish line"
    Symmetry and positive stiffness are basic consistency checks. They do not
    prove local strength, joint behavior, finite-element correlation, a shell
    buckling margin, or manufacturing suitability.

## Strains and Member Loads

Given membrane forces, bending moments, and transverse shear resultants, solve
the full coupled law before reading a rib load:

```python
import numpy as np
from tensyl import member_loads

# N11, N22, N12, M11, M22, M12, Q13, Q23 in the cell frame.
loads = np.array([100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
eta = result.stiffness.strains(loads)
for load in member_loads(cell, eta):
    print(load.label, load.axial_force, load.bending_moment)
```

`strains` solves `C8 @ eta = loads`; the returned vector is read-only. A
singular tangent raises `ValueError` because it does not define a unique
strain. A very poorly conditioned but nonsingular law can still amplify input
roundoff, so inspect the stiffness and validity before interpreting the solve.

`member_loads` returns one `MemberLoads` value per entry in `cell.members`,
with an index as well as the possibly repeated label. The forces are for one
physical rib. Multiplicity, length, and cell area affect the smeared stiffness
but do not scale that rib's force under a prescribed strain.

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

These are beam resultants under the affine, first-approximation strain field.
They do not recover local skin stresses, joint forces, warping stresses, or
intersection concentrations. Omitted `kGAy` or `kGAz` produces zero for the
corresponding force, following the same assumption used by homogenization.

## Comparing ABD Stiffnesses

For a quick inspection, `repr(result.stiffness)` shows the frame, areal mass,
A11 and D11 scales, and warning count. A missing report shows `warnings=None`;
that means validity has not been evaluated.

Use `print(result.summary())` to read all four blocks, warning codes, and
modeling assumptions. `stiffness.summary()` returns the same block display
without the homogenizer's source and assumptions. Both return strings, so they
can also be written to a report or log:

```python
print(result.summary(
    units={"A": "lbf/in", "B": "lbf", "D": "lbf in", "As": "lbf/in"},
    precision=6,
))
```

Unit labels are supplied by the caller and do not convert values. Blocks use
the engineering-shear ordering `11, 22, 12`, with `13, 23` for transverse shear.

Compare ABD stiffnesses block by block:

- compare `A`, `B`, `D`, and `As`;
- compare coupling ratios and warnings;
- rotate stiffnesses into a common frame before comparing anisotropic blocks;
- avoid comparing scalar equivalent moduli unless the reduction assumptions are
  stated.

## Thermal Loading of a Stiffened Cell

Use `cell_thermal_resultants(cell, skin=skin_thermal)` with an explicit
`ThermalResultants` for the skin. Its axes, normal, convention, and reference
surface must match the cell. Every `BeamSection` must provide
`thermal_expansion`, the member's uniform axial expansion per temperature
increment. Isotropic thin-wall helpers copy this from the material's `alpha`.
Unknown values raise an error; use zero explicitly when expansion is absent.

For member strain map $T$, the added thermal load per unit temperature is

$$r_{T,member}=\frac{mL}{A_{cell}}T^T
[EA\alpha,0,0,0,0]^T.$$

This follows by expanding the axial energy
$\tfrac12 EA(\epsilon_{member}-\alpha\Delta T)^2$. The map supplies the angle
projection and the moment from axial eccentricity automatically. The returned
thermal vector is used with the mechanical homogenized stiffness as described
in [Uniform Temperature Changes](materials-and-laminates.md#uniform-temperature-changes).
For member load recovery, subtract `EA * thermal_expansion * delta_temperature`
from each recovered axial force; the existing `member_loads` call reports its
mechanical contribution only.

This beam model assumes uniform axial expansion. It omits intrinsic thermal
curvature of a heterogeneous rib, local relaxation, and thermal gradients.
The laminated wall reduction does not infer a member expansion coefficient;
use an independently justified effective coefficient or a section solver.
Thermal resultants are separate from mechanical ABD exports, including the
Abaqus adapter.
