"""Generate documentation SVGs for thin-wall stiffener section geometry."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = ROOT / "docs" / "assets" / "sections"


@dataclass(frozen=True, slots=True)
class Segment:
    start_y: float
    start_z: float
    end_y: float
    end_z: float
    thickness: float
    label: str


@dataclass(frozen=True, slots=True)
class Dimension:
    start_y: float
    start_z: float
    end_y: float
    end_z: float
    label: str
    offset: float = 0.0


@dataclass(frozen=True, slots=True)
class Diagram:
    filename: str
    title: str
    desc: str
    segments: tuple[Segment, ...]
    dimensions: tuple[Dimension, ...]
    centroid: tuple[float, float]
    note: str


WIDTH = 680
HEIGHT = 430
MARGIN_X = 82
MARGIN_TOP = 54
MARGIN_BOTTOM = 82


def diagrams() -> tuple[Diagram, ...]:
    return (
        Diagram(
            filename="blade-section.svg",
            title="blade_section geometry",
            desc="A blade web rises in positive z from the skin-face construction datum.",
            segments=(Segment(0.0, 0.0, 0.0, 3.2, 0.34, "blade web"),),
            dimensions=(
                Dimension(0.0, 0.0, 0.0, 3.2, "height", offset=-0.72),
                Dimension(-0.17, 1.05, 0.17, 1.05, "thickness", offset=0.25),
            ),
            centroid=(0.0, 1.6),
            note="Web root touches z = 0; centroid_z is measured upward from that datum.",
        ),
        Diagram(
            filename="tee-section.svg",
            title="tee_section geometry",
            desc="A tee section has a web rooted at z = 0 and a flange above the web.",
            segments=(
                Segment(0.0, 0.0, 0.0, 2.7, 0.24, "web"),
                Segment(-1.25, 2.85, 1.25, 2.85, 0.30, "flange"),
            ),
            dimensions=(
                Dimension(0.0, 0.0, 0.0, 2.7, "web_height", offset=-0.58),
                Dimension(-1.25, 3.34, 1.25, 3.34, "flange_width"),
                Dimension(1.42, 2.70, 1.42, 3.00, "flange_thickness"),
                Dimension(-0.12, 1.1, 0.12, 1.1, "web_thickness", offset=0.25),
            ),
            centroid=(0.0, 1.83),
            note="The flange is on the +z side of the web.",
        ),
        Diagram(
            filename="zee-section.svg",
            title="zee_section geometry",
            desc="A zee section has bottom and top flanges on opposite sides of the web.",
            segments=(
                Segment(-1.35, 0.15, 0.0, 0.15, 0.30, "bottom flange"),
                Segment(0.0, 0.30, 0.0, 2.65, 0.24, "web"),
                Segment(0.0, 2.80, 1.18, 2.80, 0.30, "top flange"),
            ),
            dimensions=(
                Dimension(-1.35, -0.34, 0.0, -0.34, "bottom_flange_width"),
                Dimension(0.0, 3.28, 1.18, 3.28, "top_flange_width"),
                Dimension(0.0, 0.30, 0.0, 2.65, "web_height", offset=-0.58),
                Dimension(1.35, 2.65, 1.35, 2.95, "flange_thickness"),
            ),
            centroid=(-0.08, 1.35),
            note="Bottom and top flanges point to opposite sides in y.",
        ),
        Diagram(
            filename="channel-section.svg",
            title="channel_section geometry",
            desc="A channel section has top and bottom flanges on the same side of the web.",
            segments=(
                Segment(0.0, 0.15, 1.35, 0.15, 0.30, "bottom flange"),
                Segment(0.0, 0.30, 0.0, 2.65, 0.24, "web"),
                Segment(0.0, 2.80, 1.35, 2.80, 0.30, "top flange"),
            ),
            dimensions=(
                Dimension(0.0, -0.34, 1.35, -0.34, "flange_width"),
                Dimension(0.0, 0.30, 0.0, 2.65, "web_height", offset=-0.58),
                Dimension(1.56, 2.65, 1.56, 2.95, "flange_thickness"),
                Dimension(-0.12, 1.25, 0.12, 1.25, "web_thickness", offset=-0.24),
            ),
            centroid=(0.46, 1.45),
            note="Both flanges extend to the same +y side.",
        ),
        Diagram(
            filename="hat-section.svg",
            title="hat_section geometry",
            desc="An open hat section rises in positive z with lower mounting flanges at z = 0.",
            segments=(
                Segment(-1.60, 0.13, -0.75, 0.13, 0.26, "left flange"),
                Segment(-0.75, 0.26, -0.75, 2.55, 0.22, "left web"),
                Segment(-0.75, 2.70, 0.75, 2.70, 0.30, "crown"),
                Segment(0.75, 0.26, 0.75, 2.55, 0.22, "right web"),
                Segment(0.75, 0.13, 1.60, 0.13, 0.26, "right flange"),
            ),
            dimensions=(
                Dimension(-0.75, 3.18, 0.75, 3.18, "crown_width"),
                Dimension(-1.60, -0.32, -0.75, -0.32, "flange_width"),
                Dimension(-0.75, 0.26, -0.75, 2.55, "web_height", offset=-0.50),
                Dimension(0.93, 2.55, 0.93, 2.85, "crown_thickness"),
                Dimension(1.79, 0.00, 1.79, 0.26, "flange_thickness"),
            ),
            centroid=(0.0, 1.24),
            note="The hat is not flipped downward; mounting flanges sit on the skin-face datum.",
        ),
        Diagram(
            filename="thin-wall-segment.svg",
            title="thin_wall_section segment coordinates",
            desc="A custom thin-wall segment is defined by midline endpoints and thickness.",
            segments=(Segment(-1.15, 0.50, 1.15, 2.35, 0.26, "segment"),),
            dimensions=(
                Dimension(-1.15, 0.50, 1.15, 2.35, "segment midline length"),
                Dimension(0.15, 1.64, 0.32, 1.43, "thickness"),
            ),
            centroid=(0.0, 1.425),
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
        "<defs>",
        '<marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#475569"/>',
        "</marker>",
        "</defs>",
        '<rect x="0" y="0" width="680" height="430" fill="#ffffff"/>',
        *_draw_header(diagram),
        *_draw_skin_and_axes(xy, bounds),
        *(_draw_segment(segment, xy) for segment in diagram.segments),
        *(_draw_dimension(dimension, xy) for dimension in diagram.dimensions),
        _draw_centroid(diagram.centroid, xy),
        *_draw_segment_labels(diagram.segments, xy),
        *_draw_note(diagram.note),
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def _bounds(diagram: Diagram) -> tuple[float, float, float, float]:
    ys: list[float] = []
    zs: list[float] = [-0.45, 0.0]
    for segment in diagram.segments:
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
        ys.extend([dimension.start_y, dimension.end_y])
        zs.extend([dimension.start_z, dimension.end_z])
    ys.append(diagram.centroid[0])
    zs.append(diagram.centroid[1])
    min_y = min(ys) - 0.55
    max_y = max(ys) + 0.55
    min_z = min(zs) - 0.40
    max_z = max(zs) + 0.52
    return min_y, min_z, max_y, max_z


def _transform(bounds: tuple[float, float, float, float]) -> tuple[float, float, float]:
    min_y, min_z, max_y, max_z = bounds
    span_y = max_y - min_y
    span_z = max_z - min_z
    available_y = WIDTH - 2 * MARGIN_X
    available_z = HEIGHT - MARGIN_TOP - MARGIN_BOTTOM
    scale = min(available_y / span_y, available_z / span_z)
    origin_x = MARGIN_X + 0.5 * ((WIDTH - 2 * MARGIN_X) - span_y * scale)
    origin_y = HEIGHT - MARGIN_BOTTOM - 0.5 * (available_z - span_z * scale)
    return scale, origin_x, origin_y


def _draw_header(diagram: Diagram) -> list[str]:
    return [
        f'<text x="28" y="34" class="title" font-family="Inter, Arial, sans-serif" '
        f'font-size="20" font-weight="700" fill="#0f172a">{escape(diagram.title)}</text>',
    ]


def _draw_skin_and_axes(xy, bounds: tuple[float, float, float, float]) -> list[str]:
    _, datum = xy(0.0, 0.0)
    left = 28.0
    right = WIDTH - 28.0
    _, skin_bottom = xy(0.0, -0.42)
    _, ref = xy(0.0, -0.21)
    axis_world_y = bounds[0] + 0.45
    axis_x, axis_z0 = xy(axis_world_y, 0.0)
    axis_y_end, _ = xy(axis_world_y + 0.80, 0.0)
    _, axis_z_end = xy(axis_world_y, 0.75)
    return [
        f'<rect x="{left:.2f}" y="{datum:.2f}" width="{right - left:.2f}" '
        f'height="{skin_bottom - datum:.2f}" fill="#e2e8f0"/>',
        f'<line x1="{left:.2f}" y1="{datum:.2f}" x2="{right:.2f}" y2="{datum:.2f}" '
        'stroke="#0f172a" stroke-width="1.5" stroke-dasharray="5 4"/>',
        f'<line x1="{left:.2f}" y1="{ref:.2f}" x2="{right:.2f}" y2="{ref:.2f}" '
        'stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3 5"/>',
        f'<text x="{right - 208:.2f}" y="{datum - 8:.2f}" font-family="Inter, Arial, sans-serif" '
        'font-size="12" fill="#334155">section datum z = 0 / skin face</text>',
        f'<text x="{right - 208:.2f}" y="{ref - 8:.2f}" font-family="Inter, Arial, sans-serif" '
        'font-size="12" fill="#64748b">skin reference surface</text>',
        f'<line x1="{axis_x:.2f}" y1="{axis_z0:.2f}" x2="{axis_y_end:.2f}" y2="{axis_z0:.2f}" '
        'stroke="#334155" stroke-width="1.6" marker-end="url(#arrow)"/>',
        f'<line x1="{axis_x:.2f}" y1="{axis_z0:.2f}" x2="{axis_x:.2f}" y2="{axis_z_end:.2f}" '
        'stroke="#334155" stroke-width="1.6" marker-end="url(#arrow)"/>',
        f'<text x="{axis_y_end + 8:.2f}" y="{axis_z0 + 4:.2f}" '
        'font-family="Inter, Arial, sans-serif" '
        'font-size="12" fill="#334155">+y</text>',
        f'<text x="{axis_x + 7:.2f}" y="{axis_z_end - 5:.2f}" '
        'font-family="Inter, Arial, sans-serif" '
        'font-size="12" fill="#334155">+z / +n</text>',
    ]


def _draw_segment(segment: Segment, xy) -> str:
    length = (
        (segment.end_y - segment.start_y) ** 2 + (segment.end_z - segment.start_z) ** 2
    ) ** 0.5
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
        f'<polygon points="{points}" fill="#bfdbfe" stroke="#1d4ed8" stroke-width="1.8"/>'
        f'\n<line x1="{mid1[0]:.2f}" y1="{mid1[1]:.2f}" x2="{mid2[0]:.2f}" y2="{mid2[1]:.2f}" '
        'stroke="#1e3a8a" stroke-width="1" stroke-dasharray="4 3"/>'
    )


def _draw_dimension(dimension: Dimension, xy) -> str:
    start_y = dimension.start_y
    start_z = dimension.start_z
    end_y = dimension.end_y
    end_z = dimension.end_z
    if abs(start_y - end_y) < 1.0e-12:
        start_y += dimension.offset
        end_y += dimension.offset
    elif abs(start_z - end_z) < 1.0e-12:
        start_z += dimension.offset
        end_z += dimension.offset
    x1, y1 = xy(start_y, start_z)
    x2, y2 = xy(end_y, end_z)
    tx = 0.5 * (x1 + x2)
    ty = 0.5 * (y1 + y2) - 8
    if abs(x1 - x2) < 4:
        tx += 13
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        'stroke="#475569" stroke-width="1.3" marker-start="url(#arrow)" marker-end="url(#arrow)"/>'
        f'\n<text x="{tx:.2f}" y="{ty:.2f}" font-family="Inter, Arial, sans-serif" font-size="12" '
        f'text-anchor="middle" fill="#334155">{escape(dimension.label)}</text>'
    )


def _draw_centroid(centroid: tuple[float, float], xy) -> str:
    x, y = xy(*centroid)
    return (
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="#dc2626"/>'
        f'\n<line x1="{x - 9:.2f}" y1="{y:.2f}" x2="{x + 9:.2f}" y2="{y:.2f}" '
        'stroke="#dc2626" stroke-width="1.2"/>'
        f'\n<line x1="{x:.2f}" y1="{y - 9:.2f}" x2="{x:.2f}" y2="{y + 9:.2f}" '
        'stroke="#dc2626" stroke-width="1.2"/>'
        f'\n<text x="{x + 12:.2f}" y="{y - 10:.2f}" font-family="Inter, Arial, sans-serif" '
        'font-size="12" fill="#991b1b">centroid zc</text>'
    )


def _draw_segment_labels(segments: tuple[Segment, ...], xy) -> list[str]:
    labels: list[str] = []
    for segment in segments:
        mid_y = 0.5 * (segment.start_y + segment.end_y)
        mid_z = 0.5 * (segment.start_z + segment.end_z)
        x, y = xy(mid_y, mid_z)
        labels.append(
            f'<text x="{x:.2f}" y="{y + 18:.2f}" font-family="Inter, Arial, sans-serif" '
            f'font-size="11" text-anchor="middle" fill="#1e3a8a">{escape(segment.label)}</text>'
        )
    return labels


def _draw_note(note: str) -> list[str]:
    return [
        '<rect x="28" y="374" width="624" height="34" rx="4" fill="#f8fafc" stroke="#cbd5e1"/>',
        f'<text x="42" y="396" font-family="Inter, Arial, sans-serif" font-size="13" '
        f'fill="#334155">{escape(note)}</text>',
    ]


if __name__ == "__main__":
    render_all()
