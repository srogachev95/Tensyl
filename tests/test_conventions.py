from __future__ import annotations

import numpy as np
import pytest

from tensyl import Frame2D, StrainConvention


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
