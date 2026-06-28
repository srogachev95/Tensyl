"""Generate documentation SVGs for thin-wall stiffener section geometry."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

from tensyl.materials import IsotropicMaterial
from tensyl.sections.thin_wall import (
    ThinWallSection,
    ThinWallSegment,
    blade_section,
    channel_section,
    hat_section,
    tee_section,
    thin_wall_section,
    zee_section,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "assets" / "sections"


@dataclass(frozen=True, slots=True)
class Dimension:
    start_y: float
    start_z: float
    end_y: float
    end_z: float
    label: str
    offset: float = 0.0
    label_dx: float | None = None
    label_dy: float | None = None
    label_anchor: str | None = None


@dataclass(frozen=True, slots=True)
class LabelPlacement:
    label: str
    offset_y: float = 0.0
    offset_z: float = 0.0
    rotate: float = 0.0
    anchor: str = "middle"


@dataclass(frozen=True, slots=True)
class Diagram:
    filename: str
    title: str
    desc: str
    section: ThinWallSection
    dimensions: tuple[Dimension, ...]
    labels: Mapping[str, LabelPlacement]
    note: str


WIDTH = 760
HEIGHT = 470
MARGIN_LEFT = 84
MARGIN_RIGHT = 224
MARGIN_TOP = 78
MARGIN_BOTTOM = 112
TEXT_STYLE = (
    'font-family="Inter, Arial, sans-serif" paint-order="stroke" stroke="#ffffff" '
    'stroke-width="3" stroke-linejoin="round"'
)
DUMMY_MATERIAL = IsotropicMaterial(E=1.0, nu=0.3)


def diagrams() -> tuple[Diagram, ...]:
    blade_height = 3.2
    blade_thickness = 0.34

    tee_web_height = 2.7
    tee_web_thickness = 0.24
    tee_flange_width = 2.5
    tee_flange_thickness = 0.30
    tee_flange_z = tee_web_height + 0.5 * tee_flange_thickness

    zee_web_height = 2.35
    zee_web_thickness = 0.24
    zee_top_flange_width = 1.18
    zee_bottom_flange_width = 1.35
    zee_flange_thickness = 0.30
    zee_web_start_z = zee_flange_thickness
    zee_web_end_z = zee_flange_thickness + zee_web_height
    zee_top_flange_z = zee_web_end_z + 0.5 * zee_flange_thickness
    zee_bottom_flange_z = 0.5 * zee_flange_thickness

    channel_web_height = 2.35
    channel_web_thickness = 0.24
    channel_flange_width = 1.35
    channel_flange_thickness = 0.30
    channel_web_start_z = channel_flange_thickness
    channel_web_end_z = channel_flange_thickness + channel_web_height
    channel_bottom_flange_z = 0.5 * channel_flange_thickness

    hat_web_height = 2.29
    hat_web_thickness = 0.22
    hat_crown_width = 1.50
    hat_crown_thickness = 0.30
    hat_flange_width = 0.85
    hat_flange_thickness = 0.26
    hat_half_crown = 0.5 * hat_crown_width
    hat_top_z = hat_flange_thickness + hat_web_height
    hat_crown_z = hat_top_z + 0.5 * hat_crown_thickness
    hat_flange_z = 0.5 * hat_flange_thickness

    return (
        Diagram(
            filename="blade-section.svg",
            title="blade_section geometry",
            desc="A blade web rises in positive z from the skin-face construction datum.",
            section=blade_section(
                material=DUMMY_MATERIAL,
                height=blade_height,
                thickness=blade_thickness,
            ),
            dimensions=(
                Dimension(0.0, 0.0, 0.0, blade_height, "height", offset=0.72),
                Dimension(
                    -0.5 * blade_thickness,
                    1.05,
                    0.5 * blade_thickness,
                    1.05,
                    "thickness",
                    offset=-0.28,
                    label_dy=17,
                ),
            ),
            labels={
                "": LabelPlacement("blade web", offset_y=0.45, offset_z=0.42, rotate=-90),
            },
            note="Web root touches z = 0; centroid_z is measured upward from that datum.",
        ),
        Diagram(
            filename="tee-section.svg",
            title="tee_section geometry",
            desc="A tee section has a web rooted at z = 0 and a flange above the web.",
            section=tee_section(
                material=DUMMY_MATERIAL,
                web_height=tee_web_height,
                web_thickness=tee_web_thickness,
                flange_width=tee_flange_width,
                flange_thickness=tee_flange_thickness,
            ),
            dimensions=(
                Dimension(0.0, 0.0, 0.0, tee_web_height, "web_height", offset=0.62),
                Dimension(
                    -0.5 * tee_flange_width,
                    tee_flange_z,
                    0.5 * tee_flange_width,
                    tee_flange_z,
                    "flange_width",
                    offset=0.55,
                ),
                Dimension(
                    0.5 * tee_flange_width,
                    tee_web_height,
                    0.5 * tee_flange_width,
                    tee_web_height + tee_flange_thickness,
                    "flange_thickness",
                    offset=-0.34,
                    label_dx=14,
                    label_anchor="start",
                ),
                Dimension(
                    -0.5 * tee_web_thickness,
                    1.10,
                    0.5 * tee_web_thickness,
                    1.10,
                    "web_thickness",
                    offset=-0.30,
                    label_dy=17,
                ),
            ),
            labels={
                "web": LabelPlacement("web", offset_y=0.38, offset_z=0.10, rotate=-90),
                "flange": LabelPlacement("flange", offset_z=-0.33),
            },
            note="The flange is on the +z side of the web.",
        ),
        Diagram(
            filename="zee-section.svg",
            title="zee_section geometry",
            desc="A zee section has bottom and top flanges on opposite sides of the web.",
            section=zee_section(
                material=DUMMY_MATERIAL,
                web_height=zee_web_height,
                web_thickness=zee_web_thickness,
                top_flange_width=zee_top_flange_width,
                bottom_flange_width=zee_bottom_flange_width,
                flange_thickness=zee_flange_thickness,
            ),
            dimensions=(
                Dimension(
                    -zee_bottom_flange_width,
                    zee_bottom_flange_z,
                    0.0,
                    zee_bottom_flange_z,
                    "bottom_flange_width",
                    offset=-0.52,
                    label_dy=17,
                ),
                Dimension(
                    0.0,
                    zee_top_flange_z,
                    zee_top_flange_width,
                    zee_top_flange_z,
                    "top_flange_width",
                    offset=0.55,
                ),
                Dimension(0.0, zee_web_start_z, 0.0, zee_web_end_z, "web_height", offset=0.67),
                Dimension(
                    zee_top_flange_width,
                    zee_web_end_z,
                    zee_top_flange_width,
                    zee_web_end_z + zee_flange_thickness,
                    "flange_thickness",
                    offset=-0.35,
                    label_dx=14,
                    label_anchor="start",
                ),
            ),
            labels={
                "bottom_flange": LabelPlacement("bottom flange", offset_z=0.34),
                "web": LabelPlacement("web", offset_y=-0.36, rotate=-90),
                "top_flange": LabelPlacement("top flange", offset_z=-0.34),
            },
            note="Bottom and top flanges point to opposite sides in y.",
        ),
        Diagram(
            filename="channel-section.svg",
            title="channel_section geometry",
            desc="A channel section has top and bottom flanges on the same side of the web.",
            section=channel_section(
                material=DUMMY_MATERIAL,
                web_height=channel_web_height,
                web_thickness=channel_web_thickness,
                flange_width=channel_flange_width,
                flange_thickness=channel_flange_thickness,
            ),
            dimensions=(
                Dimension(
                    0.0,
                    channel_bottom_flange_z,
                    channel_flange_width,
                    channel_bottom_flange_z,
                    "flange_width",
                    offset=-0.52,
                    label_dy=17,
                ),
                Dimension(
                    0.0,
                    channel_web_start_z,
                    0.0,
                    channel_web_end_z,
                    "web_height",
                    offset=0.67,
                ),
                Dimension(
                    channel_flange_width,
                    channel_web_end_z,
                    channel_flange_width,
                    channel_web_end_z + channel_flange_thickness,
                    "flange_thickness",
                    offset=-0.36,
                    label_dx=14,
                    label_anchor="start",
                ),
                Dimension(
                    -0.5 * channel_web_thickness,
                    1.25,
                    0.5 * channel_web_thickness,
                    1.25,
                    "web_thickness",
                    offset=-0.32,
                    label_dy=17,
                ),
            ),
            labels={
                "bottom_flange": LabelPlacement("bottom flange", offset_z=0.34),
                "web": LabelPlacement("web", offset_y=-0.36, rotate=-90),
                "top_flange": LabelPlacement("top flange", offset_z=-0.34),
            },
            note="Both flanges extend to the same +y side.",
        ),
        Diagram(
            filename="hat-section.svg",
            title="hat_section geometry",
            desc="An open hat section rises in positive z with lower mounting flanges at z = 0.",
            section=hat_section(
                material=DUMMY_MATERIAL,
                web_height=hat_web_height,
                web_thickness=hat_web_thickness,
                crown_width=hat_crown_width,
                crown_thickness=hat_crown_thickness,
                flange_width=hat_flange_width,
                flange_thickness=hat_flange_thickness,
            ),
            dimensions=(
                Dimension(
                    -hat_half_crown,
                    hat_crown_z,
                    hat_half_crown,
                    hat_crown_z,
                    "crown_width",
                    offset=0.55,
                ),
                Dimension(
                    -hat_half_crown - hat_flange_width,
                    hat_flange_z,
                    -hat_half_crown,
                    hat_flange_z,
                    "flange_width",
                    offset=-0.50,
                    label_dy=17,
                ),
                Dimension(
                    -hat_half_crown,
                    hat_flange_thickness,
                    -hat_half_crown,
                    hat_top_z,
                    "web_height",
                    offset=0.58,
                ),
                Dimension(
                    hat_half_crown,
                    hat_top_z,
                    hat_half_crown,
                    hat_top_z + hat_crown_thickness,
                    "crown_thickness",
                    offset=-0.34,
                    label_dx=14,
                    label_anchor="start",
                ),
                Dimension(
                    hat_half_crown + hat_flange_width,
                    0.0,
                    hat_half_crown + hat_flange_width,
                    hat_flange_thickness,
                    "flange_thickness",
                    offset=-0.28,
                    label_dx=14,
                    label_dy=-11,
                    label_anchor="start",
                ),
            ),
            labels={
                "left_flange": LabelPlacement("left flange", offset_z=0.32),
                "left_web": LabelPlacement("left web", offset_y=0.32, rotate=-90),
                "crown": LabelPlacement("crown", offset_z=-0.34),
                "right_web": LabelPlacement("right web", offset_y=-0.32, rotate=-90),
                "right_flange": LabelPlacement("right flange", offset_z=0.32),
            },
            note="The hat is not flipped downward; mounting flanges sit on the skin-face datum.",
        ),
        Diagram(
            filename="thin-wall-segment.svg",
            title="thin_wall_section segment coordinates",
            desc="A custom thin-wall segment is defined by midline endpoints and thickness.",
            section=thin_wall_section(
                material=DUMMY_MATERIAL,
                segments=(ThinWallSegment(-1.15, 0.50, 1.15, 2.35, 0.26, label="segment"),),
            ),
            dimensions=(
                Dimension(
                    -1.15,
                    0.50,
                    1.15,
                    2.35,
                    "segment midline length",
                    offset=0.34,
                ),
                Dimension(
                    0.15,
                    1.64,
                    0.32,
                    1.43,
                    "thickness",
                    offset=-0.23,
                    label_dx=-28,
                    label_dy=-8,
                    label_anchor="end",
                ),
            ),
            labels={
                "segment": LabelPlacement("segment", offset_y=0.24, offset_z=-0.28, rotate=38),
            },
            note="start_y/start_z and end_y/end_z are midline endpoints.",
        ),
    )


def render_all(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for diagram in diagrams():
        (output_dir / diagram.filename).write_text(render(diagram), encoding="utf-8")


def render(diagram: Diagram) -> str:
    bounds = _bounds(diagram)
    scale, origin_x, origin_y = _transform(bounds)

    def xy(y: float, z: float) -> tuple[float, float]:
        return origin_x + (y - bounds[0]) * scale, origin_y - (z - bounds[1]) * scale

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(diagram.title)}</title>',
        f'<desc id="desc">{escape(diagram.desc)}</desc>',
        *_draw_defs(),
        f'<rect x="0" y="0" width="{WIDTH}" height="{HEIGHT}" fill="#ffffff"/>',
        *_draw_header(diagram),
        *_draw_skin_and_axes(xy),
        *(_draw_segment(segment, xy) for segment in diagram.section.segments),
        *(_draw_dimension(dimension, xy) for dimension in diagram.dimensions),
        _draw_centroid((diagram.section.centroid_y, diagram.section.centroid_z), xy),
        *_draw_segment_labels(diagram.section.segments, diagram.labels, xy),
        *_draw_legend(),
        *_draw_note(diagram.note),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def _bounds(diagram: Diagram) -> tuple[float, float, float, float]:
    ys: list[float] = []
    zs: list[float] = [-0.52, 0.0]
    for segment in diagram.section.segments:
        pad = segment.thickness
        ys.extend(
            [
                segment.start_y - pad,
                segment.start_y + pad,
                segment.end_y - pad,
                segment.end_y + pad,
            ]
        )
        zs.extend(
            [
                segment.start_z - pad,
                segment.start_z + pad,
                segment.end_z - pad,
                segment.end_z + pad,
            ]
        )
    for dimension in diagram.dimensions:
        for y, z in _dimension_points_world(dimension):
            ys.append(y)
            zs.append(z)
    ys.append(diagram.section.centroid_y)
    zs.append(diagram.section.centroid_z)
    min_y = min(ys) - 0.42
    max_y = max(ys) + 0.42
    min_z = min(zs) - 0.34
    max_z = max(zs) + 0.48
    return min_y, min_z, max_y, max_z


def _transform(bounds: tuple[float, float, float, float]) -> tuple[float, float, float]:
    min_y, min_z, max_y, max_z = bounds
    span_y = max_y - min_y
    span_z = max_z - min_z
    available_y = WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    available_z = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    scale = min(available_y / span_y, available_z / span_z)
    origin_x = MARGIN_LEFT + 0.5 * (available_y - span_y * scale)
    origin_y = HEIGHT - MARGIN_BOTTOM - 0.5 * (available_z - span_z * scale)
    return scale, origin_x, origin_y


def _draw_defs() -> list[str]:
    return [
        "<defs>",
        '<linearGradient id="wall-fill" x1="0" y1="0" x2="0" y2="1">',
        '<stop offset="0%" stop-color="#dbeafe"/>',
        '<stop offset="100%" stop-color="#bfdbfe"/>',
        "</linearGradient>",
        '<filter id="wall-shadow" x="-20%" y="-20%" width="140%" height="150%">',
        '<feDropShadow dx="0" dy="1.2" stdDeviation="1.4" flood-color="#0f172a" '
        'flood-opacity="0.18"/>',
        "</filter>",
        '<pattern id="skin-hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">',
        '<rect width="8" height="8" fill="#f8fafc"/>',
        '<line x1="0" y1="0" x2="0" y2="8" stroke="#cbd5e1" stroke-width="2"/>',
        "</pattern>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>',
        "</marker>",
        "</defs>",
    ]


def _draw_header(diagram: Diagram) -> list[str]:
    return [
        f'<text x="28" y="32" {TEXT_STYLE} font-size="20" font-weight="760" '
        f'letter-spacing="0" fill="#0f172a">{escape(diagram.title)}</text>',
        f'<text x="28" y="54" {TEXT_STYLE} font-size="12.5" fill="#475569">'
        f"{escape(diagram.desc)}</text>",
    ]


def _draw_skin_and_axes(xy) -> list[str]:
    _, datum = xy(0.0, 0.0)
    left = 28.0
    right = WIDTH - 28.0
    _, skin_bottom = xy(0.0, -0.42)
    _, ref = xy(0.0, -0.21)
    axis_x = 52.0
    axis_z0 = HEIGHT - MARGIN_BOTTOM - 18.0
    axis_y_end = axis_x + 58.0
    axis_z_end = axis_z0 - 54.0
    return [
        f'<rect x="{left:.2f}" y="{datum:.2f}" width="{right - left:.2f}" '
        f'height="{skin_bottom - datum:.2f}" fill="url(#skin-hatch)" stroke="#cbd5e1" '
        'stroke-width="0.8"/>',
        f'<line x1="{left:.2f}" y1="{datum:.2f}" x2="{right:.2f}" y2="{datum:.2f}" '
        'stroke="#0f172a" stroke-width="1.5" stroke-dasharray="6 5"/>',
        f'<line x1="{left:.2f}" y1="{ref:.2f}" x2="{right:.2f}" y2="{ref:.2f}" '
        'stroke="#64748b" stroke-width="1.2" stroke-dasharray="3 5"/>',
        f'<text x="{right - 190:.2f}" y="{datum - 22:.2f}" {TEXT_STYLE} font-size="12" '
        'fill="#334155">section datum z = 0 / skin face</text>',
        f'<text x="{right - 190:.2f}" y="{skin_bottom + 17:.2f}" {TEXT_STYLE} '
        'font-size="12" fill="#64748b">skin reference surface</text>',
        f'<line x1="{axis_x:.2f}" y1="{axis_z0:.2f}" x2="{axis_y_end:.2f}" y2="{axis_z0:.2f}" '
        'stroke="#334155" stroke-width="1.6" marker-end="url(#arrow)"/>',
        f'<line x1="{axis_x:.2f}" y1="{axis_z0:.2f}" x2="{axis_x:.2f}" y2="{axis_z_end:.2f}" '
        'stroke="#334155" stroke-width="1.6" marker-end="url(#arrow)"/>',
        f'<text x="{axis_y_end + 9:.2f}" y="{axis_z0 + 4:.2f}" {TEXT_STYLE} '
        'font-size="12" fill="#334155">+y</text>',
        f'<text x="{axis_x + 8:.2f}" y="{axis_z_end - 5:.2f}" {TEXT_STYLE} '
        'font-size="12" fill="#334155">+z / +n</text>',
    ]


def _draw_segment(segment: ThinWallSegment, xy) -> str:
    length = segment.length
    unit_y = (segment.end_y - segment.start_y) / length
    unit_z = (segment.end_z - segment.start_z) / length
    normal_y = -unit_z
    normal_z = unit_y
    half_t = 0.5 * segment.thickness
    corners = (
        (segment.start_y + normal_y * half_t, segment.start_z + normal_z * half_t),
        (segment.end_y + normal_y * half_t, segment.end_z + normal_z * half_t),
        (segment.end_y - normal_y * half_t, segment.end_z - normal_z * half_t),
        (segment.start_y - normal_y * half_t, segment.start_z - normal_z * half_t),
    )
    points = " ".join(f"{x:.2f},{y:.2f}" for x, y in (xy(y, z) for y, z in corners))
    mid1 = xy(segment.start_y, segment.start_z)
    mid2 = xy(segment.end_y, segment.end_z)
    return (
        f'<polygon points="{points}" fill="url(#wall-fill)" stroke="#2563eb" '
        'stroke-width="1.8" stroke-linejoin="round" filter="url(#wall-shadow)"/>'
        f'\n<line x1="{mid1[0]:.2f}" y1="{mid1[1]:.2f}" x2="{mid2[0]:.2f}" '
        f'y2="{mid2[1]:.2f}" stroke="#1d4ed8" stroke-width="1" '
        'stroke-dasharray="4 4" opacity="0.55"/>'
    )


def _draw_dimension(dimension: Dimension, xy) -> str:
    start, end, dim_start, dim_end = _dimension_points_world(dimension)
    x1, y1 = xy(*start)
    x2, y2 = xy(*end)
    dx1, dy1 = xy(*dim_start)
    dx2, dy2 = xy(*dim_end)
    tx = 0.5 * (dx1 + dx2)
    ty = 0.5 * (dy1 + dy2)
    label_dx, label_dy, anchor = _dimension_label_offset(dimension, dx1, dy1, dx2, dy2)
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{dx1:.2f}" y2="{dy1:.2f}" '
        'stroke="#94a3b8" stroke-width="1" stroke-dasharray="3 3"/>'
        f'\n<line x1="{x2:.2f}" y1="{y2:.2f}" x2="{dx2:.2f}" y2="{dy2:.2f}" '
        'stroke="#94a3b8" stroke-width="1" stroke-dasharray="3 3"/>'
        f'\n<line x1="{dx1:.2f}" y1="{dy1:.2f}" x2="{dx2:.2f}" y2="{dy2:.2f}" '
        'stroke="#475569" stroke-width="1.3" marker-start="url(#arrow)" '
        'marker-end="url(#arrow)"/>'
        f'\n<text x="{tx + label_dx:.2f}" y="{ty + label_dy:.2f}" {TEXT_STYLE} '
        f'font-size="12" text-anchor="{anchor}" fill="#334155">'
        f"{escape(dimension.label)}</text>"
    )


def _dimension_points_world(
    dimension: Dimension,
) -> tuple[
    tuple[float, float],
    tuple[float, float],
    tuple[float, float],
    tuple[float, float],
]:
    start = (dimension.start_y, dimension.start_z)
    end = (dimension.end_y, dimension.end_z)
    length = ((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5
    unit_y = (end[0] - start[0]) / length
    unit_z = (end[1] - start[1]) / length
    normal_y = -unit_z
    normal_z = unit_y
    dim_start = (
        start[0] + normal_y * dimension.offset,
        start[1] + normal_z * dimension.offset,
    )
    dim_end = (
        end[0] + normal_y * dimension.offset,
        end[1] + normal_z * dimension.offset,
    )
    return start, end, dim_start, dim_end


def _dimension_label_offset(
    dimension: Dimension,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
) -> tuple[float, float, str]:
    label_dx = dimension.label_dx
    label_dy = dimension.label_dy
    anchor = dimension.label_anchor
    if label_dx is None or label_dy is None or anchor is None:
        if abs(x1 - x2) < 4.0:
            sign = -1.0 if dimension.offset > 0.0 else 1.0
            label_dx = 18.0 * sign if label_dx is None else label_dx
            label_dy = 4.0 if label_dy is None else label_dy
            if anchor is None:
                anchor = "end" if sign < 0.0 else "start"
        elif abs(y1 - y2) < 4.0:
            sign = -1.0 if dimension.offset > 0.0 else 1.0
            label_dx = 0.0 if label_dx is None else label_dx
            if label_dy is None:
                label_dy = -8.0 if sign < 0.0 else 17.0
            anchor = "middle" if anchor is None else anchor
        else:
            label_dx = 0.0 if label_dx is None else label_dx
            label_dy = -8.0 if label_dy is None else label_dy
            anchor = "middle" if anchor is None else anchor
    return label_dx, label_dy, anchor


def _draw_centroid(centroid: tuple[float, float], xy) -> str:
    x, y = xy(*centroid)
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7.2" fill="#ffffff" stroke="#dc2626" '
        'stroke-width="1.2"/>'
        f'\n<circle cx="{x:.2f}" cy="{y:.2f}" r="4.3" fill="#dc2626"/>'
        f'\n<line x1="{x - 10:.2f}" y1="{y:.2f}" x2="{x + 10:.2f}" y2="{y:.2f}" '
        'stroke="#dc2626" stroke-width="1.2"/>'
        f'\n<line x1="{x:.2f}" y1="{y - 10:.2f}" x2="{x:.2f}" y2="{y + 10:.2f}" '
        'stroke="#dc2626" stroke-width="1.2"/>'
    )


def _draw_segment_labels(
    segments: tuple[ThinWallSegment, ...],
    placements: Mapping[str, LabelPlacement],
    xy,
) -> list[str]:
    labels: list[str] = []
    for segment in segments:
        placement = placements.get(segment.label)
        if placement is None:
            display_label = segment.label.replace("_", " ") if segment.label else "segment"
            placement = LabelPlacement(display_label)
        mid_y = 0.5 * (segment.start_y + segment.end_y) + placement.offset_y
        mid_z = 0.5 * (segment.start_z + segment.end_z) + placement.offset_z
        x, y = xy(mid_y, mid_z)
        transform = (
            f' transform="rotate({placement.rotate:.1f} {x:.2f} {y:.2f})"'
            if placement.rotate
            else ""
        )
        labels.append(
            f'<text x="{x:.2f}" y="{y:.2f}"{transform} {TEXT_STYLE} font-size="11.5" '
            f'text-anchor="{placement.anchor}" dominant-baseline="middle" '
            f'fill="#1e3a8a">{escape(placement.label)}</text>'
        )
    return labels


def _draw_legend() -> list[str]:
    x = WIDTH - 194.0
    y = 78.0
    return [
        f'<rect x="{x:.2f}" y="{y:.2f}" width="166" height="104" rx="5" '
        'fill="#ffffff" stroke="#cbd5e1"/>',
        f'<text x="{x + 14:.2f}" y="{y + 22:.2f}" {TEXT_STYLE} font-size="12" '
        'font-weight="700" fill="#0f172a">Legend</text>',
        f'<rect x="{x + 14:.2f}" y="{y + 34:.2f}" width="22" height="10" '
        'fill="url(#wall-fill)" stroke="#2563eb" stroke-width="1"/>',
        f'<text x="{x + 44:.2f}" y="{y + 44:.2f}" {TEXT_STYLE} font-size="11.5" '
        'fill="#334155">section wall</text>',
        f'<line x1="{x + 14:.2f}" y1="{y + 58:.2f}" x2="{x + 36:.2f}" y2="{y + 58:.2f}" '
        'stroke="#1d4ed8" stroke-width="1" stroke-dasharray="4 4" opacity="0.7"/>',
        f'<text x="{x + 44:.2f}" y="{y + 62:.2f}" {TEXT_STYLE} font-size="11.5" '
        'fill="#334155">segment midline</text>',
        f'<circle cx="{x + 25:.2f}" cy="{y + 76:.2f}" r="4" fill="#dc2626"/>',
        f'<text x="{x + 44:.2f}" y="{y + 80:.2f}" {TEXT_STYLE} font-size="11.5" '
        'fill="#334155">computed centroid</text>',
        f'<line x1="{x + 14:.2f}" y1="{y + 94:.2f}" x2="{x + 36:.2f}" y2="{y + 94:.2f}" '
        'stroke="#0f172a" stroke-width="1.3" stroke-dasharray="6 5"/>',
        f'<text x="{x + 44:.2f}" y="{y + 98:.2f}" {TEXT_STYLE} font-size="11.5" '
        'fill="#334155">z = 0 datum</text>',
    ]


def _draw_note(note: str) -> list[str]:
    y = HEIGHT - 48.0
    return [
        f'<rect x="28" y="{y:.2f}" width="{WIDTH - 56}" height="32" rx="5" '
        'fill="#f8fafc" stroke="#cbd5e1"/>',
        f'<rect x="28" y="{y:.2f}" width="4" height="32" rx="2" fill="#2563eb"/>',
        f'<text x="44" y="{y + 21:.2f}" {TEXT_STYLE} font-size="12.5" '
        f'fill="#334155">{escape(note)}</text>',
    ]


if __name__ == "__main__":
    render_all()
