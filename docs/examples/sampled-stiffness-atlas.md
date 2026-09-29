# Variable Stiffness Fields

Let the spacing between a cylinder's axial ribs increase from 100 mm to 120 mm
along its 3 m length. Recompute the local orthogrid at each station, then sample
that field for a portable stiffness map.

Start with the material and cylinder setup from
[constant fields](../user-guide/geometry-and-fields.md#constant-stiffness-field).
The [complete script](scripts/surface_fields.py) runs all the steps on this page.

## Pointwise Homogenized Field

```python
--8<-- "docs/examples/scripts/surface_fields.py:varying"
```

The factory creates the skin and cell in `point.frame`. The context factory
supplies local curvature and the chosen response length. The inferred pitch is
the largest repeat dimension.

## Interpretation

The axial stiffness `A11` falls from 192.109 MN/m at the root to 186.276 MN/m at
the tip. Increasing axial-rib spacing spreads the same rib stiffness over more
panel area. Circumferential ribs retain their 150 mm spacing.

The cylinder radius sets the curvature scale, while the cell factory defines
the changing construction. The [surface guide](../user-guide/geometry-and-fields.md)
explains the local axes and material orientation.

## Sampled Stiffness Atlas

```python
--8<-- "docs/examples/scripts/surface_fields.py:atlas"
```

The query at 0.75 m lies halfway between the first two sampled stations. Its
`A11` is 190.518 MN/m. Bilinear interpolation uses the sampled matrix entries;
its result approaches the directly computed field as the grid resolves the
variation in spacing.

## Saving the Samples

The JSON roundtrip above stores the built-in surface definition, grid, local
stiffness samples, and provenance. Query `restored_atlas` using its restored
surface without the original Python factory. See
[files and sweeps](../user-guide/external-workflows.md#cell-inputs-and-sampled-atlases)
for the serialized data.

The atlas retains the Tensyl version recorded when its samples were created.
Loading it with a newer release preserves that provenance; sampling a new atlas
with `ABDAtlas.from_field` records the current version. Each saved file also
identifies the version that wrote the file in its `producer` block.
