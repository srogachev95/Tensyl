from __future__ import annotations

import numpy as np
import pytest

from tensyl import IsotropicMaterial, Ply, laminate_plate, layup

MATERIAL = IsotropicMaterial(E=70e9, nu=0.3)


def test_ply_from_degrees_preserves_thickness_material_and_label() -> None:
    ply = Ply.from_degrees(MATERIAL, 0.001, -45.0, "bottom")
    assert ply == Ply(MATERIAL, 0.001, -np.pi / 4, "bottom")


@pytest.mark.parametrize(
    ("notation", "angles"),
    [
        ("[0/±45/90]s", [0, 45, -45, 90, 90, -45, 45, 0]),
        ("[0/+-45/90]s", [0, 45, -45, 90, 90, -45, 45, 0]),
        ("[∓30/90]", [-30, 30, 90]),
        ("[0_2/90₂]", [0, 0, 90, 90]),
        ("[0/90]2", [0, 90, 0, 90]),
        ("[0/90]2s", [0, 90, 0, 90, 90, 0, 90, 0]),
        (" -22.5 / +.5 / 90 ", [-22.5, 0.5, 90]),
        ("[±45_2]", [45, -45, 45, -45]),
    ],
)
def test_layup_notation_expands_bottom_to_top(notation: str, angles: list[float]) -> None:
    plies = layup(MATERIAL, 0.001, notation)
    assert isinstance(plies, tuple)
    np.testing.assert_allclose([p.angle_rad for p in plies], np.deg2rad(angles))
    assert all(p.material is MATERIAL and p.thickness == 0.001 for p in plies)


@pytest.mark.parametrize(
    "notation",
    [
        "",
        "[]",
        "[0//90]",
        "[0,90]",
        "[0/90",
        "0/90]",
        "[0/90]0",
        "[0_0]",
        "[nan]",
        "[inf]",
        "[45deg]",
        "[±-45]",
        "[0]ss",
        "[0]2.5",
        "[0]S",
        "[[0/90]2]",
        "[0/90]s2",
        "[0/]",
        "0 90",
        "[0₀]",
    ],
)
def test_layup_rejects_unsupported_or_ambiguous_notation(notation: str) -> None:
    with pytest.raises(ValueError, match="layup"):
        layup(MATERIAL, 0.001, notation)


def test_symmetric_expansion_has_zero_B_for_an_orthotropic_laminate() -> None:
    from tensyl import OrthotropicPlyMaterial

    material = OrthotropicPlyMaterial(E1=130e9, E2=10e9, G12=5e9, nu12=0.3, G13=5e9, G23=4e9)
    stiffness = laminate_plate(layup(material, 0.000125, "[0/±45/90]s"))
    np.testing.assert_allclose(stiffness.B, 0.0, atol=1e-11)


@pytest.mark.parametrize("angle", [np.nan, np.inf, -np.inf])
def test_degrees_reject_nonfinite_angles(angle: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        Ply.from_degrees(MATERIAL, 0.001, angle)
