"""Abaqus conventional-shell general section keyword output."""

from __future__ import annotations

import re

import numpy as np

from tensyl.core.constitutive import ABDStiffness


def _name(value: str) -> str:
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,79}", value) is None:
        msg = (
            "Abaqus name must start with a letter and contain 1–80 letters, digits, or underscores."
        )
        raise ValueError(msg)
    return value


def abaqus_shell_general_section(
    stiffness: ABDStiffness,
    *,
    elset: str,
    orientation: str | None = None,
    explicit: bool = False,
) -> str:
    """Return full ABD and transverse-shear keyword data in consistent units.

    The caller must align Abaqus section axes and normal with ``stiffness.frame``
    and place the shell at the stiffness reference surface. No offset, rotation,
    unit conversion, or material definition is added.

    Args:
        stiffness: Local stiffness with engineering shear and twist components.
        elset: Existing element-set name (letters, digits, underscores).
        orientation: Existing orientation name, if the default axes do not match.
        explicit: Require positive known surface mass for Abaqus/Explicit.

    Returns:
        Keyword fragment ending in a newline. Density is mass per surface area.

    Raises:
        ValueError: If names are invalid, shear stiffness is not positive
            definite, or Explicit has no positive areal mass.
    """
    keyword = f"*SHELL GENERAL SECTION, ELSET={_name(elset)}"
    if orientation is not None:
        keyword += f", ORIENTATION={_name(orientation)}"
    mass = stiffness.areal_mass
    if explicit and (mass is None or mass <= 0):
        msg = "Abaqus/Explicit requires a positive known areal_mass."
        raise ValueError(msg)
    if mass is not None:
        keyword += f", DENSITY={mass:.17g}"
    # Abaqus replaces a zero diagonal with the other diagonal. Refuse laws
    # whose shear response could therefore change at the solver boundary.
    try:
        np.linalg.cholesky(stiffness.As)
    except np.linalg.LinAlgError as exc:
        msg = "Abaqus export requires positive definite transverse shear stiffness."
        raise ValueError(msg) from exc
    packed = [f"{stiffness.C8[row, col]:.17g}" for row in range(6) for col in range(row + 1)]
    lines = [
        "** Tensyl: align section axes/normal and reference surface with the supplied stiffness.",
        keyword,
        *(", ".join(packed[start : start + 8]) for start in range(0, 21, 8)),
        "*TRANSVERSE SHEAR STIFFNESS",
        ", ".join(
            f"{value:.17g}"
            for value in (stiffness.As[0, 0], stiffness.As[1, 1], stiffness.As[0, 1])
        ),
    ]
    return "\n".join(lines) + "\n"
