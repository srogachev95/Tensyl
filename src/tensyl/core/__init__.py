"""Core frames, typing, constitutive stiffnesses, and rotations."""

from tensyl.core.constitutive import (
    ABDStiffness,
    ABDStiffnessCoefficients,
    HyperelasticModel,
    OrthotropicStiffnessCoefficients,
    ReducedOrthotropicProperties,
    StiffnessSymmetryError,
    shift_reference_surface,
    superpose_abd_stiffnesses,
)
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.rotations import (
    engineering_strain_transform,
    generalized_resultant_transform,
    generalized_strain_transform,
    resultant_transform,
    rotate_abd_stiffness,
    rotate_tangent,
    transverse_shear_transform,
)
from tensyl.core.typing import (
    FloatArray,
    GeneralizedResultant,
    GeneralizedStrain,
    generalized_resultant,
    generalized_strain,
)
from tensyl.core.validity import (
    ValidityContext,
    ValidityReport,
    ValidityThresholds,
)
from tensyl.core.validity_checks import validity_report_for_stiffness

__all__ = [
    "DEFAULT_FRAME",
    "DEFAULT_STRAIN_CONVENTION",
    "FloatArray",
    "Frame2D",
    "GeneralizedResultant",
    "GeneralizedStrain",
    "HyperelasticModel",
    "ABDStiffness",
    "ABDStiffnessCoefficients",
    "OrthotropicStiffnessCoefficients",
    "ReducedOrthotropicProperties",
    "StrainConvention",
    "StiffnessSymmetryError",
    "engineering_strain_transform",
    "generalized_resultant",
    "generalized_resultant_transform",
    "generalized_strain",
    "generalized_strain_transform",
    "resultant_transform",
    "rotate_abd_stiffness",
    "rotate_tangent",
    "shift_reference_surface",
    "superpose_abd_stiffnesses",
    "transverse_shear_transform",
    "validity_report_for_stiffness",
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
]
