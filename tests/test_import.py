from __future__ import annotations

import tensyl


def test_package_exposes_version() -> None:
    assert isinstance(tensyl.__version__, str)
    assert tensyl.__version__
