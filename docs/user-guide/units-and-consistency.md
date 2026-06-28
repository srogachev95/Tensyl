# Units and Consistency

Tensyl does not own a unit system. It carries unit *labels* through to exported
artifacts, but it never inspects, infers, or converts the numbers you give it.
That keeps the library small and predictable — and it puts the entire burden of
consistency on you. Pick one unit system, use it for every input into a wall law
or cell, and Tensyl will hand you back results in that same system.

This is the one page that owns the unit policy. Other pages link here instead of
repeating it.

## The Rule

All numeric inputs to a single wall law or cell must already be in one
consistent unit system. "Consistent" means stiffness, length, force, and moment
all derive from the same base units — so that, for example, `lbf/in` times `in`
genuinely gives `lbf`.

!!! warning "Mixing unit systems fails silently"
    Tensyl will not catch a mixed-unit input. Feed it `E` in `psi` and a
    thickness in millimetres and it will dutifully compute a wall law from
    nonsense — no exception, no warning, just wrong numbers that look plausible.
    Unit discipline is yours to enforce *before* the data reaches Tensyl.

## Reference Unit Systems

For the US customary examples throughout this manual:

| Quantity | Unit |
| --- | --- |
| Length | `in` |
| Force | `lbf` |
| Stress | `psi` |
| Moment | `lbf*in` |
| Membrane stiffness (`A`, `As`) | `lbf/in` |
| Bending stiffness (`D`) | `lbf*in` |
| Coupling stiffness (`B`) | `lbf` |

For SI examples, use `m`, `N`, and `Pa`; the corresponding stiffness blocks come
out in `N/m`, `N`, and `N*m`. Either system is fine. Do not mix the two inside
one wall law or one cell.

## Recording Units in Exports

When you serialize a result, attach the labels explicitly so the downstream
consumer knows what the numbers mean:

```python
from tensyl.io import to_yaml

text = to_yaml(
    result,
    units={"length": "in", "force": "lbf", "stress": "psi"},
)
```

The labels travel with the artifact; the values are passed through untouched.
See [External Workflows](external-workflows.md) for the full serialization
schema.
