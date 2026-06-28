"""Thin-wall stiffener section geometry helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from tensyl.core._validation import (
    finite_number,
    optional_positive_number,
    positive_number,
    readonly_mapping,
)
from tensyl.materials import IsotropicMaterial
from tensyl.sections.beam import BeamSection


def _finite(value: float, *, name: str) -> float:
    return finite_number(value, name=name)


def _positive(value: float, *, name: str) -> float:
    return positive_number(value, name=name)


def _optional_positive(value: float | None, *, name: str) -> float | None:
    return optional_positive_number(value, name=name)


@dataclass(frozen=True, slots=True)
class ThinWallSegment:
    """A rectangular wall segment in member-local section coordinates.

    ``start_*`` and ``end_*`` are the segment midline endpoints in member-local
    ``(y, z)`` coordinates. ``thickness`` is measured normal to that midline in
    the same coordinate plane. For section constructors, ``z = 0`` is a
    construction datum, not automatically the skin mid-surface.
    """

    start_y: float
    start_z: float
    end_y: float
    end_z: float
    thickness: float
    label: str = ""

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_y", _finite(self.start_y, name="start_y"))
        object.__setattr__(self, "start_z", _finite(self.start_z, name="start_z"))
        object.__setattr__(self, "end_y", _finite(self.end_y, name="end_y"))
        object.__setattr__(self, "end_z", _finite(self.end_z, name="end_z"))
        object.__setattr__(self, "thickness", _positive(self.thickness, name="thickness"))
        if self.length <= 0.0:
            msg = "segment length must be finite and positive."
            raise ValueError(msg)

    @property
    def length(self) -> float:
        """Segment midline length."""

        return float(np.hypot(self.end_y - self.start_y, self.end_z - self.start_z))


@dataclass(frozen=True, slots=True)
class SectionProperties:
    """Centroidal geometric properties of a thin-wall section."""

    area: float
    centroid_y: float
    centroid_z: float
    Iy: float
    Iz: float
    Iyz: float
    J: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "area", _positive(self.area, name="area"))
        object.__setattr__(self, "centroid_y", _finite(self.centroid_y, name="centroid_y"))
        object.__setattr__(self, "centroid_z", _finite(self.centroid_z, name="centroid_z"))
        object.__setattr__(self, "Iy", _positive(self.Iy, name="Iy"))
        object.__setattr__(self, "Iz", _positive(self.Iz, name="Iz"))
        object.__setattr__(self, "Iyz", _finite(self.Iyz, name="Iyz"))
        object.__setattr__(self, "J", _positive(self.J, name="J"))
        if self.Iy * self.Iz - self.Iyz**2 <= 0.0:
            msg = "section inertia block must be positive definite."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ThinWallSection:
    """A geometry-derived isotropic thin-wall stiffener section."""

    material: IsotropicMaterial
    segments: tuple[ThinWallSegment, ...]
    shear_correction_y: float | None = None
    shear_correction_z: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    properties: SectionProperties = field(init=False)
    section: BeamSection = field(init=False)

    def __post_init__(self) -> None:
        segments = tuple(self.segments)
        if not segments:
            msg = "ThinWallSection requires at least one segment."
            raise ValueError(msg)
        shear_correction_y = _optional_positive(
            self.shear_correction_y,
            name="shear_correction_y",
        )
        shear_correction_z = _optional_positive(
            self.shear_correction_z,
            name="shear_correction_z",
        )
        properties = _section_properties(segments)
        metadata = {"source": "thin_wall_section"}
        metadata.update(self.metadata)
        # Convert geometry to centroidal stiffness products because the
        # homogenizer consumes BeamSection values, not raw wall coordinates.
        # Optional shear corrections are deliberately opt-in. Missing
        # corrections become None and later appear as homogenizer assumptions
        # instead of guessed stiffness.
        section = BeamSection(
            EA=self.material.E * properties.area,
            EIy=self.material.E * properties.Iy,
            EIz=self.material.E * properties.Iz,
            GJ=self.material.G * properties.J,
            kGAy=(
                shear_correction_y * self.material.G * properties.area
                if shear_correction_y is not None
                else None
            ),
            kGAz=(
                shear_correction_z * self.material.G * properties.area
                if shear_correction_z is not None
                else None
            ),
            EIyz=self.material.E * properties.Iyz,
            metadata=metadata,
        )
        object.__setattr__(self, "segments", segments)
        object.__setattr__(self, "shear_correction_y", shear_correction_y)
        object.__setattr__(self, "shear_correction_z", shear_correction_z)
        object.__setattr__(self, "metadata", readonly_mapping(metadata))
        object.__setattr__(self, "properties", properties)
        object.__setattr__(self, "section", section)

    @property
    def centroid_y(self) -> float:
        """Centroid ``y`` coordinate."""

        return self.properties.centroid_y

    @property
    def centroid_z(self) -> float:
        """Centroid ``z`` coordinate, commonly used as member eccentricity."""

        return self.properties.centroid_z


def _section_properties(segments: tuple[ThinWallSegment, ...]) -> SectionProperties:
    # First pass finds the centroid from thin rectangular segment midline areas.
    area = 0.0
    first_y = 0.0
    first_z = 0.0
    for segment in segments:
        segment_area = segment.length * segment.thickness
        mid_y = 0.5 * (segment.start_y + segment.end_y)
        mid_z = 0.5 * (segment.start_z + segment.end_z)
        area += segment_area
        first_y += segment_area * mid_y
        first_z += segment_area * mid_z
    centroid_y = first_y / area
    centroid_z = first_z / area

    iy = 0.0
    iz = 0.0
    iyz = 0.0
    torsion = 0.0
    for segment in segments:
        length = segment.length
        thickness = segment.thickness
        segment_area = length * thickness
        mid_y = 0.5 * (segment.start_y + segment.end_y)
        mid_z = 0.5 * (segment.start_z + segment.end_z)
        unit_y = (segment.end_y - segment.start_y) / length
        unit_z = (segment.end_z - segment.start_z) / length
        normal_y = -unit_z
        normal_z = unit_y
        # Segment inertia is computed in its local along/across axes and then
        # rotated into the member-local y/z axes.
        along = length**3 * thickness / 12.0
        across = length * thickness**3 / 12.0
        m_yy = along * unit_y**2 + across * normal_y**2
        m_zz = along * unit_z**2 + across * normal_z**2
        m_yz = along * unit_y * unit_z + across * normal_y * normal_z
        dy = mid_y - centroid_y
        dz = mid_z - centroid_z
        # Shift every segment from its own centroid to the section centroid.
        iz += m_yy + segment_area * dy**2
        iy += m_zz + segment_area * dz**2
        iyz += m_yz + segment_area * dy * dz
        # Open-section St Venant torsion approximation. Closed-cell torsion and
        # restrained warping belong in an external section solver for now.
        torsion += length * thickness**3 / 3.0

    return SectionProperties(
        area=area,
        centroid_y=centroid_y,
        centroid_z=centroid_z,
        Iy=iy,
        Iz=iz,
        Iyz=iyz,
        J=torsion,
    )


def thin_wall_section(
    *,
    material: IsotropicMaterial,
    segments: tuple[ThinWallSegment, ...],
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build an isotropic thin-wall section from rectangular wall segments.

    Segment coordinates use the member-local ``(y, z)`` section plane. The
    returned ``centroid_z`` is measured from the same ``z = 0`` construction
    datum used by the supplied segments; shift it before using it as a member
    eccentricity when the wall reference surface is somewhere else.
    """

    return ThinWallSection(
        material=material,
        segments=segments,
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata={} if metadata is None else metadata,
    )


def blade_section(
    *,
    material: IsotropicMaterial,
    height: float,
    thickness: float,
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build a vertical blade stiffener rooted at ``z = 0``.

    The blade web rises in ``+z`` from the construction datum. If that datum is
    the skin outer face and the wall reference surface is the skin mid-surface,
    use ``0.5 * skin_thickness + section.centroid_z`` as member eccentricity.
    """

    return thin_wall_section(
        material=material,
        segments=(ThinWallSegment(0.0, 0.0, 0.0, _positive(height, name="height"), thickness),),
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata=_metadata("blade", metadata),
    )


def tee_section(
    *,
    material: IsotropicMaterial,
    web_height: float,
    web_thickness: float,
    flange_width: float,
    flange_thickness: float,
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build a tee stiffener with a vertical web and top flange.

    The web root is at ``z = 0`` and the flange sits above the web in ``+z``.
    """

    web_height = _positive(web_height, name="web_height")
    flange_width = _positive(flange_width, name="flange_width")
    flange_thickness = _positive(flange_thickness, name="flange_thickness")
    return thin_wall_section(
        material=material,
        segments=(
            ThinWallSegment(0.0, 0.0, 0.0, web_height, web_thickness, label="web"),
            ThinWallSegment(
                -0.5 * flange_width,
                web_height + 0.5 * flange_thickness,
                0.5 * flange_width,
                web_height + 0.5 * flange_thickness,
                flange_thickness,
                label="flange",
            ),
        ),
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata=_metadata("tee", metadata),
    )


def zee_section(
    *,
    material: IsotropicMaterial,
    web_height: float,
    web_thickness: float,
    top_flange_width: float,
    bottom_flange_width: float,
    flange_thickness: float,
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build a zee stiffener with opposite top and bottom flanges.

    The lower flange sits at the ``z = 0`` datum and extends toward negative
    ``y``. The upper flange sits above the web and extends toward positive
    ``y``.
    """

    web_height = _positive(web_height, name="web_height")
    top_flange_width = _positive(top_flange_width, name="top_flange_width")
    bottom_flange_width = _positive(bottom_flange_width, name="bottom_flange_width")
    flange_thickness = _positive(flange_thickness, name="flange_thickness")
    return thin_wall_section(
        material=material,
        segments=(
            ThinWallSegment(
                -bottom_flange_width,
                0.5 * flange_thickness,
                0.0,
                0.5 * flange_thickness,
                flange_thickness,
                label="bottom_flange",
            ),
            ThinWallSegment(
                0.0,
                flange_thickness,
                0.0,
                flange_thickness + web_height,
                web_thickness,
                label="web",
            ),
            ThinWallSegment(
                0.0,
                flange_thickness + web_height + 0.5 * flange_thickness,
                top_flange_width,
                flange_thickness + web_height + 0.5 * flange_thickness,
                flange_thickness,
                label="top_flange",
            ),
        ),
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata=_metadata("zee", metadata),
    )


def channel_section(
    *,
    material: IsotropicMaterial,
    web_height: float,
    web_thickness: float,
    flange_width: float,
    flange_thickness: float,
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build a channel stiffener with same-side top and bottom flanges.

    Both flanges extend toward positive ``y``. The lower flange sits at the
    ``z = 0`` construction datum.
    """

    web_height = _positive(web_height, name="web_height")
    flange_width = _positive(flange_width, name="flange_width")
    flange_thickness = _positive(flange_thickness, name="flange_thickness")
    return thin_wall_section(
        material=material,
        segments=(
            ThinWallSegment(
                0.0,
                0.5 * flange_thickness,
                flange_width,
                0.5 * flange_thickness,
                flange_thickness,
                label="bottom_flange",
            ),
            ThinWallSegment(
                0.0,
                flange_thickness,
                0.0,
                flange_thickness + web_height,
                web_thickness,
                label="web",
            ),
            ThinWallSegment(
                0.0,
                flange_thickness + web_height + 0.5 * flange_thickness,
                flange_width,
                flange_thickness + web_height + 0.5 * flange_thickness,
                flange_thickness,
                label="top_flange",
            ),
        ),
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata=_metadata("channel", metadata),
    )


def hat_section(
    *,
    material: IsotropicMaterial,
    web_height: float,
    web_thickness: float,
    crown_width: float,
    crown_thickness: float,
    flange_width: float,
    flange_thickness: float,
    shear_correction_y: float | None = None,
    shear_correction_z: float | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> ThinWallSection:
    """Build an open hat stiffener with two webs, crown, and mounting flanges.

    The open hat rises in ``+z``. The mounting flanges sit on the ``z = 0``
    construction datum, so this is the usual external hat orientation rather
    than a hat flipped down into the skin.
    """

    web_height = _positive(web_height, name="web_height")
    crown_width = _positive(crown_width, name="crown_width")
    crown_thickness = _positive(crown_thickness, name="crown_thickness")
    flange_width = _positive(flange_width, name="flange_width")
    flange_thickness = _positive(flange_thickness, name="flange_thickness")
    half_crown = 0.5 * crown_width
    top_z = flange_thickness + web_height
    return thin_wall_section(
        material=material,
        segments=(
            ThinWallSegment(
                -half_crown - flange_width,
                0.5 * flange_thickness,
                -half_crown,
                0.5 * flange_thickness,
                flange_thickness,
                label="left_flange",
            ),
            ThinWallSegment(
                -half_crown,
                flange_thickness,
                -half_crown,
                top_z,
                web_thickness,
                label="left_web",
            ),
            ThinWallSegment(
                -half_crown,
                top_z + 0.5 * crown_thickness,
                half_crown,
                top_z + 0.5 * crown_thickness,
                crown_thickness,
                label="crown",
            ),
            ThinWallSegment(
                half_crown,
                flange_thickness,
                half_crown,
                top_z,
                web_thickness,
                label="right_web",
            ),
            ThinWallSegment(
                half_crown,
                0.5 * flange_thickness,
                half_crown + flange_width,
                0.5 * flange_thickness,
                flange_thickness,
                label="right_flange",
            ),
        ),
        shear_correction_y=shear_correction_y,
        shear_correction_z=shear_correction_z,
        metadata=_metadata("hat", metadata),
    )


def _metadata(kind: str, metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    # Keep the human-facing named constructor in metadata while allowing callers
    # to add project-specific provenance.
    values = {"section_geometry": kind}
    if metadata is not None:
        values.update(metadata)
    return values


__all__ = [
    "SectionProperties",
    "ThinWallSection",
    "ThinWallSegment",
    "blade_section",
    "channel_section",
    "hat_section",
    "tee_section",
    "thin_wall_section",
    "zee_section",
]
