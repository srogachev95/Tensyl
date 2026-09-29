"""Exercise the actual field-map generators used by the handbook."""

import importlib.util
from pathlib import Path

import numpy as np


def _stiffness_maps_module():
    path = Path(__file__).parents[2] / "docs" / "examples" / "scripts" / "stiffness_field_maps.py"
    spec = importlib.util.spec_from_file_location("stiffness_field_maps", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cylinder_stiffness_map_numerics() -> None:
    module = _stiffness_maps_module()
    data = module.sample_cylinder(x_count=8, theta_count=10)

    assert data["A11"].shape == (8, 10)
    assert np.all(np.isfinite(data["A11"]))
    assert np.all(np.isfinite(data["D11"]))
    assert np.all(np.isfinite(data["p_over_R"]))
    assert np.isclose(data["radius"], 1.25)
    assert np.isclose(data["stiffener_height"], 0.025)
    assert np.ptp(data["skin_thickness"][:, 0]) > 0.0005
    assert np.ptp(data["e1_pitch"][:, 0]) > 0.025
    assert np.ptp(data["e2_pitch"][:, 0]) > 0.0375
    assert np.ptp(data["A11_ratio"][:, 0]) > 0.20
    assert np.ptp(data["D11_ratio"][:, 0]) > 0.25
    assert np.max(data["warning_count"]) > 0


def test_ellipsoid_stiffness_map_numerics() -> None:
    module = _stiffness_maps_module()
    data = module.sample_ellipsoid(phi_count=6, theta_count=9)

    assert data["A11"].shape == (6, 9)
    assert np.all(np.isfinite(data["A11"]))
    assert np.all(np.isfinite(data["D11"]))
    assert np.all(np.isfinite(data["p_over_R"]))
    assert np.min(data["phi"]) > 0.0
    assert np.max(data["phi"]) < np.pi
    assert np.ptp(data["A11_ratio"]) > 0.10
    assert np.ptp(data["p_over_R"]) > 0.05
    assert np.max(data["warning_count"]) > 0


def test_stiffness_field_map_render_smoke(tmp_path: Path) -> None:
    module = _stiffness_maps_module()
    cylinder = module.render_cylinder_map(
        tmp_path / "cylinder-stiffness-map.png",
        data=module.sample_cylinder(x_count=6, theta_count=7),
    )
    ellipsoid = module.render_ellipsoid_map(
        tmp_path / "ellipsoid-stiffness-map.png",
        data=module.sample_ellipsoid(phi_count=5, theta_count=7),
    )

    assert cylinder.exists()
    assert cylinder.stat().st_size > 10_000
    assert ellipsoid.exists()
    assert ellipsoid.stat().st_size > 10_000
