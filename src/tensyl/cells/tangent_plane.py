"""Canonical tangent-plane stiffener-cell value objects and constructors."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal

import numpy as np

from tensyl.core.constitutive import (
    LinearABDWall,
    shift_reference_surface,
    superpose_linear_abd_walls,
)
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.sections.beam import BeamSection


def _positive(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be finite and positive."
        raise ValueError(msg)
    return checked


def _finite(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{name} must be finite."
        raise ValueError(msg)
    return checked


@dataclass(frozen=True, slots=True)
class BeamMember:
    """A canonical stiffener member in a local tangent-plane unit cell."""

    section: BeamSection
    length: float
    angle_rad: float
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "length", _positive(self.length, name="length"))
        object.__setattr__(self, "angle_rad", _finite(self.angle_rad, name="angle_rad"))
        object.__setattr__(self, "eccentricity", _finite(self.eccentricity, name="eccentricity"))
        object.__setattr__(self, "multiplicity", _positive(self.multiplicity, name="multiplicity"))


@dataclass(frozen=True, slots=True)
class CellNode:
    """A node in a local tangent-plane graph cell."""

    x: float
    y: float
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _finite(self.x, name="x"))
        object.__setattr__(self, "y", _finite(self.y, name="y"))


@dataclass(frozen=True, slots=True)
class CellEdge:
    """A beam edge in a local tangent-plane graph cell."""

    start: int
    end: int
    section: BeamSection
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "eccentricity", _finite(self.eccentricity, name="eccentricity"))
        object.__setattr__(self, "multiplicity", _positive(self.multiplicity, name="multiplicity"))


@dataclass(frozen=True, slots=True)
class CanonicalUnitCell:
    """Canonical tangent-plane cell consumed by tangent-plane homogenizers."""

    area: float
    skin: LinearABDWall
    members: tuple[BeamMember, ...]
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION
    metadata: dict[str, Any] | MappingProxyType[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "area", _positive(self.area, name="area"))
        members = tuple(self.members)
        if not members:
            msg = "CanonicalUnitCell requires at least one beam member."
            raise ValueError(msg)
        if self.skin.frame != self.frame:
            msg = "cell frame must match the skin frame."
            raise ValueError(msg)
        if self.skin.convention != self.convention:
            msg = "cell convention must match the skin convention."
            raise ValueError(msg)
        object.__setattr__(self, "members", members)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class StiffenerFamily:
    """Continuous straight stiffener-family input for direct EC homogenization."""

    section: BeamSection
    spacing: float
    angle_rad: float
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "spacing", _positive(self.spacing, name="spacing"))
        object.__setattr__(self, "angle_rad", _finite(self.angle_rad, name="angle_rad"))
        object.__setattr__(self, "eccentricity", _finite(self.eccentricity, name="eccentricity"))
        object.__setattr__(self, "multiplicity", _positive(self.multiplicity, name="multiplicity"))


def _cell_frame_and_convention(
    skin: LinearABDWall,
    frame: Frame2D | None,
    convention: StrainConvention | None,
) -> tuple[Frame2D, StrainConvention]:
    cell_frame = skin.frame if frame is None else frame
    cell_convention = skin.convention if convention is None else convention
    return cell_frame, cell_convention


def _same_or_second(first: BeamSection, second: BeamSection | None) -> BeamSection:
    return first if second is None else second


def graph_unit_cell(
    *,
    area: float,
    skin: LinearABDWall,
    nodes: tuple[CellNode, ...],
    edges: tuple[CellEdge, ...],
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    metadata: dict[str, Any] | MappingProxyType[str, Any] | None = None,
) -> CanonicalUnitCell:
    """Convert a local graph cell into the canonical member representation."""

    node_tuple = tuple(nodes)
    if len(node_tuple) < 2:
        msg = "graph_unit_cell requires at least two nodes."
        raise ValueError(msg)
    members: list[BeamMember] = []
    for edge in tuple(edges):
        if edge.start < 0 or edge.start >= len(node_tuple):
            msg = f"edge start index {edge.start} is out of range."
            raise ValueError(msg)
        if edge.end < 0 or edge.end >= len(node_tuple):
            msg = f"edge end index {edge.end} is out of range."
            raise ValueError(msg)
        if edge.start == edge.end:
            msg = "edge start and end nodes must be distinct."
            raise ValueError(msg)
        start = node_tuple[edge.start]
        end = node_tuple[edge.end]
        dx = end.x - start.x
        dy = end.y - start.y
        length = float(np.hypot(dx, dy))
        members.append(
            BeamMember(
                section=edge.section,
                length=length,
                angle_rad=float(np.arctan2(dy, dx)),
                eccentricity=edge.eccentricity,
                multiplicity=edge.multiplicity,
                label=edge.label,
            )
        )
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    cell_metadata = {"source": "graph_unit_cell"}
    if metadata is not None:
        cell_metadata.update(metadata)
    return CanonicalUnitCell(
        area=area,
        skin=skin,
        members=tuple(members),
        frame=cell_frame,
        convention=cell_convention,
        metadata=cell_metadata,
    )


def unidirectional_cell(
    *,
    skin: LinearABDWall,
    member_section: BeamSection,
    spacing: float,
    eccentricity: float,
    angle_rad: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    label: str = "unidirectional",
) -> CanonicalUnitCell:
    """Create a one-family canonical strip cell."""

    d = _positive(spacing, name="spacing")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    member = BeamMember(
        section=member_section,
        length=1.0,
        angle_rad=angle_rad,
        eccentricity=eccentricity,
        label="stiffener",
    )
    return CanonicalUnitCell(
        area=d,
        skin=skin,
        members=(member,),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": label, "spacing": d},
    )


def orthogrid_cell(
    *,
    skin: LinearABDWall,
    stringer_section: BeamSection,
    rib_section: BeamSection,
    stringer_spacing: float,
    rib_spacing: float,
    stringer_eccentricity: float,
    rib_eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid cell with one stringer and one rib family."""

    ds = _positive(stringer_spacing, name="stringer_spacing")
    dr = _positive(rib_spacing, name="rib_spacing")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=ds * dr,
        skin=skin,
        members=(
            BeamMember(
                section=stringer_section,
                length=dr,
                angle_rad=0.0,
                eccentricity=stringer_eccentricity,
                label="stringer",
            ),
            BeamMember(
                section=rib_section,
                length=ds,
                angle_rad=np.pi / 2.0,
                eccentricity=rib_eccentricity,
                label="rib",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={
            "source": "orthogrid",
            "stringer_spacing": ds,
            "rib_spacing": dr,
        },
    )


def equilateral_isogrid_cell(
    *,
    skin: LinearABDWall,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an equilateral isogrid cell with three identical member families."""

    p = _positive(pitch, name="pitch")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    height = np.sqrt(3.0) * p / 2.0
    return CanonicalUnitCell(
        area=p * height,
        skin=skin,
        members=(
            BeamMember(
                member_section,
                length=p,
                angle_rad=0.0,
                eccentricity=eccentricity,
                label="0",
            ),
            BeamMember(
                member_section,
                length=p,
                angle_rad=np.pi / 3.0,
                eccentricity=eccentricity,
                label="+60",
            ),
            BeamMember(
                member_section,
                length=p,
                angle_rad=-np.pi / 3.0,
                eccentricity=eccentricity,
                label="-60",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": "equilateral_isogrid", "pitch": p},
    )


def braced_orthogrid_cell(
    *,
    skin: LinearABDWall,
    stringer_section: BeamSection,
    rib_section: BeamSection,
    brace_section: BeamSection,
    stringer_spacing: float,
    rib_spacing: float,
    stringer_eccentricity: float,
    rib_eccentricity: float,
    brace_eccentricity: float,
    opposite_brace_section: BeamSection | None = None,
    opposite_brace_eccentricity: float | None = None,
    brace_pattern: Literal["double", "single"] = "double",
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a braced orthogrid with alternating or crossed diagonal braces."""

    ds = _positive(stringer_spacing, name="stringer_spacing")
    dr = _positive(rib_spacing, name="rib_spacing")
    if brace_pattern not in {"double", "single"}:
        msg = "brace_pattern must be 'double' or 'single'."
        raise ValueError(msg)
    brace_multiplier = 1.0 if brace_pattern == "double" else 0.5
    diagonal_length = float(np.hypot(ds, dr))
    diagonal_angle = float(np.arctan2(dr, ds))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=ds * dr,
        skin=skin,
        members=(
            BeamMember(stringer_section, dr, 0.0, stringer_eccentricity, label="stringer"),
            BeamMember(rib_section, ds, np.pi / 2.0, rib_eccentricity, label="rib"),
            BeamMember(
                brace_section,
                diagonal_length,
                diagonal_angle,
                brace_eccentricity,
                multiplicity=brace_multiplier,
                label="+brace",
            ),
            BeamMember(
                _same_or_second(brace_section, opposite_brace_section),
                diagonal_length,
                -diagonal_angle,
                brace_eccentricity
                if opposite_brace_eccentricity is None
                else opposite_brace_eccentricity,
                multiplicity=brace_multiplier,
                label="-brace",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={
            "source": "braced_orthogrid",
            "brace_pattern": brace_pattern,
            "stringer_spacing": ds,
            "rib_spacing": dr,
        },
    )


def isosceles_triangle_grid_cell(
    *,
    skin: LinearABDWall,
    stringer_section: BeamSection,
    diagonal_section: BeamSection,
    base: float,
    height: float,
    stringer_eccentricity: float,
    diagonal_eccentricity: float,
    opposite_diagonal_section: BeamSection | None = None,
    opposite_diagonal_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create Nemeth's isosceles-triangle grid cell."""

    b = _positive(base, name="base")
    h = _positive(height, name="height")
    diagonal_length = float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(h, 0.5 * b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=b * h,
        skin=skin,
        members=(
            BeamMember(stringer_section, b, 0.0, stringer_eccentricity, label="stringer"),
            BeamMember(
                diagonal_section,
                diagonal_length,
                diagonal_angle,
                diagonal_eccentricity,
                label="+diagonal",
            ),
            BeamMember(
                _same_or_second(diagonal_section, opposite_diagonal_section),
                diagonal_length,
                -diagonal_angle,
                diagonal_eccentricity
                if opposite_diagonal_eccentricity is None
                else opposite_diagonal_eccentricity,
                label="-diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": "isosceles_triangle_grid", "base": b, "height": h},
    )


def kagome_cell(
    *,
    skin: LinearABDWall,
    stringer_section: BeamSection,
    diagonal_section: BeamSection,
    base: float,
    height: float,
    stringer_eccentricity: float,
    diagonal_eccentricity: float,
    opposite_diagonal_section: BeamSection | None = None,
    opposite_diagonal_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create Nemeth's Kagome grid cell."""

    b = _positive(base, name="base")
    h = _positive(height, name="height")
    diagonal_length = 2.0 * float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(2.0 * h, b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=2.0 * b * h,
        skin=skin,
        members=(
            BeamMember(
                stringer_section,
                b,
                0.0,
                stringer_eccentricity,
                multiplicity=2.0,
                label="stringer",
            ),
            BeamMember(
                diagonal_section,
                diagonal_length,
                diagonal_angle,
                diagonal_eccentricity,
                label="+diagonal",
            ),
            BeamMember(
                _same_or_second(diagonal_section, opposite_diagonal_section),
                diagonal_length,
                -diagonal_angle,
                diagonal_eccentricity
                if opposite_diagonal_eccentricity is None
                else opposite_diagonal_eccentricity,
                label="-diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": "kagome", "base": b, "height": h},
    )


def hexagonal_grid_cell(
    *,
    skin: LinearABDWall,
    rib_section: BeamSection,
    diagonal_section: BeamSection,
    half_width: float,
    diagonal_rise: float,
    rib_length: float,
    rib_eccentricity: float,
    diagonal_eccentricity: float,
    opposite_diagonal_section: BeamSection | None = None,
    opposite_diagonal_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create Nemeth's hexagon-shaped grid cell."""

    a = _positive(half_width, name="half_width")
    b = _positive(diagonal_rise, name="diagonal_rise")
    c = _positive(rib_length, name="rib_length")
    diagonal_length = 0.5 * float(np.hypot(a, b))
    diagonal_angle = float(np.arctan2(b, a))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=2.0 * a * (b + c),
        skin=skin,
        members=(
            BeamMember(
                diagonal_section,
                diagonal_length,
                diagonal_angle,
                diagonal_eccentricity,
                multiplicity=2.0,
                label="+diagonal",
            ),
            BeamMember(
                _same_or_second(diagonal_section, opposite_diagonal_section),
                diagonal_length,
                -diagonal_angle,
                diagonal_eccentricity
                if opposite_diagonal_eccentricity is None
                else opposite_diagonal_eccentricity,
                multiplicity=2.0,
                label="-diagonal",
            ),
            BeamMember(rib_section, c, np.pi / 2.0, rib_eccentricity, label="rib"),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={
            "source": "hexagonal_grid",
            "half_width": a,
            "diagonal_rise": b,
            "rib_length": c,
        },
    )


def regular_hexagonal_grid_cell(
    *,
    skin: LinearABDWall,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member regular hexagonal-grid special case."""

    p = _positive(pitch, name="pitch")
    return hexagonal_grid_cell(
        skin=skin,
        rib_section=member_section,
        diagonal_section=member_section,
        half_width=np.sqrt(3.0) * p / 2.0,
        diagonal_rise=0.5 * p,
        rib_length=p,
        rib_eccentricity=eccentricity,
        diagonal_eccentricity=eccentricity,
        frame=frame,
        convention=convention,
    )


def star_cell(
    *,
    skin: LinearABDWall,
    stringer_section: BeamSection,
    diagonal_section: BeamSection,
    base: float,
    height: float,
    stringer_eccentricity: float,
    diagonal_eccentricity: float,
    opposite_diagonal_section: BeamSection | None = None,
    opposite_diagonal_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create Nemeth's isosceles-star-cell grid."""

    b = _positive(base, name="base")
    h = _positive(height, name="height")
    nodes = (
        CellNode(b / 3.0, 0.0),
        CellNode(b / 2.0, h / 3.0),
        CellNode(b / 6.0, h / 3.0),
        CellNode(0.0, 2.0 * h / 3.0),
        CellNode(-b / 6.0, h / 3.0),
        CellNode(-b / 2.0, h / 3.0),
        CellNode(-b / 3.0, 0.0),
        CellNode(-b / 2.0, -h / 3.0),
        CellNode(-b / 6.0, -h / 3.0),
        CellNode(0.0, -2.0 * h / 3.0),
        CellNode(b / 6.0, -h / 3.0),
        CellNode(b / 2.0, -h / 3.0),
    )
    diagonal_2 = _same_or_second(diagonal_section, opposite_diagonal_section)
    diagonal_2_eccentricity = (
        diagonal_eccentricity
        if opposite_diagonal_eccentricity is None
        else opposite_diagonal_eccentricity
    )
    edges = (
        CellEdge(0, 11, diagonal_2, diagonal_2_eccentricity, label="d2-1"),
        CellEdge(0, 1, diagonal_section, diagonal_eccentricity, label="d1-1"),
        CellEdge(2, 1, stringer_section, stringer_eccentricity, label="s-1"),
        CellEdge(2, 3, diagonal_2, diagonal_2_eccentricity, label="d2-2"),
        CellEdge(4, 3, diagonal_section, diagonal_eccentricity, label="d1-2"),
        CellEdge(4, 5, stringer_section, stringer_eccentricity, label="s-2"),
        CellEdge(6, 5, diagonal_2, diagonal_2_eccentricity, label="d2-3"),
        CellEdge(6, 7, diagonal_section, diagonal_eccentricity, label="d1-3"),
        CellEdge(8, 7, stringer_section, stringer_eccentricity, label="s-3"),
        CellEdge(8, 9, diagonal_2, diagonal_2_eccentricity, label="d2-4"),
        CellEdge(10, 9, diagonal_section, diagonal_eccentricity, label="d1-4"),
        CellEdge(10, 11, stringer_section, stringer_eccentricity, label="s-4"),
    )
    return graph_unit_cell(
        area=4.0 * b * h / 3.0,
        skin=skin,
        nodes=nodes,
        edges=edges,
        frame=frame,
        convention=convention,
        metadata={"source": "star_cell", "base": b, "height": h},
    )


def equilateral_star_cell(
    *,
    skin: LinearABDWall,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member equilateral star-cell special case."""

    p = _positive(pitch, name="pitch")
    return star_cell(
        skin=skin,
        stringer_section=member_section,
        diagonal_section=member_section,
        base=p,
        height=np.sqrt(3.0) * p / 2.0,
        stringer_eccentricity=eccentricity,
        diagonal_eccentricity=eccentricity,
        frame=frame,
        convention=convention,
    )


def _sandwich_face_skin(
    *,
    bottom_face: LinearABDWall,
    top_face: LinearABDWall,
    bottom_face_offset: float,
    top_face_offset: float,
    source: str,
) -> LinearABDWall:
    return superpose_linear_abd_walls(
        shift_reference_surface(bottom_face, bottom_face_offset),
        shift_reference_surface(top_face, top_face_offset),
        metadata={
            "source": source,
            "bottom_face_offset": float(bottom_face_offset),
            "top_face_offset": float(top_face_offset),
        },
    )


def sandwich_orthogrid_core_cell(
    *,
    bottom_face: LinearABDWall,
    top_face: LinearABDWall,
    bottom_face_offset: float,
    top_face_offset: float,
    stringer_section: BeamSection,
    rib_section: BeamSection,
    stringer_spacing: float,
    rib_spacing: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid-core sandwich cell with shifted face sheets."""

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_offset=bottom_face_offset,
        top_face_offset=top_face_offset,
        source="sandwich_orthogrid_core_faces",
    )
    return orthogrid_cell(
        skin=skin,
        stringer_section=stringer_section,
        rib_section=rib_section,
        stringer_spacing=stringer_spacing,
        rib_spacing=rib_spacing,
        stringer_eccentricity=0.0,
        rib_eccentricity=0.0,
        frame=frame,
        convention=convention,
    )


def sandwich_hexagonal_core_cell(
    *,
    bottom_face: LinearABDWall,
    top_face: LinearABDWall,
    bottom_face_offset: float,
    top_face_offset: float,
    rib_section: BeamSection,
    diagonal_section: BeamSection,
    half_width: float,
    diagonal_rise: float,
    rib_length: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a hexagonal-core sandwich cell with shifted face sheets."""

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_offset=bottom_face_offset,
        top_face_offset=top_face_offset,
        source="sandwich_hexagonal_core_faces",
    )
    return hexagonal_grid_cell(
        skin=skin,
        rib_section=rib_section,
        diagonal_section=diagonal_section,
        half_width=half_width,
        diagonal_rise=diagonal_rise,
        rib_length=rib_length,
        rib_eccentricity=0.0,
        diagonal_eccentricity=0.0,
        frame=frame,
        convention=convention,
    )


def sandwich_star_core_cell(
    *,
    bottom_face: LinearABDWall,
    top_face: LinearABDWall,
    bottom_face_offset: float,
    top_face_offset: float,
    stringer_section: BeamSection,
    diagonal_section: BeamSection,
    base: float,
    height: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a star-core sandwich cell with shifted face sheets."""

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_offset=bottom_face_offset,
        top_face_offset=top_face_offset,
        source="sandwich_star_core_faces",
    )
    return star_cell(
        skin=skin,
        stringer_section=stringer_section,
        diagonal_section=diagonal_section,
        base=base,
        height=height,
        stringer_eccentricity=0.0,
        diagonal_eccentricity=0.0,
        frame=frame,
        convention=convention,
    )


__all__ = [
    "BeamMember",
    "CanonicalUnitCell",
    "CellEdge",
    "CellNode",
    "StiffenerFamily",
    "braced_orthogrid_cell",
    "equilateral_isogrid_cell",
    "equilateral_star_cell",
    "graph_unit_cell",
    "hexagonal_grid_cell",
    "isosceles_triangle_grid_cell",
    "kagome_cell",
    "orthogrid_cell",
    "regular_hexagonal_grid_cell",
    "sandwich_hexagonal_core_cell",
    "sandwich_orthogrid_core_cell",
    "sandwich_star_core_cell",
    "star_cell",
    "unidirectional_cell",
]
