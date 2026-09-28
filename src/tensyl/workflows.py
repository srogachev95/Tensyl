"""Small batch workflows over the public cell and homogenizer interfaces."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from dataclasses import asdict, fields
from itertools import product
from typing import Any

from tensyl.cells import CanonicalUnitCell
from tensyl.core.constitutive import ABDStiffnessCoefficients
from tensyl.homogenizers import EnergyHomogenizer, Homogenizer


def sweep(
    builder: Callable[..., CanonicalUnitCell],
    grid: Mapping[str, Iterable[Any]],
    *,
    homogenizer: Homogenizer | None = None,
) -> list[dict[str, Any]]:
    """Evaluate every parameter combination in mapping/iterable order.

    Args:
        builder: Cell factory called with each combination as keyword arguments.
        grid: Finite parameter iterables. Coefficient names, ``areal_mass``, and
            ``warning_codes`` are reserved output columns.
        homogenizer: Optional configured homogenizer; defaults to EnergyHomogenizer.

    Returns:
        Rows containing input parameters, all named stiffness coefficients,
        areal mass, and a tuple of validity warning codes. An empty grid calls
        the builder once; an empty axis produces no rows.

    Raises:
        ValueError: If a parameter shadows a reserved output column. Builder
            and homogenizer exceptions propagate with a parameter note; failed
            combinations are never silently dropped.
    """
    reserved = {f.name for f in fields(ABDStiffnessCoefficients)} | {"areal_mass", "warning_codes"}
    collisions = reserved.intersection(grid)
    if collisions:
        msg = f"Sweep parameter names are reserved output columns: {sorted(collisions)}."
        raise ValueError(msg)
    solver = EnergyHomogenizer() if homogenizer is None else homogenizer
    names = tuple(grid)
    axes = tuple(tuple(grid[name]) for name in names)
    rows = []
    for values in product(*axes):
        parameters = dict(zip(names, values, strict=True))
        try:
            result = solver.compute(builder(**parameters))
        except Exception as exc:
            exc.add_note(f"Sweep parameters: {parameters!r}")
            raise
        rows.append(
            {
                **parameters,
                **asdict(result.coefficients),
                "areal_mass": result.stiffness.areal_mass,
                "warning_codes": tuple(result.validity.warnings),
            }
        )
    return rows


__all__ = ["sweep"]
