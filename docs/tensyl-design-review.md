# Tensyl — Software Design & Abstraction Review

**Reviewer perspective:** principal-level software engineering, focused on the constitutive-kernel abstraction and downstream usability.
**Scope of this document:** the software architecture and API contracts proposed in the Tensyl white paper. It does not re-derive the mechanics; it evaluates whether the abstractions are elegant *and* survivable once other teams build on them.
**Key scoping decision adopted:** the constitutive kernel is **hyperelastic-only** (no inelasticity / path dependence) for its lifetime. Several recommendations below depend on that decision and are marked accordingly.

---

## 1. Executive Summary

The spine of this design is correct. Four decisions are genuinely load-bearing and should not be touched: the constitutive/geometry separation, the energy-method-as-oracle validation strategy, the canonicalize-then-homogenize pipeline, and results that carry their own validity reports. If only that skeleton shipped, it would be a defensible foundation.

The work that remains is at the *seams*, not the bones. The abstractions occasionally promise more than their current shapes can deliver, and a few idiomatic usage patterns quietly defeat the safety mechanisms the architecture is built to provide. The highest-value changes are:

1. Reshape `ConstitutiveLaw` around a **stored-energy potential**, now that the kernel is hyperelastic-only. This buys a free correctness invariant, makes tangent symmetry structural rather than tested, and shrinks the JAX problem from "reimplement the kernel" to "express one scalar function."
2. Make the type system actually catch **strain / resultant / convention confusion** — the dangerous, common error in this domain — rather than only the coarse errors it catches today.
3. Make the frozen value objects **honestly immutable and hashable**, so the provenance / caching / dedup story actually holds.
4. Stop the **validity report from falling on the floor** in the first three lines of idiomatic use.

None of these disturb the load-bearing structure. They are the difference between "elegant in the white paper" and "still elegant after the third team builds on it."

---

## 2. What Is Load-Bearing and Correct

These are the real architecture. They are right. Keep them.

### 2.1 The constitutive / geometry split

`K = ∫ Bᵀ C B dΩ` is a genuine invariant, not a slogan. Material-and-structure information lives in `C`; kinematics lives in `B`. Keeping the kernel ignorant of barrels, domes, and solvers is the correct dependency direction, and the one-way dependency graph in §16.1 enforces it. This is the single most important decision in the document and it is made correctly.

### 2.2 Energy method as oracle, direct formulas as accelerators

One slow, obviously-correct reference implementation; everything faster validated against it by differential testing. This is exactly how numerical code earns trust. The energy assembly `Σ_m (L_m / A_cell) T_mᵀ K_m T_m` is compact, testable, and generalizes to graph cells — a good oracle.

### 2.3 Canonicalize-then-homogenize as a distinct stage

Producing a distinct `CanonicalUnitCell` type that raw user input cannot masquerade as is the correct way to stop every homogenizer from re-implementing its own partial interpretation of units, frames, shear conventions, and eccentricity signs. This is where the historically error-prone factors live, and isolating it is right.

### 2.4 Results carry their own validity

`HomogenizationResult` bundling `law + validity + diagnostics + assumptions` is the right move for a library that will run in unattended design sweeps where nobody reads logs. (See §5.4 — the bundling is correct, but the *first idiomatic move* currently unbundles it.)

---

## 3. The Hyperelastic Decision and Its Consequences

> **Scope:** the kernel is hyperelastic-only. "Hyperelastic" here means *every law derives from a generalized-strain stored-energy potential `W(η)`, and no law remembers its past.* This is **not** finite-strain continuum hyperelasticity (no large deformation, no work-conjugacy machinery, no finite-rotation frame-indifference baggage). At Level 1 the potential is simply quadratic, `W(η) = ½ ηᵀ C η`, whose gradient is the linear ABD wall law.

This decision is more than the removal of a worry. It changes the *shape* of the right protocol, because the three public quantities stop being independent:

```
r(η) = ∂W/∂η          (resultants = gradient of energy)
C(η) = ∂²W/∂η²         (tangent  = Hessian of energy, symmetric by construction)
```

`energy`, `resultants`, and `tangent` form a derivative tower with `energy` at the root. Three concrete consequences follow.

### 3.1 A free correctness invariant

Nothing today enforces that `resultants` is actually the gradient of `energy`. An implementer can get one closed form right and the other subtly wrong, and no test notices. Under the potential structure you can finite-difference the energy and assert agreement:

- `grad(energy)(η) ≈ resultants(η)`
- `hessian(energy)(η) ≈ tangent(η)`

over random `η`. This is a high-value property-based test that is *only meaningful because the kernel is hyperelastic*. It belongs next to the rotation-objectivity test.

### 3.2 Tangent symmetry becomes structural, not tested

A Hessian is symmetric by construction. If a law is *defined* through its energy and the tangent is *derived* as `∂²W/∂η²`, then an asymmetric `C` is literally unrepresentable. This retires the nastiest form of Risk 1 (the §10.3 case where a dropped ½ factor silently breaks constitutive symmetry).

Note the asymmetry in *who* gets this guarantee for free:

- The **energy homogenizer** assembles `Σ_m (L_m/A) T_mᵀ K_m T_m` — manifestly symmetric.
- The **direct method** builds `C` contributions by hand and *can* produce a plausible asymmetric matrix.

This is a sharper argument for the oracle/accelerator split than the white paper currently gives: the oracle is symmetry-safe by construction, the accelerator is the thing that can drift, therefore the accelerator is tested against the oracle and never the reverse. State it that way.

### 3.3 JAX is substantially de-risked

If energy is the primitive, autodiff-through-homogenization requires expressing **one scalar function** functionally; `jax.grad` and `jax.hessian` then yield resultants and tangent. Inverse identification and gradient-based sizing (both listed as goals) flow from differentiating `W`. This does not make JAX free — the energy path must still be pytree-traceable — but it shrinks "reimplement the kernel" to "express one function," a different size of problem. (See §6.3 for the remaining JAX caveat.)

### 3.4 The revised contract

```python
class HyperelasticLaw(Protocol):
    frame: Frame2D
    convention: StrainConvention

    def energy(self, eta: GeneralizedStrain) -> float: ...                     # primitive
    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant: ...   # == ∂W/∂η
    def tangent(self, eta: GeneralizedStrain) -> FloatArray: ...                # == ∂²W/∂η², symmetric
```

Two deliberate caveats:

- **"Energy is the semantic primitive" must not mean "always differentiate numerically at runtime."** `LinearABDWall` has closed forms for all three and should use them. The potential structure is a *consistency contract the closed forms must satisfy*, with autodiff as the fallback for laws nobody wants to hand-derive.
- **Hyperelastic is not the same as linear.** A valid hyperelastic law can have energy quartic in `η`, giving a tangent that genuinely varies with `η`. That is why `tangent(eta=None)` must die (see §5.1): "constant tangent" is a *refinement*, not the general case.

### 3.5 The three-way picture

| | Stored potential `W`? | Depends on | Signature needed | In scope? |
|---|---|---|---|---|
| Linear elastic | yes, quadratic | current `η` | `resultants(η)`, constant `C` | **yes — the MVP** |
| Nonlinear hyperelastic | yes, higher-order | current `η` | `resultants(η)`, `C(η)` varies | door stays open |
| Inelastic (plastic, damage) | **no** | full strain *history* | `resultants(η, state)` | **out — by decision** |

The decision draws the line after row two. The MVP is row one. The protocol admits row two for free (same signature; the tangent simply stops being constant). Row three is excluded — and that exclusion is *what lets the signature stay clean* and what makes the finite-difference consistency check valid.

---

## 4. Scoping Note to Add to the White Paper

One sentence belongs in the document so a future reader does not import heavier baggage:

> "Hyperelastic" here denotes a generalized-strain stored-energy potential at small strain, not finite-strain continuum hyperelasticity. The only objectivity owed is the cell-rotation property of §10 (a material-frame transformation); the work-conjugacy and finite-rotation frame-indifference apparatus of large-deformation elasticity does not apply.

---

## 5. Abstractions That Will Bite (Priority Fixes)

### 5.1 Kill `tangent(eta=None)` — it hides two different contracts

The optional argument silently changes semantics: ignored when the law is linear, required when it is not. The type does not tell the caller which world they are in, and `| None` is papering over two genuinely different contracts.

**Fix:** make "constant tangent" a *refinement* of the hyperelastic protocol.

```python
class LinearLaw(HyperelasticLaw, Protocol):
    @property
    def constant_tangent(self) -> FloatArray: ...   # C is independent of η
```

`LinearABDWall` lives in this refinement. The entire MVP is here. The general `HyperelasticLaw.tangent(η)` always takes a strain, with no `None` hack, leaving the nonlinear-hyperelastic door open above it.

### 5.2 Make the type system catch the error that actually happens

The white paper leans hard on static typing to catch "category errors," but `FloatArray = NDArray[float64]` is the *same type* for:

- a generalized strain,
- a generalized resultant,
- an 8-vector in convention A versus convention B.

mypy will happily let someone pass resultants into `energy()`, or feed a convention-A strain to a convention-B law. **That** strain/resultant/convention confusion is the dangerous, common, plausible-but-wrong-answer error in this domain — far more than passing a `Surface` where a `Cell` is expected, which is the only error the current types catch. You are one stray `.T` away from a symmetric, plausible, wrong matrix, which §10.3 already warns is the failure mode.

**Fix:** wrap the boundaries with `NewType` at the public API.

```python
from typing import NewType
GeneralizedStrain    = NewType("GeneralizedStrain", FloatArray)
GeneralizedResultant = NewType("GeneralizedResultant", FloatArray)
```

Keep the wrappers thin — unwrap at the kernel boundary so NumPy ergonomics survive internally. The consistency invariant of §3.1 is exactly where a transposed or mis-conventioned array would otherwise sail through, so this is where the newtypes earn their keep.

### 5.3 Make frozen value objects honestly immutable and hashable

A `frozen=True` dataclass holding a `FloatArray` is **not** immutable (array contents are mutable) and **not** hashable (arrays are unhashable). So a `LinearABDWall` cannot go into a set or serve as a cache key, despite the decorator implying it can. Meanwhile `metadata: Mapping = field(default_factory=dict)` hands back a mutable dict.

This directly undercuts the WallAtlas "input hash / provenance record" goal: content-addressable walls are wanted, and the value objects cannot be keys as designed. The elegant frozen-value-object story fails *exactly where it is needed* — caching, dedup, reproducibility.

**Fix (deliberate, not decorative):**

- Set `arr.flags.writeable = False` on construction.
- Define a real `__hash__` over `(shape, dtype, bytes)`.
- Use an immutable mapping for `metadata` (e.g. a frozen mapping type), not a bare `dict`.

### 5.4 Stop the validity report from falling on the floor

The §19 example does:

```python
result = EnergyHomogenizer().compute(cell)
wall = result.law          # <-- validity report is now orphaned
```

From this line on, the wall escapes into the shell exporter carrying no memory of its own warnings. The entire point of bundling validity with the result (§2.4) is defeated if the first idiomatic move unbundles it. Nothing then stops a wall with `p / L_response ≈ 1` from being silently integrated into a buckling analysis.

**Fix:** make the safe path the easy path. Either have the law hold a back-reference to its `ValidityReport`, or refuse to construct a bare law without one. A wall that lands in a solver should still be able to answer "am I being used outside my scale-separation envelope?"

---

## 6. Smaller Things a Reviewer Would Flag

### 6.1 `C8` is rebuilt in the hot loop

`LinearABDWall.C8` reassembles the 8×8 from A/B/D/As blocks on *every* `resultants` / `energy` / `tangent` call. For a library whose entire value over a formula sheet is correctness-at-scale (sweeps, per-quadrature-point evaluation), rebuilding in the hot loop is backwards.

**Fix:** store `C8` as the canonical representation; expose A/B/D/As as slices, not the reverse.

### 6.2 "Oracle" slightly oversells self-justification

The energy method is an oracle *for the direct method*, but its own correctness rides entirely on `T_m`, the strain-equivalence matrix. If `T_m` is wrong, direct and energy agree on a *shared* error. The external ground truth — NASA cases (§13.6) and discrete FE (§13.7) — is what actually closes that loop.

**Fix:** state explicitly that direct-vs-energy agreement is *necessary but not sufficient*; "oracle" must not imply self-justification.

### 6.3 The JAX story is still underpriced (even after §3.3)

"Keep it behind an optional backend with a functional API" reads like a backend swap, but JAX wants traceable, pytree-registered, functional structures, and frozen-OO value objects will not trace as-is. Section 3.3 shrinks the problem to one scalar function, but that function's inputs (the wall, the cell) still must be pytree-registered.

**Fix:** either register the core dataclasses as pytrees from the start, or scope autodiff honestly as "requires a functional kernel variant." Do not present it as a transparent backend toggle.

### 6.4 Canonicalization needs an idempotence invariant

Canonicalization is where the error-prone ½ shear/twist factors live (the white paper flags this itself). The cheapest high-value property test for that stage is:

```
canon(canon(x)) == canon(x)
```

It is not in the Hypothesis list, which currently jumps straight to objectivity. Add it.

### 6.5 The fidelity ladder must stay metadata, never a class hierarchy

The ladder is an excellent communication device. The moment `Level1Wall` / `Level3Wall` become *types*, real problems that are Level 1 in membrane response and need Level 3 for a local detail will not fit the hierarchy.

**Fix:** keep "level" a field on `source` / diagnostics. The unifying contract is the law plus its provenance — which the document already does correctly elsewhere.

### 6.6 No defined error channel

The `Homogenizer` protocol has no failure contract. What comes back for a zero-area cell, a mechanism, a singular `K_m`? A raised exception, or a result with warnings and a rank-deficient `C`? Downstream usability depends on the failure contract as much as the success one.

**Fix:** define it explicitly and document it. Whichever you choose, choose it once and uniformly.

### 6.7 No serialization schema version

The document wants JSON/YAML export with provenance but never mentions versioning the serialization. The first time `StrainConvention` gains a field, every persisted wall breaks. For a library whose pitch is "traceable and reproducible," a versioned schema is table stakes.

**Fix:** add an explicit schema version to every serialized artifact and a documented migration policy.

---

## 7. Consolidated Recommendation Table

| # | Recommendation | Severity | Depends on hyperelastic decision? |
|---|---|---|---|
| 1 | Reshape `ConstitutiveLaw` around a stored-energy potential `W`; add `grad(energy)≈resultants`, `hessian(energy)≈tangent` consistency tests | High | **Yes** |
| 2 | `NewType` the strain / resultant boundaries; carry `StrainConvention` so confusion is type-visible | High | No |
| 3 | Make frozen value objects honestly immutable (`writeable=False`) and hashable (`__hash__` over bytes); immutable metadata | High | No |
| 4 | Make the validity report inseparable from the law (back-reference or no-bare-law construction) | High | No |
| 5 | Replace `tangent(eta=None)` with a `LinearLaw` refinement exposing a constant tangent | Medium | **Yes** |
| 6 | Store `C8` as canonical; expose A/B/D/As as slices | Medium | No |
| 7 | Document that energy is symmetry-safe by construction; direct method can drift → justifies oracle/accelerator split | Medium | **Yes** |
| 8 | State that direct-vs-energy agreement is necessary, not sufficient; external NASA/FE truth closes the loop | Medium | No |
| 9 | Scope JAX honestly (pytree registration required); not a transparent backend toggle | Medium | Partly |
| 10 | Add `canon(canon(x)) == canon(x)` idempotence property test | Medium | No |
| 11 | Keep the fidelity ladder as metadata, never a class hierarchy | Medium | No |
| 12 | Define the `Homogenizer` failure contract explicitly | Medium | No |
| 13 | Version the serialization schema; document migration policy | Medium | No |
| 14 | Add the small-strain scoping sentence distinguishing this from finite-strain hyperelasticity | Low | **Yes** |

---

## 8. Net Assessment

The separation of concerns, the oracle-plus-accelerator validation strategy, the canonicalization stage, and results-carry-their-own-validity are the right bones. I would not touch them.

The work is at the seams. With the kernel scoped to hyperelastic, the single most valuable move is to make the **stored-energy potential the organizing principle of the constitutive contract** — it converts symmetry and gradient-consistency from things you hope the implementer got right into things the structure enforces, and it makes the differentiable-backend ambition tractable. Alongside that: make the type system catch the error that actually occurs, make the value objects honestly support the provenance story they promise, and never let the validity report fall on the floor.

Do those, and the abstraction is not just elegant on paper — it stays elegant when other teams depend on it.
