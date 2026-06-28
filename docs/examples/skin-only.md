# Skin-Only ABD Stiffness

This first example builds the smallest useful ABD stiffness: an isotropic skin
about its own mid-surface.

All examples in this section use one consistent US customary unit set unless
noted otherwise: length in `in`, force in `lbf`, and stress in `psi`. Tensyl
does not convert units; it only carries unit labels when you export data. The
unit policy lives in [Units and Consistency](../user-guide/units-and-consistency.md).

## Problem

Build a skin-only ABD stiffness for a flat reference surface. Because the
reference surface is the skin mid-surface, the membrane-bending coupling block
`B` should be zero.

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
stiffness = isotropic_plate(aluminum, thickness=0.080)

assert stiffness.A.shape == (3, 3)
assert stiffness.B.shape == (3, 3)
assert stiffness.D.shape == (3, 3)
assert stiffness.As.shape == (2, 2)
assert abs(stiffness.B).max() == 0.0
```

## Interpretation

This verifies the ABD block shapes and the expected zero coupling for a
symmetric isotropic skin. It does not include stiffeners, shell curvature, local
failure, or buckling. One thing at a time; the matrix has enough opinions
already.
