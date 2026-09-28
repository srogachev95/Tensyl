"""Compare periodic drawings with the member lengths used in homogenization."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

import numpy as np

from tensyl.cells.tangent_plane import CanonicalUnitCell
from tensyl.core.typing import FloatArray

_TOL = 1.0e-10


def _cross(a: FloatArray, b: FloatArray) -> float:
    return float(a[0] * b[1] - a[1] * b[0])


def _clip(start: FloatArray, end: FloatArray) -> tuple[FloatArray, FloatArray] | None:
    delta = end - start
    lower, upper = 0.0, 1.0
    for axis in range(2):
        if abs(delta[axis]) <= _TOL:
            if start[axis] < -_TOL or start[axis] >= 1.0 - _TOL:
                # Count the lower edge only; its periodic upper copy is the
                # same physical rib, not another length contribution.
                return None
        else:
            first, last = sorted((-start[axis] / delta[axis], (1 - start[axis]) / delta[axis]))
            lower, upper = max(lower, first), min(upper, last)
    if upper <= lower or np.linalg.norm((upper - lower) * delta) <= _TOL:
        return None
    return start + lower * delta, start + upper * delta


@dataclass
class _Line:
    origin: FloatArray
    direction: FloatArray
    intervals: list[tuple[float, float]] = field(default_factory=list)

    def length(self, basis: FloatArray) -> float:
        intervals = sorted(self.intervals)
        left, right = intervals[0]
        total = 0.0
        for next_left, next_right in intervals[1:]:
            if next_left <= right + _TOL:
                right = max(right, next_right)
            else:
                total += right - left
                left, right = next_left, next_right
        return (total + right - left) * float(np.linalg.norm(basis @ self.direction))


def check_cell_geometry(cell: CanonicalUnitCell) -> dict[str, tuple[float, float]]:
    """Compare drawn and modeled member length per area for each family.

    The drawing is tiled 3x3, clipped to one half-open repeat parallelogram,
    and overlapping collinear segments within each family are counted once.
    Modeled density is the sum of ``multiplicity * length / cell.area``.

    Args:
        cell: Cell with drawable geometry and independent repeat vectors.
            Member labels must identify drawing families or uniquely labeled
            drawing edges. A drawing with one family needs no label mapping.

    Returns:
        Family names mapped to ``(drawn_density, modeled_density)`` in inverse
        length units. Unequal values report a discrepancy; they do not raise.

    Raises:
        ValueError: If geometry is absent, a family cannot be identified, or
            the drawing extends beyond the 3x3 neighborhood. Geometric
            comparisons use a tolerance of 1e-10 in repeat coordinates.

    This audits length accounting, not connectivity, material, eccentricity,
    member orientation, or mechanical validity. Coincident members assigned to
    different families are treated as separate physical contributions.
    """

    geometry = cell.geometry
    if geometry is None:
        raise ValueError("check_cell_geometry requires cell geometry.")
    a, b = geometry.repeat_vectors
    basis = np.array([[a.e1, b.e1], [a.e2, b.e2]])
    repeat_area = abs(float(np.linalg.det(basis)))
    nodes = np.array([(n.e1, n.e2) for n in geometry.nodes])
    coordinates = np.linalg.solve(basis, nodes.T).T
    coordinates -= 0.5 * (coordinates.min(axis=0) + coordinates.max(axis=0)) - 0.5
    if np.any(coordinates < -1 - _TOL) or np.any(coordinates > 2 + _TOL):
        raise ValueError("cell geometry must fit within the surrounding 3x3 repeat neighborhood.")
    families = {edge.family for edge in geometry.edges}
    modeled = dict.fromkeys(families, 0.0)
    for member in cell.members:
        candidates = {member.label} if member.label in families else set()
        candidates.update(
            edge.family for edge in geometry.edges if member.label and edge.label == member.label
        )
        if not candidates and len(families) == 1:
            candidates = families
        if len(candidates) != 1:
            raise ValueError(f"geometry family is ambiguous for member {member.label!r}.")
        family = next(iter(candidates))
        modeled[family] += member.multiplicity * member.length / cell.area

    lines: dict[str, list[_Line]] = {name: [] for name in families}
    for i, j in product((-1, 0, 1), repeat=2):
        offset = np.array([i, j])
        for edge in geometry.edges:
            clipped = _clip(coordinates[edge.start] + offset, coordinates[edge.end] + offset)
            if clipped is None:
                continue
            start, end = clipped
            direction = end - start
            direction /= np.linalg.norm(direction)
            family_lines = lines[edge.family]
            line = next(
                (
                    candidate
                    for candidate in family_lines
                    if abs(_cross(candidate.direction, direction)) <= _TOL
                    and abs(_cross(start - candidate.origin, candidate.direction)) <= _TOL
                ),
                None,
            )
            if line is None:
                line = _Line(start, direction)
                family_lines.append(line)
            left, right = sorted(
                (
                    float((start - line.origin) @ line.direction),
                    float((end - line.origin) @ line.direction),
                )
            )
            line.intervals.append((left, right))
    return {
        name: (sum(line.length(basis) for line in lines[name]) / repeat_area, modeled[name])
        for name in sorted(families)
    }


__all__ = ["check_cell_geometry"]
