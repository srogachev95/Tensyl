"""Draw repeated grids and their translation cells from public builder geometry."""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs" / "examples" / "scripts"))
from pattern_gallery import Pattern, build_patterns  # noqa: E402

DEFAULT_OUTPUT_DIR = ROOT / "docs" / "assets" / "patterns"


def text(x, y, value, size=16, color="#18344a"):
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Arial, Helvetica, sans-serif" '
        f'font-size="{size}" fill="{color}">{escape(value)}</text>'
    )


def repeat_polygon(pattern: Pattern):
    geometry = pattern.cell.geometry
    assert geometry is not None
    a, b = geometry.repeat_vectors
    # Center the orthogrid cell on a rib intersection, as in the walkthrough.
    center = geometry.nodes[0] if pattern.slug in {"orthogrid", "sandwich-orthogrid"} else None
    cx, cy = (center.e1, center.e2) if center else (0, 0)
    return tuple(
        (cx + u * a.e1 + v * b.e1, cy + u * a.e2 + v * b.e2)
        for u, v in ((-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5))
    )


def vector_mm(vector):
    # Adding zero normalizes -0.0 for axis-aligned directions.
    return f"({vector.e1 * 1000 + 0.0:.2f}, {vector.e2 * 1000 + 0.0:.2f})"


def render(pattern: Pattern) -> str:
    geometry = pattern.cell.geometry
    assert geometry is not None
    a, b = geometry.repeat_vectors
    polygon = repeat_polygon(pattern)
    cx = sum(p[0] for p in polygon) / 4
    cy = sum(p[1] for p in polygon) / 4
    span_x = max(p[0] for p in polygon) - min(p[0] for p in polygon)
    span_y = max(p[1] for p in polygon) - min(p[1] for p in polygon)
    parts = [
        (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 550" '
            'role="img" aria-labelledby="title desc">'
        ),
        f'<title id="title">{escape(pattern.title)}</title>',
        (
            '<desc id="desc">Rib centerlines tiled from the cell geometry. The dashed orange '
            "parallelogram spans one pair of repeat vectors; the right view enlarges "
            "that same cell.</desc>"
        ),
        '<rect width="960" height="550" fill="white"/>',
        (
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" '
            'markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" orient="auto">'
            '<path d="M0 0L10 5L0 10Z" fill="#18344a"/></marker></defs>'
        ),
        text(28, 35, pattern.title, 25),
        text(28, 63, pattern.constructor + "(...)", 17),
        text(28, 101, "Repeated layout", 18),
        text(522, 101, "One repeat · enlarged", 18),
    ]
    # A generous set of actual translations covers both windows, including oblique cells.
    segments = geometry.segments(repeat_a=25, repeat_b=25)
    for index, (x, y, w, h) in enumerate(((28, 120, 450, 285), (522, 120, 410, 285))):
        scale = min((w - 64) / span_x, (h - 64) / span_y) / (3 if index == 0 else 1)

        def xy(point, ox=x + w / 2, oy=y + h / 2, scale=scale):
            return ox + (point[0] - cx) * scale, oy - (point[1] - cy) * scale

        points = " ".join(f"{px:.3f},{py:.3f}" for px, py in map(xy, polygon))
        parts.extend(
            [
                (
                    f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" '
                    'fill="#f7fafc" stroke="#d7e1e7"/>'
                ),
                (
                    f'<defs><clipPath id="view{index}"><rect x="{x + 1}" y="{y + 1}" '
                    f'width="{w - 2}" height="{h - 2}"/></clipPath>'
                ),
                f'<clipPath id="cell{index}"><polygon points="{points}"/></clipPath></defs>',
                f'<polygon points="{points}" fill="#fff0e5"/>',
                f'<g clip-path="url(#view{index})">',
            ]
        )
        lines = []
        for segment in segments:
            p = xy((segment.start_e1 - 12 * (a.e1 + b.e1), segment.start_e2 - 12 * (a.e2 + b.e2)))
            q = xy((segment.end_e1 - 12 * (a.e1 + b.e1), segment.end_e2 - 12 * (a.e2 + b.e2)))
            if (
                max(p[0], q[0]) < x
                or min(p[0], q[0]) > x + w
                or max(p[1], q[1]) < y
                or min(p[1], q[1]) > y + h
            ):
                continue
            lines.append(f'<path d="M{p[0]:.3f} {p[1]:.3f}L{q[0]:.3f} {q[1]:.3f}"/>')
        linework = "\n".join(sorted(set(lines)))
        parts.append(
            f'<g fill="none" stroke="{"#a8c4d0" if index else "#176b87"}" '
            f'stroke-width="2" stroke-linecap="round">{linework}</g>'
        )
        if index:
            parts.append(
                f'<g clip-path="url(#cell{index})" fill="none" stroke="#176b87" '
                f'stroke-width="3" stroke-linecap="round">{linework}</g>'
            )
        parts.extend(
            [
                "</g>",
                (
                    f'<polygon points="{points}" fill="none" stroke="#b65020" '
                    'stroke-width="2" stroke-dasharray="7 5"/>'
                ),
            ]
        )
    parts.extend(
        [
            '<path d="M845 70H888" stroke="#18344a" stroke-width="1.5" marker-end="url(#arrow)"/>',
            '<path d="M845 70V30" stroke="#18344a" stroke-width="1.5" marker-end="url(#arrow)"/>',
            text(899, 75, "e1", 15),
            text(834, 20, "e2", 15),
            text(28, 440, pattern.inputs, 16),
            text(
                28,
                470,
                f"Repeat vectors (e1, e2), mm:  a = {vector_mm(a)}   b = {vector_mm(b)}",
                16,
            ),
            text(28, 499, f"Repeat area = {geometry.repeat_area * 1e6:,.1f} mm²", 16),
            '<path d="M28 528H60" stroke="#176b87" stroke-width="3"/>',
            text(70, 533, "Rib centerline", 16),
            '<path d="M250 528H282" stroke="#b65020" stroke-width="2" stroke-dasharray="7 5"/>',
            text(292, 533, "Repeat boundary", 16),
            text(660, 533, "Plan view · equal scale on both axes", 15),
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def render_all(output_dir: Path = DEFAULT_OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for pattern in build_patterns():
        (output_dir / f"{pattern.slug}.svg").write_text(render(pattern), encoding="utf-8")


if __name__ == "__main__":
    render_all()
