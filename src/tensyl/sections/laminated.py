"""Membrane-equivalent laminated wall strips for uncoupled beam sections."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from tensyl.core.constitutive import ABDStiffness
from tensyl.materials.laminates import Ply, laminate_plate
from tensyl.sections.beam import BeamSection
from tensyl.sections.thin_wall import ThinWallSegment, _RectangularStrip


@dataclass(frozen=True, slots=True)
class LaminatedWallSegment:
    """Wall geometry and an uncoupled laminate aligned along the member.

    Laminate direction 1 is the beam axis; direction 2 follows the wall
    midline. Supply an ABD stiffness or bottom-to-top plies whose total
    thickness matches the geometry. Nonzero B or A16/A26 is refused because
    BeamSection cannot retain those couplings. Local D and As are not used.
    """

    geometry: ThinWallSegment
    laminate: ABDStiffness | tuple[Ply, ...]
    stiffness: ABDStiffness = field(init=False)
    E: float = field(init=False)
    G: float = field(init=False)

    def __post_init__(self) -> None:
        laminate = self.laminate
        if isinstance(laminate, ABDStiffness):
            stiffness = laminate
        else:
            laminate = tuple(laminate)
            if not np.isclose(
                sum(p.thickness for p in laminate), self.geometry.thickness, rtol=1e-12, atol=0
            ):
                msg = "Ply thickness sum must match the wall geometry thickness."
                raise ValueError(msg)
            stiffness = laminate_plate(laminate)
        scale = float(np.max(np.abs(stiffness.A)))
        if (
            np.max(np.abs(stiffness.B)) > 1e-12 * scale * self.geometry.thickness
            or np.max(np.abs(stiffness.A[:2, 2])) > 1e-12 * scale
        ):
            msg = "Laminated wall reduction cannot represent B or membrane-shear coupling."
            raise ValueError(msg)
        try:
            np.linalg.cholesky(stiffness.A)
            compliance = np.linalg.inv(stiffness.A)
        except np.linalg.LinAlgError as exc:
            msg = "Laminated wall requires positive definite membrane stiffness."
            raise ValueError(msg) from exc
        object.__setattr__(self, "laminate", laminate)
        object.__setattr__(self, "stiffness", stiffness)
        object.__setattr__(self, "E", float(1 / (compliance[0, 0] * self.geometry.thickness)))
        object.__setattr__(self, "G", float(1 / (compliance[2, 2] * self.geometry.thickness)))


@dataclass(frozen=True, slots=True)
class LaminatedThinWallSection:
    """Reduce laminated strips to a beam about its stiffness-weighted centroid.

    Uses membrane-equivalent E and G for axial/bending stiffness and open-strip
    torsion. This omits laminate wall bending, warping, and section distortion.
    Shear stiffnesses are left unspecified. Mass is known only if every wall
    provides areal mass. ``centroid_y/z`` locate the elastic centroid, which
    should be used for the member's axial eccentricity.
    """

    segments: tuple[LaminatedWallSegment, ...]
    centroid_y: float = field(init=False)
    centroid_z: float = field(init=False)
    section: BeamSection = field(init=False)

    def __post_init__(self) -> None:
        walls = tuple(self.segments)
        if not walls:
            msg = "LaminatedThinWallSection requires at least one wall."
            raise ValueError(msg)
        strips = tuple(_RectangularStrip.from_segment(w.geometry) for w in walls)
        EA = sum(w.E * s.area for w, s in zip(walls, strips, strict=True))
        cy = sum(w.E * s.area * s.centroid.y for w, s in zip(walls, strips, strict=True)) / EA
        cz = sum(w.E * s.area * s.centroid.z for w, s in zip(walls, strips, strict=True)) / EA
        EIy = EIz = EIyz = GJ = mass = 0.0
        complete_mass = True
        for wall, strip in zip(walls, strips, strict=True):
            inertia = strip.centroidal_inertia()
            dy, dz = strip.centroid.y - cy, strip.centroid.z - cz
            EIy += wall.E * (inertia.Iy + strip.area * dz**2)
            EIz += wall.E * (inertia.Iz + strip.area * dy**2)
            EIyz += wall.E * (inertia.Iyz + strip.area * dy * dz)
            GJ += wall.G * strip.open_section_torsion_constant()
            if wall.stiffness.areal_mass is None:
                complete_mass = False
            else:
                mass += wall.stiffness.areal_mass * strip.length
        section = BeamSection(
            EA=EA,
            EIy=EIy,
            EIz=EIz,
            EIyz=EIyz,
            GJ=GJ,
            mass_per_length=mass if complete_mass else None,
            metadata={
                "source": "laminated_thin_wall_section",
                "reduction": "uncoupled membrane-equivalent E/G; open-strip torsion",
            },
        )
        object.__setattr__(self, "segments", walls)
        object.__setattr__(self, "centroid_y", cy)
        object.__setattr__(self, "centroid_z", cz)
        object.__setattr__(self, "section", section)


__all__ = ["LaminatedThinWallSection", "LaminatedWallSegment"]
