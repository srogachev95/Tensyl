"""Artifact helpers for validation runs."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import tensyl


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write compact, deterministic JSON for committed validation artifacts."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


@dataclass(frozen=True, slots=True)
class ArtifactManifest:
    """Minimal manifest for a validation run."""

    case_name: str
    command: list[str]
    inputs: list[Path]
    outputs: list[Path]
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = "tensyl.validation.artifact-manifest.v1"

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable manifest."""

        git_commit = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            check=False,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return {
            "schema_version": self.schema_version,
            "created_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
            "case_name": self.case_name,
            "command": self.command,
            "inputs": [
                {"path": str(path), "sha256": _sha256(path)}
                for path in self.inputs
                if path.exists()
            ],
            "outputs": [{"path": str(path)} for path in self.outputs],
            "software": {
                "python": platform.python_version(),
                "platform": platform.platform(),
                "tensyl": tensyl.__version__,
                "git_commit": git_commit or None,
            },
            "metadata": self.metadata,
        }
