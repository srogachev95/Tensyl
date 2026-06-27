"""Canonical Level 1 stiffener-cell value objects and constructors."""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

import numpy as np

from tensyl.constitutive import LinearABDWall
from tensyl.conventions import DEFAULT_FRAME, DEFAULT_STRAIN_CONVENTION, Frame2D, StrainConvention
from tensyl.sections import BeamSection


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
class CanonicalUnitCell:
    """Canonical tangent-plane cell consumed by Level 1 homogenizers."""

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
    cell_frame = skin.frame if frame is None else frame
    cell_convention = skin.convention if convention is None else convention
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
    cell_frame = skin.frame if frame is None else frame
    cell_convention = skin.convention if convention is None else convention
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
    cell_frame = skin.frame if frame is None else frame
    cell_convention = skin.convention if convention is None else convention
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


__all__ = [
    "BeamMember",
    "CanonicalUnitCell",
    "StiffenerFamily",
    "equilateral_isogrid_cell",
    "orthogrid_cell",
    "unidirectional_cell",
]
