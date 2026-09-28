"""Repeating stiffener-cell value objects and constructors."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal

import numpy as np

from tensyl.core._validation import finite_number, positive_number
from tensyl.core.constitutive import (
    ABDStiffness,
    shift_reference_surface,
    superpose_abd_stiffnesses,
)
from tensyl.core.conventions import (
    DEFAULT_FRAME,
    DEFAULT_STRAIN_CONVENTION,
    Frame2D,
    StrainConvention,
)
from tensyl.sections.beam import BeamSection


@dataclass(frozen=True, slots=True)
class BeamMember:
    """A straight stiffener member in a local tangent-plane unit cell.

    ``angle_rad`` is measured from local ``e1`` toward ``e2``. Both offset
    inputs are signed from the reference surface along ``+n``. Most homogeneous
    members need only ``axial_eccentricity``; when ``shear_eccentricity`` is
    omitted, Tensyl uses the axial value for both effects.

    Attributes:
        section: Centroidal beam stiffness for the member.
        length: Positive member length inside the repeated cell.
        angle_rad: Member angle measured from local ``e1`` toward ``e2``.
        axial_eccentricity: Signed effective offset for axial response along ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear
            response.
            Defaults to ``axial_eccentricity``.
        multiplicity: Positive count or density multiplier for identical
            members represented by this object.
        label: Optional member label for diagnostics and metadata.
    """

    section: BeamSection
    length: float
    angle_rad: float
    axial_eccentricity: float
    multiplicity: float = 1.0
    label: str = ""
    shear_eccentricity: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "length", positive_number(self.length, name="length"))
        object.__setattr__(self, "angle_rad", finite_number(self.angle_rad, name="angle_rad"))
        axial = finite_number(self.axial_eccentricity, name="axial_eccentricity")
        shear = (
            axial
            if self.shear_eccentricity is None
            else finite_number(
                self.shear_eccentricity,
                name="shear_eccentricity",
            )
        )
        object.__setattr__(self, "axial_eccentricity", axial)
        object.__setattr__(self, "shear_eccentricity", shear)
        object.__setattr__(
            self, "multiplicity", positive_number(self.multiplicity, name="multiplicity")
        )


@dataclass(frozen=True, slots=True)
class CellNode:
    """A node in a local tangent-plane graph cell.

    Attributes:
        e1: Node coordinate along local ``e1``.
        e2: Node coordinate along local ``e2``.
        label: Optional node label for caller provenance.
    """

    e1: float
    e2: float
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "e1", finite_number(self.e1, name="e1"))
        object.__setattr__(self, "e2", finite_number(self.e2, name="e2"))


@dataclass(frozen=True, slots=True)
class CellVector:
    """A translation that moves one cell drawing to the next repeat.

    Attributes:
        e1: Vector component along local ``e1``.
        e2: Vector component along local ``e2``.
    """

    e1: float
    e2: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "e1", finite_number(self.e1, name="e1"))
        object.__setattr__(self, "e2", finite_number(self.e2, name="e2"))


@dataclass(frozen=True, slots=True)
class CellGeometryEdge:
    """A line between two nodes in a cell drawing.

    Attributes:
        start: Index of the start node.
        end: Index of the end node.
        family: Stable member-family identifier used for grouping or styling.
        label: Optional source member label.
    """

    start: int
    end: int
    family: str
    label: str = ""

    def __post_init__(self) -> None:
        if not self.family:
            msg = "CellGeometryEdge family must be nonempty."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class CellSegment:
    """One drawable line returned by ``CellGeometry.segments``.

    Attributes:
        start_e1: Start coordinate along local ``e1``.
        start_e2: Start coordinate along local ``e2``.
        end_e1: End coordinate along local ``e1``.
        end_e2: End coordinate along local ``e2``.
        family: Stable member-family identifier.
        label: Optional source member label.
    """

    start_e1: float
    start_e2: float
    end_e1: float
    end_e2: float
    family: str
    label: str = ""


@dataclass(frozen=True, slots=True)
class CellGeometry:
    """Coordinates and connections used to draw and repeat a unit cell.

    Geometry is separate from the ``members`` list used in the stiffness
    calculation. A drawing may show a shared boundary member twice, while the
    calculation counts only the amount that belongs to one repeat area.

    Attributes:
        nodes: Cell nodes in local tangent-plane coordinates.
        edges: Drawable edges between nodes.
        repeat_vectors: Two independent translations that tile the pattern.
        boundary: Optional ordered node indices around the basic-cell outline.
            The outline is a drawing aid, not a beam family.
    """

    nodes: tuple[CellNode, ...]
    edges: tuple[CellGeometryEdge, ...]
    repeat_vectors: tuple[CellVector, CellVector]
    boundary: tuple[int, ...] = ()

    def __post_init__(self) -> None:
        nodes = tuple(self.nodes)
        edges = tuple(self.edges)
        repeat_vectors = tuple(self.repeat_vectors)
        boundary = tuple(self.boundary)
        if len(nodes) < 2:
            msg = "CellGeometry requires at least two nodes."
            raise ValueError(msg)
        if not edges:
            msg = "CellGeometry requires at least one edge."
            raise ValueError(msg)
        if len(repeat_vectors) != 2:
            msg = "CellGeometry requires exactly two repeat vectors."
            raise ValueError(msg)
        for edge in edges:
            if edge.start < 0 or edge.start >= len(nodes):
                msg = f"geometry edge start index {edge.start} is out of range."
                raise ValueError(msg)
            if edge.end < 0 or edge.end >= len(nodes):
                msg = f"geometry edge end index {edge.end} is out of range."
                raise ValueError(msg)
            if edge.start == edge.end:
                msg = "geometry edge start and end nodes must be distinct."
                raise ValueError(msg)
        for index in boundary:
            if index < 0 or index >= len(nodes):
                msg = f"geometry boundary index {index} is out of range."
                raise ValueError(msg)
        a, b = repeat_vectors
        determinant = a.e1 * b.e2 - a.e2 * b.e1
        if determinant == 0.0:
            msg = "CellGeometry repeat vectors must be linearly independent."
            raise ValueError(msg)
        object.__setattr__(self, "nodes", nodes)
        object.__setattr__(self, "edges", edges)
        object.__setattr__(self, "repeat_vectors", repeat_vectors)
        object.__setattr__(self, "boundary", boundary)

    @property
    def repeat_area(self) -> float:
        """Return the positive area spanned by the two repeat vectors."""

        a, b = self.repeat_vectors
        return abs(a.e1 * b.e2 - a.e2 * b.e1)

    def segments(self, *, repeat_a: int = 1, repeat_b: int = 1) -> tuple[CellSegment, ...]:
        """Return drawable segments for one cell or a rectangular repeat block.

        Args:
            repeat_a: Positive number of repeats along the first repeat vector.
            repeat_b: Positive number of repeats along the second repeat vector.

        Returns:
            Immutable line segments with member-family metadata.

        Raises:
            ValueError: If either repeat count is not a positive integer.
        """

        if isinstance(repeat_a, bool) or not isinstance(repeat_a, int) or repeat_a <= 0:
            msg = "repeat_a must be a positive integer."
            raise ValueError(msg)
        if isinstance(repeat_b, bool) or not isinstance(repeat_b, int) or repeat_b <= 0:
            msg = "repeat_b must be a positive integer."
            raise ValueError(msg)
        vector_a, vector_b = self.repeat_vectors
        segments: list[CellSegment] = []
        for index_a in range(repeat_a):
            for index_b in range(repeat_b):
                offset_e1 = index_a * vector_a.e1 + index_b * vector_b.e1
                offset_e2 = index_a * vector_a.e2 + index_b * vector_b.e2
                for edge in self.edges:
                    start = self.nodes[edge.start]
                    end = self.nodes[edge.end]
                    segments.append(
                        CellSegment(
                            start_e1=start.e1 + offset_e1,
                            start_e2=start.e2 + offset_e2,
                            end_e1=end.e1 + offset_e1,
                            end_e2=end.e2 + offset_e2,
                            family=edge.family,
                            label=edge.label,
                        )
                    )
        return tuple(segments)


@dataclass(frozen=True, slots=True)
class CellEdge:
    """A stiffener between two nodes in a custom graph cell.

    Attributes:
        start: Index of the start node in the node tuple.
        end: Index of the end node in the node tuple.
        section: Centroidal beam stiffness for the edge.
        axial_eccentricity: Signed effective offset for axial response along
            ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear
            response.
        multiplicity: Positive count or density multiplier.
        label: Optional edge label for diagnostics and metadata.
        family: Optional stable family name retained in drawable geometry.
    """

    start: int
    end: int
    section: BeamSection
    axial_eccentricity: float
    multiplicity: float = 1.0
    label: str = ""
    shear_eccentricity: float | None = None
    family: str = ""

    def __post_init__(self) -> None:
        axial = finite_number(self.axial_eccentricity, name="axial_eccentricity")
        shear = (
            axial
            if self.shear_eccentricity is None
            else finite_number(
                self.shear_eccentricity,
                name="shear_eccentricity",
            )
        )
        object.__setattr__(self, "axial_eccentricity", axial)
        object.__setattr__(self, "shear_eccentricity", shear)
        object.__setattr__(
            self, "multiplicity", positive_number(self.multiplicity, name="multiplicity")
        )


@dataclass(frozen=True, slots=True)
class CanonicalUnitCell:
    """A complete repeating cell ready for tangent-plane homogenization.

    ``area`` is the repeated tangent-plane area represented by ``members``.
    The cell frame and strain convention must match the skin ABD stiffness.

    Attributes:
        area: Positive repeated tangent-plane area.
        skin: Baseline skin stiffness for the cell.
        members: One or more straight beam members in the local tangent plane.
        frame: Local frame shared by the skin and members.
        convention: Generalized strain convention shared by the skin and cell.
        geometry: Optional coordinates and repeat vectors for drawing the cell.
        metadata: Read-only cell provenance.
    """

    area: float
    skin: ABDStiffness
    members: tuple[BeamMember, ...]
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION
    geometry: CellGeometry | None = None
    metadata: dict[str, Any] | MappingProxyType[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "area", positive_number(self.area, name="area"))
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
        if self.geometry is not None and not np.isclose(
            self.geometry.repeat_area,
            self.area,
            rtol=1.0e-12,
            atol=0.0,
        ):
            msg = "cell geometry repeat area must match the homogenization cell area."
            raise ValueError(msg)
        object.__setattr__(self, "members", members)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class StiffenerFamily:
    """A repeating family of parallel stiffeners for the direct calculation.

    ``spacing`` is the family pitch normal to the member direction.
    Eccentricities use the same signed ``+n`` convention as ``BeamMember``.

    Attributes:
        section: Centroidal beam stiffness for the family.
        spacing: Positive family pitch normal to the member direction.
        angle_rad: Family angle measured from local ``e1`` toward ``e2``.
        axial_eccentricity: Signed effective offset for axial response along
            ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear
            response.
        multiplicity: Positive family multiplier.
        label: Optional family label for diagnostics and metadata.
    """

    section: BeamSection
    spacing: float
    angle_rad: float
    axial_eccentricity: float
    multiplicity: float = 1.0
    label: str = ""
    shear_eccentricity: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "spacing", positive_number(self.spacing, name="spacing"))
        object.__setattr__(self, "angle_rad", finite_number(self.angle_rad, name="angle_rad"))
        axial = finite_number(self.axial_eccentricity, name="axial_eccentricity")
        shear = (
            axial
            if self.shear_eccentricity is None
            else finite_number(
                self.shear_eccentricity,
                name="shear_eccentricity",
            )
        )
        object.__setattr__(self, "axial_eccentricity", axial)
        object.__setattr__(self, "shear_eccentricity", shear)
        object.__setattr__(
            self, "multiplicity", positive_number(self.multiplicity, name="multiplicity")
        )


def _cell_frame_and_convention(
    skin: ABDStiffness,
    frame: Frame2D | None,
    convention: StrainConvention | None,
) -> tuple[Frame2D, StrainConvention]:
    # Cell helpers default to the skin's frame and convention because the
    # homogenizer assumes skin and stiffeners are assembled in one local basis.
    cell_frame = skin.frame if frame is None else frame
    cell_convention = skin.convention if convention is None else convention
    return cell_frame, cell_convention


def _same_or_second(first: BeamSection, second: BeamSection | None) -> BeamSection:
    return first if second is None else second


def _same_or_value(first: float, second: float | None) -> float:
    return first if second is None else second


def _paired_oblique_members(
    *,
    section: BeamSection,
    opposite_section: BeamSection | None,
    length: float,
    angle_rad: float,
    axial_eccentricity: float,
    shear_eccentricity: float | None,
    opposite_axial_eccentricity: float | None,
    opposite_shear_eccentricity: float | None,
    multiplicity: float = 1.0,
    positive_label: str,
    negative_label: str,
) -> tuple[BeamMember, BeamMember]:
    # Several Nemeth-style cells use mirrored oblique members. Keep the pairing
    # in one helper so opposite material/eccentricity overrides stay symmetric.
    negative_axial_eccentricity = _same_or_value(
        axial_eccentricity,
        opposite_axial_eccentricity,
    )
    negative_shear_eccentricity = opposite_shear_eccentricity
    if opposite_axial_eccentricity is None and opposite_shear_eccentricity is None:
        negative_shear_eccentricity = shear_eccentricity
    return (
        BeamMember(
            section=section,
            length=length,
            angle_rad=angle_rad,
            axial_eccentricity=axial_eccentricity,
            shear_eccentricity=shear_eccentricity,
            multiplicity=multiplicity,
            label=positive_label,
        ),
        BeamMember(
            section=_same_or_second(section, opposite_section),
            length=length,
            angle_rad=-angle_rad,
            axial_eccentricity=negative_axial_eccentricity,
            shear_eccentricity=negative_shear_eccentricity,
            multiplicity=multiplicity,
            label=negative_label,
        ),
    )


def _geometry(
    *,
    nodes: tuple[tuple[float, float], ...],
    edges: tuple[tuple[int, int, str, str], ...],
    repeat_vectors: tuple[tuple[float, float], tuple[float, float]],
    boundary: tuple[int, ...] = (),
) -> CellGeometry:
    vector_a, vector_b = repeat_vectors
    return CellGeometry(
        nodes=tuple(CellNode(e1, e2) for e1, e2 in nodes),
        edges=tuple(
            CellGeometryEdge(start=start, end=end, family=family, label=label)
            for start, end, family, label in edges
        ),
        repeat_vectors=(CellVector(*vector_a), CellVector(*vector_b)),
        boundary=boundary,
    )


def graph_unit_cell(
    *,
    area: float,
    skin: ABDStiffness,
    nodes: tuple[CellNode, ...],
    edges: tuple[CellEdge, ...],
    repeat_vectors: tuple[CellVector, CellVector] | None = None,
    boundary: tuple[int, ...] = (),
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    metadata: dict[str, Any] | MappingProxyType[str, Any] | None = None,
) -> CanonicalUnitCell:
    """Build a repeating cell from local node coordinates and beam edges.

    Node coordinates are local tangent-plane coordinates in the same length
    unit used by ``area``.

    Args:
        area: Positive repeated-cell area.
        skin: Baseline skin stiffness.
        nodes: Graph nodes in local tangent-plane coordinates.
        edges: Beam edges connecting nodes by index.
        repeat_vectors: Optional pair of independent pattern translations. When
            provided, Tensyl retains drawable geometry on the returned cell.
        boundary: Optional ordered node indices for the cell perimeter.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.
        metadata: Optional metadata merged into the cell provenance.

    Returns:
        Repeating cell with each graph edge converted to a member.

    Raises:
        ValueError: If the graph is underspecified, an edge index is invalid,
            an edge has zero length, or the resulting cell is incompatible with
            the skin.
    """

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
        dx = end.e1 - start.e1
        dy = end.e2 - start.e2
        length = float(np.hypot(dx, dy))
        members.append(
            BeamMember(
                section=edge.section,
                length=length,
                angle_rad=float(np.arctan2(dy, dx)),
                axial_eccentricity=edge.axial_eccentricity,
                shear_eccentricity=edge.shear_eccentricity,
                multiplicity=edge.multiplicity,
                label=edge.label,
            )
        )
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    cell_metadata = {"source": "graph_unit_cell"}
    if metadata is not None:
        cell_metadata.update(metadata)
    geometry = None
    if repeat_vectors is not None:
        geometry = CellGeometry(
            nodes=node_tuple,
            edges=tuple(
                CellGeometryEdge(
                    start=edge.start,
                    end=edge.end,
                    family=edge.family or edge.label or "member",
                    label=edge.label,
                )
                for edge in edges
            ),
            repeat_vectors=repeat_vectors,
            boundary=boundary,
        )
    return CanonicalUnitCell(
        area=area,
        skin=skin,
        members=tuple(members),
        frame=cell_frame,
        convention=cell_convention,
        geometry=geometry,
        metadata=cell_metadata,
    )


def unidirectional_cell(
    *,
    skin: ABDStiffness,
    member_section: BeamSection,
    spacing: float,
    axial_eccentricity: float,
    shear_eccentricity: float | None = None,
    angle_rad: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    label: str = "unidirectional",
) -> CanonicalUnitCell:
    """Create a repeating strip with one family of parallel stiffeners.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for the repeated family.
        spacing: Positive pitch normal to the family direction.
        axial_eccentricity: Signed effective offset for axial response along ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear.
        angle_rad: Family angle measured from local ``e1``.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.
        label: Source label stored in metadata.

    Returns:
        Canonical unit cell with one representative member.

    Raises:
        ValueError: If spacing, angle, eccentricity, frame, or convention
            validation fails.
    """

    d = positive_number(spacing, name="spacing")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # A unit-length strip gives length / area = 1 / spacing, matching the
    # continuous family density used by the direct calculation.
    member = BeamMember(
        section=member_section,
        length=1.0,
        angle_rad=angle_rad,
        axial_eccentricity=axial_eccentricity,
        shear_eccentricity=shear_eccentricity,
        label="stiffener",
    )
    angle = member.angle_rad
    direction = (float(np.cos(angle)), float(np.sin(angle)))
    normal = (-d * direction[1], d * direction[0])
    return CanonicalUnitCell(
        area=d,
        skin=skin,
        members=(member,),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=((0.0, 0.0), direction),
            edges=((0, 1, "member", "member"),),
            repeat_vectors=(direction, normal),
        ),
        metadata={"source": label, "spacing": d},
    )


def orthogrid_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    e2_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    e2_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    e2_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid with members aligned to local ``e1`` and ``e2``.

    ``e1_pitch`` and ``e2_pitch`` are the repeat-box dimensions measured along
    those axes. The distance between ``e1`` members is therefore ``e2_pitch``,
    and vice versa.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for members running along local ``e1``.
        e2_section: Section stiffness for members running along local ``e2``.
        e1_pitch: Positive basic-cell span along local ``e1``.
        e2_pitch: Positive basic-cell span along local ``e2``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        e2_axial_eccentricity: Signed ``e2`` family offset for axial response.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        e2_shear_eccentricity: Optional ``e2`` offset for in-plane shear.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical orthogrid unit cell.

    Raises:
        ValueError: If a pitch, eccentricity, frame, or convention validation
            fails.
    """

    pitch_e1 = positive_number(e1_pitch, name="e1_pitch")
    pitch_e2 = positive_number(e2_pitch, name="e2_pitch")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # Each member spans its coordinate pitch, so length / area reduces to the
    # reciprocal pitch normal to that family.
    return CanonicalUnitCell(
        area=pitch_e1 * pitch_e2,
        skin=skin,
        members=(
            BeamMember(
                section=e1_section,
                length=pitch_e1,
                angle_rad=0.0,
                axial_eccentricity=e1_axial_eccentricity,
                shear_eccentricity=e1_shear_eccentricity,
                label="e1",
            ),
            BeamMember(
                section=e2_section,
                length=pitch_e2,
                angle_rad=np.pi / 2.0,
                axial_eccentricity=e2_axial_eccentricity,
                shear_eccentricity=e2_shear_eccentricity,
                label="e2",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=(
                (-0.5 * pitch_e1, -0.5 * pitch_e2),
                (0.5 * pitch_e1, -0.5 * pitch_e2),
                (0.5 * pitch_e1, 0.5 * pitch_e2),
                (-0.5 * pitch_e1, 0.5 * pitch_e2),
            ),
            edges=(
                (0, 1, "e1", "e1-bottom"),
                (3, 2, "e1", "e1-top"),
                (0, 3, "e2", "e2-left"),
                (1, 2, "e2", "e2-right"),
            ),
            repeat_vectors=((pitch_e1, 0.0), (0.0, pitch_e2)),
            boundary=(0, 1, 2, 3),
        ),
        metadata={
            "source": "orthogrid",
            "e1_pitch": pitch_e1,
            "e2_pitch": pitch_e2,
        },
    )


def equilateral_isogrid_cell(
    *,
    skin: ABDStiffness,
    member_section: BeamSection,
    side_length: float,
    axial_eccentricity: float,
    shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an equilateral isogrid cell with three identical families.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all three families.
        side_length: Positive equilateral-triangle side length.
        axial_eccentricity: Signed effective offset for axial response along ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical cell with members at 0 and +/-60 degrees.

    Raises:
        ValueError: If side length, eccentricity, frame, or convention
            validation
            fails.
    """

    p = positive_number(side_length, name="side_length")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    height = np.sqrt(3.0) * p / 2.0
    # The three directions share one parallelogram cell area. Multiplicity is
    # left at one because the cell already contains one representative member
    # from each family.
    return CanonicalUnitCell(
        area=p * height,
        skin=skin,
        members=(
            BeamMember(
                section=member_section,
                length=p,
                angle_rad=0.0,
                axial_eccentricity=axial_eccentricity,
                shear_eccentricity=shear_eccentricity,
                label="e1",
            ),
            BeamMember(
                section=member_section,
                length=p,
                angle_rad=np.pi / 3.0,
                axial_eccentricity=axial_eccentricity,
                shear_eccentricity=shear_eccentricity,
                label="positive_diagonal",
            ),
            BeamMember(
                section=member_section,
                length=p,
                angle_rad=-np.pi / 3.0,
                axial_eccentricity=axial_eccentricity,
                shear_eccentricity=shear_eccentricity,
                label="negative_diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=((0.0, 0.0), (p, 0.0), (0.5 * p, height)),
            edges=(
                (0, 1, "e1", "e1"),
                (0, 2, "positive_diagonal", "+60"),
                (1, 2, "negative_diagonal", "-60"),
            ),
            repeat_vectors=((p, 0.0), (0.5 * p, height)),
            boundary=(0, 1, 2),
        ),
        metadata={"source": "equilateral_isogrid", "side_length": p},
    )


def braced_orthogrid_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    e2_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    e2_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    e2_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    diagonal_pattern: Literal["double", "single"] = "double",
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a braced orthogrid with alternating or crossed braces.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for members running along local ``e1``.
        e2_section: Section stiffness for members running along local ``e2``.
        positive_diagonal_section: Section stiffness for the positive diagonal.
        e1_pitch: Basic-bay span along local ``e1``; Nemeth's ``Lx``.
        e2_pitch: Basic-bay span along local ``e2``; Nemeth's ``Ly``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        e2_axial_eccentricity: Signed ``e2`` family offset for axial response.
        diagonal_axial_eccentricity: Signed positive-diagonal offset for axial
            response.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        e2_shear_eccentricity: Optional ``e2`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        diagonal_pattern: ``"double"`` for Nemeth figure 14 or ``"single"``
            for the alternating figure-16 pattern.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical braced orthogrid unit cell.

    Raises:
        ValueError: If a pitch is invalid or ``diagonal_pattern`` is not
            ``"double"`` or ``"single"``.
    """

    pitch_e1 = positive_number(e1_pitch, name="e1_pitch")
    pitch_e2 = positive_number(e2_pitch, name="e2_pitch")
    if diagonal_pattern not in {"double", "single"}:
        msg = "diagonal_pattern must be 'double' or 'single'."
        raise ValueError(msg)
    diagonal_length = float(np.hypot(pitch_e1, pitch_e2))
    diagonal_angle = float(np.arctan2(pitch_e2, pitch_e1))
    single = diagonal_pattern == "single"
    member_scale = 2.0 if single else 1.0
    orthogonal_multiplicity = 2.0 if single else 1.0
    cell_area = (4.0 if single else 1.0) * pitch_e1 * pitch_e2
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    if single:
        geometry = _geometry(
            nodes=(
                (-pitch_e1, 0.0),
                (pitch_e1, 0.0),
                (0.0, -pitch_e2),
                (0.0, pitch_e2),
                (-pitch_e1, -pitch_e2),
                (pitch_e1, pitch_e2),
                (pitch_e1, -pitch_e2),
                (-pitch_e1, pitch_e2),
            ),
            edges=(
                (0, 1, "e1", "1-2"),
                (2, 3, "e2", "3-4"),
                (4, 5, "positive_diagonal", "5-6"),
                (4, 6, "e1", "5-7"),
                (4, 7, "e2", "5-8"),
                (6, 7, "negative_diagonal", "7-8"),
            ),
            repeat_vectors=((2.0 * pitch_e1, 0.0), (0.0, 2.0 * pitch_e2)),
            boundary=(4, 6, 5, 7),
        )
    else:
        geometry = _geometry(
            nodes=(
                (-0.5 * pitch_e1, 0.0),
                (0.5 * pitch_e1, 0.0),
                (0.0, -0.5 * pitch_e2),
                (0.0, 0.5 * pitch_e2),
                (-0.5 * pitch_e1, -0.5 * pitch_e2),
                (0.5 * pitch_e1, 0.5 * pitch_e2),
                (0.5 * pitch_e1, -0.5 * pitch_e2),
                (-0.5 * pitch_e1, 0.5 * pitch_e2),
            ),
            edges=(
                (0, 1, "e1", "1-2"),
                (2, 3, "e2", "3-4"),
                (4, 5, "positive_diagonal", "5-6"),
                (6, 7, "negative_diagonal", "7-8"),
            ),
            repeat_vectors=((pitch_e1, 0.0), (0.0, pitch_e2)),
            boundary=(4, 6, 5, 7),
        )
    return CanonicalUnitCell(
        area=cell_area,
        skin=skin,
        members=(
            BeamMember(
                section=e1_section,
                length=member_scale * pitch_e1,
                angle_rad=0.0,
                axial_eccentricity=e1_axial_eccentricity,
                shear_eccentricity=e1_shear_eccentricity,
                multiplicity=orthogonal_multiplicity,
                label="e1",
            ),
            BeamMember(
                section=e2_section,
                length=member_scale * pitch_e2,
                angle_rad=np.pi / 2.0,
                axial_eccentricity=e2_axial_eccentricity,
                shear_eccentricity=e2_shear_eccentricity,
                multiplicity=orthogonal_multiplicity,
                label="e2",
            ),
            *_paired_oblique_members(
                section=positive_diagonal_section,
                opposite_section=negative_diagonal_section,
                length=member_scale * diagonal_length,
                angle_rad=diagonal_angle,
                axial_eccentricity=diagonal_axial_eccentricity,
                shear_eccentricity=diagonal_shear_eccentricity,
                opposite_axial_eccentricity=negative_diagonal_axial_eccentricity,
                opposite_shear_eccentricity=negative_diagonal_shear_eccentricity,
                positive_label="positive_diagonal",
                negative_label="negative_diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=geometry,
        metadata={
            "source": "braced_orthogrid",
            "diagonal_pattern": diagonal_pattern,
            "e1_pitch": pitch_e1,
            "e2_pitch": pitch_e2,
        },
    )


def diamond_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create Nemeth's figure-15 diamond pattern without an ``e2`` family.

    ``e1_pitch`` and ``e2_pitch`` are the rectangular repeat spans. The
    pattern contains one ``e1`` member family and two mirrored diagonal
    families; it is not an orthogrid with a nearly-zero ``e2`` stiffness.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for members running along local ``e1``.
        positive_diagonal_section: Section for the positive diagonal family.
        e1_pitch: Rectangular repeat span along local ``e1``.
        e2_pitch: Rectangular repeat span along local ``e2``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        diagonal_axial_eccentricity: Positive-diagonal axial offset.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical figure-15 diamond cell.

    Raises:
        ValueError: If a pitch, eccentricity, frame, or convention validation
            fails.
    """

    pitch_e1 = positive_number(e1_pitch, name="e1_pitch")
    pitch_e2 = positive_number(e2_pitch, name="e2_pitch")
    diagonal_length = float(np.hypot(pitch_e1, pitch_e2))
    diagonal_angle = float(np.arctan2(pitch_e2, pitch_e1))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=pitch_e1 * pitch_e2,
        skin=skin,
        members=(
            BeamMember(
                section=e1_section,
                length=pitch_e1,
                angle_rad=0.0,
                axial_eccentricity=e1_axial_eccentricity,
                shear_eccentricity=e1_shear_eccentricity,
                label="e1",
            ),
            *_paired_oblique_members(
                section=positive_diagonal_section,
                opposite_section=negative_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                axial_eccentricity=diagonal_axial_eccentricity,
                shear_eccentricity=diagonal_shear_eccentricity,
                opposite_axial_eccentricity=negative_diagonal_axial_eccentricity,
                opposite_shear_eccentricity=negative_diagonal_shear_eccentricity,
                positive_label="positive_diagonal",
                negative_label="negative_diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=(
                (-0.5 * pitch_e1, -0.5 * pitch_e2),
                (0.5 * pitch_e1, -0.5 * pitch_e2),
                (0.5 * pitch_e1, 0.5 * pitch_e2),
                (-0.5 * pitch_e1, 0.5 * pitch_e2),
            ),
            edges=(
                (0, 1, "e1", "e1-bottom"),
                (3, 2, "e1", "e1-top"),
                (0, 2, "positive_diagonal", "positive-diagonal"),
                (1, 3, "negative_diagonal", "negative-diagonal"),
            ),
            repeat_vectors=((pitch_e1, 0.0), (0.0, pitch_e2)),
            boundary=(0, 1, 2, 3),
        ),
        metadata={"source": "diamond", "e1_pitch": pitch_e1, "e2_pitch": pitch_e2},
    )


def isosceles_triangle_grid_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an isosceles-triangle grid cell.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for members running along local ``e1``.
        positive_diagonal_section: Section stiffness for the positive diagonal.
        e1_pitch: Triangle base along local ``e1``; Nemeth's ``Lx``.
        e2_pitch: Triangle height along local ``e2``; Nemeth's ``Ly``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        diagonal_axial_eccentricity: Positive-diagonal axial offset.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical isosceles-triangle grid unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    b = positive_number(e1_pitch, name="e1_pitch")
    h = positive_number(e2_pitch, name="e2_pitch")
    diagonal_length = float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(h, 0.5 * b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # The base member plus mirrored diagonals represent one triangular repeat
    # area in the local tangent plane.
    return CanonicalUnitCell(
        area=b * h,
        skin=skin,
        members=(
            BeamMember(
                section=e1_section,
                length=b,
                angle_rad=0.0,
                axial_eccentricity=e1_axial_eccentricity,
                shear_eccentricity=e1_shear_eccentricity,
                label="e1",
            ),
            *_paired_oblique_members(
                section=positive_diagonal_section,
                opposite_section=negative_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                axial_eccentricity=diagonal_axial_eccentricity,
                shear_eccentricity=diagonal_shear_eccentricity,
                opposite_axial_eccentricity=negative_diagonal_axial_eccentricity,
                opposite_shear_eccentricity=negative_diagonal_shear_eccentricity,
                positive_label="positive_diagonal",
                negative_label="negative_diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        # Table 6 cuts each diagonal halfway between stringer rows. A staggered
        # lattice reconnects those pieces into the continuous grid in figure 17.
        geometry=_geometry(
            nodes=(
                (-0.5 * b, 0.0),
                (0.5 * b, 0.0),
                (-0.25 * b, -0.5 * h),
                (0.25 * b, 0.5 * h),
                (0.25 * b, -0.5 * h),
                (-0.25 * b, 0.5 * h),
                (-0.5 * b, -h / 3.0),
                (0.0, -2.0 * h / 3.0),
                (0.5 * b, -h / 3.0),
                (0.5 * b, h / 3.0),
                (0.0, 2.0 * h / 3.0),
                (-0.5 * b, h / 3.0),
            ),
            edges=(
                (0, 1, "e1", "1-2"),
                (2, 3, "positive_diagonal", "3-4"),
                (4, 5, "negative_diagonal", "5-6"),
            ),
            repeat_vectors=((b, 0.0), (0.5 * b, h)),
            boundary=(6, 7, 8, 9, 10, 11),
        ),
        metadata={"source": "isosceles_triangle_grid", "e1_pitch": b, "e2_pitch": h},
    )


def kagome_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a Kagome grid cell.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for members running along local ``e1``.
        positive_diagonal_section: Section stiffness for the positive diagonal.
        e1_pitch: Kagome repeat width; Nemeth's ``Lx``.
        e2_pitch: Half of the Kagome repeat height; Nemeth's ``Ly``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        diagonal_axial_eccentricity: Positive-diagonal axial offset.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical Kagome unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    b = positive_number(e1_pitch, name="e1_pitch")
    h = positive_number(e2_pitch, name="e2_pitch")
    diagonal_length = 2.0 * float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(2.0 * h, b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # The doubled e1 multiplicity reflects two horizontal members in the
    # Kagome repeat area without duplicating identical BeamMember objects.
    return CanonicalUnitCell(
        area=2.0 * b * h,
        skin=skin,
        members=(
            BeamMember(
                section=e1_section,
                length=b,
                angle_rad=0.0,
                axial_eccentricity=e1_axial_eccentricity,
                shear_eccentricity=e1_shear_eccentricity,
                multiplicity=2.0,
                label="e1",
            ),
            *_paired_oblique_members(
                section=positive_diagonal_section,
                opposite_section=negative_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                axial_eccentricity=diagonal_axial_eccentricity,
                shear_eccentricity=diagonal_shear_eccentricity,
                opposite_axial_eccentricity=negative_diagonal_axial_eccentricity,
                opposite_shear_eccentricity=negative_diagonal_shear_eccentricity,
                positive_label="positive_diagonal",
                negative_label="negative_diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=(
                (-0.5 * b, -0.5 * h),
                (0.5 * b, -0.5 * h),
                (-0.5 * b, 0.5 * h),
                (0.5 * b, 0.5 * h),
                (-0.5 * b, -h),
                (0.5 * b, h),
                (0.5 * b, -h),
                (-0.5 * b, h),
            ),
            edges=(
                (0, 1, "e1", "1-2"),
                (2, 3, "e1", "3-4"),
                (4, 5, "positive_diagonal", "5-6"),
                (6, 7, "negative_diagonal", "7-8"),
            ),
            repeat_vectors=((b, 0.0), (0.0, 2.0 * h)),
            boundary=(4, 6, 5, 7),
        ),
        metadata={"source": "kagome", "e1_pitch": b, "e2_pitch": h},
    )


def hexagonal_grid_cell(
    *,
    skin: ABDStiffness,
    e2_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_half_pitch: float,
    diagonal_e2_rise: float,
    e2_member_length: float,
    e2_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e2_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a hexagon-shaped grid cell.

    Args:
        skin: Baseline skin stiffness.
        e2_section: Section stiffness for members running along local ``e2``.
        positive_diagonal_section: Section stiffness for the positive diagonal.
        e1_half_pitch: Nemeth's horizontal construction dimension ``a``.
        diagonal_e2_rise: Nemeth's diagonal rise ``b``.
        e2_member_length: Nemeth's vertical member length ``c``.
        e2_axial_eccentricity: Signed ``e2`` family offset for axial response.
        diagonal_axial_eccentricity: Positive-diagonal axial offset.
        e2_shear_eccentricity: Optional ``e2`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical hexagonal-grid unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    a = positive_number(e1_half_pitch, name="e1_half_pitch")
    b = positive_number(diagonal_e2_rise, name="diagonal_e2_rise")
    c = positive_number(e2_member_length, name="e2_member_length")
    diagonal_length = 0.5 * float(np.hypot(a, b))
    diagonal_angle = float(np.arctan2(b, a))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # These dimensions follow Nemeth table 8; metadata preserves the source
    # construction dimensions.
    return CanonicalUnitCell(
        area=2.0 * a * (b + c),
        skin=skin,
        members=(
            *_paired_oblique_members(
                section=positive_diagonal_section,
                opposite_section=negative_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                axial_eccentricity=diagonal_axial_eccentricity,
                shear_eccentricity=diagonal_shear_eccentricity,
                opposite_axial_eccentricity=negative_diagonal_axial_eccentricity,
                opposite_shear_eccentricity=negative_diagonal_shear_eccentricity,
                multiplicity=2.0,
                positive_label="positive_diagonal",
                negative_label="negative_diagonal",
            ),
            BeamMember(
                section=e2_section,
                length=c,
                angle_rad=np.pi / 2.0,
                axial_eccentricity=e2_axial_eccentricity,
                shear_eccentricity=e2_shear_eccentricity,
                label="e2",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        geometry=_geometry(
            nodes=(
                (0.5 * a, -0.5 * (b + c)),
                (0.0, -0.5 * c),
                (-0.5 * a, -0.5 * (b + c)),
                (0.5 * a, 0.5 * (b + c)),
                (0.0, 0.5 * c),
                (-0.5 * a, 0.5 * (b + c)),
            ),
            edges=(
                (1, 0, "negative_diagonal", "2-1"),
                (1, 2, "positive_diagonal", "2-3"),
                (1, 4, "e2", "2-5"),
                (4, 3, "positive_diagonal", "5-4"),
                (4, 5, "negative_diagonal", "5-6"),
            ),
            repeat_vectors=((a, b + c), (a, -(b + c))),
        ),
        metadata={
            "source": "hexagonal_grid",
            "e1_half_pitch": a,
            "diagonal_e2_rise": b,
            "e2_member_length": c,
        },
    )


def regular_hexagonal_grid_cell(
    *,
    skin: ABDStiffness,
    member_section: BeamSection,
    side_length: float,
    axial_eccentricity: float,
    shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member regular hexagonal-grid case.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all grid members.
        side_length: Positive regular-hexagon side length.
        axial_eccentricity: Signed effective offset for axial response along ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical regular hexagonal-grid unit cell.

    Raises:
        ValueError: If side length, eccentricity, frame, or convention
            validation
            fails.
    """

    p = positive_number(side_length, name="side_length")
    return hexagonal_grid_cell(
        skin=skin,
        e2_section=member_section,
        positive_diagonal_section=member_section,
        e1_half_pitch=np.sqrt(3.0) * p / 2.0,
        diagonal_e2_rise=0.5 * p,
        e2_member_length=p,
        e2_axial_eccentricity=axial_eccentricity,
        diagonal_axial_eccentricity=axial_eccentricity,
        e2_shear_eccentricity=shear_eccentricity,
        diagonal_shear_eccentricity=shear_eccentricity,
        frame=frame,
        convention=convention,
    )


def star_cell(
    *,
    skin: ABDStiffness,
    e1_section: BeamSection,
    positive_diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    e1_axial_eccentricity: float,
    diagonal_axial_eccentricity: float,
    e1_shear_eccentricity: float | None = None,
    diagonal_shear_eccentricity: float | None = None,
    negative_diagonal_section: BeamSection | None = None,
    negative_diagonal_axial_eccentricity: float | None = None,
    negative_diagonal_shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an isosceles star-cell grid.

    Args:
        skin: Baseline skin stiffness.
        e1_section: Section stiffness for short members along local ``e1``.
        positive_diagonal_section: Section stiffness for positive diagonals.
        e1_pitch: Nemeth's star base dimension ``B``.
        e2_pitch: Nemeth's star height dimension ``H``.
        e1_axial_eccentricity: Signed ``e1`` family offset for axial response.
        diagonal_axial_eccentricity: Positive-diagonal axial offset.
        e1_shear_eccentricity: Optional ``e1`` offset for in-plane shear.
        diagonal_shear_eccentricity: Optional positive-diagonal shear offset.
        negative_diagonal_section: Optional negative-diagonal section.
        negative_diagonal_axial_eccentricity: Optional negative-diagonal axial
            offset.
        negative_diagonal_shear_eccentricity: Optional negative-diagonal shear
            offset.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical star-cell grid.

    Raises:
        ValueError: If dimensions, eccentricities, graph connectivity, frame,
            or convention validation fails.
    """

    b = positive_number(e1_pitch, name="e1_pitch")
    h = positive_number(e2_pitch, name="e2_pitch")
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
    diagonal_2 = _same_or_second(positive_diagonal_section, negative_diagonal_section)
    diagonal_2_axial = _same_or_value(
        diagonal_axial_eccentricity,
        negative_diagonal_axial_eccentricity,
    )
    diagonal_2_shear = negative_diagonal_shear_eccentricity
    if (
        negative_diagonal_axial_eccentricity is None
        and negative_diagonal_shear_eccentricity is None
    ):
        diagonal_2_shear = diagonal_shear_eccentricity
    edges = (
        CellEdge(
            0,
            11,
            diagonal_2,
            diagonal_2_axial,
            shear_eccentricity=diagonal_2_shear,
            label="d2-1",
            family="negative_diagonal",
        ),
        CellEdge(
            0,
            1,
            positive_diagonal_section,
            diagonal_axial_eccentricity,
            shear_eccentricity=diagonal_shear_eccentricity,
            label="d1-1",
            family="positive_diagonal",
        ),
        CellEdge(
            2,
            1,
            e1_section,
            e1_axial_eccentricity,
            shear_eccentricity=e1_shear_eccentricity,
            label="e1-1",
            family="e1",
        ),
        CellEdge(
            2,
            3,
            diagonal_2,
            diagonal_2_axial,
            shear_eccentricity=diagonal_2_shear,
            label="d2-2",
            family="negative_diagonal",
        ),
        CellEdge(
            4,
            3,
            positive_diagonal_section,
            diagonal_axial_eccentricity,
            shear_eccentricity=diagonal_shear_eccentricity,
            label="d1-2",
            family="positive_diagonal",
        ),
        CellEdge(
            4,
            5,
            e1_section,
            e1_axial_eccentricity,
            shear_eccentricity=e1_shear_eccentricity,
            label="e1-2",
            family="e1",
        ),
        CellEdge(
            6,
            5,
            diagonal_2,
            diagonal_2_axial,
            shear_eccentricity=diagonal_2_shear,
            label="d2-3",
            family="negative_diagonal",
        ),
        CellEdge(
            6,
            7,
            positive_diagonal_section,
            diagonal_axial_eccentricity,
            shear_eccentricity=diagonal_shear_eccentricity,
            label="d1-3",
            family="positive_diagonal",
        ),
        CellEdge(
            8,
            7,
            e1_section,
            e1_axial_eccentricity,
            shear_eccentricity=e1_shear_eccentricity,
            label="e1-3",
            family="e1",
        ),
        CellEdge(
            8,
            9,
            diagonal_2,
            diagonal_2_axial,
            shear_eccentricity=diagonal_2_shear,
            label="d2-4",
            family="negative_diagonal",
        ),
        CellEdge(
            10,
            9,
            positive_diagonal_section,
            diagonal_axial_eccentricity,
            shear_eccentricity=diagonal_shear_eccentricity,
            label="d1-4",
            family="positive_diagonal",
        ),
        CellEdge(
            10,
            11,
            e1_section,
            e1_axial_eccentricity,
            shear_eccentricity=e1_shear_eccentricity,
            label="e1-4",
            family="e1",
        ),
    )
    return graph_unit_cell(
        area=4.0 * b * h / 3.0,
        skin=skin,
        nodes=nodes,
        edges=edges,
        repeat_vectors=(CellVector(b, 0.0), CellVector(0.0, 4.0 * h / 3.0)),
        boundary=tuple(range(12)),
        frame=frame,
        convention=convention,
        metadata={"source": "star_cell", "e1_pitch": b, "e2_pitch": h},
    )


def equilateral_star_cell(
    *,
    skin: ABDStiffness,
    member_section: BeamSection,
    side_length: float,
    axial_eccentricity: float,
    shear_eccentricity: float | None = None,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member equilateral star-cell case.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all star-cell members.
        side_length: Positive equilateral-triangle side length.
        axial_eccentricity: Signed effective offset for axial response along ``+n``.
        shear_eccentricity: Optional signed effective offset for in-plane shear.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical equilateral star-cell grid.

    Raises:
        ValueError: If side length, eccentricity, frame, or convention
            validation
            fails.
    """

    p = positive_number(side_length, name="side_length")
    return star_cell(
        skin=skin,
        e1_section=member_section,
        positive_diagonal_section=member_section,
        e1_pitch=p,
        e2_pitch=np.sqrt(3.0) * p / 2.0,
        e1_axial_eccentricity=axial_eccentricity,
        diagonal_axial_eccentricity=axial_eccentricity,
        e1_shear_eccentricity=shear_eccentricity,
        diagonal_shear_eccentricity=shear_eccentricity,
        frame=frame,
        convention=convention,
    )


def _sandwich_face_skin(
    *,
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_to_reference: float,
    top_face_to_reference: float,
    source: str,
) -> ABDStiffness:
    return superpose_abd_stiffnesses(
        shift_reference_surface(bottom_face, bottom_face_to_reference),
        shift_reference_surface(top_face, top_face_to_reference),
        metadata={
            "source": source,
            "bottom_face_to_reference": float(bottom_face_to_reference),
            "top_face_to_reference": float(top_face_to_reference),
        },
    )


def sandwich_orthogrid_core_cell(
    *,
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_to_reference: float,
    top_face_to_reference: float,
    e1_section: BeamSection,
    e2_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    core_axial_eccentricity: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_to_reference: Signed shift from the bottom-face reference
            surface to the sandwich reference surface. This is the negative of
            Nemeth's bottom-face eccentricity.
        top_face_to_reference: Signed shift from the top-face reference surface
            to the sandwich reference surface. This is the negative of Nemeth's
            top-face eccentricity.
        e1_section: Section stiffness for core members along local ``e1``.
        e2_section: Section stiffness for core members along local ``e2``.
        e1_pitch: Core repeat span along local ``e1``.
        e2_pitch: Core repeat span along local ``e2``.
        core_axial_eccentricity: Signed offset from the sandwich reference
            surface to the core centroid along ``+n``. The default ``0.0``
            is Nemeth's choice: the reference surface sits at the core
            midplane. Set it whenever the face shifts above point at a
            different reference surface, or the core is not centered on it.
        frame: Optional cell frame. Defaults to the combined face stiffness
            frame.
        convention: Optional strain convention. Defaults to the combined face
            stiffness convention.

    Returns:
        Canonical orthogrid-core sandwich unit cell.

    Raises:
        ValueError: If shifts, dimensions, faces, frame, or convention validation
            fails.
    """

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_to_reference=bottom_face_to_reference,
        top_face_to_reference=top_face_to_reference,
        source="sandwich_orthogrid_core_faces",
    )
    return orthogrid_cell(
        skin=skin,
        e1_section=e1_section,
        e2_section=e2_section,
        e1_pitch=e1_pitch,
        e2_pitch=e2_pitch,
        e1_axial_eccentricity=core_axial_eccentricity,
        e2_axial_eccentricity=core_axial_eccentricity,
        frame=frame,
        convention=convention,
    )


def sandwich_hexagonal_core_cell(
    *,
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_to_reference: float,
    top_face_to_reference: float,
    e2_section: BeamSection,
    diagonal_section: BeamSection,
    e1_half_pitch: float,
    diagonal_e2_rise: float,
    e2_member_length: float,
    core_axial_eccentricity: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a hexagonal-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_to_reference: Signed bottom-face-to-sandwich reference shift.
        top_face_to_reference: Signed top-face-to-sandwich reference shift.
        e2_section: Section stiffness for core members along local ``e2``.
        diagonal_section: Section stiffness for core diagonal members.
        e1_half_pitch: Nemeth's horizontal construction dimension ``a``.
        diagonal_e2_rise: Nemeth's diagonal rise ``b``.
        e2_member_length: Nemeth's vertical member length ``c``.
        core_axial_eccentricity: Signed offset from the sandwich reference
            surface to the core centroid along ``+n``. The default ``0.0``
            is Nemeth's choice: the reference surface sits at the core
            midplane. Set it whenever the face shifts above point at a
            different reference surface, or the core is not centered on it.
        frame: Optional cell frame. Defaults to the combined face stiffness
            frame.
        convention: Optional strain convention. Defaults to the combined face
            stiffness convention.

    Returns:
        Canonical hexagonal-core sandwich unit cell.

    Raises:
        ValueError: If shifts, dimensions, faces, frame, or convention
            validation fails.
    """

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_to_reference=bottom_face_to_reference,
        top_face_to_reference=top_face_to_reference,
        source="sandwich_hexagonal_core_faces",
    )
    return hexagonal_grid_cell(
        skin=skin,
        e2_section=e2_section,
        positive_diagonal_section=diagonal_section,
        e1_half_pitch=e1_half_pitch,
        diagonal_e2_rise=diagonal_e2_rise,
        e2_member_length=e2_member_length,
        e2_axial_eccentricity=core_axial_eccentricity,
        diagonal_axial_eccentricity=core_axial_eccentricity,
        frame=frame,
        convention=convention,
    )


def sandwich_star_core_cell(
    *,
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_to_reference: float,
    top_face_to_reference: float,
    e1_section: BeamSection,
    diagonal_section: BeamSection,
    e1_pitch: float,
    e2_pitch: float,
    core_axial_eccentricity: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a star-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_to_reference: Signed bottom-face-to-sandwich reference shift.
        top_face_to_reference: Signed top-face-to-sandwich reference shift.
        e1_section: Section stiffness for core members along local ``e1``.
        diagonal_section: Section stiffness for core diagonal members.
        e1_pitch: Nemeth's star base dimension ``B``.
        e2_pitch: Nemeth's star height dimension ``H``.
        core_axial_eccentricity: Signed offset from the sandwich reference
            surface to the core centroid along ``+n``. The default ``0.0``
            is Nemeth's choice: the reference surface sits at the core
            midplane. Set it whenever the face shifts above point at a
            different reference surface, or the core is not centered on it.
        frame: Optional cell frame. Defaults to the combined face stiffness
            frame.
        convention: Optional strain convention. Defaults to the combined face
            stiffness convention.

    Returns:
        Canonical star-core sandwich unit cell.

    Raises:
        ValueError: If shifts, dimensions, faces, frame, or convention
            validation fails.
    """

    skin = _sandwich_face_skin(
        bottom_face=bottom_face,
        top_face=top_face,
        bottom_face_to_reference=bottom_face_to_reference,
        top_face_to_reference=top_face_to_reference,
        source="sandwich_star_core_faces",
    )
    return star_cell(
        skin=skin,
        e1_section=e1_section,
        positive_diagonal_section=diagonal_section,
        e1_pitch=e1_pitch,
        e2_pitch=e2_pitch,
        e1_axial_eccentricity=core_axial_eccentricity,
        diagonal_axial_eccentricity=core_axial_eccentricity,
        frame=frame,
        convention=convention,
    )


__all__ = [
    "BeamMember",
    "CanonicalUnitCell",
    "CellEdge",
    "CellGeometry",
    "CellGeometryEdge",
    "CellNode",
    "CellSegment",
    "CellVector",
    "StiffenerFamily",
    "braced_orthogrid_cell",
    "diamond_cell",
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
