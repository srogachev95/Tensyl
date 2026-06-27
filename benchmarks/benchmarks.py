from __future__ import annotations

import numpy as np

from tensyl import (
    BeamSection,
    ConstantWallField,
    DirectECHomogenizer,
    EnergyHomogenizer,
    FlatPlate,
    IsotropicMaterial,
    StiffenerFamily,
    WallAtlas,
    isotropic_plate,
    orthogrid_cell,
)
from tensyl.io import from_json, from_yaml, to_json, to_yaml


def _skin():
    return isotropic_plate(IsotropicMaterial(E=70.0e9, nu=0.33), thickness=0.004)


def _section():
    return BeamSection(
        EA=1.2e6,
        EIy=50.0,
        EIz=30.0,
        GJ=20.0,
        kGAy=4.0e5,
        kGAz=3.0e5,
    )


def _orthogrid():
    section = _section()
    return orthogrid_cell(
        skin=_skin(),
        stringer_section=section,
        rib_section=section,
        stringer_spacing=0.25,
        rib_spacing=0.40,
        stringer_eccentricity=0.012,
        rib_eccentricity=0.009,
    )


class HomogenizationSuite:
    def setup(self) -> None:
        self.skin = _skin()
        self.section = _section()
        self.cell = _orthogrid()
        self.families = (
            StiffenerFamily(
                section=self.section,
                spacing=0.25,
                angle_rad=0.0,
                eccentricity=0.012,
                label="stringer",
            ),
            StiffenerFamily(
                section=self.section,
                spacing=0.40,
                angle_rad=np.pi / 2.0,
                eccentricity=0.009,
                label="rib",
            ),
        )
        self.energy = EnergyHomogenizer()
        self.direct = DirectECHomogenizer()

    def time_energy_orthogrid(self) -> None:
        self.energy.compute(self.cell)

    def time_direct_ec_orthogrid(self) -> None:
        self.direct.compute(skin=self.skin, families=self.families)


class WallFieldSuite:
    def setup(self) -> None:
        self.surface = FlatPlate()
        self.field = ConstantWallField(EnergyHomogenizer().compute(_orthogrid()).law)
        self.u_values = tuple(np.linspace(0.0, 1.0, 8))
        self.v_values = tuple(np.linspace(0.0, 1.0, 8))
        self.atlas = WallAtlas.from_field(
            self.surface,
            self.field,
            u_values=self.u_values,
            v_values=self.v_values,
        )

    def time_constant_field_grid(self) -> None:
        for u in self.u_values:
            for v in self.v_values:
                self.field.law_at(self.surface, u, v)

    def time_wall_atlas_grid(self) -> None:
        for u in self.u_values:
            for v in self.v_values:
                self.atlas.law_at(self.surface, u, v)


class SerializationSuite:
    def setup(self) -> None:
        self.result = EnergyHomogenizer().compute(_orthogrid())
        self.yaml_text = to_yaml(self.result)
        self.json_text = to_json(self.result)

    def time_to_yaml_homogenization_result(self) -> None:
        to_yaml(self.result)

    def time_from_yaml_homogenization_result(self) -> None:
        from_yaml(self.yaml_text)

    def time_to_json_homogenization_result(self) -> None:
        to_json(self.result)

    def time_from_json_homogenization_result(self) -> None:
        from_json(self.json_text)
