"""Explicit expansion of common laminate stacking notation."""

from __future__ import annotations

import re

from tensyl.core._validation import positive_number
from tensyl.materials.laminates import Ply, PlyMaterial

_SUBSCRIPTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
_ANGLE = re.compile(
    r"(?P<pair>±|\+-|∓)?(?P<angle>[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+))"
    r"(?:_(?P<repeat>[0-9]+))?"
)


def layup(material: PlyMaterial, ply_thickness: float, notation: str) -> tuple[Ply, ...]:
    """Expand a layup string into equal-thickness plies, bottom to top.

    Args:
        material: Material shared by all expanded plies.
        ply_thickness: Positive thickness of each ply.
        notation: Slash-separated angles in degrees, optionally enclosed in
            brackets. ``±a`` and ``+-a`` expand to +a, -a; ``∓a`` reverses
            that pair. ``0_2`` and ``0₂`` repeat an entry. A bracketed group
            may have an integer repeat count followed by ``s`` for symmetry:
            ``[0/90]2s`` repeats twice, then appends the reversed stack.

    Returns:
        Tuple of plies ordered from the negative-normal face to the positive
        face. Symmetry duplicates the middle ply; none is shared across it.

    Raises:
        ValueError: If notation is empty, malformed, nested, or unsupported,
            a repeat count is not positive, or thickness is invalid.
    """

    thickness = positive_number(ply_thickness, name="ply_thickness")
    text = notation.strip()
    group = re.fullmatch(r"\[([^\[\]]+)\]([0-9]*)(s?)", text)
    repetitions = 1
    symmetric = False
    if group is not None:
        text, count, suffix = group.groups()
        repetitions = int(count) if count else 1
        symmetric = suffix == "s"
    if repetitions < 1:
        raise ValueError("layup repeat counts must be positive.")
    angles: list[float] = []
    for raw in text.split("/"):
        token = re.sub(r"[₀₁₂₃₄₅₆₇₈₉]+", lambda m: "_" + m[0].translate(_SUBSCRIPTS), raw.strip())
        match = _ANGLE.fullmatch(token)
        if match is None:
            raise ValueError(f"unsupported layup entry: {raw!r}.")
        pair, value, count = match.groups()
        if pair and value.startswith(("+", "-")):
            raise ValueError("layup paired angles need an unsigned magnitude.")
        repeat = int(count) if count else 1
        if repeat < 1:
            raise ValueError("layup repeat counts must be positive.")
        angle = float(value)
        entry = [angle] if pair is None else ([-angle, angle] if pair == "∓" else [angle, -angle])
        angles.extend(entry * repeat)
    angles *= repetitions
    if symmetric:
        angles += angles[::-1]
    return tuple(Ply.from_degrees(material, thickness, angle) for angle in angles)


__all__ = ["layup"]
