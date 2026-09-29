# Materials and Laminates

Start with the skin construction. An isotropic skin needs a modulus, Poisson's
ratio, and thickness. A laminate needs the material, thickness, and angle of each
ply. Both produce the same `ABDStiffness` interface for the next modeling step.

## Isotropic Plate

```python
--8<-- "docs/examples/scripts/walkthrough.py:skin"
```

These SI inputs give the [walkthrough's 2 mm skin](../getting-started/first-abd-stiffness.md).
Density is mass per volume, here kg/m³. Supply it to obtain areal mass in kg/m².

## Orthotropic Laminate

A ply's direction 1 follows its fibers; direction 2 is transverse in the ply.
Define the elastic and shear moduli in Pa, density in kg/m³, and thermal
expansion coefficients in 1/K. The values below illustrate a carbon/epoxy ply:

```python
--8<-- "docs/examples/scripts/materials_sections.py:laminate"
```

Plies are ordered **bottom to top along `+n`**, with the reference at the laminate
midplane. The symmetric stack has a near-zero `B` block. The `[0/90]` stack is
unsymmetric and couples extension to curvature; reversing that stack reverses
`B` while preserving `A` and `D`.

Classical laminate theory integrates each transformed ply stiffness
$\bar{\mathbf Q}_k$ between its lower and upper coordinates:

$$
\mathbf A=\sum_k\bar{\mathbf Q}_k(z_k-z_{k-1}),\quad
\mathbf B=\frac12\sum_k\bar{\mathbf Q}_k(z_k^2-z_{k-1}^2),\quad
\mathbf D=\frac13\sum_k\bar{\mathbf Q}_k(z_k^3-z_{k-1}^3).
$$

See [NASA RP-1351](https://ntrs.nasa.gov/citations/19950009349) for the laminate
constitutive and thermal derivations. Each ply angle rotates material axes into
the laminate axes before integration.

## Angles and Stacking Strings

`Ply.from_degrees` accepts angles from a drawing directly. `Ply(..., angle_rad=...)`
uses radians. For equal-thickness plies of one material, `layup` expands common
stacking notation:

| String | Angles from bottom to top, degrees |
| --- | --- |
| `[0/±45/90]s` | 0, +45, −45, 90, 90, −45, +45, 0 |
| `[0/90]2s` | 0, 90, 0, 90, 90, 0, 90, 0 |
| `[0_2/90]` | 0, 0, 90 |
| `[±45_2]` | +45, −45, +45, −45 |

`+-` also spells `±`; `∓` expands the negative angle first. Repeats use positive
integers. The symmetric suffix mirrors the whole expanded stack, including its
middle ply. Use explicit `Ply` objects for mixed materials or thicknesses.

## Shear Correction

`isotropic_plate` and `laminate_plate` use a default transverse-shear correction
of 5/6. Set `shear_correction` explicitly to match the plate or shell theory in
your analysis. It scales the `As` block, while `A`, `B`, and `D` follow the
through-thickness integration above.

## Uniform Temperature Changes

Supply isotropic `alpha`, or orthotropic `alpha1` and `alpha2`, to calculate
expansion under a uniform temperature change. Zero specifies zero expansion;
`None` leaves the property unknown. Thermal resultants are a separate object
so the same elastic stiffness can be used for several temperature changes.

```python
--8<-- "docs/examples/scripts/materials_sections.py:thermal"
```

The free aluminum skin expands by $23\times10^{-6}\times50=0.00115$ in each
in-plane direction, with zero curvature. The section law is

$$\mathbf r=\mathbf C_8\boldsymbol\eta-\mathbf r_T\Delta T,\qquad
\mathbf r_T=[\mathbf N_T,\mathbf M_T,0,0]^T,$$

where $\mathbf N_T$ and $\mathbf M_T$ are force and moment resultants per kelvin.
Laminate theory gives

$$\mathbf N_T=\sum_k\bar{\mathbf Q}_k\bar{\boldsymbol\alpha}_k(z_k-z_{k-1}),\quad
\mathbf M_T=\frac12\sum_k\bar{\mathbf Q}_k\bar{\boldsymbol\alpha}_k(z_k^2-z_{k-1}^2).$$

The transformed expansion vector uses engineering shear. For applied mechanical
loads, solve `stiffness.strains(loads + thermal.equivalent_load(delta_temperature))`.
Full restraint sets strain to zero and therefore gives negative thermal resultants.
Properties are linear elastic and temperature independent over the chosen increment.

Keep mechanical and thermal objects in the same axes and at the same reference
surface. `thermal.rotate(angle)` follows the stiffness rotation;
`thermal.shift_reference_surface(d)` changes `M_T` to `M_T - d*N_T`.
The [stiffened-cell example](homogenization.md#thermal-loading-of-a-stiffened-cell)
adds rib expansion using the same sign convention.

[Complete material and section script](../examples/scripts/materials_sections.py).
