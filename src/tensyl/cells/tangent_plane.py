"""Canonical tangent-plane stiffener-cell value objects and constructors."""

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

    ``angle_rad`` is measured from local ``e1`` toward ``e2``. ``eccentricity``
    is the signed distance from the reference surface to the member
    centroid along ``+n``.

    Attributes:
        section: Centroidal beam stiffness for the member.
        length: Positive member length inside the repeated cell.
        angle_rad: Member angle measured from local ``e1`` toward ``e2``.
        eccentricity: Signed centroid offset from the reference surface along
            ``+n``.
        multiplicity: Positive count or density multiplier for identical
            members represented by this object.
        label: Optional member label for diagnostics and metadata.
    """

    section: BeamSection
    length: float
    angle_rad: float
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "length", positive_number(self.length, name="length"))
        object.__setattr__(self, "angle_rad", finite_number(self.angle_rad, name="angle_rad"))
        object.__setattr__(
            self, "eccentricity", finite_number(self.eccentricity, name="eccentricity")
        )
        object.__setattr__(
            self, "multiplicity", positive_number(self.multiplicity, name="multiplicity")
        )


@dataclass(frozen=True, slots=True)
class CellNode:
    """A node in a local tangent-plane graph cell.

    Attributes:
        x: Node coordinate along local ``e1``.
        y: Node coordinate along local ``e2``.
        label: Optional node label for caller provenance.
    """

    x: float
    y: float
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", finite_number(self.x, name="x"))
        object.__setattr__(self, "y", finite_number(self.y, name="y"))


@dataclass(frozen=True, slots=True)
class CellEdge:
    """A beam edge in a local tangent-plane graph cell.

    Attributes:
        start: Index of the start node in the node tuple.
        end: Index of the end node in the node tuple.
        section: Centroidal beam stiffness for the edge.
        eccentricity: Signed centroid offset from the reference surface along
            ``+n``.
        multiplicity: Positive count or density multiplier.
        label: Optional edge label for diagnostics and metadata.
    """

    start: int
    end: int
    section: BeamSection
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "eccentricity", finite_number(self.eccentricity, name="eccentricity")
        )
        object.__setattr__(
            self, "multiplicity", positive_number(self.multiplicity, name="multiplicity")
        )


@dataclass(frozen=True, slots=True)
class CanonicalUnitCell:
    """Canonical tangent-plane cell consumed by tangent-plane homogenizers.

    ``area`` is the repeated tangent-plane area represented by ``members``.
    The cell frame and strain convention must match the skin ABD stiffness.

    Attributes:
        area: Positive repeated tangent-plane area.
        skin: Baseline skin stiffness for the cell.
        members: One or more straight beam members in the local tangent plane.
        frame: Local frame shared by the skin and members.
        convention: Generalized strain convention shared by the skin and cell.
        metadata: Read-only cell provenance.
    """

    area: float
    skin: ABDStiffness
    members: tuple[BeamMember, ...]
    frame: Frame2D = DEFAULT_FRAME
    convention: StrainConvention = DEFAULT_STRAIN_CONVENTION
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
        object.__setattr__(self, "members", members)
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True, slots=True)
class StiffenerFamily:
    """Continuous straight stiffener-family input for direct EC homogenization.

    ``spacing`` is the family pitch normal to the member direction.
    ``eccentricity`` uses the same signed ``+n`` convention as ``BeamMember``.

    Attributes:
        section: Centroidal beam stiffness for the family.
        spacing: Positive family pitch normal to the member direction.
        angle_rad: Family angle measured from local ``e1`` toward ``e2``.
        eccentricity: Signed centroid offset from the reference surface along
            ``+n``.
        multiplicity: Positive family multiplier.
        label: Optional family label for diagnostics and metadata.
    """

    section: BeamSection
    spacing: float
    angle_rad: float
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "spacing", positive_number(self.spacing, name="spacing"))
        object.__setattr__(self, "angle_rad", finite_number(self.angle_rad, name="angle_rad"))
        object.__setattr__(
            self, "eccentricity", finite_number(self.eccentricity, name="eccentricity")
        )
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
    eccentricity: float,
    opposite_eccentricity: float | None,
    multiplicity: float = 1.0,
    positive_label: str,
    negative_label: str,
) -> tuple[BeamMember, BeamMember]:
    # Several Nemeth-style cells use mirrored oblique members. Keep the pairing
    # in one helper so opposite material/eccentricity overrides stay symmetric.
    return (
        BeamMember(
            section,
            length,
            angle_rad,
            eccentricity,
            multiplicity=multiplicity,
            label=positive_label,
        ),
        BeamMember(
            _same_or_second(section, opposite_section),
            length,
            -angle_rad,
            _same_or_value(eccentricity, opposite_eccentricity),
            multiplicity=multiplicity,
            label=negative_label,
        ),
    )


def graph_unit_cell(
    *,
    area: float,
    skin: ABDStiffness,
    nodes: tuple[CellNode, ...],
    edges: tuple[CellEdge, ...],
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    metadata: dict[str, Any] | MappingProxyType[str, Any] | None = None,
) -> CanonicalUnitCell:
    """Convert a local graph cell into the canonical member representation.

    Node coordinates are local tangent-plane coordinates in the same length
    unit used by ``area``.

    Args:
        area: Positive repeated-cell area.
        skin: Baseline skin stiffness.
        nodes: Graph nodes in local tangent-plane coordinates.
        edges: Beam edges connecting nodes by index.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.
        metadata: Optional metadata merged into the cell provenance.

    Returns:
        Canonical unit cell with graph edges converted to length and angle.

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
        dx = end.x - start.x
        dy = end.y - start.y
        # Graph input is only a convenience layer. The canonical homogenizer
        # consumes length and angle, so all graph geometry is collapsed here.
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
    skin: ABDStiffness,
    member_section: BeamSection,
    spacing: float,
    eccentricity: float,
    angle_rad: float = 0.0,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
    label: str = "unidirectional",
) -> CanonicalUnitCell:
    """Create a one-family canonical strip cell.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for the repeated family.
        spacing: Positive pitch normal to the family direction.
        eccentricity: Signed family centroid offset along ``+n``.
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
    # continuous family density used by the direct EC path.
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
    skin: ABDStiffness,
    stringer_section: BeamSection,
    rib_section: BeamSection,
    stringer_spacing: float,
    rib_spacing: float,
    stringer_eccentricity: float,
    rib_eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid cell with one stringer and one rib family.

    Stringers run along local ``e1`` and ribs run along local ``e2``. The two
    eccentricity inputs are signed centroid offsets along ``+n``.

    Args:
        skin: Baseline skin stiffness.
        stringer_section: Section stiffness for local ``e1`` members.
        rib_section: Section stiffness for local ``e2`` members.
        stringer_spacing: Positive pitch between stringers.
        rib_spacing: Positive pitch between ribs.
        stringer_eccentricity: Signed stringer centroid offset along ``+n``.
        rib_eccentricity: Signed rib centroid offset along ``+n``.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical orthogrid unit cell.

    Raises:
        ValueError: If spacing, eccentricity, frame, or convention validation
            fails.
    """

    ds = positive_number(stringer_spacing, name="stringer_spacing")
    dr = positive_number(rib_spacing, name="rib_spacing")
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # Each member spans the opposite cell pitch, so length / area reduces to
    # the expected 1 / family spacing for stringers and ribs.
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
    skin: ABDStiffness,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an equilateral isogrid cell with three identical families.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all three families.
        pitch: Positive triangle side length.
        eccentricity: Signed member centroid offset along ``+n``.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical cell with members at 0 and +/-60 degrees.

    Raises:
        ValueError: If pitch, eccentricity, frame, or convention validation
            fails.
    """

    p = positive_number(pitch, name="pitch")
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
    skin: ABDStiffness,
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
    """Create a braced orthogrid with alternating or crossed braces.

    Args:
        skin: Baseline skin stiffness.
        stringer_section: Section stiffness for local ``e1`` members.
        rib_section: Section stiffness for local ``e2`` members.
        brace_section: Section stiffness for positive diagonal braces.
        stringer_spacing: Positive pitch between stringers.
        rib_spacing: Positive pitch between ribs.
        stringer_eccentricity: Signed stringer centroid offset along ``+n``.
        rib_eccentricity: Signed rib centroid offset along ``+n``.
        brace_eccentricity: Signed positive-brace centroid offset along ``+n``.
        opposite_brace_section: Optional section for the negative diagonal.
        opposite_brace_eccentricity: Optional eccentricity for the negative
            diagonal.
        brace_pattern: ``"double"`` for crossed braces or ``"single"`` for an
            averaged alternating diagonal.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical braced orthogrid unit cell.

    Raises:
        ValueError: If spacing is invalid or ``brace_pattern`` is not
            ``"double"`` or ``"single"``.
    """

    ds = positive_number(stringer_spacing, name="stringer_spacing")
    dr = positive_number(rib_spacing, name="rib_spacing")
    if brace_pattern not in {"double", "single"}:
        msg = "brace_pattern must be 'double' or 'single'."
        raise ValueError(msg)
    brace_multiplier = 1.0 if brace_pattern == "double" else 0.5
    # A single alternating diagonal contributes half of a crossed-brace pair in
    # an averaged repeated cell.
    diagonal_length = float(np.hypot(ds, dr))
    diagonal_angle = float(np.arctan2(dr, ds))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    return CanonicalUnitCell(
        area=ds * dr,
        skin=skin,
        members=(
            BeamMember(stringer_section, dr, 0.0, stringer_eccentricity, label="stringer"),
            BeamMember(rib_section, ds, np.pi / 2.0, rib_eccentricity, label="rib"),
            *_paired_oblique_members(
                section=brace_section,
                opposite_section=opposite_brace_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                eccentricity=brace_eccentricity,
                opposite_eccentricity=opposite_brace_eccentricity,
                multiplicity=brace_multiplier,
                positive_label="+brace",
                negative_label="-brace",
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
    skin: ABDStiffness,
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
    """Create an isosceles-triangle grid cell.

    Args:
        skin: Baseline skin stiffness.
        stringer_section: Section stiffness for the base member.
        diagonal_section: Section stiffness for the positive diagonal.
        base: Positive triangle base length.
        height: Positive triangle height.
        stringer_eccentricity: Signed base-member centroid offset along ``+n``.
        diagonal_eccentricity: Signed positive-diagonal centroid offset along
            ``+n``.
        opposite_diagonal_section: Optional section for the negative diagonal.
        opposite_diagonal_eccentricity: Optional eccentricity for the negative
            diagonal.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical isosceles-triangle grid unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    b = positive_number(base, name="base")
    h = positive_number(height, name="height")
    diagonal_length = float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(h, 0.5 * b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # The base member plus mirrored diagonals represent one triangular repeat
    # area in the local tangent plane.
    return CanonicalUnitCell(
        area=b * h,
        skin=skin,
        members=(
            BeamMember(stringer_section, b, 0.0, stringer_eccentricity, label="stringer"),
            *_paired_oblique_members(
                section=diagonal_section,
                opposite_section=opposite_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                eccentricity=diagonal_eccentricity,
                opposite_eccentricity=opposite_diagonal_eccentricity,
                positive_label="+diagonal",
                negative_label="-diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": "isosceles_triangle_grid", "base": b, "height": h},
    )


def kagome_cell(
    *,
    skin: ABDStiffness,
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
    """Create a Kagome grid cell.

    Args:
        skin: Baseline skin stiffness.
        stringer_section: Section stiffness for horizontal members.
        diagonal_section: Section stiffness for the positive diagonal family.
        base: Positive base length of the repeat geometry.
        height: Positive height of the repeat geometry.
        stringer_eccentricity: Signed stringer centroid offset along ``+n``.
        diagonal_eccentricity: Signed positive-diagonal centroid offset along
            ``+n``.
        opposite_diagonal_section: Optional section for the negative diagonal.
        opposite_diagonal_eccentricity: Optional eccentricity for the negative
            diagonal.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical Kagome unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    b = positive_number(base, name="base")
    h = positive_number(height, name="height")
    diagonal_length = 2.0 * float(np.hypot(0.5 * b, h))
    diagonal_angle = float(np.arctan2(2.0 * h, b))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # The doubled stringer multiplicity reflects two horizontal members in the
    # Kagome repeat area without duplicating identical BeamMember objects.
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
            *_paired_oblique_members(
                section=diagonal_section,
                opposite_section=opposite_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                eccentricity=diagonal_eccentricity,
                opposite_eccentricity=opposite_diagonal_eccentricity,
                positive_label="+diagonal",
                negative_label="-diagonal",
            ),
        ),
        frame=cell_frame,
        convention=cell_convention,
        metadata={"source": "kagome", "base": b, "height": h},
    )


def hexagonal_grid_cell(
    *,
    skin: ABDStiffness,
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
    """Create a hexagon-shaped grid cell.

    Args:
        skin: Baseline skin stiffness.
        rib_section: Section stiffness for vertical rib members.
        diagonal_section: Section stiffness for positive diagonal members.
        half_width: Positive half-width of the hexagon construction.
        diagonal_rise: Positive rise of the diagonal construction.
        rib_length: Positive vertical rib length.
        rib_eccentricity: Signed rib centroid offset along ``+n``.
        diagonal_eccentricity: Signed positive-diagonal centroid offset along
            ``+n``.
        opposite_diagonal_section: Optional section for the negative diagonal.
        opposite_diagonal_eccentricity: Optional eccentricity for the negative
            diagonal.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical hexagonal-grid unit cell.

    Raises:
        ValueError: If dimensions, eccentricities, frame, or convention
            validation fails.
    """

    a = positive_number(half_width, name="half_width")
    b = positive_number(diagonal_rise, name="diagonal_rise")
    c = positive_number(rib_length, name="rib_length")
    diagonal_length = 0.5 * float(np.hypot(a, b))
    diagonal_angle = float(np.arctan2(b, a))
    cell_frame, cell_convention = _cell_frame_and_convention(skin, frame, convention)
    # The half-width/rise/rib-length parameters follow the legacy Nemeth cell
    # sketch; the metadata preserves those construction dimensions.
    return CanonicalUnitCell(
        area=2.0 * a * (b + c),
        skin=skin,
        members=(
            *_paired_oblique_members(
                section=diagonal_section,
                opposite_section=opposite_diagonal_section,
                length=diagonal_length,
                angle_rad=diagonal_angle,
                eccentricity=diagonal_eccentricity,
                opposite_eccentricity=opposite_diagonal_eccentricity,
                multiplicity=2.0,
                positive_label="+diagonal",
                negative_label="-diagonal",
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
    skin: ABDStiffness,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member regular hexagonal-grid case.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all grid members.
        pitch: Positive regular-hexagon pitch.
        eccentricity: Signed member centroid offset along ``+n``.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical regular hexagonal-grid unit cell.

    Raises:
        ValueError: If pitch, eccentricity, frame, or convention validation
            fails.
    """

    p = positive_number(pitch, name="pitch")
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
    skin: ABDStiffness,
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
    """Create an isosceles star-cell grid.

    Args:
        skin: Baseline skin stiffness.
        stringer_section: Section stiffness for short horizontal members.
        diagonal_section: Section stiffness for positive diagonal members.
        base: Positive star-cell base dimension.
        height: Positive star-cell height dimension.
        stringer_eccentricity: Signed stringer centroid offset along ``+n``.
        diagonal_eccentricity: Signed positive-diagonal centroid offset along
            ``+n``.
        opposite_diagonal_section: Optional section for the negative diagonal.
        opposite_diagonal_eccentricity: Optional eccentricity for the negative
            diagonal.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical star-cell grid.

    Raises:
        ValueError: If dimensions, eccentricities, graph connectivity, frame,
            or convention validation fails.
    """

    b = positive_number(base, name="base")
    h = positive_number(height, name="height")
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
    skin: ABDStiffness,
    member_section: BeamSection,
    pitch: float,
    eccentricity: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create the identical-member equilateral star-cell case.

    Args:
        skin: Baseline skin stiffness.
        member_section: Section stiffness for all star-cell members.
        pitch: Positive equilateral base pitch.
        eccentricity: Signed member centroid offset along ``+n``.
        frame: Optional cell frame. Defaults to ``skin.frame``.
        convention: Optional strain convention. Defaults to
            ``skin.convention``.

    Returns:
        Canonical equilateral star-cell grid.

    Raises:
        ValueError: If pitch, eccentricity, frame, or convention validation
            fails.
    """

    p = positive_number(pitch, name="pitch")
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
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_offset: float,
    top_face_offset: float,
    source: str,
) -> ABDStiffness:
    return superpose_abd_stiffnesses(
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
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_offset: float,
    top_face_offset: float,
    stringer_section: BeamSection,
    rib_section: BeamSection,
    stringer_spacing: float,
    rib_spacing: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create an orthogrid-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_offset: Signed shift from bottom-face reference surface to
            the sandwich reference surface.
        top_face_offset: Signed shift from top-face reference surface to the
            sandwich reference surface.
        stringer_section: Section stiffness for the core stringer family.
        rib_section: Section stiffness for the core rib family.
        stringer_spacing: Positive pitch between stringers.
        rib_spacing: Positive pitch between ribs.
        frame: Optional cell frame. Defaults to the combined face stiffness
            frame.
        convention: Optional strain convention. Defaults to the combined face
            stiffness convention.

    Returns:
        Canonical orthogrid-core sandwich unit cell.

    Raises:
        ValueError: If shifts, spacings, faces, frame, or convention validation
            fails.
    """

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
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
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
    """Create a hexagonal-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_offset: Signed shift from bottom-face reference surface to
            the sandwich reference surface.
        top_face_offset: Signed shift from top-face reference surface to the
            sandwich reference surface.
        rib_section: Section stiffness for core rib members.
        diagonal_section: Section stiffness for core diagonal members.
        half_width: Positive half-width of the hexagon construction.
        diagonal_rise: Positive rise of the diagonal construction.
        rib_length: Positive vertical rib length.
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
    bottom_face: ABDStiffness,
    top_face: ABDStiffness,
    bottom_face_offset: float,
    top_face_offset: float,
    stringer_section: BeamSection,
    diagonal_section: BeamSection,
    base: float,
    height: float,
    frame: Frame2D | None = None,
    convention: StrainConvention | None = None,
) -> CanonicalUnitCell:
    """Create a star-core sandwich cell with shifted faces.

    Args:
        bottom_face: Bottom face-sheet stiffness about its own reference
            surface.
        top_face: Top face-sheet stiffness about its own reference surface.
        bottom_face_offset: Signed shift from bottom-face reference surface to
            the sandwich reference surface.
        top_face_offset: Signed shift from top-face reference surface to the
            sandwich reference surface.
        stringer_section: Section stiffness for core stringer members.
        diagonal_section: Section stiffness for core diagonal members.
        base: Positive star-cell base dimension.
        height: Positive star-cell height dimension.
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
