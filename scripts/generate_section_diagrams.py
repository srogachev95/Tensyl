"""Generate documentation SVGs for thin-wall stiffener section geometry."""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import hypot
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
class Diagram:
    filename: str
    title: str
    desc: str
    section: ThinWallSection
    dimensions: tuple[Dimension, ...]
    note: str
    closure_thickness: float | None = None


WIDTH = 760
HEIGHT = 540
DUMMY_MATERIAL = IsotropicMaterial(E=1.0, nu=0.3)
SYMBOLS = {
    "height": "h",
    "thickness": "t",
    "web_height": "h_w",
    "web_thickness": "t_w",
    "flange_width": "b_f",
    "flange_thickness": "t_f",
    "crown_width": "b_c",
    "crown_thickness": "t_c",
    "top_flange_width": "b_t",
    "bottom_flange_width": "b_b",
    "segment midline length": "L",
    "closure_thickness": "t_s",
    "median_height": "h_m",
}


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
    wall_segment = ThinWallSegment(-1.15, 0.50, 1.15, 2.35, 0.26, label="segment")

    sections = (
        Diagram(
            filename="blade-section.svg",
            title="Blade section",
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
                    label_dx=65,
                    label_dy=4,
                    label_anchor="start",
                ),
            ),
            note="h runs from the skin face to the free end of the blade.",
        ),
        Diagram(
            filename="tee-section.svg",
            title="Tee section",
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
                    label_dx=65,
                    label_dy=4,
                    label_anchor="start",
                ),
            ),
            note="The web height ends at the underside of the flange.",
        ),
        Diagram(
            filename="zee-section.svg",
            title="Zee section",
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
                    -zee_web_thickness / 2,
                    1.25,
                    zee_web_thickness / 2,
                    1.25,
                    "web_thickness",
                    offset=-0.32,
                    label_dx=65,
                    label_dy=4,
                    label_anchor="start",
                ),
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
            note="Flange widths start at the web midline; web height is the clear gap.",
        ),
        Diagram(
            filename="channel-section.svg",
            title="Channel section",
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
                    label_dx=65,
                    label_dy=4,
                    label_anchor="start",
                ),
            ),
            note="Both flanges extend in +y; web height is the clear distance between them.",
        ),
        Diagram(
            filename="hat-section.svg",
            title="Hat section",
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
                Dimension(
                    hat_half_crown - hat_web_thickness / 2,
                    1.25,
                    hat_half_crown + hat_web_thickness / 2,
                    1.25,
                    "web_thickness",
                    offset=-0.32,
                    label_dx=65,
                    label_dy=4,
                    label_anchor="start",
                ),
            ),
            note="Crown width is between web midlines; web height is the clear gap.",
        ),
        Diagram(
            filename="thin-wall-segment.svg",
            title="Thin-wall segment coordinates",
            desc="A custom thin-wall segment is defined by midline endpoints and thickness.",
            section=thin_wall_section(
                material=DUMMY_MATERIAL,
                segments=(wall_segment,),
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
                _segment_thickness_dimension(wall_segment),
            ),
            note="start_y/start_z and end_y/end_z are midline endpoints.",
        ),
    )
    hat = next(section for section in sections if section.filename == "hat-section.svg")
    closure = 0.20
    closed = hat_section(
        material=DUMMY_MATERIAL,
        web_height=hat_web_height,
        web_thickness=hat_web_thickness,
        crown_width=hat_crown_width,
        crown_thickness=hat_crown_thickness,
        flange_width=hat_flange_width,
        flange_thickness=hat_flange_thickness,
        closure_thickness=closure,
    )
    return (
        *sections,
        replace(
            hat,
            filename="closed-hat-section.svg",
            title="Hat closed by the skin",
            desc="The skin completes the median shear-flow path around the enclosed area.",
            section=closed,
            closure_thickness=closure,
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
                    -hat_half_crown,
                    -closure / 2,
                    -hat_half_crown,
                    hat_crown_z,
                    "median_height",
                    offset=0.75,
                ),
                Dimension(
                    hat_half_crown + hat_flange_width,
                    -closure,
                    hat_half_crown + hat_flange_width,
                    0,
                    "closure_thickness",
                    offset=-0.45,
                    label_dx=18,
                    label_dy=33,
                    label_anchor="start",
                ),
            ),
            note="The orange median path defines the enclosed area used in Bredt torsion.",
        ),
    )


def render_all(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for diagram in diagrams():
        (output_dir / diagram.filename).write_text(render(diagram), encoding="utf-8")


def _segment_thickness_dimension(segment: ThinWallSegment) -> Dimension:
    # Place both endpoints on the wall faces, exactly normal to its midline.
    dy = segment.end_y - segment.start_y
    dz = segment.end_z - segment.start_z
    thickness = segment.thickness
    length = hypot(dy, dz)
    ny, nz = -dz / length, dy / length
    y, z = segment.start_y + 0.72 * dy, segment.start_z + 0.72 * dz
    return Dimension(
        y + ny * thickness / 2,
        z + nz * thickness / 2,
        y - ny * thickness / 2,
        z - nz * thickness / 2,
        "thickness",
        offset=0.75,
        label_dx=20,
        label_dy=15,
        label_anchor="start",
    )


def _label(value: str) -> str:
    """Use compact engineering symbols, with proper SVG subscripts."""
    symbol = SYMBOLS.get(value, value)
    if "_" not in symbol:
        return escape(symbol)
    base, subscript = symbol.split("_", 1)
    return f'{escape(base)}<tspan baseline-shift="sub" font-size="13">{escape(subscript)}</tspan>'


def _text(x, y, label, *, size=17, anchor="start", color="#18344a", symbol=False):
    content = _label(label) if symbol else escape(label)
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" fill="{color}">{content}</text>'
    )


def _line(a, b, *, color="#71828c", width=1, dash=False, dimension=False):
    attrs = ' stroke-dasharray="6 4"' if dash else ""
    if dimension:
        attrs += ' marker-start="url(#arrow)" marker-end="url(#arrow)"'
    return (
        f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" '
        f'stroke="{color}" stroke-width="{width}"{attrs}/>'
    )


def wall_corners(segment: ThinWallSegment):
    """Wall face coordinates calculated normal to its centerline."""
    ny = -(segment.end_z - segment.start_z) / segment.length
    nz = (segment.end_y - segment.start_y) / segment.length
    half = segment.thickness / 2
    return (
        (segment.start_y + ny * half, segment.start_z + nz * half),
        (segment.end_y + ny * half, segment.end_z + nz * half),
        (segment.end_y - ny * half, segment.end_z - nz * half),
        (segment.start_y - ny * half, segment.start_z - nz * half),
    )


def render(diagram: Diagram) -> str:
    corners = [point for segment in diagram.section.segments for point in wall_corners(segment)]
    min_y, max_y = min(p[0] for p in corners), max(p[0] for p in corners)
    max_z = max(p[1] for p in corners)
    scale = min(235 / max_z, 330 / (max_y - min_y))
    origin_x = 340 - (min_y + max_y) * scale / 2

    def xy(y, z):
        return origin_x + y * scale, 380 - z * scale

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(diagram.title)}</title>',
        f'<desc id="desc">{escape(diagram.desc)}</desc>',
        "<defs>",
        (
            '<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" '
            'markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" '
            'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#18344a"/></marker>'
        ),
        '<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)"><path d="M0 0V8" stroke="#bdcbd3" stroke-width="2"/>'
        "</pattern>",
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>',
        _text(28, 34, diagram.title, size=23),
        _text(28, 62, diagram.desc, size=15),
    ]
    custom = diagram.filename == "thin-wall-segment.svg"
    skin_height = scale * (diagram.closure_thickness or 0.16)
    if not custom:
        parts.extend(
            [
                f'<rect x="140" y="380" width="564" height="{skin_height:.2f}" '
                'fill="#f3f6f8" stroke="#a2b1ba"/>',
                (
                    f'<rect x="140" y="380" width="564" height="{skin_height:.2f}" '
                    'fill="url(#hatch)"/>'
                ),
                _text(704, 368, "Skin face · z = 0", anchor="end", size=16),
            ]
        )
    else:
        parts.extend(
            [
                _line((140, 380), (704, 380), dash=True),
                _text(704, 404, "Construction datum · z = 0", anchor="end", size=16),
            ]
        )
    # Axes are a separate orientation key; dimensions use the datum above.
    parts.extend(
        [
            '<path d="M62 414V354" fill="none" stroke="#18344a" '
            'stroke-width="1.5" marker-end="url(#arrow)"/>',
            '<path d="M62 414H112" fill="none" stroke="#18344a" '
            'stroke-width="1.5" marker-end="url(#arrow)"/>',
            _text(120, 420, "+y"),
            _text(44, 342, "+z"),
        ]
    )
    for segment in diagram.section.segments:
        points = " ".join(
            f"{x:.2f},{y:.2f}" for x, y in map(lambda p: xy(*p), wall_corners(segment))
        )
        parts.extend(
            [
                f'<polygon points="{points}" fill="#dfedf3" stroke="#176b87" stroke-width="2"/>',
                _line(
                    xy(segment.start_y, segment.start_z),
                    xy(segment.end_y, segment.end_z),
                    color="#176b87",
                    dash=True,
                ),
            ]
        )
    if diagram.closure_thickness is not None:
        crown = next(s for s in diagram.section.segments if s.label == "crown")
        left, right = crown.start_y, crown.end_y
        bottom, top = -diagram.closure_thickness / 2, crown.start_z
        points = [xy(left, bottom), xy(right, bottom), xy(right, top), xy(left, top)]
        path = " ".join(f"{x:.2f},{y:.2f}" for x, y in [*points, points[0]])
        parts.extend(
            [
                f'<polyline points="{path}" fill="none" stroke="#b65020" stroke-width="2" '
                'stroke-dasharray="7 4"/>',
                _text(
                    *xy(0, (bottom + top) / 2 + 0.85), "A_m", size=22, anchor="middle", symbol=True
                ),
            ]
        )
    for dimension in diagram.dimensions:
        parts.extend(_dimension(dimension, xy))
    cx, cy = xy(diagram.section.centroid_y, diagram.section.centroid_z)
    parts.extend(
        [
            (
                f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="5" fill="#b65020" '
                'stroke="white" stroke-width="1"/>'
            ),
            _text(
                cx + (55 if custom else 20),
                cy + (38 if custom else -9),
                "C",
                color="#b65020",
                size=20,
            ),
        ]
    )
    if custom:
        parts.append(_line((cx + 5, cy + 5), (cx + 48, cy + 30), color="#b65020"))
        segment = diagram.section.segments[0]
        for point, label, offset in [
            ((segment.start_y, segment.start_z), "(start_y, start_z)", (-110, 28)),
            ((segment.end_y, segment.end_z), "(end_y, end_z)", (24, -18)),
        ]:
            x, y = xy(*point)
            parts.extend(
                [
                    f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#18344a"/>',
                    _text(x + offset[0], y + offset[1], label, size=16),
                ]
            )
    parts.extend(
        [
            _line((28, 458), (732, 458), color="#d7e1e7"),
            '<rect x="32" y="477" width="22" height="10" fill="#dfedf3" stroke="#176b87"/>',
            _text(64, 488, "Section wall", size=16),
            _line((246, 482), (276, 482), color="#176b87", dash=True),
            _text(287, 488, "Wall midline", size=16),
            '<circle cx="495" cy="482" r="4" fill="#b65020"/>',
            _text(510, 488, "C · computed centroid", size=16),
            _text(28, 522, diagram.note, size=15),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def _dimension_points_world(dimension: Dimension):
    start = (dimension.start_y, dimension.start_z)
    end = (dimension.end_y, dimension.end_z)
    length = hypot(end[0] - start[0], end[1] - start[1])
    normal = (-(end[1] - start[1]) / length, (end[0] - start[0]) / length)
    return (
        start,
        end,
        (
            start[0] + normal[0] * dimension.offset,
            start[1] + normal[1] * dimension.offset,
        ),
        (
            end[0] + normal[0] * dimension.offset,
            end[1] + normal[1] * dimension.offset,
        ),
    )


def _dimension(dimension, xy):
    start, end, first, last = [xy(*p) for p in _dimension_points_world(dimension)]
    tx, ty = (first[0] + last[0]) / 2, (first[1] + last[1]) / 2
    vertical = abs(first[0] - last[0]) < 1
    dx = dimension.label_dx
    dy = dimension.label_dy
    anchor = dimension.label_anchor
    if dx is None:
        dx = (-18 if dimension.offset > 0 else 18) if vertical else 0
    if dy is None:
        dy = 5 if vertical else (-12 if dimension.offset > 0 else 24)
    if anchor is None:
        anchor = ("end" if dx < 0 else "start") if vertical else "middle"
    parts = [
        _line(start, first),
        _line(end, last),
        _line(first, last, color="#18344a", dimension=True),
    ]
    if dimension.label in {"thickness", "web_thickness"} and abs(first[1] - last[1]) < 1:
        parts.append(_line((max(first[0], last[0]), ty), (tx + dx - 7, ty)))
    parts.append(_text(tx + dx, ty + dy, dimension.label, size=20, anchor=anchor, symbol=True))
    return parts


if __name__ == "__main__":
    render_all()
