# Ellipsoid Stiffness Map

This example is intentionally a little theatrical. A triaxial ellipsoid is not
the first shape anyone reaches for when they want a tidy closed-form stiffened
shell calculation. That is the point.

Tensyl does not need a new formula for every surface-and-stiffener combination.
The local rule stays the same:

1. ask the surface for a point, frame, and curvature scale;
2. build a tangent-plane stiffened cell in that local frame;
3. homogenize the cell into an ABD stiffness;
4. attach validity ratios to the result;
5. repeat wherever the wall definition changes.

The figure below uses that workflow over a fictional ellipsoid. The local skin
thickness, stiffener pitch, stiffener orientation, and section scale vary with
position. The left panel colors the ellipsoid by normalized local `A11`
membrane stiffness. The right panel shows `p_over_R`, the pitch-to-local-radius
ratio that says where the tangent-plane approximation is working hardest. The
white contours are normalized `A11` again, because a contour line is sometimes
the polite way to tell a heatmap it has company.

![A two-panel Matplotlib figure: a triaxial ellipsoid colored by normalized local membrane stiffness, beside a latitude-longitude map of pitch over local radius with stiffness contours.](../assets/examples/ellipsoid-stiffness-map.png)

!!! warning "This is a formulation demo, not a flight article"
    The layout is fictional and chosen to make the moving parts visible. Tensyl
    computes local equivalent stiffnesses and validity signals here. It does not
    compute buckling loads, joint stresses, imperfections, margins, or allowables.

## What Changes Pointwise

The example uses `Ellipsoid` for geometry and `HomogenizedStiffnessField` for the
wall law. At each sample point:

- `surface.point_at(phi, theta)` supplies position, local frame, curvature, and
  `min_radius`;
- the cell factory computes local pitch, section scale, stiffener angle, skin
  thickness, and eccentricity;
- `EnergyHomogenizer` returns a local `ABDStiffness`;
- `ValidityContext` records `p_over_R`, `h_over_R`, and response-length checks.

That is the useful trick. The curved surface does not magically bend the ABD
matrix. The pointwise cell factory changes the wall law, while the surface tells
Tensyl how to read that law locally.

## Rebuild the Figure

The full generator lives at
[`docs/examples/scripts/ellipsoid_stiffness_map.py`](scripts/ellipsoid_stiffness_map.py).
It writes the committed documentation image:

```bash
uv run python docs/examples/scripts/ellipsoid_stiffness_map.py
```

The core field setup looks like this:

```python
from tensyl import (
    BeamMember,
    CanonicalUnitCell,
    Ellipsoid,
    EnergyHomogenizer,
    HomogenizedStiffnessField,
    StiffnessCache,
    ValidityContext,
)

surface = Ellipsoid(a=180.0, b=125.0, c=75.0, label="ellipsoid_showpiece")


def cell_factory(surface, point):
    del surface
    design = design_at(point.u, point.v)
    skin = isotropic_plate(material, thickness=design["skin_thickness"], frame=point.frame)
    skin_face = 0.5 * design["skin_thickness"]
    return CanonicalUnitCell(
        area=design["primary_pitch"] * design["secondary_pitch"],
        skin=skin,
        members=(
            BeamMember(
                section=primary_section(design),
                length=design["secondary_pitch"],
                angle_rad=design["angle_rad"],
                eccentricity=skin_face + primary_centroid_z,
            ),
            BeamMember(
                section=secondary_section(design),
                length=design["primary_pitch"],
                angle_rad=design["angle_rad"] + 0.5 * math.pi,
                eccentricity=skin_face + secondary_centroid_z,
            ),
        ),
        frame=point.frame,
        convention=skin.convention,
    )


def validity_context(point, cell):
    pitch = max(cell.metadata["primary_pitch"], cell.metadata["secondary_pitch"])
    return ValidityContext(
        characteristic_height=0.62,
        pitch=pitch,
        min_radius=point.min_radius,
        response_length=52.0,
    )


field = HomogenizedStiffnessField(
    surface,
    cell_factory,
    EnergyHomogenizer(),
    cache=StiffnessCache(),
    validity_context_factory=validity_context,
)
```

The generator includes the missing setup details: material values,
geometry-derived sections, the pointwise design function, Matplotlib styling,
and the image export. The short excerpt above is only the shape of the method;
the script is the executable version.

## Why This Is Useful

Closed-form equivalent-plate formulas are valuable, but they usually want a
friendly geometry, repeated layout, and fixed assumptions. This example is not
friendly. The local frame moves, the curvature changes, the pitch changes, the
stiffener angle sweeps, and the stiffness is still computed as one consistent
local wall law at each point.

That does not make the result automatically valid. It does make the assumptions
visible enough to argue with, which is a more useful starting point than a
beautiful spreadsheet with no place to put curvature.
