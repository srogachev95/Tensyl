# US Customary Skin-Only Stiffness

This example builds an isotropic aluminum-like skin in a consistent US
customary unit system.

## Problem

Build a skin-only ABD stiffness for a flat reference surface. The reference surface
is the skin mid-surface, so `B` should be zero.

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

Assumed units:

| Quantity | Unit |
| --- | --- |
| Length | `in` |
| Force | `lbf` |
| Stress | `psi` |
| Membrane stiffness | `lbf/in` |
| Bending stiffness | `lbf*in` |

The `density` value is passed through to areal mass calculations where
applicable. Choose a mass convention consistent with the rest of the workflow.

## Interpretation

This example verifies the basic ABD block shapes and the expected zero coupling
for a symmetric isotropic skin. It does not include stiffeners, shell curvature,
local failure, or buckling.
