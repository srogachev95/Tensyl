"""Deterministic CalculiX input decks for local ABD extraction patches."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import isfinite, sqrt


def _positive(value: float, *, name: str) -> float:
    checked = float(value)
    if not isfinite(checked) or checked <= 0.0:
        msg = f"{name} must be a finite positive number."
        raise ValueError(msg)
    return checked


def _poisson(value: float) -> float:
    checked = float(value)
    if not isfinite(checked) or checked <= -1.0 or checked >= 0.5:
        msg = "poissons_ratio must be finite and in the open interval (-1, 0.5)."
        raise ValueError(msg)
    return checked


def _positive_int(value: int, *, name: str) -> int:
    checked = int(value)
    if checked <= 0:
        msg = f"{name} must be positive."
        raise ValueError(msg)
    return checked


def _name(value: str, *, name: str) -> str:
    checked = str(value)
    if not checked or not checked.replace("_", "").isalnum() or checked[0].isdigit():
        msg = f"{name} must be a non-empty identifier using letters, numbers, and underscores."
        raise ValueError(msg)
    return checked


def _fmt(value: float) -> str:
    return f"{value:.12g}"


@dataclass(frozen=True, slots=True)
class CalculixSkinPatch:
    """Structured rectangular isotropic shell patch for CalculiX validation."""

    length: float
    width: float
    thickness: float
    youngs_modulus: float
    poissons_ratio: float
    divisions_x: int
    divisions_y: int
    name: str = "skin_patch"
    material_name: str = "skin_material"

    def __post_init__(self) -> None:
        object.__setattr__(self, "length", _positive(self.length, name="length"))
        object.__setattr__(self, "width", _positive(self.width, name="width"))
        object.__setattr__(self, "thickness", _positive(self.thickness, name="thickness"))
        object.__setattr__(
            self,
            "youngs_modulus",
            _positive(self.youngs_modulus, name="youngs_modulus"),
        )
        object.__setattr__(self, "poissons_ratio", _poisson(self.poissons_ratio))
        object.__setattr__(
            self,
            "divisions_x",
            _positive_int(self.divisions_x, name="divisions_x"),
        )
        object.__setattr__(
            self,
            "divisions_y",
            _positive_int(self.divisions_y, name="divisions_y"),
        )
        object.__setattr__(self, "name", _name(self.name, name="name"))
        object.__setattr__(
            self,
            "material_name",
            _name(self.material_name, name="material_name").upper(),
        )

    @property
    def area(self) -> float:
        """Patch midsurface area."""

        return self.length * self.width


@dataclass(frozen=True, slots=True)
class CalculixBeamStiffness:
    """Target beam stiffnesses carried into a CalculiX probe deck."""

    EA: float
    EIy: float
    EIz: float
    GJ: float
    kGAy: float | None = None
    kGAz: float | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "EA", _positive(self.EA, name="EA"))
        object.__setattr__(self, "EIy", _positive(self.EIy, name="EIy"))
        object.__setattr__(self, "EIz", _positive(self.EIz, name="EIz"))
        object.__setattr__(self, "GJ", _positive(self.GJ, name="GJ"))
        if self.kGAy is not None:
            object.__setattr__(self, "kGAy", _positive(self.kGAy, name="kGAy"))
        if self.kGAz is not None:
            object.__setattr__(self, "kGAz", _positive(self.kGAz, name="kGAz"))

    def as_comments(self) -> list[str]:
        """Return deterministic comments recording the intended section law."""

        values = [
            f"EA={_fmt(self.EA)}",
            f"EIy={_fmt(self.EIy)}",
            f"EIz={_fmt(self.EIz)}",
            f"GJ={_fmt(self.GJ)}",
        ]
        if self.kGAy is not None:
            values.append(f"kGAy={_fmt(self.kGAy)}")
        if self.kGAz is not None:
            values.append(f"kGAz={_fmt(self.kGAz)}")
        return ["** target_beam_stiffness: " + ", ".join(values)]


@dataclass(frozen=True, slots=True)
class CalculixUnidirectionalStiffenedPatch:
    """Structured skin patch with one shared-node beam stiffener line."""

    skin: CalculixSkinPatch
    beam: CalculixBeamStiffness
    stiffener_y: float = 0.0
    stiffener_elset: str = "STIFFENER"
    stiffener_material_name: str = "stiffener_material"

    def __post_init__(self) -> None:
        if self.skin.divisions_y % 2 != 0:
            msg = "unidirectional stiffener probe requires an even divisions_y for a y=0 line."
            raise ValueError(msg)
        if abs(float(self.stiffener_y)) > 0.5 * self.skin.width:
            msg = "stiffener_y must lie inside the skin patch."
            raise ValueError(msg)
        object.__setattr__(
            self,
            "stiffener_elset",
            _name(self.stiffener_elset, name="stiffener_elset").upper(),
        )
        object.__setattr__(
            self,
            "stiffener_material_name",
            _name(self.stiffener_material_name, name="stiffener_material_name").upper(),
        )

    @property
    def stiffener_node_row(self) -> int:
        """Structured grid row used by the zero-eccentric stiffener."""

        dy = self.skin.width / self.skin.divisions_y
        row = round((float(self.stiffener_y) + 0.5 * self.skin.width) / dy)
        y = -0.5 * self.skin.width + row * dy
        if abs(y - float(self.stiffener_y)) > 1.0e-10:
            msg = "stiffener_y must fall on the structured skin grid."
            raise ValueError(msg)
        return row

    @property
    def beam_area(self) -> float:
        """Equivalent beam area implied by the target axial stiffness."""

        return self.beam.EA / self.skin.youngs_modulus

    @property
    def beam_rect_dimensions(self) -> tuple[float, float]:
        """Return a rectangular proxy preserving EA and EIy for review runs."""

        area = self.beam_area
        inertia_y = self.beam.EIy / self.skin.youngs_modulus
        thickness_1 = sqrt(12.0 * inertia_y / area)
        thickness_2 = area / thickness_1
        return thickness_1, thickness_2


@dataclass(frozen=True, slots=True)
class GeneralizedStrainLoadCase:
    """One canonical membrane/bending generalized strain load case."""

    name: str
    values: tuple[float, float, float, float, float, float]

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _name(self.name, name="name"))
        values = tuple(float(value) for value in self.values)
        if len(values) != 6 or any(not isfinite(value) for value in values):
            msg = "values must contain six finite generalized strain components."
            raise ValueError(msg)
        object.__setattr__(self, "values", values)

    @property
    def e11(self) -> float:
        return self.values[0]

    @property
    def e22(self) -> float:
        return self.values[1]

    @property
    def g12(self) -> float:
        return self.values[2]

    @property
    def k11(self) -> float:
        return self.values[3]

    @property
    def k22(self) -> float:
        return self.values[4]

    @property
    def k12(self) -> float:
        return self.values[5]


STANDARD_ABD_LOAD_CASES: tuple[GeneralizedStrainLoadCase, ...] = (
    GeneralizedStrainLoadCase("e11", (1.0, 0.0, 0.0, 0.0, 0.0, 0.0)),
    GeneralizedStrainLoadCase("e22", (0.0, 1.0, 0.0, 0.0, 0.0, 0.0)),
    GeneralizedStrainLoadCase("g12", (0.0, 0.0, 1.0, 0.0, 0.0, 0.0)),
    GeneralizedStrainLoadCase("k11", (0.0, 0.0, 0.0, 1.0, 0.0, 0.0)),
    GeneralizedStrainLoadCase("k22", (0.0, 0.0, 0.0, 0.0, 1.0, 0.0)),
    GeneralizedStrainLoadCase("k12", (0.0, 0.0, 0.0, 0.0, 0.0, 1.0)),
)


def _node_id(i: int, j: int, divisions_x: int) -> int:
    return j * (divisions_x + 1) + i + 1


def _nodes(patch: CalculixSkinPatch) -> Iterator[tuple[int, float, float, float]]:
    dx = patch.length / patch.divisions_x
    dy = patch.width / patch.divisions_y
    x0 = -0.5 * patch.length
    y0 = -0.5 * patch.width
    for j in range(patch.divisions_y + 1):
        for i in range(patch.divisions_x + 1):
            yield _node_id(i, j, patch.divisions_x), x0 + i * dx, y0 + j * dy, 0.0


def _elements(patch: CalculixSkinPatch) -> Iterator[tuple[int, int, int, int, int]]:
    element_id = 1
    for j in range(patch.divisions_y):
        for i in range(patch.divisions_x):
            n1 = _node_id(i, j, patch.divisions_x)
            n2 = _node_id(i + 1, j, patch.divisions_x)
            n3 = _node_id(i + 1, j + 1, patch.divisions_x)
            n4 = _node_id(i, j + 1, patch.divisions_x)
            yield element_id, n1, n2, n3, n4
            element_id += 1


def _beam_elements(
    patch: CalculixUnidirectionalStiffenedPatch,
) -> Iterator[tuple[int, int, int]]:
    element_id = patch.skin.divisions_x * patch.skin.divisions_y + 1
    row = patch.stiffener_node_row
    for i in range(patch.skin.divisions_x):
        n1 = _node_id(i, row, patch.skin.divisions_x)
        n2 = _node_id(i + 1, row, patch.skin.divisions_x)
        yield element_id, n1, n2
        element_id += 1


def _prescribed_dofs(
    x: float,
    y: float,
    load_case: GeneralizedStrainLoadCase,
) -> tuple[float, float, float, float, float, float]:
    u1 = load_case.e11 * x + 0.5 * load_case.g12 * y
    u2 = load_case.e22 * y + 0.5 * load_case.g12 * x
    u3 = 0.5 * load_case.k11 * x * x + 0.5 * load_case.k22 * y * y + 0.5 * load_case.k12 * x * y
    rot1 = -(load_case.k22 * y + 0.5 * load_case.k12 * x)
    rot2 = load_case.k11 * x + 0.5 * load_case.k12 * y
    rot3 = 0.0
    return u1, u2, u3, rot1, rot2, rot3


def _node_list(divisions_x: int, divisions_y: int) -> list[str]:
    node_ids = [
        str(_node_id(i, j, divisions_x))
        for j in range(divisions_y + 1)
        for i in range(divisions_x + 1)
    ]
    return [", ".join(node_ids[index : index + 12]) for index in range(0, len(node_ids), 12)]


def render_skin_patch_inp(
    patch: CalculixSkinPatch,
    load_case: GeneralizedStrainLoadCase,
) -> str:
    """Return a CalculiX ``.inp`` deck for one generalized strain basis case."""

    lines = [
        "*HEADING",
        f"Tensyl validation local ABD extraction: {patch.name}",
        f"** load_case: {load_case.name}",
        "** generalized_strain_order: e11, e22, g12, k11, k22, k12",
        "** rotations: dof4=rot_x, dof5=rot_y, dof6=rot_z on a +z shell normal",
        "*NODE",
    ]
    for node_id, x, y, z in _nodes(patch):
        lines.append(f"{node_id}, {_fmt(x)}, {_fmt(y)}, {_fmt(z)}")

    lines.append("*ELEMENT, TYPE=S4, ELSET=SKIN")
    for element_id, n1, n2, n3, n4 in _elements(patch):
        lines.append(f"{element_id}, {n1}, {n2}, {n3}, {n4}")

    lines.extend(
        [
            "*NSET, NSET=ALLNODES",
            *_node_list(patch.divisions_x, patch.divisions_y),
            f"*MATERIAL, NAME={patch.material_name}",
            "*ELASTIC",
            f"{_fmt(patch.youngs_modulus)}, {_fmt(patch.poissons_ratio)}",
            f"*SHELL SECTION, ELSET=SKIN, MATERIAL={patch.material_name}",
            _fmt(patch.thickness),
            "*BOUNDARY",
        ]
    )

    for node_id, x, y, _z in _nodes(patch):
        for dof, value in enumerate(_prescribed_dofs(x, y, load_case), start=1):
            lines.append(f"{node_id}, {dof}, {dof}, {_fmt(value)}")

    lines.extend(
        [
            "*STEP",
            "*STATIC",
            "*NODE PRINT, NSET=ALLNODES, TOTALS=YES",
            "RF",
            "*NODE FILE, NSET=ALLNODES",
            "U, RF",
            "*EL PRINT, ELSET=SKIN",
            "S",
            "*END STEP",
            "",
        ]
    )
    return "\n".join(lines)


def render_unidirectional_stiffened_probe_inp(
    patch: CalculixUnidirectionalStiffenedPatch,
    load_case: GeneralizedStrainLoadCase,
) -> str:
    """Return a CalculiX probe deck for a shared-node unidirectional stiffener.

    The beam section is a rectangular CalculiX proxy that preserves the target
    beam ``EA`` and ``EIy``. It is intentionally not an extracted-stiffness
    validation model until the remaining section stiffness mapping is audited.
    """

    thickness_1, thickness_2 = patch.beam_rect_dimensions
    lines = [
        "*HEADING",
        f"Tensyl validation unidirectional stiffener probe: {patch.skin.name}",
        f"** load_case: {load_case.name}",
        "** probe_status: review_deck_only_not_promoted_validation",
        "** stiffener_coupling: shared shell/beam nodes on the skin reference surface",
        "** beam_proxy: CalculiX RECT section preserves target EA and EIy only",
        *patch.beam.as_comments(),
        "** generalized_strain_order: e11, e22, g12, k11, k22, k12",
        "*NODE",
    ]
    for node_id, x, y, z in _nodes(patch.skin):
        lines.append(f"{node_id}, {_fmt(x)}, {_fmt(y)}, {_fmt(z)}")

    lines.append("*ELEMENT, TYPE=S4, ELSET=SKIN")
    for element_id, n1, n2, n3, n4 in _elements(patch.skin):
        lines.append(f"{element_id}, {n1}, {n2}, {n3}, {n4}")

    lines.append(f"*ELEMENT, TYPE=B31, ELSET={patch.stiffener_elset}")
    for element_id, n1, n2 in _beam_elements(patch):
        lines.append(f"{element_id}, {n1}, {n2}")

    lines.extend(
        [
            "*NSET, NSET=ALLNODES",
            *_node_list(patch.skin.divisions_x, patch.skin.divisions_y),
            f"*MATERIAL, NAME={patch.skin.material_name}",
            "*ELASTIC",
            f"{_fmt(patch.skin.youngs_modulus)}, {_fmt(patch.skin.poissons_ratio)}",
            f"*MATERIAL, NAME={patch.stiffener_material_name}",
            "*ELASTIC",
            f"{_fmt(patch.skin.youngs_modulus)}, {_fmt(patch.skin.poissons_ratio)}",
            f"*SHELL SECTION, ELSET=SKIN, MATERIAL={patch.skin.material_name}",
            _fmt(patch.skin.thickness),
            (
                f"*BEAM SECTION, ELSET={patch.stiffener_elset}, "
                f"MATERIAL={patch.stiffener_material_name}, SECTION=RECT"
            ),
            f"{_fmt(thickness_1)}, {_fmt(thickness_2)}",
            "0., 0., 1.",
            "*BOUNDARY",
        ]
    )

    for node_id, x, y, _z in _nodes(patch.skin):
        for dof, value in enumerate(_prescribed_dofs(x, y, load_case), start=1):
            lines.append(f"{node_id}, {dof}, {dof}, {_fmt(value)}")

    lines.extend(
        [
            "*STEP",
            "*STATIC",
            "*NODE PRINT, NSET=ALLNODES, TOTALS=YES",
            "RF",
            "*EL PRINT, ELSET=SKIN",
            "S",
            f"*EL PRINT, ELSET={patch.stiffener_elset}",
            "S",
            "*END STEP",
            "",
        ]
    )
    return "\n".join(lines)


def render_skin_patch_decks(
    patch: CalculixSkinPatch,
    load_cases: tuple[GeneralizedStrainLoadCase, ...] = STANDARD_ABD_LOAD_CASES,
) -> dict[str, str]:
    """Return one deterministic CalculiX deck per supplied load case."""

    return {load_case.name: render_skin_patch_inp(patch, load_case) for load_case in load_cases}


def render_unidirectional_stiffened_probe_decks(
    patch: CalculixUnidirectionalStiffenedPatch,
    load_cases: tuple[GeneralizedStrainLoadCase, ...] = STANDARD_ABD_LOAD_CASES,
) -> dict[str, str]:
    """Return one unidirectional stiffener probe deck per supplied load case."""

    return {
        load_case.name: render_unidirectional_stiffened_probe_inp(patch, load_case)
        for load_case in load_cases
    }
