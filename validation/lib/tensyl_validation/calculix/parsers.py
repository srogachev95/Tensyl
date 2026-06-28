"""CalculiX reaction-summary parsers for validation post-processing."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

_NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?"
_KEY_VALUE = re.compile(rf"^\s*([A-Za-z][A-Za-z0-9_/-]*)\s*(?:=|:|,|\s)\s*({_NUMBER})\s*$")
_CASE = re.compile(r"^\s*(?:case|load(?:[-_ ]case)?)\s*(?:=|:|\s)\s*([A-Za-z][A-Za-z0-9_-]*)\s*$")
_COMPONENT = re.compile(r"\b(?:RF|RM)[1-6]\b", re.IGNORECASE)
_FORCE_HEADER = re.compile(r"\bforces?\s*\(([^)]*)\)", re.IGNORECASE)
_MOMENT_HEADER = re.compile(r"\bmoments?\s*\(([^)]*)\)", re.IGNORECASE)
_STRESS_HEADER = re.compile(
    r"\bstresses?\s*\([^)]*\)\s+for\s+set\s+([A-Za-z][A-Za-z0-9_-]*)\b",
    re.IGNORECASE,
)
_NUMERIC_TOKEN = re.compile(rf"^{_NUMBER}$")


@dataclass(frozen=True, slots=True)
class CalculixReactionSummary:
    """Parsed compact reaction/resultant summary."""

    load_case: str | None
    values: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"load_case": self.load_case, "values": dict(self.values)}


@dataclass(frozen=True, slots=True)
class CalculixNodalReaction:
    """Reaction components for one CalculiX node row."""

    node_id: int
    values: dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"node_id": self.node_id, "values": dict(self.values)}


@dataclass(frozen=True, slots=True)
class CalculixReactionTable:
    """Parsed CalculiX ``.dat`` reaction table."""

    load_case: str | None
    totals: dict[str, float] = field(default_factory=dict)
    nodal_reactions: tuple[CalculixNodalReaction, ...] = ()

    def summed_nodal_values(self) -> dict[str, float]:
        """Return component sums from nodal rows."""

        values: dict[str, float] = {}
        for row in self.nodal_reactions:
            for component, value in row.values.items():
                values[component] = values.get(component, 0.0) + value
        return values

    def as_dict(self) -> dict[str, Any]:
        return {
            "load_case": self.load_case,
            "totals": dict(self.totals),
            "nodal_reactions": [row.as_dict() for row in self.nodal_reactions],
        }


@dataclass(frozen=True, slots=True)
class CalculixStressRow:
    """One CalculiX shell stress output row."""

    element_id: int
    integration_point: int
    sxx: float
    syy: float
    szz: float
    sxy: float
    sxz: float
    syz: float
    element_set: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "integration_point": self.integration_point,
            "sxx": self.sxx,
            "syy": self.syy,
            "szz": self.szz,
            "sxy": self.sxy,
            "sxz": self.sxz,
            "syz": self.syz,
            "element_set": self.element_set,
        }


@dataclass(frozen=True, slots=True)
class CalculixStressTable:
    """Parsed CalculiX shell stress table."""

    load_case: str | None
    rows: tuple[CalculixStressRow, ...]

    def rows_for_set(self, element_set: str) -> tuple[CalculixStressRow, ...]:
        """Return rows from one CalculiX element set."""

        key = element_set.upper()
        return tuple(row for row in self.rows if (row.element_set or "").upper() == key)

    def table_for_set(self, element_set: str) -> CalculixStressTable:
        """Return a stress table filtered to one CalculiX element set."""

        return CalculixStressTable(
            load_case=self.load_case,
            rows=self.rows_for_set(element_set),
        )

    def component_means(self) -> dict[str, float]:
        """Return mean stress components over all parsed rows."""

        if not self.rows:
            return {}
        components = ("sxx", "syy", "szz", "sxy", "sxz", "syz")
        return {
            component: sum(getattr(row, component) for row in self.rows) / len(self.rows)
            for component in components
        }

    def top_bottom_component_means(self) -> tuple[dict[str, float], dict[str, float]]:
        """Return bottom/top means using CalculiX's 1-4 and 5-8 shell points."""

        bottom = [row for row in self.rows if row.integration_point <= 4]
        top = [row for row in self.rows if row.integration_point > 4]
        if not bottom or not top:
            return {}, {}
        components = ("sxx", "syy", "szz", "sxy", "sxz", "syz")
        bottom_means = {
            component: sum(getattr(row, component) for row in bottom) / len(bottom)
            for component in components
        }
        top_means = {
            component: sum(getattr(row, component) for row in top) / len(top)
            for component in components
        }
        return bottom_means, top_means

    def as_dict(self) -> dict[str, Any]:
        return {
            "load_case": self.load_case,
            "rows": [row.as_dict() for row in self.rows],
        }


def parse_reaction_summary(text: str) -> CalculixReactionSummary:
    """Parse compact reaction/resultant text or a CalculiX ``.dat`` RF table.

    The accepted format is deliberately small: optional ``case`` or
    ``load_case`` line, followed by numeric key/value rows such as ``RF1
    12.5`` or ``N11 = 12.5``. Blank lines and ``#``/``**`` comments are ignored.

    For CalculiX ``*NODE PRINT, NSET=ALLNODES, TOTALS=YES`` output, total RF/RM
    components are returned when present. If the solver output only contains
    nodal rows, component sums from those rows are returned.
    """

    load_case: str | None = None
    values: dict[str, float] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized_line = _strip_comment_prefix(line)
        case_match = _CASE.match(normalized_line)
        if case_match:
            load_case = case_match.group(1)
            continue
        if line.startswith("#") or line.startswith("**"):
            continue
        value_match = _KEY_VALUE.match(line)
        if value_match:
            key = value_match.group(1)
            values[key] = _to_float(value_match.group(2))

    dat_table = parse_calculix_reaction_dat(text)
    if load_case is None:
        load_case = dat_table.load_case
    if dat_table.totals:
        values.update(dat_table.totals)
    elif dat_table.nodal_reactions:
        values.update(dat_table.summed_nodal_values())
    return CalculixReactionSummary(load_case=load_case, values=values)


def parse_calculix_stress_dat(text: str) -> CalculixStressTable:
    """Parse CalculiX ``.dat`` shell stress output."""

    load_case: str | None = None
    rows: list[CalculixStressRow] = []
    in_stress_block = False
    active_element_set: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        normalized_line = _strip_comment_prefix(line)
        case_match = _CASE.match(normalized_line)
        if case_match:
            load_case = case_match.group(1)
            continue
        if line.startswith("#") or line.startswith("**"):
            continue
        stress_header = _STRESS_HEADER.search(line)
        if stress_header:
            in_stress_block = True
            active_element_set = stress_header.group(1).upper()
            continue
        if line.lower().startswith("stresses "):
            in_stress_block = True
            active_element_set = None
            continue
        if not in_stress_block:
            continue
        row = _parse_stress_row(line, element_set=active_element_set)
        if row is not None:
            rows.append(row)
            continue
        if rows and re.search(r"[A-Za-z]", line):
            in_stress_block = False
            active_element_set = None

    return CalculixStressTable(load_case=load_case, rows=tuple(rows))


def parse_calculix_reaction_dat(text: str) -> CalculixReactionTable:
    """Parse CalculiX ``.dat`` reaction force/moment node-print output.

    The parser targets the deterministic text tables written by CalculiX for
    ``*NODE PRINT, NSET=ALLNODES, TOTALS=YES``. It recognizes force headers such
    as ``forces (fx,fy,fz)`` as RF1/RF2/RF3, moment headers as RM1/RM2/RM3, and
    explicit column headers such as ``node RF1 RF2 RF3``.
    """

    load_case: str | None = None
    totals: dict[str, float] = {}
    nodal_values: dict[int, dict[str, float]] = {}
    active_columns: tuple[str, ...] = ()
    saw_data_in_block = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        normalized_line = _strip_comment_prefix(line)
        case_match = _CASE.match(normalized_line)
        if case_match:
            load_case = case_match.group(1)
            continue
        if line.startswith("#") or line.startswith("**"):
            continue

        header_columns = _columns_from_header(line)
        if header_columns:
            active_columns = header_columns
            saw_data_in_block = False
            continue

        explicit_columns = _columns_from_explicit_header(line)
        if explicit_columns:
            active_columns = explicit_columns
            continue

        if not active_columns:
            continue

        total_values = _parse_total_row(line, active_columns)
        if total_values is not None:
            totals.update(total_values)
            active_columns = ()
            saw_data_in_block = False
            continue

        node_row = _parse_node_row(line, active_columns)
        if node_row is not None:
            node_id, values = node_row
            nodal_values.setdefault(node_id, {}).update(values)
            saw_data_in_block = True
            continue

        if saw_data_in_block and re.search(r"[A-Za-z]", line):
            active_columns = ()
            saw_data_in_block = False

    nodal_reactions = tuple(
        CalculixNodalReaction(node_id=node_id, values=values)
        for node_id, values in sorted(nodal_values.items())
    )
    return CalculixReactionTable(
        load_case=load_case,
        totals=totals,
        nodal_reactions=nodal_reactions,
    )


def _strip_comment_prefix(line: str) -> str:
    if line.startswith("**"):
        return line[2:].strip()
    if line.startswith("#"):
        return line[1:].strip()
    return line


def _to_float(token: str) -> float:
    return float(token.replace("D", "E").replace("d", "e"))


def _columns_from_header(line: str) -> tuple[str, ...]:
    force_match = _FORCE_HEADER.search(line)
    if force_match:
        return _columns_from_component_list(force_match.group(1), default_prefix="RF")

    moment_match = _MOMENT_HEADER.search(line)
    if moment_match:
        return _columns_from_component_list(moment_match.group(1), default_prefix="RM")

    return ()


def _columns_from_explicit_header(line: str) -> tuple[str, ...]:
    components = tuple(match.group(0).upper() for match in _COMPONENT.finditer(line))
    return components


def _columns_from_component_list(text: str, *, default_prefix: str) -> tuple[str, ...]:
    components: list[str] = []
    for raw_component in re.split(r"[\s,]+", text):
        component = raw_component.strip().lower()
        if not component:
            continue
        normalized = _normalize_component(component, default_prefix=default_prefix)
        if normalized is not None:
            components.append(normalized)
    return tuple(components)


def _normalize_component(component: str, *, default_prefix: str) -> str | None:
    component = component.strip().lower()
    explicit = _COMPONENT.fullmatch(component)
    if explicit:
        return explicit.group(0).upper()

    axis_components = {"x": 1, "y": 2, "z": 3}
    if len(component) == 2 and component[1] in axis_components:
        if component[0] == "f":
            return f"RF{axis_components[component[1]]}"
        if component[0] == "m":
            return f"RM{axis_components[component[1]]}"
    if component in axis_components:
        return f"{default_prefix}{axis_components[component]}"
    if component.isdigit():
        return f"{default_prefix}{int(component)}"
    return None


def _parse_total_row(line: str, columns: tuple[str, ...]) -> dict[str, float] | None:
    parts = _split_dat_row(line)
    if not parts or parts[0].lower().rstrip(":") not in {"total", "totals"}:
        return None
    values = _numeric_values(parts[1:])
    if len(values) < len(columns):
        return None
    return dict(zip(columns, values, strict=False))


def _parse_node_row(line: str, columns: tuple[str, ...]) -> tuple[int, dict[str, float]] | None:
    parts = _split_dat_row(line)
    if len(parts) < len(columns) + 1 or not parts[0].isdigit():
        return None
    values = _numeric_values(parts[1:])
    if len(values) < len(columns):
        return None
    return int(parts[0]), dict(zip(columns, values, strict=False))


def _split_dat_row(line: str) -> list[str]:
    return [part for part in re.split(r"[\s,]+", line.strip()) if part]


def _numeric_values(parts: list[str]) -> list[float]:
    values: list[float] = []
    for part in parts:
        token = part.rstrip(",")
        if _NUMERIC_TOKEN.match(token):
            values.append(_to_float(token))
    return values


def _parse_stress_row(line: str, *, element_set: str | None) -> CalculixStressRow | None:
    parts = _split_dat_row(line)
    if len(parts) < 8 or not parts[0].isdigit() or not parts[1].isdigit():
        return None
    values = _numeric_values(parts[2:8])
    if len(values) != 6:
        return None
    return CalculixStressRow(
        element_id=int(parts[0]),
        integration_point=int(parts[1]),
        sxx=values[0],
        syy=values[1],
        szz=values[2],
        sxy=values[3],
        sxz=values[4],
        syz=values[5],
        element_set=element_set,
    )
