# Validation Overview

Tensyl checks the stiffness calculation against plate formulas, independent
implementations of published grid equations, and a retained CalculiX skin
comparison. Each comparison identifies its inputs, reference calculation, and
measured differences.

## Evidence Available Now

| Comparison | What was compared | Result and evidence |
| --- | --- | --- |
| Plate and laminate formulas | Isotropic stiffness, laminate integration, transformations, and energy | [Library tests](https://github.com/srogachev95/Tensyl/tree/main/tests) and the executable handbook examples |
| Nemeth cell tables | Eight named grid cases, all four stiffness blocks, independently transcribed member data | [Formula comparison](nemeth-cells.md): agreement to floating-point roundoff |
| SP-8007 elastic constants | Orthogrid and centered/eccentric isogrid barred coefficients | [Reconciliation](sp8007-reconciliation.md): agreement to roundoff with the eccentric isogrid correction |
| CalculiX 2.23 | Skin-only membrane/bending ABD6 extraction | [Solver comparison](calculix-skin.md): relative matrix error 3.79×10⁻⁸ |

The source-equation checks exercise member counts, angles, offsets, section
terms, and coefficient ordering. The CalculiX case compares extracted solver
resultants with the isotropic skin's membrane and bending stiffness.

## How to Read the Evidence

Start with the case definition and the compared quantities. A formula check
shows whether the code reproduces those equations. A solver extraction shows
agreement for the retained mesh, boundary conditions, and imposed modes.
The [artifact directory](https://github.com/srogachev95/Tensyl/tree/main/validation/artifacts/committed) contains the numerical records.

For the skin-only case, `comparison_metrics.json` contains the solver residuals;
`metrics.json` describes the Tensyl target's own matrix checks. The extraction
manifest records the software versions, input hash, command, and raw-output paths.

## Evidence Still Planned

The retained solver comparison covers the skin's six membrane/bending modes.
Further campaign work includes transverse shear, mesh-convergence studies,
stiffened cells, and panel/barrel response. Existing flat-panel and barrel
artifacts are target calculations for those future comparisons. The
[validation campaign](https://github.com/srogachev95/Tensyl/tree/main/validation)
keeps case definitions and artifact provenance together.
