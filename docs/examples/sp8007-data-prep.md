# SP-8007 Data Prep Example

This example prepares equivalent wall data that an analyst could hand to a
separate SP-8007-style cylinder workflow. Tensyl does not compute SP-8007
knockdown factors or margins.

```python
from tensyl import (
    BeamSection,
    Cylinder,
    EnergyHomogenizer,
    IsotropicMaterial,
    ValidityContext,
    isotropic_plate,
    orthogrid_cell,
)
from tensyl.io import from_yaml, to_yaml


def sp8007_orthotropic_coefficients(wall, *, tolerance=1.0e-9):
    """Extract the SP-8007 orthotropic-cylinder coefficients from a local wall law."""

    unsupported = {
        "A16": wall.A[0, 2],
        "A26": wall.A[1, 2],
        "B16": wall.B[0, 2],
        "B26": wall.B[1, 2],
        "B61": wall.B[2, 0],
        "B62": wall.B[2, 1],
        "D16": wall.D[0, 2],
        "D26": wall.D[1, 2],
    }
    nonzero = {
        name: value
        for name, value in unsupported.items()
        if abs(value) > tolerance
    }
    if nonzero:
        msg = (
            "SP-8007 orthotropic-cylinder coefficients assume axial/circumferential "
            f"orthotropy; unsupported coupling terms are nonzero: {nonzero}"
        )
        raise ValueError(msg)

    return {
        "Ebar_x": wall.A[0, 0],
        "Ebar_y": wall.A[1, 1],
        "Ebar_xy": wall.A[0, 1],
        "Gbar_xy": wall.A[2, 2],
        "Dbar_x": wall.D[0, 0],
        "Dbar_y": wall.D[1, 1],
        "Dbar_xy": 2.0 * wall.D[0, 1] + 4.0 * wall.D[2, 2],
        "Cbar_x": wall.B[0, 0],
        "Cbar_y": wall.B[1, 1],
        "Cbar_xy": wall.B[0, 1],
        "Kbar_xy": wall.B[2, 2],
    }

skin = isotropic_plate(IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1), thickness=0.080)
section = BeamSection(EA=3.2e6, EIy=2.4e4, EIz=6.5e3, GJ=4.0e3, kGAy=1.1e6, kGAz=0.9e6)
cell = orthogrid_cell(
    skin=skin,
    stringer_section=section,
    rib_section=section,
    stringer_spacing=6.0,
    rib_spacing=8.0,
    stringer_eccentricity=0.45,
    rib_eccentricity=0.45,
)
result = EnergyHomogenizer().compute(
    cell,
    validity_context=ValidityContext(
        characteristic_height=0.50,
        pitch=8.0,
        min_radius=120.0,
        response_length=80.0,
    ),
)
surface = Cylinder(radius=120.0, length=300.0)
sp8007 = sp8007_orthotropic_coefficients(result.law)

report = {
    "radius": surface.radius,
    "length": surface.length,
    "sp8007": sp8007,
    "transverse_shear": {
        "Abar_xz": result.law.As[0, 0],
        "Abar_yz": result.law.As[1, 1],
    },
    "h_over_R": result.validity.h_over_R,
    "p_over_R": result.validity.p_over_R,
    "p_over_L_response": result.validity.p_over_L_response,
    "warnings": result.validity.warnings,
}

artifact = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)
loaded = from_yaml(artifact)

assert loaded.law.C8.shape == (8, 8)
assert report["sp8007"]["Ebar_x"] == result.law.A[0, 0]
assert report["sp8007"]["Dbar_xy"] == 2.0 * result.law.D[0, 1] + 4.0 * result.law.D[2, 2]
assert report["p_over_R"] == 8.0 / 120.0
```

For `Cylinder`, Tensyl's local `e1` direction is axial and local `e2` is
circumferential, matching the SP-8007 `x/y` convention used in Section 4.1.2.
The extraction above maps Tensyl's local wall law to the barred coefficients
used in the SP-8007 orthotropic-cylinder equations:

| SP-8007 coefficient | Tensyl source |
| --- | --- |
| `Ebar_x` | `A[0, 0]` |
| `Ebar_y` | `A[1, 1]` |
| `Ebar_xy` | `A[0, 1]` |
| `Gbar_xy` | `A[2, 2]` |
| `Dbar_x` | `D[0, 0]` |
| `Dbar_y` | `D[1, 1]` |
| `Dbar_xy` | `2*D[0, 1] + 4*D[2, 2]` |
| `Cbar_x` | `B[0, 0]` |
| `Cbar_y` | `B[1, 1]` |
| `Cbar_xy` | `B[0, 1]` |
| `Kbar_xy` | `B[2, 2]` |

This reduction assumes the wall is orthotropic in the axial/circumferential
frame used by SP-8007. If `A16`, `A26`, `B16`, `B26`, `B61`, `B62`, `D16`, or
`D26` are not negligible, the wall is not represented by this coefficient set
without an additional rotation or a more general shell-buckling workflow.
