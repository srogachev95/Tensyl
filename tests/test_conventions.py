from __future__ import annotations

import numpy as np
import pytest

from tensyl import (
    CanonicalUnitCell,
    Frame2D,
    IsotropicMaterial,
    StrainConvention,
    isotropic_plate,
    superpose_abd_stiffnesses,
)
from tensyl.cells import BeamMember
from tests._helpers import beam_section


def test_frame_rejects_left_handed_basis() -> None:
    with pytest.raises(ValueError, match="right-handed"):
        Frame2D(
            e1=np.array([1.0, 0.0, 0.0]),
            e2=np.array([0.0, 1.0, 0.0]),
            n=np.array([0.0, 0.0, -1.0]),
        )


def test_frame_rotation_is_right_handed() -> None:
    frame = Frame2D.canonical().rotate(np.pi / 3.0)

    np.testing.assert_allclose(np.linalg.norm(frame.e1), 1.0)
    np.testing.assert_allclose(np.linalg.norm(frame.e2), 1.0)
    np.testing.assert_allclose(frame.e1 @ frame.e2, 0.0, atol=1.0e-15)
    np.testing.assert_allclose(np.cross(frame.e1, frame.e2), frame.n, atol=1.0e-15)


def test_phase1_rejects_tensor_shear_convention() -> None:
    with pytest.raises(ValueError, match="engineering shear"):
        StrainConvention(engineering_shear=False)


def _nearly_canonical_frame(*, label: str = "nudged") -> Frame2D:
    wobble = 1.0e-13
    e1 = np.array([1.0, wobble, 0.0])
    e2 = np.array([-wobble, 1.0, 0.0])
    return Frame2D(
        e1=e1 / np.linalg.norm(e1),
        e2=e2 / np.linalg.norm(e2),
        n=np.array([0.0, 0.0, 1.0]),
        label=label,
    )


def test_frames_are_close_when_only_label_or_roundoff_differs() -> None:
    canonical = Frame2D.canonical()

    assert canonical.is_close(Frame2D.canonical(label="panel"))
    assert canonical.is_close(_nearly_canonical_frame())
    assert not canonical.is_close(canonical.rotate(0.1))


def test_superposition_accepts_frames_that_differ_only_by_label_or_roundoff() -> None:
    material = IsotropicMaterial(E=70.0e9, nu=0.33)
    skin = isotropic_plate(material, thickness=0.002)
    relabeled = isotropic_plate(material, thickness=0.001, frame=Frame2D.canonical(label="face"))
    nudged = isotropic_plate(material, thickness=0.001, frame=_nearly_canonical_frame())

    combined = superpose_abd_stiffnesses(skin, relabeled, nudged)

    assert combined.frame == skin.frame
    np.testing.assert_allclose(combined.A, 2.0 * skin.A)


def test_superposition_still_rejects_rotated_frames() -> None:
    material = IsotropicMaterial(E=70.0e9, nu=0.33)
    skin = isotropic_plate(material, thickness=0.002)

    with pytest.raises(ValueError, match="same frame"):
        superpose_abd_stiffnesses(skin, skin.rotate(0.1))


def test_cell_accepts_a_skin_whose_frame_differs_only_by_label() -> None:
    skin = isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.002)

    cell = CanonicalUnitCell(
        area=1.0,
        skin=skin,
        members=(BeamMember(beam_section(), 1.0, 0.0, 0.0),),
        frame=Frame2D.canonical(label="panel"),
    )

    assert cell.frame.label == "panel"
