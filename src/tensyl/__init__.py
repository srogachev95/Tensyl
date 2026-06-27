"""Tensyl public package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("tensyl")
except PackageNotFoundError:  # pragma: no cover - editable tree before install
    __version__ = "0.0.0"

__all__ = ["__version__"]
