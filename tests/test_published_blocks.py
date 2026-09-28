from __future__ import annotations

import numpy as np
import pytest

from tensyl import ABDStiffness, StiffnessSymmetryError


def _blocks():
    return {"A": np.eye(3), "B": np.eye(3) * 0.1, "D": np.eye(3), "As": np.eye(2)}


def test_strict_symmetry_error_points_to_the_explicit_import_path() -> None:
    blocks = _blocks()
    blocks["A"][0, 1] = 1e-7
    with pytest.raises(StiffnessSymmetryError, match="from_published_blocks"):
        ABDStiffness(**blocks)


@pytest.mark.parametrize("name", ["A", "B", "D", "As"])
def test_printed_precision_blocks_are_averaged_with_recorded_corrections(name: str) -> None:
    blocks = _blocks()
    scale = float(np.max(np.abs(blocks[name])))
    blocks[name][0, 1] = scale * 8e-7
    original = blocks[name].copy()
    stiffness = ABDStiffness.from_published_blocks(**blocks, metadata={"paper": "example"})
    np.testing.assert_array_equal(getattr(stiffness, name), (original + original.T) / 2)
    np.testing.assert_array_equal(blocks[name], original)
    assert stiffness.metadata["paper"] == "example"
    provenance = stiffness.metadata["published_blocks"]
    assert provenance["max_relative_correction"] == pytest.approx(4e-7)
    assert provenance["absolute_corrections"][name] == pytest.approx(scale * 4e-7)
    assert not stiffness.C8.flags.writeable


def test_published_blocks_use_each_block_scale_and_reject_large_asymmetry() -> None:
    blocks = _blocks()
    blocks["A"] *= 1e12
    blocks["B"][0, 1] = 1e-5
    with pytest.raises(StiffnessSymmetryError, match="B"):
        ABDStiffness.from_published_blocks(**blocks)


def test_published_blocks_accept_zero_blocks_and_reject_nonfinite_data() -> None:
    blocks = _blocks()
    blocks["B"][:] = 0.0
    stiffness = ABDStiffness.from_published_blocks(**blocks, rtol=0.0)
    assert stiffness.metadata["published_blocks"]["max_relative_correction"] == 0.0
    blocks["D"][0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        ABDStiffness.from_published_blocks(**blocks)


@pytest.mark.parametrize("rtol", [-1.0, np.inf, np.nan, 1.0])
def test_published_blocks_reject_invalid_tolerances(rtol: float) -> None:
    with pytest.raises(ValueError, match="rtol"):
        ABDStiffness.from_published_blocks(**_blocks(), rtol=rtol)
