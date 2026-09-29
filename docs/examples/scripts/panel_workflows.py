"""SI examples for rib patterns, transformations, sweeps, and data handoff."""

# ruff: noqa: E402

# --8<-- [start:setup]
import math

from tensyl import EnergyHomogenizer, IsotropicMaterial, blade_section, isotropic_plate

aluminum = IsotropicMaterial(E=70e9, nu=0.33, density=2700, alpha=23e-6)
skin = isotropic_plate(aluminum, 0.002)
rib = blade_section(material=aluminum, height=0.025, thickness=0.002)
offset = 0.001 + rib.centroid_z
# --8<-- [end:setup]

# --8<-- [start:families]
from tensyl import StiffenerFamily, stiffener_family_cell

families = stiffener_family_cell(
    skin=skin,
    families=(
        StiffenerFamily(rib.section, spacing=0.10, angle_rad=0, axial_eccentricity=offset),
        StiffenerFamily(
            rib.section,
            spacing=0.15,
            angle_rad=math.pi / 2,
            axial_eccentricity=offset,
        ),
    ),
)
result = EnergyHomogenizer().compute(families)
# --8<-- [end:families]

# --8<-- [start:graph]
from tensyl import CellEdge, CellNode, CellVector, check_cell_geometry, graph_unit_cell

custom_cell = graph_unit_cell(
    skin=skin,
    area=0.15 * 0.10,
    nodes=(CellNode(0, 0), CellNode(0.15, 0), CellNode(0.15, 0.10), CellNode(0, 0.10)),
    edges=(
        CellEdge(0, 1, rib.section, axial_eccentricity=offset, family="e1"),
        CellEdge(0, 3, rib.section, axial_eccentricity=offset, family="e2"),
    ),
    repeat_vectors=(CellVector(0.15, 0), CellVector(0, 0.10)),
    boundary=(0, 1, 2, 3),
)
density_audit = check_cell_geometry(custom_cell)
# --8<-- [end:graph]

# --8<-- [start:transform]
from tensyl import shift_reference_surface

stiffness = result.stiffness
rotated = stiffness.rotate(math.pi / 2)
shift = 0.005  # Move the reference 5 mm along +n.
shifted = shift_reference_surface(stiffness, shift)
# --8<-- [end:transform]

# --8<-- [start:sweep]
from tensyl import sweep, unidirectional_cell


def build_panel(spacing):
    return unidirectional_cell(
        skin=skin,
        member_section=rib.section,
        spacing=spacing,
        axial_eccentricity=offset,
    )


rows = sweep(build_panel, {"spacing": [0.075, 0.10, 0.15]})
# --8<-- [end:sweep]

# --8<-- [start:files]
from tensyl.io import from_json, from_yaml, to_json, to_yaml

units = {"length": "m", "force": "N", "mass": "kg"}
restored_result = from_json(to_json(result, units=units))
restored_cell = from_yaml(to_yaml(custom_cell, units=units))
# --8<-- [end:files]

# --8<-- [start:abaqus]
from tensyl.adapters import abaqus_shell_general_section

keywords = abaqus_shell_general_section(stiffness, elset="PANEL")
# --8<-- [end:abaqus]

# --8<-- [start:cell-thermal]
from tensyl import Ply, cell_thermal_resultants, laminate_thermal_resultants, member_loads

skin_thermal = laminate_thermal_resultants((Ply(aluminum, 0.002),))
cell_thermal = cell_thermal_resultants(families, skin=skin_thermal)
thermal_strain = stiffness.strains(cell_thermal.equivalent_load(50.0))
mechanical_rib_loads = member_loads(families, thermal_strain)
net_axial_forces = tuple(
    load.axial_force - member.section.EA * member.section.thermal_expansion * 50.0
    for load, member in zip(mechanical_rib_loads, families.members, strict=True)
)
# --8<-- [end:cell-thermal]

if __name__ == "__main__":
    for row in rows:
        print(row["spacing"], row["A11"], row["D11"], row["areal_mass"])
    print("Drawn / modeled rib density:", density_audit)
    print(keywords)

# --8<-- [start:sp8007]
from tensyl import equilateral_isogrid_cell

orthogrid_constants = result.orthotropic_coefficients()
isogrid = equilateral_isogrid_cell(
    skin=skin,
    member_section=rib.section,
    side_length=0.10,
    axial_eccentricity=offset,
)
isogrid_constants = EnergyHomogenizer().compute(isogrid).orthotropic_coefficients()
# --8<-- [end:sp8007]
