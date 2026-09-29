# CalculiX Skin Comparison

A skin-only local model was extracted with CalculiX 2.23 and compared with
Tensyl's isotropic plate stiffness. The comparison covers the 6×6 ABD matrix:
three membrane modes and three bending/twisting modes.

## Method and Result

The retained case uses a 6 × 6 in skin, 0.080 in thickness, Young's modulus
10.6×10⁶ psi, and Poisson's ratio 0.33, with the reference at the skin midplane.
The comparison retains these original case units.

The extraction imposes the six generalized strain cases and reconstructs the
membrane forces and moments in Tensyl's ordering. The retained comparison is:

| Quantity | Stored normalized matrix error |
| --- | ---: |
| Complete ABD6 | 3.78794×10⁻⁸ |
| A | 3.78794×10⁻⁸ |
| B | 2.68856×10⁻¹⁰ |
| D | 1.03490×10⁻⁷ |

The extracted ABD6 is symmetric. The stored metric is
`norm(actual - target) / max(norm(target), 1)`, evaluated in the original
inch–pound units. Since the target `B` block is zero, its entry is an absolute
Frobenius norm in lbf. The entrywise table provides individual absolute
differences as well.

## Reproduce and Inspect

The [committed case artifacts](https://github.com/srogachev95/Tensyl/tree/main/validation/artifacts/committed/local_abd/skin_only) include the target and
extracted matrices, comparison metrics, an entrywise CSV/JSON table, and the
extraction manifest. The
[case definition](https://github.com/srogachev95/Tensyl/blob/main/validation/cases/local_abd/skin_only.yml)
and [solver driver](https://github.com/srogachev95/Tensyl/blob/main/validation/scripts/run_local_abd_solver.py)
define the model and extraction procedure.

The retained run is dated 2026-06-28 and records Tensyl 0.1.0, source revision
`0e45047`, Python 3.12.13, and CalculiX 2.23 on macOS ARM64. It is historical
solver evidence; the current documentation overhaul preserves those artifacts.
Raw solver outputs are referenced under the scratch path in the manifest.

This case's compared scope is membrane/bending ABD6. Transverse shear and mesh
convergence are tracked in the [campaign overview](index.md#evidence-still-planned).
