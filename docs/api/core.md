# Core API

::: tensyl.core.constitutive
    options:
      show_source: false
      members:
        - ABDStiffnessCoefficients
        - HyperelasticModel
        - ABDStiffness
        - StiffnessSymmetryError
        - OrthotropicStiffnessCoefficients
        - ReducedOrthotropicProperties
        - shift_reference_surface
        - superpose_abd_stiffnesses

::: tensyl.core.conventions
    options:
      show_source: false
      members:
        - Frame2D
        - StrainConvention
        - DEFAULT_FRAME
        - DEFAULT_STRAIN_CONVENTION

::: tensyl.core.typing
    options:
      show_source: false
      members:
        - GeneralizedStrain
        - GeneralizedResultant
        - generalized_strain
        - generalized_resultant

::: tensyl.core.ThermalResultants

## Operator Storage and Protocol

`ABDStiffness` stores the symmetric 8×8 `tangent_c8` operator. Its `A`, `B`, `D`,
and `As` properties are read-only views in engineering component order.
`HyperelasticModel` describes the energy, resultant, and tangent interface:

$$\mathbf r=\partial W/\partial\boldsymbol\eta,\qquad
\mathbf C=\partial^2W/\partial\boldsymbol\eta^2.$$

For the linear plate stiffness, $W=\tfrac12\boldsymbol\eta^T\mathbf C_8\boldsymbol\eta$.
Here the protocol name describes a stored-energy operator in generalized strain
space. Its methods are used by the small-strain plate model documented in
[Equivalent-Stiffness Mechanics](../theory/equivalent-stiffness.md).
