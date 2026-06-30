# SP-8007 Data Handoff

Tensyl can prepare equivalent stiffness-property data for a separate
SP-8007-style or orthotropic-cylinder calculation. Tensyl does not compute
SP-8007 knockdown factors, buckling loads, margins, or allowables. Its job here
is narrower: compute and preserve local equivalent ABD stiffness data, geometry
context, validity ratios, assumptions, and serialized artifacts for another
calculation to consume.

NASA SP-8007 is shell-buckling guidance. Nemeth's equivalent-plate work is a
source for stiffened equivalent-plate stiffness concepts. Tensyl sits between
those worlds: it produces local stiffness data, then gets out of the way.

Treat an SP-8007 handoff as a translation, not as proof that either model is
right. The barred constants below are the data shape expected by a classical
orthotropic-cylinder calculation. They are useful precisely because they are
small and familiar, but that also means they can hide terms that are present in
the full ABD stiffness. The public
[SP-8007 reconciliation report](../validation/sp8007-reconciliation.md) shows
where Tensyl and the SP-8007 elastic-constant formulas agree, and where they
diverge because the models retain different bending physics. That report also
calls out a printed-equation problem in SP-8007: isogrid Eqs. 97-98 do not show
the explicit eccentric `EA z^2` bending terms. Correct that omission before
using the isogrid bending formulas as a physics reference.

A downstream SP-8007-style workflow commonly needs these data categories from a
stiffness model:

- SP-8007 orthotropic-cylinder extensional coefficients `Ebar_x`, `Ebar_y`,
  `Ebar_xy`, and `Gbar_xy`;
- bending and twisting coefficients `Dbar_x`, `Dbar_y`, and `Dbar_xy`;
- membrane-bending coupling coefficients `Cbar_x`, `Cbar_y`, `Cbar_xy`, and
  `Kbar_xy` when coupling is not negligible;
- transverse-shear stiffnesses `As` when relevant;
- whether membrane-bending coupling `B` is negligible or must be retained;
- cylinder radius and length from geometry;
- pitch, stiffener height, and validity ratios such as `h_over_R`, `p_over_R`,
  and `p_over_L_response`;
- warnings, assumptions, and serialized artifacts for traceability.

## Coefficient Extraction

For the built-in `Cylinder`, Tensyl's local `e1` direction is axial and local
`e2` is circumferential. Under the SP-8007 Section 4.1.2 orthotropic-cylinder
assumption that the orthotropy axes coincide with those directions, the barred
coefficients used in Eqs. 54-59 and 71-81 map to Tensyl's local ABD stiffness as:

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

`Dbar_xy` is not just `D[2, 2]`; SP-8007 uses a modified twisting coefficient
that combines anticlastic bending and engineering twist terms. Tensyl's public
strain convention uses engineering shear/twist ordering
`(e11, e22, gamma12, k11, k22, k12, gamma13, gamma23)`, so the coefficient is
`2*D12 + 4*D66`.

For stiffened walls, pay special attention to `Dbar_x`, `Dbar_y`, and
`Dbar_xy`. Tensyl retains centroidal beam-section terms through the member
strain map. Some SP-8007 elastic-constant expressions are more compact and do
not expose every possible beam contribution as a separate term. When those
numbers disagree, inspect section inertia, torsion constant, reference-surface
choice, and eccentricity before deciding that either source is wrong.

For orthogrids, the main known reduction is cross-family in-plane bending.
Tensyl includes rib `EIz` in `Dbar_x` and stringer `EIz` in `Dbar_y`. SP-8007
ring/stringer Eqs. 89-91 do not expose those terms, so a handoff that keeps only
the barred constants can hide bending stiffness from wide, flanged, capped, or
closed stiffeners.

For isogrids with eccentric members, use corrected bending terms:

$$
\bar{D}_{x,\mathrm{corr}}
=
\bar{D}_{x,\mathrm{printed}}
+
\frac{3\sqrt{3}}{4}\frac{EA}{a}z^2,
$$

$$
\bar{D}_{y,\mathrm{corr}}
=
\bar{D}_{y,\mathrm{printed}}
+
\frac{3\sqrt{3}}{4}\frac{EA}{a}z^2,
$$

and

$$
\bar{D}_{xy,\mathrm{corr}}
=
\bar{D}_{xy,\mathrm{printed}}
+
\frac{3\sqrt{3}}{2}\frac{EA}{a}z^2.
$$

```python
def sp8007_orthotropic_coefficients(stiffness, *, tolerance=1.0e-9):
    """Extract SP-8007 orthotropic-cylinder coefficients from a local ABD stiffness."""

    unsupported = {
        "A16": stiffness.A[0, 2],
        "A26": stiffness.A[1, 2],
        "B16": stiffness.B[0, 2],
        "B26": stiffness.B[1, 2],
        "B61": stiffness.B[2, 0],
        "B62": stiffness.B[2, 1],
        "D16": stiffness.D[0, 2],
        "D26": stiffness.D[1, 2],
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
        "Ebar_x": stiffness.A[0, 0],
        "Ebar_y": stiffness.A[1, 1],
        "Ebar_xy": stiffness.A[0, 1],
        "Gbar_xy": stiffness.A[2, 2],
        "Dbar_x": stiffness.D[0, 0],
        "Dbar_y": stiffness.D[1, 1],
        "Dbar_xy": 2.0 * stiffness.D[0, 1] + 4.0 * stiffness.D[2, 2],
        "Cbar_x": stiffness.B[0, 0],
        "Cbar_y": stiffness.B[1, 1],
        "Cbar_xy": stiffness.B[0, 1],
        "Kbar_xy": stiffness.B[2, 2],
    }
```

!!! warning "Do not silently drop the off-axis terms"
    This coefficient set does not represent every possible ABD stiffness. If `A16`,
    `A26`, `B16`, `B26`, `B61`, `B62`, `D16`, or `D26` are not negligible,
    rotate the stiffness into its orthotropic axes or use a more general downstream
    buckling workflow. Dropping those terms to make the data fit the SP-8007
    mold throws away real anisotropy. The structure will not file a complaint.

## Orthogrid Handoff

This worked handoff prepares an orthogrid equivalent stiffness for a separate
SP-8007-style cylinder workflow.

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
point = surface.point_at(150.0, 0.0)
sp8007 = sp8007_orthotropic_coefficients(result.stiffness)

report = {
    "radius": surface.radius,
    "length": surface.length,
    "sp8007": sp8007,
    "transverse_shear": {
        "Abar_xz": result.stiffness.As[0, 0],
        "Abar_yz": result.stiffness.As[1, 1],
    },
    "h_over_R": result.validity.h_over_R,
    "p_over_R": result.validity.p_over_R,
    "p_over_L_response": result.validity.p_over_L_response,
    "warnings": result.validity.warnings,
    "assumptions": result.assumptions,
    "frame_label": point.frame.label,
}

artifact = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)
loaded = from_yaml(artifact)

assert loaded.stiffness.C8.shape == (8, 8)
assert report["sp8007"]["Ebar_x"] == result.stiffness.A[0, 0]
assert report["sp8007"]["Dbar_xy"] == 2.0 * result.stiffness.D[0, 1] + 4.0 * result.stiffness.D[2, 2]
assert report["p_over_R"] == 8.0 / 120.0
```

Use the serialized artifact as a traceable record of the stiffness-property
calculation. Unit labels are metadata; Tensyl does not convert values.

## Isogrid Variant

For an equilateral isogrid whose local `0` degree member family is axial,
extract the same SP-8007 coefficient set from the homogenized ABD stiffness:

```python
from tensyl import equilateral_isogrid_cell


isogrid_skin = isotropic_plate(
    IsotropicMaterial(E=10.6e6, nu=0.33, density=0.1),
    thickness=0.060,
)
isogrid_section = BeamSection(
    EA=2.8e6,
    EIy=1.8e4,
    EIz=5.2e3,
    GJ=3.2e3,
    kGAy=0.9e6,
    kGAz=0.7e6,
)
isogrid_cell = equilateral_isogrid_cell(
    skin=isogrid_skin,
    member_section=isogrid_section,
    pitch=6.0,
    eccentricity=0.35,
)
isogrid_result = EnergyHomogenizer().compute(
    isogrid_cell,
    validity_context=ValidityContext(
        characteristic_height=0.42,
        pitch=6.0,
        min_radius=120.0,
        response_length=80.0,
    ),
)
isogrid_sp8007 = sp8007_orthotropic_coefficients(isogrid_result.stiffness)

assert abs(isogrid_sp8007["Ebar_x"] - isogrid_sp8007["Ebar_y"]) < 1.0e-6
assert abs(isogrid_sp8007["Cbar_x"] - isogrid_sp8007["Cbar_y"]) < 1.0e-6
```

The equality checks are not SP-8007 requirements. They are useful sanity checks
for this equilateral, equal-member example because the isogrid should be
balanced in the local axial and circumferential directions.

## Symmetric Laminate Variant

For a skin-only laminate cylinder, build the laminate ABD stiffness directly and
extract the same barred coefficients. This example uses a symmetric cross-ply
stack so the membrane-bending coupling block is negligible.

```python
from tensyl import OrthotropicPlyMaterial, Ply, laminate_plate


carbon_epoxy = OrthotropicPlyMaterial(
    E1=18.0e6,
    E2=1.4e6,
    G12=0.75e6,
    nu12=0.28,
    G13=0.75e6,
    G23=0.50e6,
    density=0.058,
)
laminate_stiffness = laminate_plate(
    (
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=1.5707963267948966),
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=1.5707963267948966),
        Ply(material=carbon_epoxy, thickness=0.005, angle_rad=0.0),
    )
)
laminate_sp8007 = sp8007_orthotropic_coefficients(laminate_stiffness)
laminate_report = {
    "radius": surface.radius,
    "length": surface.length,
    "sp8007": laminate_sp8007,
    "transverse_shear": {
        "Abar_xz": laminate_stiffness.As[0, 0],
        "Abar_yz": laminate_stiffness.As[1, 1],
    },
}

assert abs(laminate_report["sp8007"]["Cbar_x"]) < 1.0e-9
assert abs(laminate_report["sp8007"]["Cbar_y"]) < 1.0e-9
```
