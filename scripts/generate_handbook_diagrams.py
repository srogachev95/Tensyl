"""Render the handbook schematics from model geometry and analytic deformations.

Run with ``uv run python scripts/generate_handbook_diagrams.py``. Coordinates
are physical until the final drawing transform. SVG text stays selectable.
"""

from __future__ import annotations

from math import cos, pi, sin
from pathlib import Path
from runpy import run_path
from xml.sax.saxutils import escape

import numpy as np

from tensyl import Cylinder

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/assets/diagrams"
INK = "#18344a"
BLUE = "#176b87"
PALE = "#e6f0f5"
ORANGE = "#b65020"
GRAY = "#72838d"


class Drawing:
    """Small SVG writer; geometry and annotation placement live in each figure."""

    def __init__(self, title: str, desc: str, height: int):
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 {height}" '
            'role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(desc)}</desc>',
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" markerUnits="userSpaceOnUse" '
            'orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" '
            f'fill="{INK}"/></marker></defs>',
            f'<rect width="760" height="{height}" fill="white"/>',
            '<g font-family="Arial, Helvetica, sans-serif" font-size="18" '
            f'fill="{INK}" stroke-linejoin="round">',
        ]

    def line(self, points, *, color=BLUE, width=2, dash=False, arrow=False, both=False):
        attrs = f'fill="none" stroke="{color}" stroke-width="{width}"'
        if dash:
            attrs += ' stroke-dasharray="5 5"'
        if arrow or both:
            attrs += ' marker-end="url(#arrow)"'
        if both:
            attrs += ' marker-start="url(#arrow)"'
        self.parts.append(f'<polyline points="{self.points(points)}" {attrs}/>')

    @staticmethod
    def points(points):
        return " ".join(f"{x:.3f},{y:.3f}" for x, y in points)

    def polygon(self, points, *, fill=PALE, color=BLUE, width=1.5):
        self.parts.append(
            f'<polygon points="{self.points(points)}" fill="{fill}" '
            f'stroke="{color}" stroke-width="{width}"/>'
        )

    def text(self, x, y, text, *, size=18, color=INK, anchor="start", bold=False):
        self.parts.append(
            f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}" '
            f'text-anchor="{anchor}" font-weight="{600 if bold else 400}">'
            f"{escape(text)}</text>"
        )

    def dot(self, point, *, color=ORANGE, radius=4):
        x, y = point
        self.parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" fill="{color}"/>')

    def dimension(self, a, b, delta, label, label_position):
        p = np.asarray(a) + delta
        q = np.asarray(b) + delta
        self.line([a, p], color=GRAY, width=1)
        self.line([b, q], color=GRAY, width=1)
        self.line([p, q], color=INK, width=1, both=True)
        self.text(*label_position, label, size=16, anchor="middle")

    def finish(self):
        return "\n".join([*self.parts, "</g>", "</svg>", ""])


def grid(d, cell, origin, scale, repeats=1, *, highlight=False):
    """Draw node-centered repeats using the model's two orthogrid pitches.

    Translating the repeat boundary by half a pitch in each direction places
    one complete rib cross inside each cell. The physical rib density is unchanged.
    """
    p, q = cell.metadata["e1_pitch"], cell.metadata["e2_pitch"]

    def xy(x, y):
        return origin[0] + (x + p / 2) * scale, origin[1] - (y + q / 2) * scale

    outline = [
        xy(-p / 2, -q / 2),
        xy((repeats - 0.5) * p, -q / 2),
        xy((repeats - 0.5) * p, (repeats - 0.5) * q),
        xy(-p / 2, (repeats - 0.5) * q),
    ]
    d.polygon(outline, color=GRAY if repeats > 1 else "none", width=1)
    center = (repeats - 1) / 2
    boundary = [
        xy(x * p, y * q)
        for x, y in [
            (center - 0.5, center - 0.5),
            (center + 0.5, center - 0.5),
            (center + 0.5, center + 0.5),
            (center - 0.5, center + 0.5),
        ]
    ]
    if highlight or repeats == 1:
        d.polygon(boundary, fill="#fbe9dc", color="none")
    for i in range(repeats):
        d.line([xy(i * p, -q / 2), xy(i * p, (repeats - 0.5) * q)], width=4)
        d.line([xy(-p / 2, i * q), xy((repeats - 0.5) * p, i * q)], width=4)
    if highlight or repeats == 1:
        d.line([*boundary, boundary[0]], color=ORANGE, dash=True)
    return xy


def panel_model(example):
    d = Drawing(
        "From ribbed panel to equivalent plate",
        "An orthogrid with a repeat cell centered on a rib intersection. Solid lines "
        "are ribs; the dashed cell boundary lies halfway to neighboring nodes.",
        340,
    )
    cell = example["cell"]
    p, q = cell.metadata["e1_pitch"], cell.metadata["e2_pitch"]
    for x, title in [(24, "1  Repeating panel"), (315, "2  One cell"), (563, "3  Plate model")]:
        d.text(x, 35, title, bold=True)
    grid(d, cell, (24, 244), 520, repeats=3, highlight=True)
    grid(d, cell, (325, 225), 1200)
    d.line([(275, 165), (307, 165)], color=INK, arrow=True)
    d.line([(518, 165), (550, 165)], color=INK, arrow=True)
    d.polygon([(560, 105), (740, 105), (740, 225), (560, 225)])
    d.text(650, 156, "A · B · D", anchor="middle", size=24)
    d.text(650, 192, "As", anchor="middle", size=24)
    d.text(141, 282, "Skin and ribs · plan view", anchor="middle", size=16)
    d.text(415, 282, f"{p * 1000:g} × {q * 1000:g} mm", anchor="middle", size=16)
    d.text(650, 282, "Energy per unit area", anchor="middle", size=16)
    d.text(24, 319, "Solid blue: ribs. Dashed orange: repeat-cell boundary.", size=16)
    return d.finish()


def repeat_offset(example):
    d = Drawing(
        "Repeat dimensions and rib eccentricity",
        "A 150 by 100 mm orthogrid cell centered on a rib intersection, with a dashed "
        "boundary halfway to neighboring nodes, and a true-scale section through "
        "a 25 mm blade on a 2 mm skin. The rib centroid is 13.5 mm above the skin midplane.",
        390,
    )
    d.text(26, 34, "Repeat cell · plan view", bold=True)
    d.text(405, 34, "Blade on skin · section view", bold=True)
    cell = example["cell"]
    p, q = cell.metadata["e1_pitch"], cell.metadata["e2_pitch"]
    xy = grid(d, cell, (55, 241), 1500)
    d.dimension(
        xy(-p / 2, -q / 2), xy(p / 2, -q / 2), (0, 32), f"{p * 1000:g} mm along e1", (167.5, 299)
    )
    d.dimension(xy(p / 2, -q / 2), xy(p / 2, q / 2), (35, 0), f"{q * 1000:g} mm", (324, 74))
    d.line([(55, 64), (110, 64)], color=INK, arrow=True)
    d.text(120, 70, "e1", size=16)
    d.line([(26, 241), (26, 190)], color=INK, arrow=True)
    d.text(15, 178, "e2", size=16)
    scale = 5500  # SVG units per metre; identical scale for y and z.
    origin = np.array([518, 260])

    def yz(y, z):
        return origin + scale * np.array([y, -z])

    t = example["skin_thickness"]
    segment = example["rib"].segments[0]
    h, web = segment.length, segment.thickness
    z = example["centroid_offset"]
    d.polygon([yz(-0.017, -t / 2), yz(0.025, -t / 2), yz(0.025, t / 2), yz(-0.017, t / 2)])
    d.polygon(
        [yz(-web / 2, t / 2), yz(web / 2, t / 2), yz(web / 2, t / 2 + h), yz(-web / 2, t / 2 + h)]
    )
    d.line([yz(-0.019, 0), yz(0.028, 0)], color=INK, width=1, dash=True)
    d.dot(yz(0, z))
    d.line([yz(0, z), yz(0.013, z)], color=ORANGE, width=1, dash=True)
    d.dimension(yz(0.013, 0), yz(0.013, z), (0, 0), f"zₐ = {z * 1000:g} mm", (674, 220))
    d.dimension(
        yz(-web / 2, t / 2), yz(-web / 2, t / 2 + h), (-30, 0), f"{h * 1000:g} mm", (444, 195)
    )
    d.dimension(
        yz(-web / 2, t / 2 + h),
        yz(web / 2, t / 2 + h),
        (0, -28),
        f"{web * 1000:g} mm web",
        (518, 74),
    )
    d.text(560, 173, "Rib centroid", color=ORANGE, size=16)
    d.line([yz(0.02, -t / 2), (647, 291), (680, 291)], color=GRAY, width=1)
    d.text(687, 297, f"{t * 1000:g} mm", size=16)
    d.text(427, 323, "Skin midplane: z = 0", size=16)
    d.line([(711, 160), (711, 104)], color=INK, arrow=True)
    d.text(711, 91, "+n", size=16, anchor="middle")
    d.text(26, 367, "Dashed boundary: halfway to the neighboring rib intersections.", size=16)
    return d.finish()


def projection(points, elevation=pi / 6):
    """Orthographic camera: equal world lengths use one common drawing scale."""
    right = np.array([cos(pi / 6), -sin(pi / 6), 0])
    up = np.array([sin(pi / 6) * sin(elevation), cos(pi / 6) * sin(elevation), cos(elevation)])
    return np.asarray(points) @ np.array([right, -up]).T


def deformation(mode, x, y):
    """Illustrative midsurfaces; curvature signs follow epsilon(z)=epsilon0+z*kappa."""
    if mode == "stretch":
        return (1.25 * x, y, 0.0)
    if mode == "bend":
        return (x, y, -0.35 * x * x)
    if mode == "twist":
        return (x, y, -0.4 * x * y)
    raise ValueError(mode)


def deformations():
    d = Drawing(
        "Plate deformation modes",
        "Extension, cylindrical bending, saddle-shaped twisting, and transverse "
        "shear through the thickness. Dashed outlines show the undeformed state.",
        560,
    )
    d.text(24, 32, "Plate deformation modes", bold=True)
    d.text(24, 58, "Deformations are enlarged for clarity.", size=16)
    for mode, center, title, subtitle in [
        ("stretch", (189, 177), "Stretching · A", "In-plane extension"),
        ("bend", (570, 177), "Bending · D", "Curvature in one direction"),
        ("twist", (189, 410), "Twisting · D", "Opposite corners move together"),
    ]:
        origin = np.array(center)

        def project(points, origin=origin):
            return origin + 69 * projection(points)

        corners = [(-1, -0.65), (1, -0.65), (1, 0.65), (-1, 0.65)]
        d.line(
            project([(x, y, 0) for x, y in [*corners, corners[0]]]), color=GRAY, dash=True, width=1
        )
        # A sampled perimeter and grid represent a smooth, single-valued surface.
        boundary = []
        for a, b in zip(corners, [*corners[1:], corners[0]], strict=True):
            boundary.extend(deformation(mode, *p) for p in np.linspace(a, b, 25))
        d.polygon(project(boundary))
        for x in np.linspace(-1, 1, 7):
            d.line(
                project([deformation(mode, x, y) for y in np.linspace(-0.65, 0.65, 31)]), width=1
            )
        for y in np.linspace(-0.65, 0.65, 5):
            d.line(project([deformation(mode, x, y) for x in np.linspace(-1, 1, 41)]), width=1)
        if mode == "stretch":
            for sign in [-1, 1]:
                d.line(project([(1.3 * sign, 0, 0), (1.75 * sign, 0, 0)]), arrow=True)
        d.text(center[0], center[1] + 82, title, bold=True, anchor="middle")
        d.text(center[0], center[1] + 107, subtitle, size=16, anchor="middle")
    # Pure engineering shear u1 = gamma13*z: horizontal faces remain parallel.
    center = np.array([554, 410])
    scale, gamma = 70, 0.55

    def shear(x, z, g):
        return center + scale * np.array([x + g * z, -z])

    corners = [(-1, -0.5), (1, -0.5), (1, 0.5), (-1, 0.5)]
    d.polygon([shear(x, z, gamma) for x, z in corners])
    d.line([shear(x, z, 0) for x, z in [*corners, corners[0]]], color=GRAY, dash=True, width=1)
    d.line([shear(0, -0.5, gamma), shear(0, 0.5, gamma)], color=ORANGE)
    d.line([shear(0, -0.5, gamma), shear(-gamma / 2, 0.8, 0)], color=GRAY, dash=True, width=1)
    d.line([(518, 360), (590, 360)], arrow=True)
    d.line([(590, 460), (518, 460)], arrow=True)
    d.text(680, 413, "n", size=16)
    d.line([(670, 445), (670, 417)], color=INK, arrow=True)
    d.line([(670, 445), (706, 445)], color=INK, arrow=True)
    d.text(714, 451, "e1", size=16)
    d.text(570, 492, "Transverse shear · As", bold=True, anchor="middle")
    d.text(570, 517, "Section through the thickness", size=16, anchor="middle")
    return d.finish()


def axes_reference():
    d = Drawing(
        "Axis rotation and reference-surface shift",
        "A positive in-plane rotation preserves perpendicular unit axes. "
        "A positive reference shift moves the reference along the same normal.",
        370,
    )
    d.text(24, 34, "Rotate the in-plane axes", bold=True)
    d.text(410, 34, "Move the reference surface", bold=True)
    origin = np.array([147, 246])
    length, angle = 146, pi / 6

    def xy(x, y):
        return origin + np.array([x, -y])

    for vector, label in [((1, 0), "e1"), ((0, 1), "e2")]:
        end = xy(*(length * np.array(vector)))
        d.line([origin, end], color=GRAY, arrow=True)
        d.text(*(end + [12, 4]), label, color=GRAY)
    for vector, label, offset in [
        ((cos(angle), sin(angle)), "e1′", (10, 0)),
        ((-sin(angle), cos(angle)), "e2′", (-30, -10)),
    ]:
        end = xy(*(length * np.array(vector)))
        d.line([origin, end], arrow=True)
        d.text(*(end + offset), label)
    d.line(
        [xy(59 * cos(t), 59 * sin(t)) for t in np.linspace(0, angle, 30)], color=ORANGE, arrow=True
    )
    d.text(213, 232, "+ψ", color=ORANGE)
    d.dot(origin, color=INK, radius=3)
    d.text(24, 297, "View from +n toward the panel", size=16)
    d.line([(422, 243), (733, 243)], color=GRAY)
    d.line([(422, 154), (733, 154)], color=BLUE)
    d.line([(446, 266), (446, 90)], color=INK, arrow=True)
    d.text(436, 76, "+n", size=16)
    d.line([(694, 243), (694, 154)], color=ORANGE, arrow=True)
    d.text(704, 204, "+d", color=ORANGE)
    d.text(482, 140, "New reference", color=BLUE)
    d.text(482, 270, "Old reference", color=GRAY)
    d.text(410, 297, "Section along the normal", size=16)
    d.text(24, 345, "Positive ψ turns e1 toward e2.", size=16)
    d.text(410, 345, "Positive d follows the normal.", size=16)
    return d.finish()


def cylinder_axes():
    d = Drawing(
        "Local frame on a cylinder",
        "Axial e1, circumferential tangent e2, and outward normal n at one surface "
        "point. All vectors and curves use the same orthographic projection.",
        390,
    )
    d.text(24, 34, "Local directions on a cylindrical shell", bold=True)
    cylinder = Cylinder(radius=1.0)
    center, scale = np.array([203, 202]), 85

    def xy(points):
        return center + scale * projection(points, elevation=0)

    # Silhouette generators are extrema of the projected cross-section normal
    # to the projected axis. Projecting a circle supplies elliptical end rims.
    theta = np.linspace(0, 2 * pi, 181)
    ring0 = np.array([cylinder.point_at(0, t).position for t in theta])
    ring1 = ring0 + [4, 0, 0]
    # Far rim first; transparent line drawing keeps shell geometry explicit.
    d.line(xy(ring0), color=GRAY, dash=True, width=1)
    for t in [pi / 2, 3 * pi / 2]:
        d.line(xy([cylinder.point_at(x, t).position for x in [0, 4]]))
    for x in [1, 2, 3]:
        ring = np.array([cylinder.point_at(x, t).position for t in theta])
        d.line(xy(ring), color="#ccdce5", width=1)
    d.line(xy(ring1), width=2)
    point = cylinder.point_at(2.5, pi / 4)
    p = point.position
    for vector, label, offset, color in [
        (point.frame.e1, "e1 · axial", (152, 5), BLUE),
        (point.frame.e2, "e2 · circumferential", (20, 117), BLUE),
        (point.frame.n, "n · outward", (10, -5), ORANGE),
    ]:
        end = p + 0.92 * vector
        d.line(xy([p, end]), color=color, width=2.5, arrow=True)
        d.text(*(xy(end) + offset), label, color=color, size=17)
        if label.startswith("e2"):
            d.line([xy(end) + [0, 5], xy(end) + [12, 102]], color=GRAY, width=1)
        elif label.startswith("e1"):
            d.line([xy(end) + [5, 0], xy(end) + [140, 0]], color=GRAY, width=1)
    d.dot(xy(p))
    d.text(24, 348, "e1 × e2 = n", bold=True)
    d.text(
        24,
        375,
        "All three arrows share one surface point; e2 is tangent to the circumference.",
        size=16,
    )
    return d.finish()


def render_all(output=OUTPUT):
    example = run_path(str(ROOT / "docs/examples/scripts/walkthrough.py"))
    output.mkdir(parents=True, exist_ok=True)
    for name, svg in {
        "panel-model": panel_model(example),
        "repeat-offset": repeat_offset(example),
        "deformations": deformations(),
        "axes-reference": axes_reference(),
        "cylinder-axes": cylinder_axes(),
    }.items():
        (output / f"{name}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    render_all()
