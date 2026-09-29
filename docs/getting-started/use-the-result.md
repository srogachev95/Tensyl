# Apply Loads and Save the Result

Apply a membrane force of 10,000 N/m in the `e1` direction. The load vector also
has places for the other membrane forces, bending moments per width, and
transverse shear resultants. Set those to zero for this example.

Continue with `cell` and `result` from the previous page:

```python
--8<-- "docs/examples/scripts/walkthrough.py:loads"
```

`strains` solves the coupled plate relation. The returned components are
`ε11, ε22, γ12, κ11, κ22, κ12, γ13, γ23`: strains are dimensionless and curvatures
have units 1/m. `member_loads` then evaluates each rib under that deformation.

--8<-- "docs/includes/walkthrough-response.md"

Although the applied moment is zero, the panel curves. Its ribs are above the
reference surface, so axial load carried by those ribs produces a moment about
that surface. The negative curvature balances that moment. This is why solving
with the complete `A`, `B`, and `D` blocks matters for an eccentric panel.

The recovered axial force is for **one physical rib**. Cell area and the number
of represented ribs determine the equivalent stiffness; they do not multiply
that individual rib force. See [member loads](../user-guide/homogenization.md#strains-and-member-loads)
for all five recovered components and their signs.

## Inspect and Save

For a labeled display of all stiffness blocks and the report, run:

```python
print(result.summary(units={"A": "N/m", "B": "N", "D": "N m", "As": "N/m"}))
```

Save the complete result, including its modeling assumptions and validity report:

```python
--8<-- "docs/examples/scripts/walkthrough.py:save"

restored = save_result(Path("panel.json"))
```

The unit labels describe the values stored in the file. They do not rescale them.
[JSON and YAML workflows](../user-guide/external-workflows.md) cover cells, sampled
atlases, and thermal loads as well.

You now have a panel model, its stiffness and mass, and a response to applied load.
Continue with [the mechanics](../theory/equivalent-stiffness.md),
[building another construction](../user-guide/beam-sections-and-cells.md), or
[using results in a solver](../user-guide/solver-handoff.md).
