# SP-8007 Reconciliation

This page compares Tensyl's tangent-plane stiffnesses with the elastic-constant
formulas in NASA SP-8007 Section 4.1.2.6. It is not a calibration exercise.
SP-8007 is a published design reference, but it is not an oracle for Tensyl, and
Tensyl is not an oracle for SP-8007. The useful question is narrower and harder:
when the numbers diverge, which physics did each model keep or throw away?

The comparison uses synthetic public cases so the evidence can live in the
repository. Private sizing cases should be checked with the same machinery, but
they do not belong in public artifacts.

## What Was Compared

The audit computes two sets of coefficients for each case.

First, it evaluates the SP-8007 equations as written:

- ring-and-stringer orthogrids use Eqs. 82-91;
- equilateral isogrids use Eqs. 92-98.

Second, it computes a Tensyl ABD stiffness and extracts the same SP-8007-style
barred coefficients from that matrix. For a cylinder, Tensyl's local `e1`
direction is axial and `e2` is circumferential, so the mapping is:

| SP-8007 coefficient | Tensyl source |
| --- | --- |
| `Ebar_x` | `A[0, 0]` |
| `Ebar_y` | `A[1, 1]` |
| `Ebar_xy` | `A[0, 1]` |
| `Gbar_xy` | `A[2, 2]` |
| `Dbar_x` | `D[0, 0]` |
| `Dbar_y` | `D[1, 1]` |
| `Dbar_xy` | `2*D[0, 1] + 4*D[2, 2]` |
| `Cbar_x` | `B[0, 0]` |
| `Cbar_y` | `B[1, 1]` |
| `Cbar_xy` | `B[0, 1]` |
| `Kbar_xy` | `B[2, 2]` |

The last bending row is the easy place to make a bad comparison. SP-8007's
`Dbar_xy` is a modified twisting stiffness, not Tensyl's `D66` entry by itself.
With Tensyl's engineering twist convention, the coefficient is

$$
\bar{D}_{xy} = 2D_{12} + 4D_{66}.
$$

## Result

The coefficient-level picture is shown below. Values near the bottom of the log
axis are roundoff-level agreement. Large bars are not automatically errors; they
mark terms where the two models are not retaining the same stiffness.

![SP-8007 coefficient deltas](../assets/validation/sp8007-term-errors.svg)

For the orthogrid cases, the membrane terms, coupling terms, and modified
twisting term agree with SP-8007 to roundoff when the inputs are normalized the
same way. The bending terms do not, unless in-plane beam bending is suppressed.
That is an important distinction. Tensyl's member strain map gives a rib or
stringer a finite in-plane bending stiffness contribution when the equivalent
wall bends across that member. The SP-8007 ring/stringer formulas in Eqs. 89-91
do not include the corresponding cross-family `EIz` contribution.

![SP-8007 bending ratios](../assets/validation/sp8007-bending-ratio.svg)

The sweep below makes that mechanism explicit. As the member in-plane inertia is
reduced relative to its out-of-plane inertia, the orthogrid bending mismatch
collapses. The zero-eccentric isogrid case behaves the same way.

![SP-8007 in-plane bending sweep](../assets/validation/sp8007-inplane-bending-sweep.svg)

The eccentric isogrid case still diverges after in-plane bending is nearly
removed. In the SP-8007 isogrid equations, the coupling coefficients
`\bar{C}_x`, `\bar{C}_y`, `\bar{C}_{xy}`, and `\bar{K}_{xy}` include stiffener
eccentricity, but the bending coefficients in Eqs. 97-98 do not show explicit
`EA z^2` terms. Tensyl does include those terms because an axial member away
from the reference surface stores bending energy when the wall curvature
stretches or shortens that member.

That does not by itself prove SP-8007 is wrong. There are several possible
readings:

- the isogrid formulas may expect `I_s` to be supplied about the wall reference
  surface rather than the stiffener centroid;
- the formulas may be a simplified design expression that intentionally omits
  some eccentric bending energy;
- the notation may be carrying an assumption that is not obvious from the
  equation block alone;
- Tensyl may be retaining a legitimate first-approximation term that the
  SP-8007 hand formula does not model.

The report machinery is meant to keep those possibilities visible.

## Guidance

Use the SP-8007-style coefficients when a downstream classical
orthotropic-cylinder calculation expects exactly that data shape. In that
workflow, export the coefficients with the mapping above, keep the assumptions
with the artifact, and do not pass `D66` as `Dbar_xy`.

Keep the full Tensyl ABD stiffness when the wall has meaningful off-axis terms,
strong membrane-bending coupling, or section properties that do not match the
simplified SP-8007 assumptions. Reducing a richer wall law to a short list of
barred constants can be the right handoff, but it is a reduction. It should be
treated as one.

Be especially careful with these inputs:

- `J`: open-section St. Venant torsion, closed-cell torsion, and restrained
  warping can differ by large factors;
- `EIz`: Tensyl retains in-plane member bending, while the SP-8007 orthogrid and
  isogrid expressions used here do not expose the same term;
- eccentricity: Tensyl treats the beam section as centroidal and adds the
  reference-surface offset through energy, while some hand formulas may embed a
  parallel-axis choice in the inertia symbol.

## Artifacts

The committed evidence lives under
`validation/artifacts/committed/sp8007_reconciliation/`:

- `comparison_table.json` and `comparison_table.csv` contain the coefficient
  rows;
- `summary.json` records the worst term by case and the interpretation notes;
- `inplane_bending_sweep.json` records the parameter sweep;
- `manifest.json` records provenance for the run.

Regenerate the report data with:

```bash
uv run python validation/scripts/build_sp8007_reconciliation.py
```

The public mechanics references for this page are NASA SP-8007 and Nemeth's
equivalent-plate treatise, both listed in [References](../references.md).
