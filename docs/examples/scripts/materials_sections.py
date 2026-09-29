"""Complete SI examples for laminate skins and thin-wall ribs."""

# Imports stay with the step that introduces them in the handbook.
# ruff: noqa: E402

# --8<-- [start:laminate]
from tensyl import OrthotropicPlyMaterial, Ply, laminate_plate, layup

carbon = OrthotropicPlyMaterial(
    E1=135e9,
    E2=10e9,
    G12=5e9,
    nu12=0.3,
    G13=5e9,
    G23=3.8e9,
    density=1600,
    alpha1=-0.2e-6,
    alpha2=30e-6,
)
symmetric_plies = layup(carbon, 0.000125, "[0/±45/90]s")
symmetric = laminate_plate(symmetric_plies)
unsymmetric_plies = (
    Ply.from_degrees(carbon, 0.0005, 0),
    Ply.from_degrees(carbon, 0.0005, 90),
)
unsymmetric = laminate_plate(unsymmetric_plies)
# --8<-- [end:laminate]

# --8<-- [start:thermal]
from tensyl import IsotropicMaterial, laminate_thermal_resultants

aluminum = IsotropicMaterial(E=70e9, nu=0.33, density=2700, alpha=23e-6)
metal_plies = (Ply(aluminum, thickness=0.002),)
metal_skin = laminate_plate(metal_plies)
thermal = laminate_thermal_resultants(metal_plies)
delta_temperature = 50.0  # K
free_strain = metal_skin.strains(thermal.equivalent_load(delta_temperature))
# --8<-- [end:thermal]

# --8<-- [start:hat]
from tensyl import hat_section

hat_dimensions = dict(
    material=aluminum,
    web_height=0.025,
    web_thickness=0.002,
    crown_width=0.03,
    crown_thickness=0.002,
    flange_width=0.01,
    flange_thickness=0.002,
)
open_hat = hat_section(**hat_dimensions)
closed_hat = hat_section(**hat_dimensions, closure_thickness=0.002)
# --8<-- [end:hat]

# --8<-- [start:wall]
from tensyl import LaminatedThinWallSection, LaminatedWallSegment, ThinWallSegment

composite_blade = LaminatedThinWallSection(
    (
        LaminatedWallSegment(
            ThinWallSegment(0, 0, 0, 0.025, 0.001),
            symmetric_plies,
        ),
    )
)
composite_section = composite_blade.section
# --8<-- [end:wall]

# --8<-- [start:custom]
from tensyl import thin_wall_section

custom_section = thin_wall_section(
    material=aluminum,
    segments=(
        ThinWallSegment(-0.015, 0, 0.015, 0, 0.002, label="flange"),
        ThinWallSegment(0, 0, 0, 0.025, 0.002, label="web"),
    ),
)
# --8<-- [end:custom]

if __name__ == "__main__":
    import numpy as np

    print("Symmetric laminate B norm:", np.linalg.norm(symmetric.B))
    print("Free thermal strain:", free_strain)
    print("Hat GJ, open / closed [N m²]:", open_hat.section.GJ, closed_hat.section.GJ)
    print("Composite blade EA [N]:", composite_section.EA)
