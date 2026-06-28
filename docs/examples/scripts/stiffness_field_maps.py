"""Generate the stiffness-field map example figures.

Run from the repository root with:

    uv run python docs/examples/scripts/stiffness_field_maps.py
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
    Cylinder,
    Ellipsoid,
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    IsotropicMaterial,
    StiffnessCache,
    ValidityContext,
    blade_section,
    hat_section,
    isotropic_plate,
    orthogrid_cell,
)

ASSET_DIR = Path(__file__).parents[2] / "assets" / "examples"
CYLINDER_OUTPUT_PATH = ASSET_DIR / "cylinder-stiffness-map.png"
ELLIPSOID_OUTPUT_PATH = ASSET_DIR / "ellipsoid-stiffness-map.png"

# Shared figure palette so the two documentation images read as one consistent set.
FIGURE_FACECOLOR = "white"
STIFFNESS_CMAP = cm.viridis  # membrane/bending stiffness (A11, D11) in both figures
VALIDITY_CMAP = cm.magma  # validity signal (p/R) in both figures
CAPTION_COLOR = "#4b5563"

# Faint mesh boundaries on the 3D surfaces so their curvature reads as 3D.
SURFACE_EDGE_COLOR = (0.12, 0.14, 0.18, 0.35)
SURFACE_EDGE_WIDTH = 0.25

# Line colors tied to meaning. Red is reserved for the validity (p/R) signal so the
# "validity = warm" association from the magma maps carries over to the line plots.
VALIDITY_COLOR = colors.to_hex(VALIDITY_CMAP(0.55))
LINE_COLORS = {
    "skin_thickness": "#1b7837",  # green
    "stringer_pitch": "#4575b4",  # blue
    "rib_pitch": "#762a83",  # purple
    "A11": "#1f78b4",  # blue
    "D11": "#ff7f00",  # orange
    "coupling": "#7f7f7f",  # gray
    "validity": VALIDITY_COLOR,  # warm, matches the magma validity maps
}


def _set_plot_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.labelcolor": "#27323a",
            "axes.edgecolor": "#c7ced6",
            "xtick.color": "#27323a",
            "ytick.color": "#27323a",
            "text.color": "#1f2933",
            "grid.color": "#d7dde5",
            "grid.linewidth": 0.7,
        }
    )


def _style_3d_axes(ax: Any) -> None:
    """Blend a 3D surface into a white figure: transparent patch and panes."""

    ax.patch.set_facecolor("none")
    transparent = (1.0, 1.0, 1.0, 0.0)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.set_pane_color(transparent)


def _style_colorbar(colorbar: Any) -> None:
    """Apply the shared colorbar outline style."""

    colorbar.outline.set_edgecolor("#d0d7de")


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


def cylinder_design_at(x: float, length: float = 240.0) -> dict[str, float]:
    """Axially varying wall definition for the practical cylinder example."""

    station = x / length
    taper = 0.5 - 0.5 * math.cos(math.pi * station)
    reinforcement_band = math.exp(-(((station - 0.58) / 0.13) ** 2))
    return {
        "skin_thickness": 0.070 + 0.030 * taper + 0.018 * reinforcement_band,
        "stringer_spacing": 5.2 + 2.1 * station,
        "rib_spacing": 8.4 - 1.5 * taper + 0.8 * reinforcement_band,
        "stringer_scale": 1.00 + 0.26 * reinforcement_band,
        "rib_scale": 0.92 + 0.18 * taper,
    }


def build_cylinder_field() -> tuple[Cylinder, HomogenizedStiffnessField]:
    """Build a 100 inch diameter cylinder with axially varying orthogrid layout."""

    surface = Cylinder(radius=50.0, length=240.0, label="variable_orthogrid_cylinder")
    material = IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1)
    stringer = hat_section(
        material=material,
        web_height=1.0,
        web_thickness=0.060,
        crown_width=0.55,
        crown_thickness=0.060,
        flange_width=0.24,
        flange_thickness=0.060,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )
    rib = blade_section(
        material=material,
        height=1.0,
        thickness=0.065,
        shear_correction_y=5.0 / 6.0,
        shear_correction_z=5.0 / 6.0,
    )

    def cell_factory(surface: Cylinder, point: Any) -> CanonicalUnitCell:
        del surface
        design = cylinder_design_at(point.u)
        skin = isotropic_plate(
            material,
            thickness=design["skin_thickness"],
            frame=point.frame,
            metadata={"source": "variable_cylinder_skin"},
        )
        skin_face = 0.5 * design["skin_thickness"]
        return orthogrid_cell(
            skin=skin,
            stringer_section=scaled_section(
                stringer.section,
                design["stringer_scale"],
                label="axial_hat_stringer",
            ),
            rib_section=scaled_section(rib.section, design["rib_scale"], label="ring_blade_rib"),
            stringer_spacing=design["stringer_spacing"],
            rib_spacing=design["rib_spacing"],
            stringer_eccentricity=skin_face + stringer.properties.centroid_z,
            rib_eccentricity=skin_face + rib.properties.centroid_z,
            frame=point.frame,
        )

    def validity_context(point: Any, cell: CanonicalUnitCell) -> ValidityContext:
        pitch = max(cell.metadata["stringer_spacing"], cell.metadata["rib_spacing"])
        return ValidityContext(
            characteristic_height=1.0,
            pitch=pitch,
            min_radius=point.min_radius,
            response_length=60.0,
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


def sample_cylinder(x_count: int = 52, theta_count: int = 56) -> dict[str, np.ndarray]:
    """Sample the variable cylinder stiffness field for plotting or tests."""

    surface, field = build_cylinder_field()
    x_values = np.linspace(0.0, 240.0, x_count)
    theta_values = np.linspace(0.0, 2.0 * math.pi, theta_count)
    x_grid, theta_grid = np.meshgrid(x_values, theta_values, indexing="ij")

    shape = x_grid.shape
    x = np.empty(shape)
    y = np.empty(shape)
    z = np.empty(shape)
    a11 = np.empty(shape)
    d11 = np.empty(shape)
    coupling = np.empty(shape)
    p_over_r = np.empty(shape)
    p_over_l = np.empty(shape)
    thickness = np.empty(shape)
    stringer_pitch = np.empty(shape)
    rib_pitch = np.empty(shape)
    warning_count = np.empty(shape)

    for index in np.ndindex(shape):
        station = float(x_grid[index])
        theta = float(theta_grid[index])
        point = surface.point_at(station, theta)
        stiffness = field.stiffness_at(surface, station, theta)
        design = cylinder_design_at(station)
        validity = stiffness.validity
        x[index], y[index], z[index] = point.position
        a11[index] = stiffness.A[0, 0]
        d11[index] = stiffness.D[0, 0]
        coupling[index] = np.nan if validity is None else validity.coupling_ratios["B_fro"]
        p_over_r[index] = np.nan if validity is None else validity.p_over_R
        p_over_l[index] = np.nan if validity is None else validity.p_over_L_response
        thickness[index] = design["skin_thickness"]
        stringer_pitch[index] = design["stringer_spacing"]
        rib_pitch[index] = design["rib_spacing"]
        warning_count[index] = 0 if validity is None else len(validity.warnings)

    return {
        "station": x_grid,
        "theta": theta_grid,
        "x": x,
        "y": y,
        "z": z,
        "A11": a11,
        "D11": d11,
        "A11_ratio": a11 / float(np.median(a11)),
        "D11_ratio": d11 / float(np.median(d11)),
        "coupling_B": coupling,
        "p_over_R": p_over_r,
        "p_over_L_response": p_over_l,
        "skin_thickness": thickness,
        "stringer_spacing": stringer_pitch,
        "rib_spacing": rib_pitch,
        "warning_count": warning_count,
        "radius": np.array(50.0),
        "stiffener_height": np.array(1.0),
    }


def render_cylinder_map(
    output_path: Path = CYLINDER_OUTPUT_PATH,
    *,
    data: dict[str, np.ndarray] | None = None,
) -> Path:
    """Render the practical variable-cylinder figure for the documentation."""

    if data is None:
        data = sample_cylinder()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _set_plot_style()

    fig = plt.figure(figsize=(13.4, 8.0), dpi=180, facecolor=FIGURE_FACECOLOR)
    grid = fig.add_gridspec(
        2,
        2,
        width_ratios=(1.08, 1.0),
        height_ratios=(1.0, 1.0),
        wspace=0.20,
        hspace=0.34,
    )
    ax_surface = fig.add_subplot(grid[:, 0], projection="3d")
    ax_inputs = fig.add_subplot(grid[0, 1])
    ax_response = fig.add_subplot(grid[1, 1])

    ratio = data["A11_ratio"]
    norm = colors.Normalize(
        vmin=float(np.percentile(ratio, 3)),
        vmax=float(np.percentile(ratio, 97)),
    )
    surface_artist = ax_surface.plot_surface(
        data["x"],
        data["y"],
        data["z"],
        facecolors=STIFFNESS_CMAP(norm(ratio)),
        antialiased=True,
        shade=False,
    )
    surface_artist.set_edgecolor(SURFACE_EDGE_COLOR)
    surface_artist.set_linewidth(SURFACE_EDGE_WIDTH)
    ax_surface.view_init(elev=21.0, azim=-58.0)
    ax_surface.set_box_aspect((240.0, 100.0, 100.0), zoom=1.2)
    ax_surface.set_axis_off()
    _style_3d_axes(ax_surface)
    ax_surface.set_title(
        "100 inch diameter cylinder colored by local $A_{11}$", y=0.94, pad=0
    )
    colorbar = fig.colorbar(
        cm.ScalarMappable(norm=norm, cmap=STIFFNESS_CMAP),
        ax=ax_surface,
        orientation="horizontal",
        fraction=0.034,
        pad=0.01,
        shrink=0.58,
    )
    colorbar.set_label(r"normalized membrane stiffness, $A_{11}$ / median $A_{11}$")
    _style_colorbar(colorbar)

    station = data["station"][:, 0]
    thickness = data["skin_thickness"][:, 0]
    stringer_pitch = data["stringer_spacing"][:, 0]
    rib_pitch = data["rib_spacing"][:, 0]
    a11_ratio = data["A11_ratio"][:, 0]
    d11_ratio = data["D11_ratio"][:, 0]
    coupling = data["coupling_B"][:, 0]
    p_over_r = data["p_over_R"][:, 0]

    ax_inputs.plot(
        station,
        thickness,
        color=LINE_COLORS["skin_thickness"],
        linewidth=2.4,
        label="skin thickness",
    )
    ax_pitch = ax_inputs.twinx()
    ax_pitch.plot(
        station,
        stringer_pitch,
        color=LINE_COLORS["stringer_pitch"],
        linewidth=2.0,
        label="stringer pitch",
    )
    ax_pitch.plot(
        station,
        rib_pitch,
        color=LINE_COLORS["rib_pitch"],
        linewidth=2.0,
        label="rib pitch",
    )
    ax_inputs.set_title("Wall inputs along the barrel")
    ax_inputs.set_xlabel("axial station, in")
    ax_inputs.set_ylabel("skin thickness, in")
    ax_pitch.set_ylabel("orthogrid pitch, in")
    ax_inputs.grid(True, alpha=0.55)
    input_lines = ax_inputs.get_lines() + ax_pitch.get_lines()
    ax_inputs.legend(
        input_lines,
        [line.get_label() for line in input_lines],
        loc="upper left",
        bbox_to_anchor=(1.2, 1.0),
        fontsize=8.5,
        framealpha=0.95,
    )

    ax_response.plot(
        station,
        a11_ratio,
        color=LINE_COLORS["A11"],
        linewidth=2.4,
        label="$A_{11}$ ratio",
    )
    ax_response.plot(
        station,
        d11_ratio,
        color=LINE_COLORS["D11"],
        linewidth=2.4,
        label="$D_{11}$ ratio",
    )
    ax_response.plot(
        station,
        coupling / np.nanmax(coupling),
        color=LINE_COLORS["coupling"],
        linewidth=1.9,
        label="coupling ratio (scaled)",
    )
    ax_validity = ax_response.twinx()
    ax_validity.plot(
        station,
        p_over_r,
        color=LINE_COLORS["validity"],
        linewidth=2.0,
        label="$p/R$",
    )
    ax_validity.axhline(
        0.05,
        color=LINE_COLORS["validity"],
        linestyle="--",
        linewidth=1.2,
        alpha=0.7,
        label="$p/R$ caution (0.05)",
    )
    ax_response.set_title("Equivalent stiffness response")
    ax_response.set_xlabel("axial station, in")
    ax_response.set_ylabel("normalized stiffness")
    ax_validity.set_ylabel(r"pitch / radius, $p/R$")
    ax_response.grid(True, alpha=0.55)
    response_lines = ax_response.get_lines() + ax_validity.get_lines()
    ax_response.legend(
        response_lines,
        [line.get_label() for line in response_lines],
        loc="upper left",
        bbox_to_anchor=(1.2, 1.0),
        fontsize=8.5,
        framealpha=0.95,
    )

    fig.suptitle(
        "Variable orthogrid cylinder: pointwise stiffness and validity",
        fontsize=15,
        fontweight="bold",
        y=0.965,
    )
    fig.text(
        0.50,
        0.02,
        "Skin thickness and orthogrid pitch vary by axial station, so the local ABD wall "
        "law is recomputed at each station rather than assumed constant.",
        ha="center",
        fontsize=8.7,
        color=CAPTION_COLOR,
    )
    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


def ellipsoid_design_at(phi: float, theta: float) -> dict[str, float]:
    """Pointwise fictional stiffener layout used by the ellipsoid showpiece."""

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


def build_ellipsoid_field() -> tuple[Ellipsoid, HomogenizedStiffnessField]:
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
        design = ellipsoid_design_at(point.u, point.v)
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


def sample_ellipsoid(phi_count: int = 32, theta_count: int = 64) -> dict[str, np.ndarray]:
    """Sample the ellipsoid stiffness field for plotting or tests."""

    surface, field = build_ellipsoid_field()
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
        design = ellipsoid_design_at(phi, theta)
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


def render_ellipsoid_map(
    output_path: Path = ELLIPSOID_OUTPUT_PATH,
    *,
    data: dict[str, np.ndarray] | None = None,
) -> Path:
    """Render the ellipsoid showpiece image for the documentation."""

    if data is None:
        data = sample_ellipsoid()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _set_plot_style()

    fig = plt.figure(figsize=(12.8, 7.2), dpi=180, facecolor=FIGURE_FACECOLOR)
    grid = fig.add_gridspec(1, 2, width_ratios=(1.28, 1.0), wspace=0.22)

    ax_surface = fig.add_subplot(grid[0, 0], projection="3d")
    ax_map = fig.add_subplot(grid[0, 1])

    ratio = data["A11_ratio"]
    norm = colors.Normalize(
        vmin=float(np.percentile(ratio, 4)),
        vmax=float(np.percentile(ratio, 96)),
    )
    surface_artist = ax_surface.plot_surface(
        data["x"],
        data["y"],
        data["z"],
        facecolors=STIFFNESS_CMAP(norm(ratio)),
        rstride=1,
        cstride=1,
        antialiased=True,
        shade=False,
    )
    surface_artist.set_edgecolor(SURFACE_EDGE_COLOR)
    surface_artist.set_linewidth(SURFACE_EDGE_WIDTH)
    ax_surface.view_init(elev=23.0, azim=-38.0)
    ax_surface.set_box_aspect((180.0, 125.0, 75.0), zoom=1.4)
    ax_surface.set_axis_off()
    _style_3d_axes(ax_surface)
    ax_surface.set_title("Local membrane stiffness over a triaxial shell", y=0.86, pad=0)

    colorbar = fig.colorbar(
        cm.ScalarMappable(norm=norm, cmap=STIFFNESS_CMAP),
        ax=ax_surface,
        orientation="horizontal",
        fraction=0.035,
        pad=0.01,
        shrink=0.7,
    )
    colorbar.set_label(r"normalized membrane stiffness, $A_{11}$ / median $A_{11}$")
    _style_colorbar(colorbar)

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
    _style_colorbar(p_colorbar)

    fig.suptitle(
        "Pointwise equivalent stiffness on a triaxial ellipsoid",
        fontsize=15,
        fontweight="bold",
        y=0.975,
    )
    fig.text(
        0.50,
        0.02,
        "Each sampled point rebuilds the local cell with its own frame, pitch, section scale, "
        "eccentricity, and curvature-based validity context.",
        ha="center",
        fontsize=8.5,
        color=CAPTION_COLOR,
    )
    fig.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    return output_path


def render_all() -> tuple[Path, Path]:
    """Render every committed figure for this documentation example."""

    return (render_cylinder_map(), render_ellipsoid_map())


if __name__ == "__main__":
    for path in render_all():
        print(path)
