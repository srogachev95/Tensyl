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
from tensyl.constitutive import (
    ConstitutiveLaw,
    LinearABDWall,
    shift_reference_surface,
    superpose_linear_abd_walls,
)
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
    "CellEdge",
    "CellNode",
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
    "braced_orthogrid_cell",
    "equilateral_isogrid_cell",
    "equilateral_star_cell",
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
]
