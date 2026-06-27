"""Tensyl public package."""

from importlib.metadata import PackageNotFoundError, version

from tensyl.cells import (
    BeamMember,
    CanonicalUnitCell,
    StiffenerFamily,
    equilateral_isogrid_cell,
    orthogrid_cell,
    unidirectional_cell,
)
from tensyl.constitutive import ConstitutiveLaw, LinearABDWall
from tensyl.conventions import DEFAULT_FRAME, DEFAULT_STRAIN_CONVENTION, Frame2D, StrainConvention
from tensyl.homogenizers import (
    DirectECHomogenizer,
    EnergyHomogenizer,
    HomogenizationResult,
    Homogenizer,
    ValidityContext,
    ValidityReport,
    ValidityThresholds,
)
from tensyl.laminates import Ply, isotropic_plate, laminate_plate
from tensyl.materials import IsotropicMaterial, OrthotropicPlyMaterial
from tensyl.sections import BeamSection

try:
    __version__ = version("tensyl")
except PackageNotFoundError:  # pragma: no cover - editable tree before install
    __version__ = "0.0.0"

__all__ = [
    "DEFAULT_FRAME",
    "DEFAULT_STRAIN_CONVENTION",
    "BeamMember",
    "BeamSection",
    "CanonicalUnitCell",
    "ConstitutiveLaw",
    "DirectECHomogenizer",
    "EnergyHomogenizer",
    "Frame2D",
    "HomogenizationResult",
    "Homogenizer",
    "IsotropicMaterial",
    "LinearABDWall",
    "OrthotropicPlyMaterial",
    "Ply",
    "StiffenerFamily",
    "StrainConvention",
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
    "__version__",
    "equilateral_isogrid_cell",
    "isotropic_plate",
    "laminate_plate",
    "orthogrid_cell",
    "unidirectional_cell",
]
