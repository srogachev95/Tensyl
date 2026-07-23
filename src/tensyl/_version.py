"""Package-version helper for provenance metadata."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


def tensyl_version() -> str:
    """Return the installed Tensyl version.

    Returns:
        Installed package version, or ``"0.0.0"`` when running from a local
        tree before package metadata is available.
    """

    try:
        return version("tensyl")
    except PackageNotFoundError:  # pragma: no cover - editable tree before install
        return "0.0.0"


__all__ = ["tensyl_version"]
