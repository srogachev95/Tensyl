"""Wall fields, pointwise homogenization, and sampled wall atlases."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from types import MappingProxyType
from typing import Any, Protocol

import numpy as np

from tensyl.cells import CanonicalUnitCell
from tensyl.core.constitutive import LinearABDWall
from tensyl.core.typing import FloatArray
from tensyl.geometry import Surface, SurfacePoint
from tensyl.homogenizers import HomogenizationResult, Homogenizer, ValidityContext


class WallField(Protocol):
    """Protocol for objects that provide a wall law over a surface."""

    def law_at(self, surface: Surface, u: float, v: float) -> LinearABDWall:
        """Return the wall law at parametric coordinates ``(u, v)``."""


CellFactory = Callable[[Surface, SurfacePoint], CanonicalUnitCell]
ValidityContextFactory = Callable[[SurfacePoint, CanonicalUnitCell], ValidityContext | None]


def _tensyl_version() -> str:
    try:
        return version("tensyl")
    except PackageNotFoundError:  # pragma: no cover - editable tree before install
        return "0.0.0"


def _finite(value: float, *, name: str) -> float:
    checked = float(value)
    if not np.isfinite(checked):
        msg = f"{name} must be finite."
        raise ValueError(msg)
    return checked


def _increasing(values: tuple[float, ...], *, name: str) -> tuple[float, ...]:
    checked = tuple(_finite(value, name=name) for value in values)
    if len(checked) < 2:
        msg = f"{name} must contain at least two values."
        raise ValueError(msg)
    if any(right <= left for left, right in zip(checked[:-1], checked[1:], strict=True)):
        msg = f"{name} must be strictly increasing."
        raise ValueError(msg)
    return checked


def _metadata_for_surface(metadata: Mapping[str, Any], point: SurfacePoint) -> dict[str, Any]:
    combined = dict(metadata)
    combined.update(
        {
            "surface": point.metadata.get("surface", "surface"),
            "u": point.u,
            "v": point.v,
            "source": combined.get("source", "wall_field"),
        }
    )
    return combined


def _validate_law_matches_point(law: LinearABDWall, point: SurfacePoint, *, context: str) -> None:
    if law.frame != point.frame:
        msg = f"{context} law frame must match the surface point frame."
        raise ValueError(msg)


def _bind_wall_to_point(wall: LinearABDWall, point: SurfacePoint, *, source: str) -> LinearABDWall:
    metadata = _metadata_for_surface(wall.metadata, point)
    metadata["source"] = source
    return LinearABDWall.from_tangent(
        wall.C8,
        frame=point.frame,
        convention=wall.convention,
        areal_mass=wall.areal_mass,
        metadata=metadata,
        validity=wall.validity,
    )


@dataclass(frozen=True, slots=True)
class ConstantWallField:
    """Uniform wall law bound pointwise to a surface frame."""

    law: LinearABDWall

    def law_at(self, surface: Surface, u: float, v: float) -> LinearABDWall:
        point = surface.point_at(u, v)
        return _bind_wall_to_point(self.law, point, source="constant_wall_field")


@dataclass(slots=True)
class WallCache:
    """Mutable pointwise wall-law cache keyed by rounded parametric coordinates."""

    precision: int = 12
    _items: dict[tuple[float, float], LinearABDWall] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.precision < 0:
            msg = "precision must be nonnegative."
            raise ValueError(msg)

    def key(self, u: float, v: float) -> tuple[float, float]:
        return (
            round(_finite(u, name="u"), self.precision),
            round(_finite(v, name="v"), self.precision),
        )

    def get(self, u: float, v: float) -> LinearABDWall | None:
        return self._items.get(self.key(u, v))

    def set(self, u: float, v: float, law: LinearABDWall) -> None:
        self._items[self.key(u, v)] = law

    def clear(self) -> None:
        self._items.clear()

    @property
    def size(self) -> int:
        return len(self._items)


@dataclass(frozen=True, slots=True)
class HomogenizedWallField:
    """Wall field that builds and homogenizes a local cell at each surface point."""

    surface: Surface
    cell_factory: CellFactory
    homogenizer: Homogenizer
    cache: WallCache | None = None
    validity_context_factory: ValidityContextFactory | None = None

    def law_at(self, surface: Surface, u: float, v: float) -> LinearABDWall:
        if surface != self.surface:
            msg = "HomogenizedWallField can only be evaluated on its configured surface."
            raise ValueError(msg)
        cached = self.cache.get(u, v) if self.cache is not None else None
        if cached is not None:
            return cached

        point = self.surface.point_at(u, v)
        cell = self.cell_factory(self.surface, point)
        if cell.frame != point.frame:
            msg = "cell frame must match the surface point frame."
            raise ValueError(msg)
        validity_context = (
            None
            if self.validity_context_factory is None
            else self.validity_context_factory(point, cell)
        )
        result: HomogenizationResult = self.homogenizer.compute(
            cell,
            validity_context=validity_context,
        )
        _validate_law_matches_point(result.law, point, context="homogenized")
        law = _bind_wall_to_point(result.law, point, source="homogenized_wall_field")
        if self.cache is not None:
            self.cache.set(u, v, law)
        return law


def _cell_index(values: tuple[float, ...], value: float, *, name: str) -> tuple[int, float]:
    checked = _finite(value, name=name)
    if checked < values[0] or checked > values[-1]:
        msg = f"{name} is outside the atlas grid."
        raise ValueError(msg)
    if checked == values[-1]:
        return len(values) - 2, 1.0
    index = int(np.searchsorted(values, checked, side="right") - 1)
    left = values[index]
    right = values[index + 1]
    return index, (checked - left) / (right - left)


def _corner_warnings(corners: tuple[LinearABDWall, ...]) -> tuple[str, ...]:
    warnings: set[str] = set()
    for wall in corners:
        validity = wall.validity
        if validity is not None and hasattr(validity, "warnings"):
            warnings.update(str(warning) for warning in validity.warnings)
    return tuple(sorted(warnings))


def _shared_validity(corners: tuple[LinearABDWall, ...]) -> Any:
    first = corners[0].validity
    if all(wall.validity == first for wall in corners):
        return first
    return None


def _update_hash_with_float64(digest: Any, values: tuple[float, ...] | FloatArray) -> None:
    array = np.ascontiguousarray(values, dtype=np.float64)
    digest.update(array.shape[0].to_bytes(8, byteorder="big", signed=False))
    digest.update(array.tobytes())


def _update_hash_with_text(digest: Any, text: str) -> None:
    encoded = text.encode("utf-8")
    digest.update(len(encoded).to_bytes(8, byteorder="big", signed=False))
    digest.update(encoded)


def _sample_digest(
    u_values: tuple[float, ...],
    v_values: tuple[float, ...],
    laws: tuple[tuple[LinearABDWall, ...], ...],
) -> str:
    digest = hashlib.sha256()
    _update_hash_with_float64(digest, u_values)
    _update_hash_with_float64(digest, v_values)
    for row in laws:
        for law in row:
            digest.update(np.ascontiguousarray(law.C8, dtype=np.float64).tobytes())
            _update_hash_with_float64(digest, law.frame.e1)
            _update_hash_with_float64(digest, law.frame.e2)
            _update_hash_with_float64(digest, law.frame.n)
            _update_hash_with_text(digest, law.frame.label)
            for name in law.convention.membrane_order:
                _update_hash_with_text(digest, name)
            for name in law.convention.bending_order:
                _update_hash_with_text(digest, name)
            for name in law.convention.shear_order:
                _update_hash_with_text(digest, name)
            digest.update(b"\x01" if law.convention.engineering_shear else b"\x00")
            _update_hash_with_text(digest, law.convention.reference_surface)
            _update_hash_with_text(digest, law.convention.normal_positive)
            digest.update(b"\x00" if law.areal_mass is None else b"\x01")
            if law.areal_mass is not None:
                digest.update(np.float64(law.areal_mass).tobytes())
    return digest.hexdigest()


def _max_adjacent_c8_gradient(
    u_values: tuple[float, ...],
    v_values: tuple[float, ...],
    laws: tuple[tuple[LinearABDWall, ...], ...],
) -> float:
    max_gradient = 0.0
    for i, (left, right) in enumerate(zip(u_values[:-1], u_values[1:], strict=True)):
        span = right - left
        for j in range(len(v_values)):
            delta = laws[i + 1][j].C8 - laws[i][j].C8
            max_gradient = max(max_gradient, float(np.linalg.norm(delta, ord="fro") / span))
    for j, (left, right) in enumerate(zip(v_values[:-1], v_values[1:], strict=True)):
        span = right - left
        for i in range(len(u_values)):
            delta = laws[i][j + 1].C8 - laws[i][j].C8
            max_gradient = max(max_gradient, float(np.linalg.norm(delta, ord="fro") / span))
    return max_gradient


def _validate_atlas_samples(
    surface: Surface,
    u_values: tuple[float, ...],
    v_values: tuple[float, ...],
    laws: tuple[tuple[LinearABDWall, ...], ...],
) -> None:
    convention = laws[0][0].convention
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            law = laws[i][j]
            if law.convention != convention:
                msg = "all atlas samples must use the same strain convention."
                raise ValueError(msg)
            point = surface.point_at(u, v)
            _validate_law_matches_point(law, point, context="atlas sample")


@dataclass(frozen=True, slots=True)
class WallAtlas:
    """Rectangular bilinear atlas of sampled linear wall laws."""

    surface: Surface
    u_values: tuple[float, ...]
    v_values: tuple[float, ...]
    laws: tuple[tuple[LinearABDWall, ...], ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        u_values = _increasing(tuple(self.u_values), name="u_values")
        v_values = _increasing(tuple(self.v_values), name="v_values")
        law_rows = tuple(tuple(row) for row in self.laws)
        if len(law_rows) != len(u_values) or any(len(row) != len(v_values) for row in law_rows):
            msg = "laws must have shape (len(u_values), len(v_values))."
            raise ValueError(msg)
        _validate_atlas_samples(self.surface, u_values, v_values, law_rows)
        metadata = dict(self.metadata)
        metadata.setdefault("source", "wall_atlas")
        metadata.setdefault("interpolation", "bilinear_c8")
        metadata.update(
            {
                "u_values": u_values,
                "v_values": v_values,
                "sample_shape": (len(u_values), len(v_values)),
                "tensyl_version": _tensyl_version(),
                "sample_digest": _sample_digest(u_values, v_values, law_rows),
                "sample_warning_ids": _corner_warnings(
                    tuple(wall for row in law_rows for wall in row)
                ),
                "max_adjacent_c8_gradient_frobenius": _max_adjacent_c8_gradient(
                    u_values,
                    v_values,
                    law_rows,
                ),
            }
        )
        object.__setattr__(self, "u_values", u_values)
        object.__setattr__(self, "v_values", v_values)
        object.__setattr__(self, "laws", law_rows)
        object.__setattr__(self, "metadata", MappingProxyType(metadata))

    @classmethod
    def from_field(
        cls,
        surface: Surface,
        field: WallField,
        *,
        u_values: tuple[float, ...],
        v_values: tuple[float, ...],
        metadata: Mapping[str, Any] | None = None,
    ) -> WallAtlas:
        checked_u = _increasing(tuple(u_values), name="u_values")
        checked_v = _increasing(tuple(v_values), name="v_values")
        laws = tuple(tuple(field.law_at(surface, u, v) for v in checked_v) for u in checked_u)
        atlas_metadata = {"source": "wall_atlas", "interpolation": "bilinear_c8"}
        if metadata is not None:
            atlas_metadata.update(metadata)
        return cls(
            surface=surface,
            u_values=checked_u,
            v_values=checked_v,
            laws=laws,
            metadata=atlas_metadata,
        )

    def law_at(self, surface: Surface, u: float, v: float) -> LinearABDWall:
        if surface != self.surface:
            msg = "WallAtlas can only be evaluated on its configured surface."
            raise ValueError(msg)
        i, su = _cell_index(self.u_values, u, name="u")
        j, sv = _cell_index(self.v_values, v, name="v")
        w00 = (1.0 - su) * (1.0 - sv)
        w10 = su * (1.0 - sv)
        w01 = (1.0 - su) * sv
        w11 = su * sv
        corners = (
            self.laws[i][j],
            self.laws[i + 1][j],
            self.laws[i][j + 1],
            self.laws[i + 1][j + 1],
        )
        weights = (w00, w10, w01, w11)
        tangent = sum(
            (weight * wall.C8 for weight, wall in zip(weights, corners, strict=True)),
            start=np.zeros((8, 8)),
        )
        tangent = 0.5 * (tangent + tangent.T)

        areal_mass = None
        if all(wall.areal_mass is not None for wall in corners):
            areal_mass = sum(
                weight * wall.areal_mass
                for weight, wall in zip(weights, corners, strict=True)
                if wall.areal_mass is not None
            )
        point = self.surface.point_at(u, v)
        max_corner_delta = max(
            float(np.linalg.norm(wall.C8 - tangent, ord="fro")) for wall in corners
        )
        metadata = dict(self.metadata)
        metadata.update(
            {
                "source": "wall_atlas_bilinear",
                "grid_cell": (i, j),
                "weights": weights,
                "corner_warnings": _corner_warnings(corners),
                "max_corner_delta_frobenius": max_corner_delta,
                "u": point.u,
                "v": point.v,
            }
        )
        return LinearABDWall.from_tangent(
            tangent,
            frame=point.frame,
            convention=corners[0].convention,
            areal_mass=areal_mass,
            metadata=metadata,
            validity=_shared_validity(corners),
        )


__all__ = [
    "CellFactory",
    "ConstantWallField",
    "HomogenizedWallField",
    "ValidityContextFactory",
    "WallAtlas",
    "WallCache",
    "WallField",
]
