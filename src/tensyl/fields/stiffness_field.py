"""Stiffness fields, pointwise homogenization, and sampled stiffness atlases."""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, Protocol

import numpy as np

from tensyl._version import tensyl_version
from tensyl.cells import CanonicalUnitCell
from tensyl.core._validation import finite_number, readonly_mapping
from tensyl.core.constitutive import ABDStiffness
from tensyl.core.rotations import rotate_tangent
from tensyl.core.typing import FloatArray
from tensyl.geometry import Surface, SurfacePoint
from tensyl.homogenizers import HomogenizationResult, Homogenizer, ValidityContext


class StiffnessField(Protocol):
    """Protocol for objects that provide ABD stiffness over a surface.

    Attributes:
        stiffness_at: Method that evaluates the field at surface coordinates.
    """

    def stiffness_at(self, surface: Surface, u: float, v: float) -> ABDStiffness:
        """Return the ABD stiffness at parametric coordinates.

        Args:
            surface: Surface that defines the local frame and geometry.
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.

        Returns:
            The linear ABD stiffness bound to the local frame at ``(u, v)``.

        Raises:
            ValueError: If the field cannot be evaluated on the supplied
                surface or coordinates.
        """


CellFactory = Callable[[Surface, SurfacePoint], CanonicalUnitCell]
ValidityContextFactory = Callable[[SurfacePoint, CanonicalUnitCell], ValidityContext | None]


def _increasing(values: tuple[float, ...], *, name: str) -> tuple[float, ...]:
    checked = tuple(finite_number(value, name=name) for value in values)
    if len(checked) < 2:
        msg = f"{name} must contain at least two values."
        raise ValueError(msg)
    if any(right <= left for left, right in zip(checked[:-1], checked[1:], strict=True)):
        msg = f"{name} must be strictly increasing."
        raise ValueError(msg)
    return checked


def _metadata_for_surface(metadata: Mapping[str, Any], point: SurfacePoint) -> dict[str, Any]:
    # Field evaluation binds an otherwise reusable ABD stiffness to a concrete
    # surface point. Preserve caller metadata, then stamp the local coordinates.
    combined = dict(metadata)
    combined.update(
        {
            "surface": point.metadata.get("surface", "surface"),
            "u": point.u,
            "v": point.v,
            "source": combined.get("source", "stiffness_field"),
        }
    )
    return combined


def _validate_stiffness_matches_point(
    stiffness: ABDStiffness, point: SurfacePoint, *, context: str
) -> None:
    if not stiffness.frame.is_close(point.frame):
        msg = f"{context} local frame must match the surface point frame."
        raise ValueError(msg)


def _bind_stiffness_to_point(
    stiffness: ABDStiffness, point: SurfacePoint, *, source: str
) -> ABDStiffness:
    metadata = _metadata_for_surface(stiffness.metadata, point)
    metadata["source"] = source
    # The numeric C8 is unchanged here. The new object says "read this same
    # local law in the frame supplied by surface.point_at(u, v)."
    return ABDStiffness.from_tangent(
        stiffness.C8,
        frame=point.frame,
        convention=stiffness.convention,
        areal_mass=stiffness.areal_mass,
        metadata=metadata,
        validity=stiffness.validity,
    )


@dataclass(frozen=True, slots=True)
class ConstantStiffnessField:
    """Uniform ABD stiffness bound pointwise to a surface frame.

    Attributes:
        stiffness: Local stiffness to reuse at every sampled point.
        orientation_rad: Counterclockwise angle from the surface's e1 to the
            stiffness's e1 about +n. Zero preserves the original components.
    """

    stiffness: ABDStiffness
    orientation_rad: float = 0.0

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "orientation_rad", finite_number(self.orientation_rad, name="orientation_rad")
        )

    def stiffness_at(self, surface: Surface, u: float, v: float) -> ABDStiffness:
        """Return the constant stiffness at a surface point.

        Args:
            surface: Surface that supplies the point frame and metadata.
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.

        Returns:
            A new ``ABDStiffness`` expressed in the sampled surface frame,
            with the supplied material orientation.

        Raises:
            ValueError: If the surface rejects the coordinates.
        """

        point = surface.point_at(u, v)
        metadata = _metadata_for_surface(self.stiffness.metadata, point)
        metadata.update(source="constant_stiffness_field", orientation_rad=self.orientation_rad)
        tangent = self.stiffness.C8
        if self.orientation_rad != 0.0:
            # The angle locates material axes in surface axes. Expressing the
            # material law in surface components uses the opposite frame turn.
            tangent = rotate_tangent(tangent, -self.orientation_rad)
        return ABDStiffness.from_tangent(
            tangent,
            frame=point.frame,
            convention=self.stiffness.convention,
            areal_mass=self.stiffness.areal_mass,
            metadata=metadata,
            validity=self.stiffness.validity,
        )


@dataclass(slots=True)
class StiffnessCache:
    """Mutable pointwise stiffness cache keyed by rounded coordinates.

    Attributes:
        precision: Number of decimal places used when rounding ``u`` and ``v``
            into a cache key.
    """

    precision: int = 12
    _items: dict[tuple[float, float], ABDStiffness] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.precision < 0:
            msg = "precision must be nonnegative."
            raise ValueError(msg)

    def key(self, u: float, v: float) -> tuple[float, float]:
        """Build the rounded cache key for a coordinate pair.

        Args:
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.

        Returns:
            Rounded ``(u, v)`` tuple used as the dictionary key.

        Raises:
            ValueError: If either coordinate is not finite.
        """

        return (
            round(finite_number(u, name="u"), self.precision),
            round(finite_number(v, name="v"), self.precision),
        )

    def get(self, u: float, v: float) -> ABDStiffness | None:
        """Return a cached stiffness value if one exists.

        Args:
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.

        Returns:
            The cached stiffness for the rounded coordinate key, or ``None``
            when the key has not been stored.
        """

        return self._items.get(self.key(u, v))

    def set(self, u: float, v: float, stiffness: ABDStiffness) -> None:
        """Store a stiffness value under the rounded coordinate key.

        Args:
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.
            stiffness: ABD stiffness to store.
        """

        self._items[self.key(u, v)] = stiffness

    def clear(self) -> None:
        """Remove all cached stiffness values.

        Returns:
            None.
        """

        self._items.clear()

    @property
    def size(self) -> int:
        """Return the number of cached coordinate samples.

        Returns:
            Count of stored stiffness values.
        """

        return len(self._items)


@dataclass(frozen=True, slots=True)
class HomogenizedStiffnessField:
    """Pointwise field built by homogenizing a local cell at each sample.

    Attributes:
        surface: The only surface on which this field may be evaluated.
        cell_factory: Callable that builds a local cell from the surface and
            sampled ``SurfacePoint``.
        homogenizer: Homogenizer used to compute the pointwise ABD stiffness.
        cache: Optional coordinate cache for repeated evaluations.
        validity_context_factory: Optional callable that builds local validity
            context for the sampled point and cell.
    """

    surface: Surface
    cell_factory: CellFactory
    homogenizer: Homogenizer
    cache: StiffnessCache | None = None
    validity_context_factory: ValidityContextFactory | None = None

    def stiffness_at(self, surface: Surface, u: float, v: float) -> ABDStiffness:
        """Return the homogenized stiffness at a surface point.

        Args:
            surface: Surface to evaluate. It must be the field's configured
                surface.
            u: First coordinate in the surface parameterization.
            v: Second coordinate in the surface parameterization.

        Returns:
            Homogenized ABD stiffness rebound to the sampled surface frame.

        Raises:
            ValueError: If ``surface`` is not the configured surface, the cell
                factory returns a frame-mismatched cell, or the homogenized
                stiffness does not match the sampled frame.
            HomogenizationInputError: If the configured homogenizer rejects the
                generated cell.
        """

        if surface != self.surface:
            msg = "HomogenizedStiffnessField can only be evaluated on its configured surface."
            raise ValueError(msg)
        cached = self.cache.get(u, v) if self.cache is not None else None
        if cached is not None:
            return cached

        point = self.surface.point_at(u, v)
        cell = self.cell_factory(self.surface, point)
        # Pointwise factories are allowed to vary pitch, section, or material,
        # but they must still return a cell expressed in the surface point frame.
        if not cell.frame.is_close(point.frame):
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
        _validate_stiffness_matches_point(result.stiffness, point, context="homogenized")
        stiffness = _bind_stiffness_to_point(
            result.stiffness, point, source="homogenized_stiffness_field"
        )
        if self.cache is not None:
            self.cache.set(u, v, stiffness)
        return stiffness


def _cell_index(values: tuple[float, ...], value: float, *, name: str) -> tuple[int, float]:
    checked = finite_number(value, name=name)
    if checked < values[0] or checked > values[-1]:
        msg = f"{name} is outside the atlas grid."
        raise ValueError(msg)
    if checked == values[-1]:
        # The right boundary belongs to the final cell with unit local
        # coordinate; otherwise searchsorted would create an out-of-range cell.
        return len(values) - 2, 1.0
    index = int(np.searchsorted(values, checked, side="right") - 1)
    left = values[index]
    right = values[index + 1]
    return index, (checked - left) / (right - left)


def _corner_warnings(corners: tuple[ABDStiffness, ...]) -> tuple[str, ...]:
    # Interpolation can blend stiffness values but not the meaning of warning
    # codes. Carry the union forward for provenance.
    warnings: set[str] = set()
    for stiffness in corners:
        validity = stiffness.validity
        if validity is not None and hasattr(validity, "warnings"):
            warnings.update(str(warning) for warning in validity.warnings)
    return tuple(sorted(warnings))


def _shared_validity(corners: tuple[ABDStiffness, ...]) -> Any:
    # A single validity object is meaningful only when every corner agrees.
    # Mixed validity remains visible through metadata corner_warnings.
    first = corners[0].validity
    if all(stiffness.validity == first for stiffness in corners):
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
    stiffnesses: tuple[tuple[ABDStiffness, ...], ...],
) -> str:
    # The digest fingerprints the numeric samples and interpretation metadata,
    # so downstream artifacts can detect stale atlases without storing the whole
    # source field.
    digest = hashlib.sha256()
    _update_hash_with_float64(digest, u_values)
    _update_hash_with_float64(digest, v_values)
    for row in stiffnesses:
        for stiffness in row:
            digest.update(np.ascontiguousarray(stiffness.C8, dtype=np.float64).tobytes())
            _update_hash_with_float64(digest, stiffness.frame.e1)
            _update_hash_with_float64(digest, stiffness.frame.e2)
            _update_hash_with_float64(digest, stiffness.frame.n)
            _update_hash_with_text(digest, stiffness.frame.label)
            for name in stiffness.convention.membrane_order:
                _update_hash_with_text(digest, name)
            for name in stiffness.convention.bending_order:
                _update_hash_with_text(digest, name)
            for name in stiffness.convention.shear_order:
                _update_hash_with_text(digest, name)
            digest.update(b"\x01" if stiffness.convention.engineering_shear else b"\x00")
            _update_hash_with_text(digest, stiffness.convention.reference_surface)
            _update_hash_with_text(digest, stiffness.convention.normal_positive)
            digest.update(b"\x00" if stiffness.areal_mass is None else b"\x01")
            if stiffness.areal_mass is not None:
                digest.update(np.float64(stiffness.areal_mass).tobytes())
    return digest.hexdigest()


def _max_adjacent_c8_gradient(
    u_values: tuple[float, ...],
    v_values: tuple[float, ...],
    stiffnesses: tuple[tuple[ABDStiffness, ...], ...],
) -> float:
    # This is a coarse smoothness indicator for sampled fields. It is not an
    # interpolation error bound, but it helps flag abrupt atlas transitions.
    max_gradient = 0.0
    for i, (left, right) in enumerate(zip(u_values[:-1], u_values[1:], strict=True)):
        span = right - left
        for j in range(len(v_values)):
            delta = stiffnesses[i + 1][j].C8 - stiffnesses[i][j].C8
            max_gradient = max(max_gradient, float(np.linalg.norm(delta, ord="fro") / span))
    for j, (left, right) in enumerate(zip(v_values[:-1], v_values[1:], strict=True)):
        span = right - left
        for i in range(len(u_values)):
            delta = stiffnesses[i][j + 1].C8 - stiffnesses[i][j].C8
            max_gradient = max(max_gradient, float(np.linalg.norm(delta, ord="fro") / span))
    return max_gradient


def _validate_atlas_samples(
    surface: Surface,
    u_values: tuple[float, ...],
    v_values: tuple[float, ...],
    stiffnesses: tuple[tuple[ABDStiffness, ...], ...],
) -> None:
    convention = stiffnesses[0][0].convention
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            stiffness = stiffnesses[i][j]
            # Bilinear interpolation is only well-defined when every sample
            # shares the same strain convention and local surface frame.
            if stiffness.convention != convention:
                msg = "all atlas samples must use the same strain convention."
                raise ValueError(msg)
            point = surface.point_at(u, v)
            _validate_stiffness_matches_point(stiffness, point, context="atlas sample")


@dataclass(frozen=True, slots=True)
class ABDAtlas:
    """Rectangular bilinear atlas of sampled linear ABD stiffnesses.

    Attributes:
        surface: Surface on which the samples were taken.
        u_values: Strictly increasing first-coordinate grid values.
        v_values: Strictly increasing second-coordinate grid values.
        stiffnesses: Rectangular ``(len(u_values), len(v_values))`` stiffness
            samples bound to the corresponding surface frames.
        metadata: Read-only provenance, grid, and interpolation metadata.
    """

    surface: Surface
    u_values: tuple[float, ...]
    v_values: tuple[float, ...]
    stiffnesses: tuple[tuple[ABDStiffness, ...], ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        u_values = _increasing(tuple(self.u_values), name="u_values")
        v_values = _increasing(tuple(self.v_values), name="v_values")
        stiffness_rows = tuple(tuple(row) for row in self.stiffnesses)
        if len(stiffness_rows) != len(u_values) or any(
            len(row) != len(v_values) for row in stiffness_rows
        ):
            msg = "stiffnesses must have shape (len(u_values), len(v_values))."
            raise ValueError(msg)
        _validate_atlas_samples(self.surface, u_values, v_values, stiffness_rows)
        metadata = dict(self.metadata)
        metadata.setdefault("source", "abd_atlas")
        metadata.setdefault("interpolation", "bilinear_c8")
        metadata.update(
            {
                "u_values": u_values,
                "v_values": v_values,
                "sample_shape": (len(u_values), len(v_values)),
                "tensyl_version": tensyl_version(),
                "sample_digest": _sample_digest(u_values, v_values, stiffness_rows),
                "sample_warning_ids": _corner_warnings(
                    tuple(stiffness for row in stiffness_rows for stiffness in row)
                ),
                "max_adjacent_c8_gradient_frobenius": _max_adjacent_c8_gradient(
                    u_values,
                    v_values,
                    stiffness_rows,
                ),
            }
        )
        object.__setattr__(self, "u_values", u_values)
        object.__setattr__(self, "v_values", v_values)
        object.__setattr__(self, "stiffnesses", stiffness_rows)
        object.__setattr__(self, "metadata", readonly_mapping(metadata))

    @classmethod
    def from_field(
        cls,
        surface: Surface,
        field: StiffnessField,
        *,
        u_values: tuple[float, ...],
        v_values: tuple[float, ...],
        metadata: Mapping[str, Any] | None = None,
    ) -> ABDAtlas:
        """Sample a stiffness field onto a rectangular atlas grid.

        Args:
            surface: Surface used for all field evaluations.
            field: Field to sample.
            u_values: Strictly increasing coordinates in the first parameter
                direction.
            v_values: Strictly increasing coordinates in the second parameter
                direction.
            metadata: Optional metadata to merge into the atlas provenance.

        Returns:
            An ``ABDAtlas`` containing all sampled stiffness values.

        Raises:
            ValueError: If either coordinate grid is invalid or a sampled
                stiffness does not match the surface frame.
        """

        checked_u = _increasing(tuple(u_values), name="u_values")
        checked_v = _increasing(tuple(v_values), name="v_values")
        stiffnesses = tuple(
            tuple(field.stiffness_at(surface, u, v) for v in checked_v) for u in checked_u
        )
        atlas_metadata = {"source": "abd_atlas", "interpolation": "bilinear_c8"}
        if metadata is not None:
            atlas_metadata.update(metadata)
        return cls(
            surface=surface,
            u_values=checked_u,
            v_values=checked_v,
            stiffnesses=stiffnesses,
            metadata=atlas_metadata,
        )

    def stiffness_at(self, surface: Surface, u: float, v: float) -> ABDStiffness:
        """Interpolate atlas stiffness at a surface coordinate.

        Args:
            surface: Surface to evaluate. It must be the atlas surface.
            u: First coordinate in the atlas domain.
            v: Second coordinate in the atlas domain.

        Returns:
            Bilinearly interpolated ``ABDStiffness`` with metadata describing
            the grid cell, weights, and corner warnings.

        Raises:
            ValueError: If ``surface`` is not the atlas surface or the
                coordinate is outside the sampled grid.
        """

        if surface != self.surface:
            msg = "ABDAtlas can only be evaluated on its configured surface."
            raise ValueError(msg)
        i, su = _cell_index(self.u_values, u, name="u")
        j, sv = _cell_index(self.v_values, v, name="v")
        # Interpolate the canonical C8 payload directly. ABD block interpolation
        # would be equivalent, but C8 keeps the provenance and symmetry story
        # in one place.
        w00 = (1.0 - su) * (1.0 - sv)
        w10 = su * (1.0 - sv)
        w01 = (1.0 - su) * sv
        w11 = su * sv
        corners = (
            self.stiffnesses[i][j],
            self.stiffnesses[i + 1][j],
            self.stiffnesses[i][j + 1],
            self.stiffnesses[i + 1][j + 1],
        )
        weights = (w00, w10, w01, w11)
        tangent = sum(
            (weight * stiffness.C8 for weight, stiffness in zip(weights, corners, strict=True)),
            start=np.zeros((8, 8)),
        )
        tangent = 0.5 * (tangent + tangent.T)

        areal_mass = None
        if all(stiffness.areal_mass is not None for stiffness in corners):
            # Mass is interpolated only when all corners actually know it.
            areal_mass = sum(
                weight * stiffness.areal_mass
                for weight, stiffness in zip(weights, corners, strict=True)
                if stiffness.areal_mass is not None
            )
        point = self.surface.point_at(u, v)
        max_corner_delta = max(
            float(np.linalg.norm(stiffness.C8 - tangent, ord="fro")) for stiffness in corners
        )
        metadata = dict(self.metadata)
        metadata.update(
            {
                "source": "abd_atlas_bilinear",
                "grid_cell": (i, j),
                "weights": weights,
                "corner_warnings": _corner_warnings(corners),
                "max_corner_delta_frobenius": max_corner_delta,
                "u": point.u,
                "v": point.v,
            }
        )
        return ABDStiffness.from_tangent(
            tangent,
            frame=point.frame,
            convention=corners[0].convention,
            areal_mass=areal_mass,
            metadata=metadata,
            validity=_shared_validity(corners),
        )


__all__ = [
    "CellFactory",
    "ConstantStiffnessField",
    "HomogenizedStiffnessField",
    "ValidityContextFactory",
    "ABDAtlas",
    "StiffnessCache",
    "StiffnessField",
]
