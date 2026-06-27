"""Package-version helper for provenance metadata."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def tensyl_version() -> str:
    """Return the installed Tensyl version or a local editable-tree fallback."""

    try:
        return version("tensyl")
    except PackageNotFoundError:  # pragma: no cover - editable tree before install
        return "0.0.0"


__all__ = ["tensyl_version"]
