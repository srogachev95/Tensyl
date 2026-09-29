# Equivalent-Stiffness Mechanics

A plate stiffness connects loads per unit width to stretching, bending, and
shearing at a reference surface. Homogenization supplies that relation for a
ribbed panel by matching the energy of its skin and ribs over one repeat area.

## Linear ABD Stiffness

Group the deformation into membrane strain $\boldsymbol\epsilon^0$, curvature
$\boldsymbol\kappa$, and transverse shear $\boldsymbol\gamma_s$:

$$
\begin{bmatrix}\mathbf N\\\mathbf M\\\mathbf Q\end{bmatrix}=
\begin{bmatrix}\mathbf A&\mathbf B&\mathbf0\\
\mathbf B&\mathbf D&\mathbf0\\\mathbf0&\mathbf0&\mathbf A_s\end{bmatrix}
\begin{bmatrix}\boldsymbol\epsilon^0\\\boldsymbol\kappa\\\boldsymbol\gamma_s\end{bmatrix}.
$$

`A` controls stretching, `D` controls bending, and `As` controls transverse shear.
`B` couples stretching and bending: an axial load on an eccentric panel can
produce curvature, as in the [walkthrough](../getting-started/use-the-result.md).
These blocks follow classical laminate theory with a transverse-shear block;
see [Reddy and NASA RP-1351](../references.md#plates-shells-and-laminates).

| Vector | Component order | SI units |
| --- | --- | --- |
| Membrane strain $\boldsymbol\epsilon^0$ | $\epsilon_{11}^0,\epsilon_{22}^0,\gamma_{12}^0$ | dimensionless |
| Curvature $\boldsymbol\kappa$ | $\kappa_{11},\kappa_{22},\kappa_{12}$ | 1/m |
| Transverse shear $\boldsymbol\gamma_s$ | $\gamma_{13}^0,\gamma_{23}^0$ | dimensionless |
| Membrane resultant $\mathbf N$ | $N_{11},N_{22},N_{12}$ | N/m |
| Moment resultant $\mathbf M$ | $M_{11},M_{22},M_{12}$ | N m/m = N |
| Transverse resultant $\mathbf Q$ | $Q_{13},Q_{23}$ | N/m |

The complete strain vector `eta` stacks those three strain groups into eight
components. The load vector uses the same group order. Positive normal membrane
strain extends the reference surface. Positive curvature increases the matching
in-plane strain with distance along `+n`:
$\boldsymbol\epsilon(z)=\boldsymbol\epsilon^0+z\boldsymbol\kappa$.
The shear and twist components use the
[engineering convention](conventions.md#engineering-shear).

## Stored Energy Contract

The energy per panel area is

$$W=\tfrac12\boldsymbol\eta^T\mathbf C_8\boldsymbol\eta,$$

where $\mathbf C_8$ is the block matrix above. In SI, $W$ has units J/m².
Differentiating this energy gives the resultants:
$\mathbf r=\partial W/\partial\boldsymbol\eta=\mathbf C_8\boldsymbol\eta$.

The public methods follow those operations directly:

| Operation | Python method |
| --- | --- |
| Loads from a given deformation | `stiffness.resultants(eta)` |
| Deformation from applied loads | `stiffness.strains(loads)` |
| Energy per area | `stiffness.energy(eta)` |
| Read the four blocks | `stiffness.A`, `.B`, `.D`, `.As` |

The [operator reference](../api/core.md#operator-storage-and-protocol) describes
matrix storage and the energy protocol used by library extensions.

<span id="what-the-abd-stiffness-does-not-prove"></span>
Use this constitutive relation in a plate or shell analysis with the structure's
geometry, loads, and boundary conditions. The [modeling guide](validity.md)
explains the cell deformation and length scales represented by the stiffness.

Next: [How the rib energy is assembled](tangent-plane-homogenization.md).
