from __future__ import annotations

from typing import NoReturn

import numpy as np
import pytest

from tensyl import (
    BeamMember,
    BeamSection,
    CanonicalUnitCell,
    ConicalFrustum,
    ConstantWallField,
    Cylinder,
    Ellipsoid,
    EnergyHomogenizer,
    FlatPlate,
    HomogenizedWallField,
    LinearABDWall,
    Sphere,
    StrainConvention,
    ValidityContext,
    ValidityReport,
    WallAtlas,
    WallCache,
    validity_report_for_law,
)
from tensyl.geometry import Surface, SurfacePoint


def _wall(
    scale: float = 1.0,
    *,
    frame=None,
    validity=None,
    areal_mass: float | None = None,
) -> LinearABDWall:
    return LinearABDWall.from_tangent(
        scale * np.eye(8),
        frame=frame if frame is not None else FlatPlate().point_at(0.0, 0.0).frame,
        areal_mass=areal_mass,
        validity=validity,
        metadata={"kind": "test_wall"},
    )


def _section() -> BeamSection:
    return BeamSection(EA=100.0, EIy=10.0, EIz=8.0, GJ=5.0)


def test_constant_wall_field_rebinds_law_to_surface_frame() -> None:
    cylinder = Cylinder(radius=2.0)
    base = _wall(scale=3.0)
    law = ConstantWallField(base).law_at(cylinder, 0.5, 0.25)
    point = cylinder.point_at(0.5, 0.25)

    np.testing.assert_allclose(law.C8, base.C8)
    assert law.frame == point.frame
    assert law.metadata["source"] == "constant_wall_field"


@pytest.mark.parametrize(
    ("surface", "u", "v"),
    (
        (Sphere(radius=3.0), 0.7, 0.25),
        (Ellipsoid(a=2.0, b=3.0, c=4.0), 0.7, 0.25),
        (ConicalFrustum(radius_start=2.0, radius_end=3.0, length=5.0), 1.0, 0.25),
    ),
)
def test_constant_wall_field_rebinds_law_to_supported_curved_surfaces(
    surface: Surface,
    u: float,
    v: float,
) -> None:
    base = _wall(scale=2.0)
    law = ConstantWallField(base).law_at(surface, u, v)
    point = surface.point_at(u, v)

    np.testing.assert_allclose(law.C8, base.C8)
    assert law.frame == point.frame
    assert law.metadata["surface"] == point.metadata["surface"]


def test_validity_report_for_law_accepts_flat_infinite_radius() -> None:
    report = validity_report_for_law(
        _wall(),
        context=ValidityContext(
            characteristic_height=0.2,
            pitch=1.0,
            min_radius=np.inf,
            response_length=10.0,
        ),
    )

    assert report.h_over_R == pytest.approx(0.0)
    assert report.p_over_R == pytest.approx(0.0)
    assert report.p_over_L_response == pytest.approx(0.1)
    assert "p_over_L_response_exceeds_threshold" in report.warnings


def test_homogenized_wall_field_uses_cache_and_surface_point() -> None:
    plate = FlatPlate()
    calls: list[SurfacePoint] = []

    def factory(surface: Surface, point: SurfacePoint) -> CanonicalUnitCell:
        calls.append(point)
        skin = _wall(scale=1.0, frame=point.frame)
        return CanonicalUnitCell(
            area=1.0,
            skin=skin,
            members=(BeamMember(_section(), length=1.0, angle_rad=0.0, eccentricity=0.0),),
            frame=point.frame,
        )

    cache = WallCache()
    field = HomogenizedWallField(plate, factory, EnergyHomogenizer(), cache=cache)

    first = field.law_at(plate, 0.1, 0.2)
    second = field.law_at(plate, 0.1, 0.2)

    assert first is second
    assert len(calls) == 1
    assert cache.size == 1
    assert first.frame == plate.point_at(0.1, 0.2).frame
    assert first.metadata["source"] == "homogenized_wall_field"


def test_homogenized_wall_field_rejects_frame_mismatch() -> None:
    cylinder = Cylinder(radius=2.0)
    calls = 0

    def factory(surface: Surface, point: SurfacePoint) -> CanonicalUnitCell:
        del surface, point
        return CanonicalUnitCell(
            area=1.0,
            skin=_wall(),
            members=(BeamMember(_section(), length=1.0, angle_rad=0.0, eccentricity=0.0),),
        )

    class CountingHomogenizer:
        def compute(
            self,
            cell: CanonicalUnitCell,
            *,
            validity_context: ValidityContext | None = None,
        ) -> NoReturn:
            nonlocal calls
            del cell, validity_context
            calls += 1
            raise AssertionError("homogenizer should not run for a bad cell frame")

    field = HomogenizedWallField(cylinder, factory, CountingHomogenizer())

    with pytest.raises(ValueError, match="frame"):
        field.law_at(cylinder, 0.1, 0.2)

    assert calls == 0


def test_homogenized_wall_field_can_use_surface_min_radius_for_validity() -> None:
    surface = ConicalFrustum(radius_start=2.0, radius_end=3.0, length=5.0)

    def factory(_surface: Surface, point: SurfacePoint) -> CanonicalUnitCell:
        return CanonicalUnitCell(
            area=1.0,
            skin=_wall(scale=1.0, frame=point.frame),
            members=(BeamMember(_section(), length=1.0, angle_rad=0.0, eccentricity=0.0),),
            frame=point.frame,
        )

    def validity_context(point: SurfacePoint, _cell: CanonicalUnitCell) -> ValidityContext:
        return ValidityContext(
            characteristic_height=0.1,
            pitch=0.2,
            min_radius=point.min_radius,
            response_length=10.0,
        )

    field = HomogenizedWallField(
        surface,
        factory,
        EnergyHomogenizer(),
        validity_context_factory=validity_context,
    )

    law = field.law_at(surface, 1.0, 0.25)

    assert law.validity is not None
    assert law.validity.h_over_R == pytest.approx(0.1 / surface.point_at(1.0, 0.25).min_radius)
    assert law.validity.p_over_R == pytest.approx(0.2 / surface.point_at(1.0, 0.25).min_radius)


class _LinearField:
    def __init__(self, validity: ValidityReport) -> None:
        self.validity = validity

    def law_at(self, surface: Surface, u: float, v: float) -> LinearABDWall:
        point = surface.point_at(u, v)
        scale = 1.0 + u + 2.0 * v
        return _wall(
            scale=scale,
            frame=point.frame,
            validity=self.validity,
            areal_mass=scale,
        )


def test_wall_atlas_bilinearly_interpolates_linear_walls() -> None:
    surface = FlatPlate()
    validity = ValidityReport(
        h_over_R=0.0,
        p_over_R=0.0,
        p_over_L_response=0.02,
        coupling_ratios={"B_fro": 0.0},
        warnings=("sample_warning",),
    )
    atlas = WallAtlas.from_field(
        surface,
        _LinearField(validity),
        u_values=(0.0, 1.0),
        v_values=(0.0, 1.0),
    )

    law = atlas.law_at(surface, 0.25, 0.5)

    assert atlas.metadata["u_values"] == (0.0, 1.0)
    assert atlas.metadata["v_values"] == (0.0, 1.0)
    assert atlas.metadata["sample_shape"] == (2, 2)
    assert isinstance(atlas.metadata["sample_digest"], str)
    assert len(atlas.metadata["sample_digest"]) == 64
    assert atlas.metadata["sample_warning_ids"] == ("sample_warning",)
    assert atlas.metadata["max_adjacent_c8_gradient_frobenius"] == pytest.approx(2.0 * np.sqrt(8.0))
    atlas_again = WallAtlas.from_field(
        surface,
        _LinearField(validity),
        u_values=(0.0, 1.0),
        v_values=(0.0, 1.0),
    )
    assert atlas_again.metadata["sample_digest"] == atlas.metadata["sample_digest"]

    np.testing.assert_allclose(law.C8, 2.25 * np.eye(8))
    assert law.areal_mass == pytest.approx(2.25)
    assert law.validity == validity
    assert law.metadata["source"] == "wall_atlas_bilinear"
    assert law.metadata["grid_cell"] == (0, 0)
    assert law.metadata["corner_warnings"] == ("sample_warning",)
    assert law.metadata["max_corner_delta_frobenius"] > 0.0


def test_wall_atlas_interpolates_on_conical_frustum() -> None:
    surface = ConicalFrustum(radius_start=2.0, radius_end=3.0, length=5.0)
    validity = ValidityReport(
        h_over_R=0.0,
        p_over_R=0.0,
        p_over_L_response=0.0,
        coupling_ratios={"B_fro": 0.0},
        warnings=(),
    )

    atlas = WallAtlas.from_field(
        surface,
        _LinearField(validity),
        u_values=(0.5, 1.5),
        v_values=(0.0, 1.0),
    )

    law = atlas.law_at(surface, 1.0, 0.25)

    np.testing.assert_allclose(law.C8, 2.5 * np.eye(8))
    assert law.frame == surface.point_at(1.0, 0.25).frame
    assert law.metadata["source"] == "wall_atlas_bilinear"


def test_wall_atlas_rejects_invalid_grid_and_out_of_bounds_lookup() -> None:
    surface = FlatPlate()
    validity = ValidityReport(
        h_over_R=0.0,
        p_over_R=0.0,
        p_over_L_response=0.0,
        coupling_ratios={"B_fro": 0.0},
        warnings=(),
    )

    with pytest.raises(ValueError, match="strictly increasing"):
        WallAtlas.from_field(
            surface,
            _LinearField(validity),
            u_values=(0.0, 0.0),
            v_values=(0.0, 1.0),
        )

    atlas = WallAtlas.from_field(
        surface,
        _LinearField(validity),
        u_values=(0.0, 1.0),
        v_values=(0.0, 1.0),
    )

    with pytest.raises(ValueError, match="outside"):
        atlas.law_at(surface, -0.1, 0.5)


def test_wall_atlas_rejects_frame_mismatched_samples() -> None:
    surface = Cylinder(radius=2.0)
    laws = (
        (_wall(), _wall()),
        (_wall(), _wall()),
    )

    with pytest.raises(ValueError, match="surface point frame"):
        WallAtlas(
            surface=surface,
            u_values=(0.0, 1.0),
            v_values=(0.0, 1.0),
            laws=laws,
        )


def test_wall_atlas_rejects_mixed_conventions() -> None:
    surface = FlatPlate()
    point = surface.point_at(0.0, 0.0)
    other_convention = StrainConvention(reference_surface="shifted_reference")
    law = _wall(frame=point.frame)
    other_law = LinearABDWall.from_tangent(
        np.eye(8),
        frame=point.frame,
        convention=other_convention,
    )
    laws = (
        (law, law),
        (law, other_law),
    )

    with pytest.raises(ValueError, match="same strain convention"):
        WallAtlas(
            surface=surface,
            u_values=(0.0, 1.0),
            v_values=(0.0, 1.0),
            laws=laws,
        )
