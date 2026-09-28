from __future__ import annotations

import pytest

from tensyl import (
    BeamSection,
    CanonicalUnitCell,
    EnergyHomogenizer,
    IsotropicMaterial,
    isotropic_plate,
    sweep,
    unidirectional_cell,
)


def _builder(thickness: float = 0.1, E: float = 100) -> CanonicalUnitCell:
    return unidirectional_cell(
        skin=isotropic_plate(IsotropicMaterial(E=E, nu=0.25, density=2), thickness),
        member_section=BeamSection(EA=10, EIy=2, EIz=3, GJ=1, mass_per_length=0.4),
        spacing=2,
        axial_eccentricity=0,
    )


def test_sweep_product_order_and_independent_coefficients() -> None:
    rows = sweep(_builder, {"thickness": iter([0.1, 0.2]), "E": [100, 200]})
    assert [(row["thickness"], row["E"]) for row in rows] == [
        (0.1, 100),
        (0.1, 200),
        (0.2, 100),
        (0.2, 200),
    ]
    for row in rows:
        expected = row["E"] * row["thickness"] / (1 - 0.25**2)
        assert row["A11"] == pytest.approx(expected + 5)
        assert row["D11"] == pytest.approx(expected * row["thickness"] ** 2 / 12 + 1)
        assert row["areal_mass"] == pytest.approx(2 * row["thickness"] + 0.2)
        assert "h_over_R_unavailable" in row["warning_codes"]


def test_sweep_empty_grid_and_empty_axis() -> None:
    assert len(sweep(_builder, {})) == 1
    assert sweep(_builder, {"E": []}) == []
    assert sweep(_builder, {}, homogenizer=EnergyHomogenizer()) == sweep(_builder, {})


def test_sweep_refuses_reserved_columns_before_calling_builder() -> None:
    with pytest.raises(ValueError, match="reserved"):
        sweep(_builder, {"A11": [1]})


def test_sweep_preserves_failure_and_reports_parameters() -> None:
    with pytest.raises(ValueError, match="thickness") as error:
        sweep(_builder, {"thickness": [0.1, -1]})
    assert "thickness" in error.value.__notes__[0]
    assert "-1" in error.value.__notes__[0]
