from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.calculix import (  # noqa: E402
    STANDARD_ABD_LOAD_CASES,
    CalculixSkinPatch,
    parse_reaction_summary,
    render_skin_patch_decks,
    render_skin_patch_inp,
)
from tensyl_validation.calculix.decks import GeneralizedStrainLoadCase  # noqa: E402
from tensyl_validation.gmsh import GmshSkinPatch, render_rectangular_skin_geo  # noqa: E402


def test_gmsh_rectangular_skin_geo_is_centered_and_recombined() -> None:
    patch = GmshSkinPatch(length=2.0, width=1.0, divisions_x=4, divisions_y=2)

    text = render_rectangular_skin_geo(patch)

    assert "Point(1) = {-1, -0.5, 0, lc};" in text
    assert "Point(3) = {1, 0.5, 0, lc};" in text
    assert "Transfinite Curve {1, 3} = 5;" in text
    assert "Transfinite Curve {2, 4} = 3;" in text
    assert "Recombine Surface {1};" in text
    assert 'Physical Surface("skin") = {1};' in text


def test_calculix_standard_decks_cover_six_abd_load_cases() -> None:
    patch = CalculixSkinPatch(
        length=2.0,
        width=1.0,
        thickness=0.1,
        youngs_modulus=70.0e9,
        poissons_ratio=0.3,
        divisions_x=2,
        divisions_y=1,
    )

    decks = render_skin_patch_decks(patch)

    assert tuple(decks) == tuple(load_case.name for load_case in STANDARD_ABD_LOAD_CASES)
    assert len(decks) == 6
    assert all("*ELEMENT, TYPE=S4, ELSET=SKIN" in deck for deck in decks.values())
    assert all("*NODE PRINT, NSET=ALLNODES, TOTALS=YES" in deck for deck in decks.values())


def test_calculix_membrane_shear_load_case_prescribes_engineering_shear() -> None:
    patch = CalculixSkinPatch(
        length=2.0,
        width=1.0,
        thickness=0.1,
        youngs_modulus=1.0,
        poissons_ratio=0.25,
        divisions_x=1,
        divisions_y=1,
    )
    load_case = GeneralizedStrainLoadCase("g12_half", (0.0, 0.0, 0.5, 0.0, 0.0, 0.0))

    deck = render_skin_patch_inp(patch, load_case)

    assert "** generalized_strain_order: e11, e22, g12, k11, k22, k12" in deck
    assert "1, 1, 1, -0.125" in deck
    assert "1, 2, 2, -0.25" in deck
    assert "4, 1, 1, 0.125" in deck
    assert "4, 2, 2, 0.25" in deck


def test_calculix_twist_load_case_prescribes_linear_rotations() -> None:
    patch = CalculixSkinPatch(
        length=2.0,
        width=1.0,
        thickness=0.1,
        youngs_modulus=1.0,
        poissons_ratio=0.25,
        divisions_x=1,
        divisions_y=1,
    )
    load_case = GeneralizedStrainLoadCase("k12_unit", (0.0, 0.0, 0.0, 0.0, 0.0, 1.0))

    deck = render_skin_patch_inp(patch, load_case)

    assert "1, 4, 4, 0.5" in deck
    assert "1, 5, 5, -0.25" in deck
    assert "4, 4, 4, -0.5" in deck
    assert "4, 5, 5, 0.25" in deck


def test_compact_reaction_summary_parser_accepts_key_value_lines() -> None:
    summary = parse_reaction_summary(
        """
        # compact post-processed CalculiX reactions
        load_case: e11
        RF1 = 12.5
        RM2, -3.0e-2
        N11 7.25
        ** ignored CalculiX-style comment
        """
    )

    assert summary.load_case == "e11"
    assert summary.values == {"RF1": 12.5, "RM2": -3.0e-2, "N11": 7.25}
    assert summary.as_dict()["values"]["N11"] == 7.25


@pytest.mark.parametrize(
    ("length", "poissons_ratio", "divisions_x", "message"),
    [
        (0.0, 0.3, 1, "length"),
        (1.0, 0.5, 1, "poissons_ratio"),
        (1.0, 0.3, 0, "divisions_x"),
    ],
)
def test_calculix_skin_patch_rejects_invalid_inputs(
    length: float,
    poissons_ratio: float,
    divisions_x: int,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        CalculixSkinPatch(
            length=length,
            width=1.0,
            thickness=0.1,
            youngs_modulus=1.0,
            poissons_ratio=poissons_ratio,
            divisions_x=divisions_x,
            divisions_y=1,
        )
