"""Compact CalculiX reaction-summary parsers for validation post-processing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"
_KEY_VALUE = re.compile(rf"^\s*([A-Za-z][A-Za-z0-9_/-]*)\s*(?:=|:|,|\s)\s*({_NUMBER})\s*$")
_CASE = re.compile(r"^\s*(?:case|load_case)\s*(?:=|:|\s)\s*([A-Za-z][A-Za-z0-9_]*)\s*$")


@dataclass(frozen=True, slots=True)
class CalculixReactionSummary:
    """Parsed compact reaction/resultant summary."""

    load_case: str | None
    values: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"load_case": self.load_case, "values": dict(self.values)}


def parse_reaction_summary(text: str) -> CalculixReactionSummary:
    """Parse compact ``key value`` reaction/resultant text.

    The accepted format is deliberately small: optional ``case`` or
    ``load_case`` line, followed by numeric key/value rows such as ``RF1
    12.5`` or ``N11 = 12.5``. Blank lines and ``#``/``**`` comments are ignored.
    """

    load_case: str | None = None
    values: dict[str, float] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("**"):
            continue
        case_match = _CASE.match(line)
        if case_match:
            load_case = case_match.group(1)
            continue
        value_match = _KEY_VALUE.match(line)
        if value_match:
            key = value_match.group(1)
            values[key] = float(value_match.group(2))
    return CalculixReactionSummary(load_case=load_case, values=values)
