# US Customary Skin-Only Wall

This example builds an isotropic aluminum-like skin in a consistent US
customary unit system.

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
wall = isotropic_plate(aluminum, thickness=0.080)

assert wall.A.shape == (3, 3)
assert wall.B.shape == (3, 3)
assert wall.D.shape == (3, 3)
assert wall.As.shape == (2, 2)
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
