"""Build every named rib pattern in SI units for the documentation gallery.

Run with ``uv run python docs/examples/scripts/pattern_gallery.py``.
"""

from dataclasses import dataclass

import tensyl as ts


@dataclass(frozen=True)
class Pattern:
    slug: str
    title: str
    constructor: str
    cell: ts.CanonicalUnitCell
    inputs: str


def build_patterns() -> tuple[Pattern, ...]:
    aluminum = ts.IsotropicMaterial(E=70e9, nu=0.33, density=2700)
    skin = ts.isotropic_plate(aluminum, 0.002)
    rib = ts.blade_section(material=aluminum, height=0.025, thickness=0.002)
    section = rib.section
    offset = 0.001 + rib.centroid_z
    orthogonal = dict(
        skin=skin,
        e1_section=section,
        e2_section=section,
        e1_pitch=0.15,
        e2_pitch=0.10,
        e1_axial_eccentricity=offset,
        e2_axial_eccentricity=offset,
    )
    diagonal = dict(
        skin=skin,
        e1_section=section,
        positive_diagonal_section=section,
        e1_pitch=0.15,
        e2_pitch=0.10,
        e1_axial_eccentricity=offset,
        diagonal_axial_eccentricity=offset,
    )
    regular = dict(skin=skin, member_section=section, side_length=0.10, axial_eccentricity=offset)
    hexagonal = dict(e1_half_pitch=0.09, diagonal_e2_rise=0.04, e2_member_length=0.07)
    faces = dict(
        bottom_face=skin,
        top_face=skin,
        bottom_face_to_reference=0.0135,
        top_face_to_reference=-0.0135,
        core_axial_eccentricity=0.0,
    )
    patterns = [
        Pattern(
            "unidirectional",
            "Parallel ribs",
            "unidirectional_cell",
            ts.unidirectional_cell(
                skin=skin, member_section=section, spacing=0.25, axial_eccentricity=offset
            ),
            "spacing = 250 mm; angle_rad = 0",
        ),
        Pattern(
            "orthogrid",
            "Orthogrid",
            "orthogrid_cell",
            ts.orthogrid_cell(**orthogonal),
            "e1_pitch = 150 mm; e2_pitch = 100 mm",
        ),
    ]
    for bracing in ("double", "single"):
        patterns.append(
            Pattern(
                f"braced-{bracing}",
                f"Orthogrid · {bracing} bracing",
                "braced_orthogrid_cell",
                ts.braced_orthogrid_cell(
                    **orthogonal,
                    positive_diagonal_section=section,
                    diagonal_axial_eccentricity=offset,
                    diagonal_pattern=bracing,
                ),
                f"e1_pitch = 150 mm; e2_pitch = 100 mm; diagonal_pattern = '{bracing}'",
            )
        )
    for slug, title, builder in (
        ("diamond", "Diamond grid", ts.diamond_cell),
        ("isosceles", "Isosceles triangular grid", ts.isosceles_triangle_grid_cell),
        ("kagome", "Kagome grid", ts.kagome_cell),
        ("star", "Star grid", ts.star_cell),
    ):
        patterns.append(
            Pattern(
                slug,
                title,
                builder.__name__,
                builder(**diagonal),
                "e1_pitch = 150 mm; e2_pitch = 100 mm",
            )
        )
    for slug, title, builder in (
        ("isogrid", "Equilateral isogrid", ts.equilateral_isogrid_cell),
        ("regular-hexagonal", "Regular hexagonal grid", ts.regular_hexagonal_grid_cell),
        ("equilateral-star", "Equilateral star grid", ts.equilateral_star_cell),
    ):
        patterns.append(
            Pattern(slug, title, builder.__name__, builder(**regular), "side_length = 100 mm")
        )
    patterns.append(
        Pattern(
            "hexagonal",
            "Hexagonal grid",
            "hexagonal_grid_cell",
            ts.hexagonal_grid_cell(
                skin=skin,
                e2_section=section,
                positive_diagonal_section=section,
                e2_axial_eccentricity=offset,
                diagonal_axial_eccentricity=offset,
                **hexagonal,
            ),
            "e1_half_pitch = 90 mm; diagonal_e2_rise = 40 mm; e2_member_length = 70 mm",
        )
    )
    patterns.extend(
        (
            Pattern(
                "sandwich-orthogrid",
                "Orthogrid sandwich core",
                "sandwich_orthogrid_core_cell",
                ts.sandwich_orthogrid_core_cell(
                    **faces, e1_section=section, e2_section=section, e1_pitch=0.15, e2_pitch=0.10
                ),
                "e1_pitch = 150 mm; e2_pitch = 100 mm",
            ),
            Pattern(
                "sandwich-hexagonal",
                "Hexagonal sandwich core",
                "sandwich_hexagonal_core_cell",
                ts.sandwich_hexagonal_core_cell(
                    **faces, e2_section=section, diagonal_section=section, **hexagonal
                ),
                "e1_half_pitch = 90 mm; diagonal_e2_rise = 40 mm; e2_member_length = 70 mm",
            ),
            Pattern(
                "sandwich-star",
                "Star sandwich core",
                "sandwich_star_core_cell",
                ts.sandwich_star_core_cell(
                    **faces,
                    e1_section=section,
                    diagonal_section=section,
                    e1_pitch=0.15,
                    e2_pitch=0.10,
                ),
                "e1_pitch = 150 mm; e2_pitch = 100 mm",
            ),
        )
    )
    return tuple(patterns)


if __name__ == "__main__":
    for pattern in build_patterns():
        result = ts.EnergyHomogenizer().compute(pattern.cell)
        print(
            pattern.slug,
            "A11 =",
            result.stiffness.A[0, 0],
            "N/m",
            "density audit =",
            ts.check_cell_geometry(pattern.cell),
        )
