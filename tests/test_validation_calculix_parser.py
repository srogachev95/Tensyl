from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "validation" / "lib"))

from tensyl_validation.calculix import (  # noqa: E402
    parse_calculix_reaction_dat,
    parse_calculix_stress_dat,
    parse_reaction_summary,
)


def test_calculix_dat_parser_extracts_load_case_nodal_rows_and_totals() -> None:
    table = parse_calculix_reaction_dat(
        """
        ** load_case: e11

         forces (fx,fy,fz) for set ALLNODES and time  1.0000000E+00

              1  1.000000E+01 -2.000000E+00  0.000000E+00
              2 -5.000000E+00  4.000000E+00  1.250000E+00
          total  5.000000E+00  2.000000E+00  1.250000E+00
        """
    )

    assert table.load_case == "e11"
    assert table.totals == {"RF1": 5.0, "RF2": 2.0, "RF3": 1.25}
    assert [row.as_dict() for row in table.nodal_reactions] == [
        {"node_id": 1, "values": {"RF1": 10.0, "RF2": -2.0, "RF3": 0.0}},
        {"node_id": 2, "values": {"RF1": -5.0, "RF2": 4.0, "RF3": 1.25}},
    ]

    summary = parse_reaction_summary(table_text_with_totals())

    assert summary.load_case == "e11"
    assert summary.values == {"RF1": 5.0, "RF2": 2.0, "RF3": 1.25}


def test_calculix_dat_parser_sums_nodal_rows_when_totals_are_absent() -> None:
    summary = parse_reaction_summary(
        """
        load case: g12_unit

              node       RF1             RF2             RF3
                 1  2.500000D+00  0.000000D+00 -1.000000D+00
                 2 -5.000000D-01  1.500000D+00  3.000000D+00
        """
    )

    assert summary.load_case == "g12_unit"
    assert summary.values == {"RF1": 2.0, "RF2": 1.5, "RF3": 2.0}


def test_calculix_dat_parser_merges_force_and_moment_blocks_by_node() -> None:
    table = parse_calculix_reaction_dat(
        """
        ** load_case: k12_unit

         forces (fx,fy,fz) for set ALLNODES and time  1.0000000E+00
              1  1.000000E+00  2.000000E+00  3.000000E+00

         moments (mx,my,mz) for set ALLNODES and time  1.0000000E+00
              1 -1.000000E-01  2.000000E-01 -3.000000E-01
          total -1.000000E-01  2.000000E-01 -3.000000E-01
        """
    )

    assert table.load_case == "k12_unit"
    assert table.nodal_reactions[0].values == {
        "RF1": 1.0,
        "RF2": 2.0,
        "RF3": 3.0,
        "RM1": -0.1,
        "RM2": 0.2,
        "RM3": -0.3,
    }
    assert table.totals == {"RM1": -0.1, "RM2": 0.2, "RM3": -0.3}


def test_calculix_stress_parser_extracts_shell_stress_rows() -> None:
    table = parse_calculix_stress_dat(
        """
        ** load_case: epsilon_11

        stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set SKIN and time 1.0

             1   1  1.000000E+01  2.000000E+00  0.0  3.000000E+00  0.0  0.0
             1   5  1.400000E+01  6.000000E+00  0.0  7.000000E+00  0.0  0.0
        """
    )

    bottom, top = table.top_bottom_component_means()

    assert table.load_case == "epsilon_11"
    assert len(table.rows) == 2
    assert table.rows[0].element_set == "SKIN"
    assert table.component_means()["sxx"] == 12.0
    assert bottom["sxy"] == 3.0
    assert top["syy"] == 6.0


def test_calculix_stress_parser_preserves_multiple_element_sets() -> None:
    table = parse_calculix_stress_dat(
        """
        stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set SKIN and time 1.0

             1   1  1.000000E+01  2.000000E+00  0.0  3.000000E+00  0.0  0.0
             1   5  1.400000E+01  6.000000E+00  0.0  7.000000E+00  0.0  0.0

        stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set STIFFENER and time 1.0

           101   1  2.000000E+01  0.0  0.0  0.0  0.0  0.0
           101   2  2.200000E+01  0.0  0.0  0.0  0.0  0.0
        """
    )

    skin = table.table_for_set("skin")
    stiffener = table.table_for_set("STIFFENER")

    assert len(table.rows) == 4
    assert len(skin.rows) == 2
    assert len(stiffener.rows) == 2
    assert skin.component_means()["sxx"] == 12.0
    assert stiffener.component_means()["sxx"] == 21.0
    assert table.rows[-1].as_dict()["element_set"] == "STIFFENER"


def table_text_with_totals() -> str:
    return """
    ** load_case: e11

     forces (fx,fy,fz) for set ALLNODES and time  1.0000000E+00

          1  1.000000E+01 -2.000000E+00  0.000000E+00
          2 -5.000000E+00  4.000000E+00  1.250000E+00
      total  5.000000E+00  2.000000E+00  1.250000E+00
    """
