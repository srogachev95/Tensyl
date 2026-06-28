"""Deterministic Gmsh geometry text for rectangular shell patches."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite


def _positive(value: float, *, name: str) -> float:
    checked = float(value)
    if not isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be a finite positive number."
        raise ValueError(msg)
    return checked


def _positive_int(value: int, *, name: str) -> int:
    checked = int(value)
    if checked <= 0:
        msg = f"{name} must be positive."
        raise ValueError(msg)
    return checked


def _name(value: str, *, name: str) -> str:
    checked = str(value)
    if not checked or not checked.replace("_", "").isalnum() or checked[0].isdigit():
        msg = f"{name} must be a non-empty identifier using letters, numbers, and underscores."
        raise ValueError(msg)
    return checked


def _fmt(value: float) -> str:
    return f"{value:.12g}"


@dataclass(frozen=True, slots=True)
class GmshSkinPatch:
    """Rectangular midsurface patch for Gmsh shell meshing."""

    length: float
    width: float
    divisions_x: int
    divisions_y: int
    name: str = "skin_patch"

    def __post_init__(self) -> None:
        object.__setattr__(self, "length", _positive(self.length, name="length"))
        object.__setattr__(self, "width", _positive(self.width, name="width"))
        object.__setattr__(
            self,
            "divisions_x",
            _positive_int(self.divisions_x, name="divisions_x"),
        )
        object.__setattr__(
            self,
            "divisions_y",
            _positive_int(self.divisions_y, name="divisions_y"),
        )
        object.__setattr__(self, "name", _name(self.name, name="name"))


def render_rectangular_skin_geo(patch: GmshSkinPatch) -> str:
    """Return Gmsh ``.geo`` text for a centered rectangular quad shell patch."""

    half_length = 0.5 * patch.length
    half_width = 0.5 * patch.width
    lc = min(patch.length / patch.divisions_x, patch.width / patch.divisions_y)
    lines = [
        'SetFactory("OpenCASCADE");',
        f"// Tensyl validation rectangular shell patch: {patch.name}",
        f"lc = {_fmt(lc)};",
        f"Point(1) = {{{_fmt(-half_length)}, {_fmt(-half_width)}, 0, lc}};",
        f"Point(2) = {{{_fmt(half_length)}, {_fmt(-half_width)}, 0, lc}};",
        f"Point(3) = {{{_fmt(half_length)}, {_fmt(half_width)}, 0, lc}};",
        f"Point(4) = {{{_fmt(-half_length)}, {_fmt(half_width)}, 0, lc}};",
        "Line(1) = {1, 2};",
        "Line(2) = {2, 3};",
        "Line(3) = {3, 4};",
        "Line(4) = {4, 1};",
        "Curve Loop(1) = {1, 2, 3, 4};",
        "Plane Surface(1) = {1};",
        f"Transfinite Curve {{1, 3}} = {patch.divisions_x + 1};",
        f"Transfinite Curve {{2, 4}} = {patch.divisions_y + 1};",
        "Transfinite Surface {1};",
        "Recombine Surface {1};",
        'Physical Surface("skin") = {1};',
        'Physical Curve("xmin") = {4};',
        'Physical Curve("xmax") = {2};',
        'Physical Curve("ymin") = {1};',
        'Physical Curve("ymax") = {3};',
        "Mesh.ElementOrder = 1;",
        "Mesh.RecombineAll = 1;",
        "",
    ]
    return "\n".join(lines)
