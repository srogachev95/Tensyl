"""Tensyl public package."""

from importlib.metadata import PackageNotFoundError, version

from tensyl.cells import (
    BeamMember,
    CanonicalUnitCell,
    CellEdge,
    CellNode,
    StiffenerFamily,
    braced_orthogrid_cell,
    equilateral_isogrid_cell,
    equilateral_star_cell,
    graph_unit_cell,
    hexagonal_grid_cell,
    isosceles_triangle_grid_cell,
    kagome_cell,
    orthogrid_cell,
    regular_hexagonal_grid_cell,
    sandwich_hexagonal_core_cell,
    sandwich_orthogrid_core_cell,
    sandwich_star_core_cell,
    star_cell,
    unidirectional_cell,
)
from tensyl.core.constitutive import (
    ConstitutiveLaw,
    HyperelasticLaw,
    LinearABDWall,
    LinearLaw,
    shift_reference_surface,
    superpose_linear_abd_walls,
)
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.core.typing import (
    GeneralizedResultant,
    GeneralizedStrain,
    generalized_resultant,
    generalized_strain,
)
from tensyl.fields import ConstantWallField, HomogenizedWallField, WallAtlas, WallCache, WallField
from tensyl.geometry import Cylinder, Ellipsoid, FlatPlate, SphericalCap, Surface, SurfacePoint
from tensyl.homogenizers import (
    DirectECHomogenizer,
    EnergyHomogenizer,
    HomogenizationFailure,
    HomogenizationInputError,
    HomogenizationResult,
    Homogenizer,
    ValidityContext,
    ValidityReport,
    ValidityThresholds,
    validity_report_for_law,
)
from tensyl.materials import (
    IsotropicMaterial,
    OrthotropicPlyMaterial,
    Ply,
    isotropic_plate,
    laminate_plate,
)
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
    "CellEdge",
    "CellNode",
    "ConstitutiveLaw",
    "ConstantWallField",
    "Cylinder",
    "DirectECHomogenizer",
    "EnergyHomogenizer",
    "Ellipsoid",
    "FlatPlate",
    "Frame2D",
    "GeneralizedResultant",
    "GeneralizedStrain",
    "HomogenizationFailure",
    "HomogenizationInputError",
    "HomogenizationResult",
    "Homogenizer",
    "HyperelasticLaw",
    "IsotropicMaterial",
    "LinearABDWall",
    "LinearLaw",
    "OrthotropicPlyMaterial",
    "Ply",
    "HomogenizedWallField",
    "SphericalCap",
    "StiffenerFamily",
    "StrainConvention",
    "Surface",
    "SurfacePoint",
    "ValidityContext",
    "ValidityReport",
    "ValidityThresholds",
    "WallAtlas",
    "WallCache",
    "WallField",
    "__version__",
    "braced_orthogrid_cell",
    "equilateral_isogrid_cell",
    "equilateral_star_cell",
    "generalized_resultant",
    "generalized_strain",
    "graph_unit_cell",
    "hexagonal_grid_cell",
    "isotropic_plate",
    "isosceles_triangle_grid_cell",
    "kagome_cell",
    "laminate_plate",
    "orthogrid_cell",
    "regular_hexagonal_grid_cell",
    "sandwich_hexagonal_core_cell",
    "sandwich_orthogrid_core_cell",
    "sandwich_star_core_cell",
    "shift_reference_surface",
    "star_cell",
    "superpose_linear_abd_walls",
    "unidirectional_cell",
    "validity_report_for_law",
]
