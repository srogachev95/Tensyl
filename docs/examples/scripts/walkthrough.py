"""SI orthogrid used throughout the getting-started walkthrough.

Run from the checkout with ``uv run python docs/examples/scripts/walkthrough.py``.
"""

# Keep imports with the tutorial step that introduces them.
# ruff: noqa: E402

# --8<-- [start:skin]
from tensyl import IsotropicMaterial, isotropic_plate

aluminum = IsotropicMaterial(E=70e9, nu=0.33, density=2700)
skin = isotropic_plate(aluminum, thickness=0.002)
# --8<-- [end:skin]

# --8<-- [start:grid]
from tensyl import EnergyHomogenizer, ValidityContext, blade_section, orthogrid_cell

rib = blade_section(material=aluminum, height=0.025, thickness=0.002)
centroid_offset = 0.002 / 2 + rib.centroid_z
cell = orthogrid_cell(
    skin=skin,
    e1_section=rib.section,
    e2_section=rib.section,
    e1_pitch=0.15,
    e2_pitch=0.10,
    e1_axial_eccentricity=centroid_offset,
    e2_axial_eccentricity=centroid_offset,
)
result = EnergyHomogenizer().compute(
    cell,
    validity_context=ValidityContext(
        characteristic_height=0.027,
        min_radius=float("inf"),
        response_length=1.0,
    ),
)
# --8<-- [end:grid]

# --8<-- [start:loads]
import numpy as np

from tensyl import member_loads

# N11, N22, N12 [N/m]; M11, M22, M12 [N]; Q13, Q23 [N/m].
loads = np.array([10_000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
strain = result.stiffness.strains(loads)
rib_loads = member_loads(cell, strain)
# --8<-- [end:loads]

# --8<-- [start:save]
from pathlib import Path

from tensyl.io import read_json, write_json


def save_result(path: Path):
    """Save the complete result and read it back for the next analysis step."""
    write_json(result, path, units={"length": "m", "force": "N", "mass": "kg"})
    return read_json(path)


# Call save_result(Path("panel.json")) to write into your working directory.
# --8<-- [end:save]

if __name__ == "__main__":
    print(result.summary(units={"A": "N/m", "B": "N", "D": "N m", "As": "N/m"}))
    print("Generalized strain:", strain)
    for load in rib_loads:
        print(load)
