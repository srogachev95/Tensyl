# First ABD Stiffness

The simplest Tensyl workflow is a skin-only isotropic plate — no stiffeners, no
surprises. It is the baseline you sanity-check everything else against before
stiffener homogenization gets interesting.

```python
from tensyl import IsotropicMaterial, isotropic_plate

aluminum_2024_like = IsotropicMaterial(
    E=10.6e6,      # psi
    nu=0.33,
    density=0.1,  # analyst-selected consistent mass unit
)

stiffness = isotropic_plate(aluminum_2024_like, thickness=0.080)

print(stiffness.A)   # membrane stiffness, lbf/in
print(stiffness.B)   # zero for a symmetric mid-surface isotropic skin
print(stiffness.D)   # bending stiffness, lbf*in
print(stiffness.As)  # transverse shear stiffness, lbf/in
```

For an isotropic plate of thickness $h$, Tensyl uses the plane-stress reduced
stiffness:

$$
\mathbf Q =
\frac{E}{1-\nu^2}
\begin{bmatrix}
1 & \nu & 0 \\
\nu & 1 & 0 \\
0 & 0 & (1-\nu)/2
\end{bmatrix}.
$$

The mid-surface plate blocks are:

$$
\mathbf A=\mathbf Qh,\qquad
\mathbf B=\mathbf 0,\qquad
\mathbf D=\frac{\mathbf Qh^3}{12}.
$$

`ABDStiffness` is an operator, not only a matrix container. Its public
mechanics contract is stored energy:

```python
from tensyl import generalized_strain

eta = generalized_strain([1.0e-4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

energy_density = stiffness.energy(eta)
resultants = stiffness.resultants(eta)
tangent = stiffness.tangent(eta)
```

`tangent` is constant for `ABDStiffness`, so `stiffness.constant_tangent` gives the
same $8\times8$ operator without a strain input.
