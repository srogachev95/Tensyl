"""Place a uniform or station-varying SI panel on a cylinder and save its atlas."""

# ruff: noqa: E402

# --8<-- [start:constant]
import math

from tensyl import ConstantStiffnessField, Cylinder, IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=70e9, nu=0.33, density=2700)
skin = isotropic_plate(aluminum, 0.002)
surface = Cylinder(radius=2.0, length=3.0)
constant = ConstantStiffnessField(skin)
local = constant.stiffness_at(surface, 1.5, 0.0)
# --8<-- [end:constant]

# --8<-- [start:varying]
from tensyl import (
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    StiffnessCache,
    ValidityContext,
    blade_section,
    orthogrid_cell,
)

rib = blade_section(material=aluminum, height=0.025, thickness=0.002)


def cell_factory(surface, point):
    local_skin = isotropic_plate(aluminum, 0.002, frame=point.frame)
    return orthogrid_cell(
        skin=local_skin,
        e1_section=rib.section,
        e2_section=rib.section,
        e1_pitch=0.15,
        e2_pitch=0.10 + 0.02 * point.u / surface.length,
        e1_axial_eccentricity=0.0135,
        e2_axial_eccentricity=0.0135,
        frame=point.frame,
    )


def context_factory(point, cell):
    return ValidityContext.from_surface_point(
        point,
        characteristic_height=0.027,
        response_length=1.0,
    )


varying = HomogenizedStiffnessField(
    surface,
    cell_factory,
    EnergyHomogenizer(),
    cache=StiffnessCache(),
    validity_context_factory=context_factory,
)
root = varying.stiffness_at(surface, 0.0, 0.0)
tip = varying.stiffness_at(surface, 3.0, 0.0)
# --8<-- [end:varying]

# --8<-- [start:atlas]
from tensyl import ABDAtlas
from tensyl.io import from_json, to_json

atlas = ABDAtlas.from_field(
    surface,
    varying,
    u_values=(0.0, 1.5, 3.0),
    v_values=(0.0, math.pi, 2 * math.pi),
)
interpolated = atlas.stiffness_at(surface, 0.75, math.pi / 2)
restored_atlas = from_json(to_json(atlas, units={"length": "m", "force": "N", "mass": "kg"}))
# --8<-- [end:atlas]

if __name__ == "__main__":
    print("Root / tip A11 [N/m]:", root.A[0, 0], tip.A[0, 0])
    print("Interpolated A11 [N/m]:", interpolated.A[0, 0])
