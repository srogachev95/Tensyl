"""Generate the ellipsoid stiffness-map example figure.

Run from the repository root with:

    uv run python docs/examples/scripts/ellipsoid_stiffness_map.py
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np

matplotlib.use("Agg")

from matplotlib import cm, colors  # noqa: E402
from matplotlib import pyplot as plt  # noqa: E402

from tensyl import (  # noqa: E402
    BeamMember,
    BeamSection,
    CanonicalUnitCell,
    Ellipsoid,
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    IsotropicMaterial,
    StiffnessCache,
    ValidityContext,
    blade_section,
    hat_section,
    isotropic_plate,
)

OUTPUT_PATH = Path(__file__).parents[2] / "assets" / "examples" / "ellipsoid-stiffness-map.png"


def scaled_section(section: BeamSection, scale: float, *, label: str) -> BeamSection:
    """Return a uniformly scaled beam section for a local design variation."""

    return BeamSection(
        EA=section.EA * scale,
        EIy=section.EIy * scale,
        EIz=section.EIz * scale,
        GJ=section.GJ * scale,
        kGAy=None if section.kGAy is None else section.kGAy * scale,
        kGAz=None if section.kGAz is None else section.kGAz * scale,
        EIyz=section.EIyz * scale,
        metadata={**section.metadata, "showpiece_scale": scale, "showpiece_label": label},
    )


def design_at(phi: float, theta: float) -> dict[str, float]:
    """Pointwise fictional stiffener layout used by the showpiece."""

    latitude_weight = math.sin(phi) ** 2
    wave = 0.5 + 0.5 * math.cos(3.0 * theta - 0.8 * math.cos(phi))
    nose_weight = abs(math.cos(phi))
    return {
        "skin_thickness": 0.052 + 0.018 * latitude_weight + 0.006 * wave,
        "primary_pitch": 4.6 + 1.8 * latitude_weight + 0.9 * wave,
        "secondary_pitch": 5.2 + 1.4 * (1.0 - wave) + 0.7 * nose_weight,
        "angle_rad": 0.55 * math.sin(theta) + 0.25 * math.sin(2.0 * phi),
        "primary_scale": 0.85 + 0.45 * wave,
        "secondary_scale": 0.80 + 0.30 * latitude_weight,
    }


def build_showpiece_field() -> tuple[Ellipsoid, HomogenizedStiffnessField]:
    """Build the ellipsoid and pointwise stiffness field used in the figure."""

    surface = Ellipsoid(a=180.0, b=125.0, c=75.0, label="ellipsoid_showpiece")
    material = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
    hat = hat_section(
        material=material,
        web_height=0.54,
        web_thickness=0.045,
        crown_width=0.42,
        crown_thickness=0.045,
        flange_width=0.22,
        flange_thickness=0.045,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )
    blade = blade_section(
        material=material,
        height=0.42,
        thickness=0.045,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )

    def cell_factory(surface: Ellipsoid, point: Any) -> CanonicalUnitCell:
        del surface
        design = design_at(point.u, point.v)
        skin = isotropic_plate(
            material,
            thickness=design["skin_thickness"],
            frame=point.frame,
            metadata={"source": "ellipsoid_showpiece_skin"},
        )
        primary = scaled_section(
            hat.section,
            design["primary_scale"],
            label="swept_hat_family",
        )
        secondary = scaled_section(
            blade.section,
            design["secondary_scale"],
            label="cross_blade_family",
        )
        skin_face = 0.5 * design["skin_thickness"]
        return CanonicalUnitCell(
            area=design["primary_pitch"] * design["secondary_pitch"],
            skin=skin,
            members=(
                BeamMember(
                    section=primary,
                    length=design["secondary_pitch"],
                    angle_rad=design["angle_rad"],
                    eccentricity=skin_face + hat.properties.centroid_z,
                    label="swept_hat",
                ),
                BeamMember(
                    section=secondary,
                    length=design["primary_pitch"],
                    angle_rad=design["angle_rad"] + 0.5 * math.pi,
                    eccentricity=skin_face + blade.properties.centroid_z,
                    label="cross_blade",
                ),
            ),
            frame=point.frame,
            convention=skin.convention,
            metadata={
                "source": "ellipsoid_showpiece_cell",
                "primary_pitch": design["primary_pitch"],
                "secondary_pitch": design["secondary_pitch"],
                "angle_rad": design["angle_rad"],
                "skin_thickness": design["skin_thickness"],
            },
        )

    def validity_context(point: Any, cell: CanonicalUnitCell) -> ValidityContext:
        pitch = max(cell.metadata["primary_pitch"], cell.metadata["secondary_pitch"])
        return ValidityContext(
            characteristic_height=0.62,
            pitch=pitch,
            min_radius=point.min_radius,
            response_length=52.0,
        )

    return (
        surface,
        HomogenizedStiffnessField(
            surface,
            cell_factory,
            EnergyHomogenizer(),
            cache=StiffnessCache(),
            validity_context_factory=validity_context,
        ),
    )


def sample_showpiece(phi_count: int = 32, theta_count: int = 64) -> dict[str, np.ndarray]:
    """Sample the ellipsoid stiffness field for plotting or tests."""

    surface, field = build_showpiece_field()
    phi_values = np.linspace(0.18, math.pi - 0.18, phi_count)
    theta_values = np.linspace(0.0, 2.0 * math.pi, theta_count)
    phi_grid, theta_grid = np.meshgrid(phi_values, theta_values, indexing="ij")

    shape = phi_grid.shape
    x = np.empty(shape)
    y = np.empty(shape)
    z = np.empty(shape)
    a11 = np.empty(shape)
    d11 = np.empty(shape)
    p_over_r = np.empty(shape)
    coupling = np.empty(shape)
    pitch = np.empty(shape)
    angle_deg = np.empty(shape)
    warning_count = np.empty(shape)

    for index in np.ndindex(shape):
        phi = float(phi_grid[index])
        theta = float(theta_grid[index])
        point = surface.point_at(phi, theta)
        stiffness = field.stiffness_at(surface, phi, theta)
        design = design_at(phi, theta)
        x[index], y[index], z[index] = point.position
        a11[index] = stiffness.A[0, 0]
        d11[index] = stiffness.D[0, 0]
        validity = stiffness.validity
        p_over_r[index] = np.nan if validity is None else validity.p_over_R
        coupling[index] = np.nan if validity is None else validity.coupling_ratios["B_fro"]
        pitch[index] = max(design["primary_pitch"], design["secondary_pitch"])
        angle_deg[index] = math.degrees(design["angle_rad"])
        warning_count[index] = 0 if validity is None else len(validity.warnings)

    return {
        "phi": phi_grid,
        "theta": theta_grid,
        "x": x,
        "y": y,
        "z": z,
        "A11": a11,
        "D11": d11,
        "A11_ratio": a11 / float(np.median(a11)),
        "p_over_R": p_over_r,
        "coupling_B": coupling,
        "pitch": pitch,
        "angle_deg": angle_deg,
        "warning_count": warning_count,
    }


def render_showpiece(
    output_path: Path = OUTPUT_PATH,
    *,
    data: dict[str, np.ndarray] | None = None,
) -> Path:
    """Render the publication image for the documentation."""

    if data is None:
        data = sample_showpiece()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.labelcolor": "#27323a",
            "xtick.color": "#27323a",
            "ytick.color": "#27323a",
            "text.color": "#1f2933",
        }
    )
    fig = plt.figure(figsize=(12.8, 7.2), dpi=180, facecolor="#fbfaf7")
    grid = fig.add_gridspec(1, 2, width_ratios=(1.28, 1.0), wspace=0.12)

    ax_surface = fig.add_subplot(grid[0, 0], projection="3d")
    ax_map = fig.add_subplot(grid[0, 1])

    ratio = data["A11_ratio"]
    norm = colors.Normalize(
        vmin=float(np.percentile(ratio, 4)),
        vmax=float(np.percentile(ratio, 96)),
    )
    surface_colors = cm.cividis(norm(ratio))
    ax_surface.plot_surface(
        data["x"],
        data["y"],
        data["z"],
        facecolors=surface_colors,
        rstride=1,
        cstride=1,
        linewidth=0.0,
        antialiased=True,
        shade=False,
    )
    ax_surface.view_init(elev=23.0, azim=-38.0)
    ax_surface.set_box_aspect((180.0, 125.0, 75.0))
    ax_surface.set_axis_off()
    ax_surface.set_title("Local membrane stiffness over a triaxial shell", pad=16)

    mappable = cm.ScalarMappable(norm=norm, cmap=cm.cividis)
    mappable.set_array(ratio)
    colorbar = fig.colorbar(mappable, ax=ax_surface, fraction=0.035, pad=0.02)
    colorbar.ax.set_title(r"$A_{11}$" + "\nratio", fontsize=8.5, pad=8)
    colorbar.outline.set_edgecolor("#d0d7de")

    theta_deg = np.degrees(data["theta"])
    phi_deg = np.degrees(data["phi"])
    p_norm = colors.Normalize(
        vmin=float(np.nanmin(data["p_over_R"])),
        vmax=float(np.nanmax(data["p_over_R"])),
    )
    mesh = ax_map.pcolormesh(
        theta_deg,
        phi_deg,
        data["p_over_R"],
        cmap="magma",
        norm=p_norm,
        shading="auto",
    )
    contours = ax_map.contour(
        theta_deg,
        phi_deg,
        ratio,
        levels=(0.92, 1.00, 1.08, 1.16),
        colors="#f7f7f2",
        linewidths=0.9,
        alpha=0.85,
    )
    ax_map.clabel(contours, inline=True, fontsize=7, fmt="%.2f")
    ax_map.set_title("Where the tangent-plane assumption works hardest", pad=14)
    ax_map.set_xlabel(r"azimuth $\theta$ (deg)")
    ax_map.set_ylabel(r"polar angle $\phi$ (deg)")
    ax_map.set_xlim(0.0, 360.0)
    ax_map.set_ylim(float(phi_deg.min()), float(phi_deg.max()))
    ax_map.grid(color="#ffffff", linewidth=0.7, alpha=0.28)
    ax_map.set_facecolor("#22212b")
    p_colorbar = fig.colorbar(mesh, ax=ax_map, fraction=0.046, pad=0.03)
    p_colorbar.set_label(r"pitch / local radius, $p/R_\mathrm{min}$")
    p_colorbar.outline.set_edgecolor("#d0d7de")

    fig.suptitle(
        "Tensyl showpiece: a pointwise stiffened-wall law on a curved ellipsoid",
        fontsize=15,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.50,
        0.035,
        "Each sampled point rebuilds the local cell with its own frame, pitch, section scale, "
        "eccentricity, and curvature-based validity context.",
        ha="center",
        fontsize=8.5,
        color="#4b5563",
    )
    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    print(render_showpiece())
