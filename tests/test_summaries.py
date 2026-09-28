from __future__ import annotations

from tensyl import EnergyHomogenizer
from tests.test_validity import _eccentric_grid


def test_stiffness_repr_is_compact_and_shows_missing_mass_and_warning_count() -> None:
    result = EnergyHomogenizer().compute(_eccentric_grid())
    text = repr(result.stiffness)
    assert len(text) < 200
    assert "array(" not in text
    assert result.stiffness.frame.label in text
    assert "areal_mass=None" in text
    assert "A11=" in text and "D11=" in text
    assert f"warnings={len(result.validity.warnings)}" in text


def test_stiffness_summary_labels_engineering_blocks_without_converting_units(capsys) -> None:
    stiffness = EnergyHomogenizer().compute(_eccentric_grid()).stiffness
    text = stiffness.summary(units={"A": "N/m", "D": "N m"}, precision=5)
    assert "engineering shear" in text
    assert "A [N/m]" in text and "D [N m]" in text
    assert "B\n" in text and "As\n" in text
    assert f"{stiffness.A[0, 0]:.5e}" in text
    assert "p_over_R_unavailable" in text
    assert capsys.readouterr().out == ""


def test_result_summary_includes_assumptions_and_warnings() -> None:
    result = EnergyHomogenizer().compute(_eccentric_grid())
    text = result.summary()
    assert "Source: energy" in text
    assert all(warning in text for warning in result.validity.warnings)
    assert all(assumption in text for assumption in result.assumptions)
