# Tensyl: A Python Library for Equivalent-Wall Homogenization of Stiffened Plates and Shells


**Primary application domain:** integrally stiffened aerospace thin-wall structures, including flat panels, cylindrical barrels, spherical and ellipsoidal domes, conical and doubly curved shell segments, and smooth parametric shell surfaces.  
**Computational target:** a Python scientific-computing library with a NumPy reference implementation; optional Numba acceleration for profiled kernels; optional finite-element RVE or solver-adapter backends only where their benefits are demonstrable. JAX is explicitly out of scope.  
**Technical basis:** first-approximation equivalent-continuum stiffness methods for stiffened laminated-composite plates and plate-like lattices, especially Nemeth's NASA/TP-2011-216882 formulation, extended as a rigorously verified constitutive kernel that can be embedded into geometry-specific shell kinematics [Nemeth 2011].  
**Status:** architecture and formulation proposal; not yet a substitute for detailed local stress, crippling, discrete-stiffener buckling, nonlinear postbuckling, or certification analysis.

---

## Executive Summary

This white paper proposes a Python library for computing and managing equivalent-wall constitutive models for stiffened thin-walled aerospace structures. The library is intended for early-stage sizing, trade studies, optimization, finite-element pre- and post-processing, and model reduction of integrally stiffened plates and shells. Its initial mechanics foundation is deliberately conservative: first-approximation equivalent-plate stiffness theory based on Reissner--Mindlin-type first-order transverse-shear deformation kinematics and shear-deformable beam stiffeners, following the systematic derivations and notation of Nemeth's NASA treatise [Nemeth 2011; Reissner 1945; Mindlin 1951].

The governing design principle is:

$$
\boxed{\text{Compute a local equivalent-wall constitutive law; embed that law into geometry-specific shell kinematics.}}
$$

The library should therefore not begin as a collection of separate calculators for barrels, domes, plates, orthogrids, isogrids, and Kagome grids. It should begin as a **constitutive kernel**. That kernel computes a local wall law from materials, laminate skins, beam sections, stiffener families, and unit cells. Geometry then enters through a separate embedding layer: plates, cylinders, spherical caps, ellipsoids, and general parametric surfaces provide frames, metrics, curvatures, integration measures, and strain-displacement operators, but they do not alter the local tangent-plane wall homogenization unless an explicitly higher-fidelity curved-cell model is selected.

The primary output is not a scalar equivalent modulus, scalar equivalent thickness, or single smeared isotropic material. The primary output is a constitutive operator whose first implementation is a linear wall law in laminated-plate notation:

$$
\begin{bmatrix}
\mathbf N \\
\mathbf M
\end{bmatrix}
=
\begin{bmatrix}
\mathbf A & \mathbf B \\
\mathbf B & \mathbf D
\end{bmatrix}
\begin{bmatrix}
\boldsymbol\epsilon^0 \\
\boldsymbol\kappa
\end{bmatrix},
\qquad
\mathbf Q = \mathbf A_s \boldsymbol\gamma_s^0.
$$

Here $\mathbf A$ is the membrane stiffness matrix, $\mathbf B$ is the membrane-bending coupling matrix, $\mathbf D$ is the bending/twisting stiffness matrix, and $\mathbf A_s$ is the transverse-shear stiffness matrix. Engineering constants such as $E_1$, $E_2$, $G_{12}$, $\nu_{12}$, and equivalent thickness are secondary interpretations with explicitly declared assumptions and thickness criteria. This mirrors the laminated-plate and equivalent-plate literature and avoids misleading reductions of anisotropic or membrane-bending coupled walls to scalar surrogates [Jones 1975; Reddy 2004; Nemeth 2011].

The main architectural changes proposed in this rewrite are:

1. **Make the energy-equivalence homogenizer the reference implementation.** Nemeth presents both a direct equilibrium-compatibility method and a basic-cell strain-energy method, and shows that they agree under the same first-approximation assumptions [Nemeth 2011]. The energy-equivalence method should be the oracle implementation because it generalizes naturally to graph-like cells and arbitrary beam-member layouts. Closed-form direct formulas should be implemented as validated accelerators for canonical rectilinear stiffener families.

2. **Elevate the matrix object into a constitutive operator.** An `EquivalentWall` may contain $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$, but the public contract should be `ConstitutiveLaw`: `energy(eta)`, `resultants(eta)`, `tangent(eta)`, `rotate(...)`, and `metadata`. This preserves the current linear theory while leaving room for temperature dependence, uncertainty, nonlinear material response, FE-RVE models, and higher-order homogenization.

3. **Add canonicalization before homogenization.** Inputs must be normalized for units, frames, strain conventions, member multiplicities, section principal axes, eccentricity signs, reference surfaces, and cell topology before stiffness assembly. This prevents common errors in shear conventions, twist conventions, and coordinate rotations.

4. **Attach verification and validity reports to every result.** Symmetry, positive semidefiniteness, energy consistency, rotation objectivity, isotropy/orthotropy identities, and literature regression status should be reported with the wall law. Scale-separation diagnostics such as $h_s/R$, $p/R$, and $p/L_\text{response}$ should be machine-readable, not only documentation prose.

5. **Stage shell analysis and FE export behind adapters.** The MVP should be a solver-agnostic constitutive platform. Shell embedding, finite-element property export, FE-RVE cell solves, and optimization interfaces should be adapters or optional packages rather than hard dependencies of the mechanics kernel.

For stiffeners about 1 inch tall on radii greater than 100 inches, the local curvature ratio $h_s/R$ is approximately $0.01$, which is favorable for tangent-plane homogenization. However, the cell pitch, target mode wavelength, local curvature variation, and stiffener topology must also be checked. Homogenization is a scale-separated approximation, not a universal replacement for a discrete model [Sanchez-Palencia 1980; Bensoussan et al. 1978; Nemeth 2011].

---

## 1. Purpose and Positioning

### 1.1 What the library is

The proposed library is a mechanics-and-software platform for constructing, validating, transforming, and exporting equivalent-wall constitutive laws for stiffened thin-wall structures. It is intended to help analysts answer questions such as:

- What are the effective membrane, bending, membrane-bending coupling, twisting, and transverse-shear stiffnesses of this stiffened wall?
- How do stiffener eccentricity, section properties, cell pitch, and grid orientation affect the full $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$ law?
- Does a nominally isogrid wall behave isotropically in membrane and bending response, or do manufacturing/geometry deviations create anisotropy?
- Can a single local wall law be embedded into a flat panel, a cylindrical barrel, and a spherical or ellipsoidal dome without rewriting the homogenization theory?
- What validity warnings should accompany a smeared model before it is used for buckling, sizing, or optimization?
- How can a detailed discrete stiffener model and a smeared equivalent-wall model be compared in a reproducible validation workflow?

The library is therefore best understood as a **constitutive kernel plus adapters**, not as a monolithic shell solver.

### 1.2 What the library is not

The tangent-plane implementation is not a local-stress recovery tool, a certification-grade buckling solver, or a replacement for detailed finite-element modeling. It should not claim to resolve:

- local skin buckling between stiffeners;
- stiffener crippling;
- stiffener intersection stress concentrations;
- weld, fastener, bondline, or joint behavior;
- local load introduction;
- cross-sectional warping restraint beyond the selected beam model;
- geometric imperfections;
- nonlinear postbuckling;
- material nonlinearity unless explicitly implemented;
- cell-scale curvature effects unless a higher-fidelity curved-cell homogenizer is selected;
- deformation modes with wavelengths comparable to the grid pitch.

These exclusions are not deficiencies. They are the necessary boundaries of a first-approximation equivalent-continuum model. Nemeth's report explicitly frames its stiffnesses as first-approximation equivalent-continuum stiffnesses and states that in-plane bending of the stiffeners and total compatibility between skin and stiffeners are neglected in the presented first-approximation theory [Nemeth 2011]. Those limitations should remain visible in the API, documentation, and result metadata.

### 1.3 Novelty of the proposal

The novelty of this proposal is primarily **architectural and computational**, not the invention of a new equivalent-stiffness theory. The initial mechanics kernel is anchored in established equivalent-plate and laminated-plate theory, particularly Nemeth's direct and energy-equivalence derivations [Nemeth 2011]. The new contribution is to express that mechanics as a modern scientific Python architecture with:

- explicit frame and strain-convention objects;
- a constitutive-law interface rather than raw matrix-only outputs;
- a graph-based unit-cell representation;
- an energy-equivalence oracle implementation;
- automatic verification and validity reporting;
- constant and spatially varying wall fields;
- solver adapters rather than solver lock-in;
- reproducible testing, typing, packaging, and benchmarking practices.

This positioning is important. It makes the project credible, traceable, and extensible.

---

## 2. Technical Lineage

### 2.1 Equivalent-continuum stiffened-wall methods

Equivalent-stiffness modeling of stiffened plates and shells has a long history in aerospace structures. Nemeth's NASA treatise surveys work dating back to early equivalent-plate and equivalent-shell approaches, including Huber, Flügge, van der Neut, Dow, Libove, Hubka, Block, Card, Mikulas, Stein, Jones, Reddy, Chen and Tsai, Wodesenbet and coauthors, Vasiliev and coauthors, and others [Nemeth 2011]. The underlying engineering motivation is unchanged: discrete stiffened models are expensive and cumbersome for early design, while equivalent-continuum representations are fast and compatible with many classical plate and shell analyses.

Nemeth's report is the primary basis for the MVP because it provides:

- a direct equilibrium-compatibility derivation for rectilinear stiffener families;
- a basic-cell strain-energy equivalence method for periodic or translationally generated cells;
- stiffness expressions in standard laminated-plate notation;
- transverse-shear stiffnesses consistent with first-order shear-deformation theory;
- shear-deformable beam stiffener assumptions;
- nonhomogeneous specially orthotropic stiffener section capability;
- canonical stiffener configurations including orthogonal grids, braced orthogrids, isosceles-triangle/isogrid-like grids, Kagome grids, hexagonal grids, star cells, and sandwich-plate cores [Nemeth 2011].

The present library should preserve that traceability. Equations, conventions, and test cases should be traceable to the NASA report where the tangent-plane implementation is derived from it.

### 2.2 Laminated-plate and first-order shear-deformation theory

The $\mathbf A$, $\mathbf B$, and $\mathbf D$ stiffness blocks come from classical and shear-deformation laminated-plate theory, where in-plane resultants and bending resultants are related to mid-surface strains and curvatures. First-order transverse-shear deformation theories are associated with Reissner and Mindlin and are now standard in many composite plate and shell treatments [Reissner 1945; Mindlin 1951; Reddy 2004].

A key reason to retain this notation is interoperability. Structural analysts already understand $A_{ij}$, $B_{ij}$, $D_{ij}$, $A_{44}$, $A_{45}$, and $A_{55}$. Finite-element shell sections, laminate calculators, Nastran-style property cards, and analytical buckling formulas often use closely related concepts. The library should therefore remain matrix-first in payload, even though its public API should be operator-first.

### 2.3 Homogenization and scale separation

The tangent-plane formulation is a classical scale-separated model. It assumes the cell size and stiffener height are small relative to geometric radii and structural response length scales. This aligns with the broader homogenization literature, in which a heterogeneous medium is replaced by an effective continuum when the microstructural length scale is sufficiently small relative to the macroscopic variation scale [Bensoussan et al. 1978; Sanchez-Palencia 1980; Bakhvalov and Panasenko 1989].

Modern work on higher-order and computational homogenization reinforces the need to encode validity boundaries. Recent second-order homogenization of beam networks shows that strain-gradient terms can materially improve accuracy when gradients are significant, while two-scale computational homogenization of truss-based lattices highlights the value and cost of RVE-based microproblem solves [Ye et al. 2024; Danesh et al. 2024; Guo et al. 2024; De Souza Neto and Feijóo 2008]. These results do not undermine the MVP. They justify a staged architecture that begins with classical first-order wall laws and leaves explicit extension points for FE-RVE, higher-order, and micropolar or strain-gradient models.

---

## 3. Scope and Model Families

The library should expose named model families rather than a single implied truth model. The names should describe the modeling assumption that matters to an analyst.

### 3.1 Skin-only laminate or isotropic plate

The skin-only family computes a conventional plate or laminate constitutive law without stiffener homogenization. It is useful for testing, baseline comparison, and skin-only regions.

Inputs include isotropic materials, orthotropic plies, ply angles, ply thicknesses, transverse-shear correction factors, and a reference surface. Outputs are $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$ blocks.

### 3.2 Tangent-plane equivalent wall

Tangent-plane homogenization is the initial production target. It treats the repeating stiffened wall cell as locally flat in the tangent plane. Curvature is used in shell kinematics and validity checks, but not in local homogenization.

This model family is appropriate when:

$$
\frac{h_s}{R_\text{min}} \ll 1,
\qquad
\frac{p}{R_\text{min}} \ll 1,
\qquad
\frac{p}{L_\text{response}} \ll 1,
$$

where $h_s$ is a characteristic stiffener height, $p$ is a characteristic cell pitch, $R_\text{min}$ is the smaller local radius of curvature, and $L_\text{response}$ is the relevant deformation or buckling wavelength.

The tangent-plane wall law may be computed by:

- direct equilibrium-compatibility formulas for canonical rectilinear families;
- the reference energy-equivalence beam-cell method;
- later, an FE-RVE method that reduces to a linear constitutive law in the same convention.

### 3.3 Spatially varying wall fields

Spatial wall fields retain the local tangent-plane homogenizer but allow the wall law to vary over a surface:

$$
\mathbf C_\text{wall}=\mathbf C_\text{wall}(u,v).
$$

This is necessary for domes, ellipsoids, tapered barrels, variable-pitch stiffeners, geodesic or principal-direction stiffeners, and manufacturing-driven grid layouts where local spacing or orientation is not constant.

The key new abstraction is `WallField`, not a new constitutive theory.

### 3.4 FE-RVE or cell-problem homogenization

FE-RVE and cell-problem homogenization introduce numerical solves for cells that cannot be represented adequately by analytic beam-member energy. Examples include open-section warping effects, local eccentricity details, nonlinear material behavior, contact-like assumptions, complex intersections, or non-beam stiffener geometry.

The numerical homogenization result should still implement `ConstitutiveLaw`. For linear problems, it may return the same $8\times 8$ tangent shape as tangent-plane homogenization. For nonlinear problems, it may return a state-dependent tangent.

### 3.5 Higher-order, strain-gradient, micropolar, or curved-cell models

Higher-order modeling is a research extension, not an MVP requirement. It covers models where a classical Cauchy-like wall law is insufficient. Candidate extensions include:

- strain-gradient wall energy, with $W(\boldsymbol\eta,\nabla\boldsymbol\eta)$;
- micropolar or Cosserat-like lattice continua when rotational degrees of freedom are essential;
- curved-cell homogenization when cell curvature is not negligible;
- bifurcation-aware or instability-aware homogenization.

A future higher-order wall law might take the schematic form:

$$
W(\boldsymbol\eta,\nabla\boldsymbol\eta)
=
\frac{1}{2}\boldsymbol\eta^T\mathbf C\boldsymbol\eta
+
\frac{1}{2}\nabla\boldsymbol\eta : \mathbf H : \nabla\boldsymbol\eta.
$$

This should not be forced into the tangent-plane API. Instead, the public interface should be broad enough that such a law can later satisfy `ConstitutiveLaw` or a richer `HigherOrderConstitutiveLaw` protocol.

---

## 4. Core Mechanics Conventions

### 4.1 Local surface frame

At each point on a shell midsurface, define a local orthonormal frame:

$$
\{\mathbf e_1,\mathbf e_2,\mathbf n\},
$$

where $\mathbf e_1$ and $\mathbf e_2$ are tangent directions and $\mathbf n$ is the unit normal. For a cylinder, $\mathbf e_1$ may be axial and $\mathbf e_2$ circumferential. For a dome, $\mathbf e_1$ may be meridional and $\mathbf e_2$ hoop/circumferential. These are choices, not hidden assumptions; the frame must be explicit.

### 4.2 Generalized strain vector

The internal generalized strain vector should use a documented ordering. The recommended internal ordering is:

$$
\boldsymbol\eta
=
\begin{bmatrix}
\epsilon_{11}^0 &
\epsilon_{22}^0 &
\gamma_{12}^0 &
\kappa_{11} &
\kappa_{22} &
\kappa_{12} &
\gamma_{13}^0 &
\gamma_{23}^0
\end{bmatrix}^T.
$$

The library must document whether $\gamma_{12}$, $\gamma_{13}$, and $\gamma_{23}$ are engineering shear strains or tensor shear strains. The tangent-plane implementation uses engineering shear strains internally because that matches much of laminated-plate and engineering shell practice, but the convention must be encoded in `StrainConvention` and carried through transformations.

### 4.3 Generalized resultant vector

The corresponding resultant vector is:

$$
\mathbf r
=
\begin{bmatrix}
N_{11} &
N_{22} &
N_{12} &
M_{11} &
M_{22} &
M_{12} &
Q_{13} &
Q_{23}
\end{bmatrix}^T.
$$

A mapping table must relate this internal convention to Nemeth-style $(x,y,z)$, $(X,Y,Z)$, $Q_{xz}$, $Q_{yz}$, $A_{44}$, $A_{45}$, and $A_{55}$ notation. Nemeth's derivation uses ordered transverse shear quantities $Q_{yz}$, $Q_{xz}$ and the $A_{44},A_{45},A_{55}$ matrix in a particular convention [Nemeth 2011]. Ambiguity here is a high-risk implementation error.

### 4.4 Reference surface and eccentricity

The reference surface is not metadata decoration; it changes $\mathbf B$ and $\mathbf D$. The default reference surface should be the skin or wall mid-surface used in the Nemeth derivation unless the user explicitly selects a different reference surface [Nemeth 2011].

The sign convention for stiffener eccentricity must be explicit. A recommended convention is:

- positive eccentricity means the stiffness-weighted stiffener centroid lies in the positive $\mathbf n$ direction from the chosen reference surface;
- the `Frame2D.n` direction defines the positive normal;
- transformations that flip the normal must update eccentricity signs or reject the operation.

### 4.5 Constitutive matrix

For the tangent-plane linear law, define:

$$
\mathbf r=\mathbf C_\text{wall}\boldsymbol\eta,
$$

with

$$
\mathbf C_\text{wall}
=
\begin{bmatrix}
\mathbf A & \mathbf B & \mathbf 0 \\
\mathbf B & \mathbf D & \mathbf 0 \\
\mathbf 0 & \mathbf 0 & \mathbf A_s
\end{bmatrix}.
$$

The zero coupling between transverse shear and membrane/bending is consistent with standard first-order plate theories for ordinary laminates and with the first implementation target. Future laws may relax this structure, but they should do so by implementing a richer constitutive interface rather than by overloading undocumented matrix entries.

---

## 5. Constitutive Operator Abstraction

### 5.1 Why `EquivalentWall` should not be the outermost contract

The current `EquivalentWall` concept is correct as a concrete data product but too narrow as the public abstraction. A matrix-only object cannot naturally express nonlinear, temperature-dependent, uncertainty-aware, FE-RVE-derived, or higher-order constitutive laws.

The public abstraction should be:

```python
class HyperelasticLaw(Protocol):
    frame: Frame2D
    convention: StrainConvention

    def energy(self, eta: GeneralizedStrain) -> float: ...
    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant: ...
    def tangent(self, eta: GeneralizedStrain) -> FloatArray: ...


class LinearLaw(HyperelasticLaw, Protocol):
    @property
    def constant_tangent(self) -> FloatArray: ...
```

"Hyperelastic" here means a small-strain generalized-wall stored-energy
potential \(W(\eta)\), not finite-strain continuum hyperelasticity. The
resultants are \(\partial W/\partial\eta\), and the tangent is
\(\partial^2 W/\partial\eta^2\). A linear law is a refinement whose tangent is
constant; it should expose that constant tangent explicitly instead of using
`tangent(eta=None)`.

A tangent-plane `LinearABDWall` is then one implementation:

```python
@dataclass(frozen=True, slots=True)
class LinearABDWall:
    C8: FloatArray
    frame: Frame2D
    convention: StrainConvention
    areal_mass: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
    validity: ValidityReport | None = None

    @property
    def constant_tangent(self) -> FloatArray:
        return self.C8

    def tangent(self, eta: GeneralizedStrain) -> FloatArray:
        return self.constant_tangent

    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant:
        return self.C8 @ eta

    def energy(self, eta: GeneralizedStrain) -> float:
        return 0.5 * float(eta @ self.C8 @ eta)
```

This pattern follows modern Python's structural typing philosophy: objects satisfy a protocol by behavior rather than by inheritance hierarchy. Python's `typing.Protocol` and static checkers such as mypy support this style of interface design [Python typing docs; mypy docs]. It is well suited to scientific libraries where users may provide custom constitutive laws, custom wall fields, or custom homogenizers.

### 5.2 Recommended core value objects

The following objects should be immutable where possible:

```python
@dataclass(frozen=True, slots=True)
class StrainConvention:
    membrane_order: tuple[str, str, str] = ("e11", "e22", "g12")
    bending_order: tuple[str, str, str] = ("k11", "k22", "k12")
    shear_order: tuple[str, str] = ("g13", "g23")
    engineering_shear: bool = True
    reference_surface: str = "wall_mid_surface"
    normal_positive: str = "+n"


@dataclass(frozen=True, slots=True)
class Frame2D:
    e1: FloatArray
    e2: FloatArray
    n: FloatArray
    label: str = "local_tangent"


@dataclass(frozen=True, slots=True)
class ValidityReport:
    h_over_R: float | None
    p_over_R: float | None
    p_over_L_response: float | None
    coupling_ratios: Mapping[str, float]
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HomogenizationResult:
    law: ConstitutiveLaw
    validity: ValidityReport
    diagnostics: Mapping[str, Any]
    assumptions: tuple[str, ...]
    source: Literal["energy", "direct_ec", "rve", "imported"]
```

Python dataclasses support frozen instances and slot generation, which helps create compact immutable mechanics value objects while preserving readable constructors and representations [Python dataclasses docs].

---

## 6. Input Pipeline and Canonicalization

The library should not homogenize raw user input directly. It should first canonicalize the model.

$$
\boxed{
\text{raw input}
\rightarrow
\text{canonical model}
\rightarrow
\text{homogenization}
\rightarrow
\text{verification}
\rightarrow
\text{validity report}
\rightarrow
\text{wall law}
}
$$

### 6.1 Raw input

Raw input may include:

- isotropic, orthotropic, or laminate material definitions;
- skin thicknesses and ply stacks;
- beam sections specified by engineering properties or geometric integration;
- stiffener families specified by spacing, orientation, eccentricity, and section;
- graph-cell definitions with nodes and edges;
- surface definitions for validity checks and spatially varying fields;
- unit systems or unit tags;
- solver/export preferences.

### 6.2 Canonical model

Canonicalization should produce a normalized internal representation:

- all units converted or verified as consistent;
- all frames orthonormalized and checked for handedness;
- all angles converted to radians internally;
- all engineering/tensor shear conventions explicitly declared;
- all section axes reduced to principal or declared axes;
- all stiffener eccentricities referenced to the selected surface;
- all graph-cell members assigned lengths, orientations, multiplicities, and section references;
- all periodic cell areas computed or verified;
- all cell topology metadata recorded.

The canonicalization stage should be separate from the homogenizer. This prevents each homogenizer from implementing its own partial interpretation of user input.

### 6.3 Homogenization

The homogenizer consumes only canonical cells. This is a clean contract:

```python
class Homogenizer(Protocol):
    def compute(self, cell: CanonicalUnitCell) -> HomogenizationResult: ...
```

The result includes not only the constitutive law but also diagnostics and assumptions.

---

## 7. Unit Cells and Stiffener Patterns

### 7.1 Graph-based cell as the general representation

The most general tangent-plane cell should be a local graph:

```python
@dataclass(frozen=True, slots=True)
class CellNode:
    x: float
    y: float
    label: str = ""


@dataclass(frozen=True, slots=True)
class CellEdge:
    start: int
    end: int
    section: BeamSection
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""


@dataclass(frozen=True, slots=True)
class GraphUnitCell:
    area: float
    skin: SkinLaw
    nodes: tuple[CellNode, ...]
    edges: tuple[CellEdge, ...]
    frame: Frame2D
    convention: StrainConvention
    metadata: Mapping[str, Any] = field(default_factory=dict)
```

Canonical named cells such as `OrthogridCell`, `IsogridCell`, `KagomeCell`, `HexCell`, and `StarCell` should be constructors that generate graph cells or family contributions, not separate mechanical universes.

### 7.2 Stiffener families for rectilinear grids

For uniformly spaced rectilinear stiffeners, a family abstraction is more concise:

```python
@dataclass(frozen=True, slots=True)
class StiffenerFamily:
    section: BeamSection
    spacing: float
    angle_rad: float
    eccentricity: float
    label: str = ""
```

A direct equilibrium-compatibility homogenizer can use `StiffenerFamily` directly. The energy-equivalence homogenizer can also convert families into an equivalent graph cell or use the family contribution formula when appropriate.

### 7.3 Canonical cells to include in the initial library

The initial library should include constructors and regression cases for:

- unidirectionally stiffened panel;
- orthogrid;
- orthogrid with one or two diagonal brace families;
- isosceles-triangle grid;
- equilateral isogrid;
- Kagome grid;
- hexagonal grid;
- star-cell grid;
- sandwich-plate cores based on these lattices.

These correspond to configurations treated or surveyed in Nemeth's NASA report and provide a strong validation suite [Nemeth 2011].

---

## 8. Beam Section and Skin Models

### 8.1 Minimal beam-section stiffnesses

The tangent-plane beam section should expose the stiffnesses needed by the shear-deformable beam model:

$$
EA, \quad EI_y, \quad EI_z, \quad GJ, \quad k_yGA, \quad k_zGA,
$$

with optional coupling terms such as $EI_{yz}$ and stiffness-weighted centroid offsets for nonhomogeneous sections.

```python
@dataclass(frozen=True, slots=True)
class BeamSection:
    EA: float
    EIy: float
    EIz: float
    GJ: float
    kGAy: float | None = None
    kGAz: float | None = None
    EIyz: float = 0.0
    centroid_y: float = 0.0
    centroid_z: float = 0.0
    shear_center_y: float | None = None
    shear_center_z: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
```

The names `y` and `z` must be tied to the member local frame and mapped to Nemeth's $(X,Y,Z)$ convention.

### 8.2 Nonhomogeneous and composite sections

Nemeth's formulation permits nonhomogeneous stiffeners constructed from specially orthotropic materials with one axis aligned to the stiffener and the other two axes aligned to cross-sectional axes [Nemeth 2011]. The library should preserve this capability through numerical section integration:

$$
EA = \int_A E_X(y,z)\,dA,
$$

$$
EI_y = \int_A E_X(y,z)z^2\,dA,
\qquad
EI_z = \int_A E_X(y,z)y^2\,dA,
\qquad
EI_{yz}=\int_A E_X(y,z)yz\,dA.
$$

Stiffness-weighted centroids should be computed as:

$$
\bar y_E=\frac{\int_A E_X y\,dA}{\int_A E_X\,dA},
\qquad
\bar z_E=\frac{\int_A E_X z\,dA}{\int_A E_X\,dA}.
$$

This enables pultruded cap reinforcements, hybrid metallic-composite ribs, locally reinforced stiffeners, and tailored composite sections.

### 8.3 Skin stiffness

For a laminate skin, use the standard through-thickness integration:

$$
A_{ij}^{\text{skin}}=\sum_k \bar Q_{ij}^{(k)}(z_k-z_{k-1}),
$$

$$
B_{ij}^{\text{skin}}=\frac{1}{2}\sum_k \bar Q_{ij}^{(k)}(z_k^2-z_{k-1}^2),
$$

$$
D_{ij}^{\text{skin}}=\frac{1}{3}\sum_k \bar Q_{ij}^{(k)}(z_k^3-z_{k-1}^3).
$$

For an isotropic metallic skin under plane stress:

$$
\mathbf Q = \frac{E}{1-\nu^2}
\begin{bmatrix}
1 & \nu & 0 \\
\nu & 1 & 0 \\
0 & 0 & \frac{1-\nu}{2}
\end{bmatrix}.
$$

Transverse shear should be represented with an explicit shear correction factor and documented convention [Mindlin 1951; Reddy 2004; Nemeth 2011].

---

## 9. Homogenization Methods

### 9.1 Energy-equivalence method as the reference implementation

For a canonical cell with area $A_\text{cell}$, the total cell energy is:

$$
U_\text{cell}(\boldsymbol\eta)
=
U_\text{skin}(\boldsymbol\eta)
+
\sum_{m=1}^{n_m} U_m(\boldsymbol\eta),
$$

where $m$ indexes beam members in the cell.

For member $m$, define the beam strain vector:

$$
\boldsymbol\epsilon_m
= \mathbf T_m\boldsymbol\eta,
$$

where $\mathbf T_m$ maps generalized plate/shell strains into the member's axial, bending, torsional, and shear strain measures. Nemeth denotes the corresponding strain-equivalence matrix in his basic-cell method and uses it to express member energy in terms of plate strains [Nemeth 2011].

Let $\mathbf K_m$ be the member constitutive matrix in the selected beam theory. Then:

$$
U_m
=
\frac{1}{2}L_m\boldsymbol\epsilon_m^T\mathbf K_m\boldsymbol\epsilon_m
=
\frac{1}{2}L_m\boldsymbol\eta^T\mathbf T_m^T\mathbf K_m\mathbf T_m\boldsymbol\eta.
$$

The member contribution to the wall tangent is:

$$
\boxed{
\Delta \mathbf C_m
=
\frac{L_m}{A_\text{cell}}\mathbf T_m^T\mathbf K_m\mathbf T_m.
}
$$

Thus:

$$
\boxed{
\mathbf C_\text{wall}
=
\mathbf C_\text{skin}
+
\sum_m
\frac{L_m}{A_\text{cell}}\mathbf T_m^T\mathbf K_m\mathbf T_m.
}
$$

This equation should be the implementation oracle for tangent-plane cells. It is compact, testable, symmetry-safe by construction, and naturally supports graph cells, named cells, and arbitrary combinations of member families. Direct-vs-energy agreement is necessary but not sufficient because both paths share the same strain-equivalence map \(\mathbf T_m\); literature cases, NASA-derived regressions, and future FE patch checks close that loop.

### 9.2 Direct equilibrium-compatibility method as a validated specialization

The direct method remains valuable for canonical rectilinear stiffener families. In Nemeth's derivation, a discrete stiffener force or moment is related to a distributed plate stress resultant by statical equivalence; the beam strain measures are then related to the equivalent-plate strains by kinematical equivalence [Nemeth 2011].

For example, for a unidirectional stiffener family with spacing $d_S$, axial beam force $P$ contributes to the equivalent membrane resultant in the member direction as:

$$
N_{XX}^{\text{stiffener}}=\frac{P}{d_S}.
$$

The resulting family stiffness contribution is transformed into the global plate or tangent-plane frame and superposed with other family and skin contributions. This is fast and traceable, but it is also more vulnerable to formula drift and convention mistakes. Therefore:

- implement direct formulas only after the energy-equivalence oracle is implemented;
- validate direct formulas against the energy method for identical cells;
- keep direct formulas in a separate module;
- mark assumptions and limitations in metadata.

### 9.3 FE-RVE homogenizer as a future extension

A future `RVEHomogenizer` should solve cell boundary-value problems numerically and fit an effective tangent. It should be optional and backend-agnostic. Candidate Python-accessible FEM frameworks include scikit-fem for lightweight assembly, DOLFINx/FEniCSx for general PDE workflows, and SfePy for multiscale finite-element experimentation [scikit-fem docs; DOLFINx docs; SfePy docs].

The initial FE-RVE extension should target linear elastic periodic cells and produce a `LinearABDWall`. Later versions can support state-dependent nonlinear tangents.

---

## 10. Coordinate Transformations and Objectivity

### 10.1 Transformation operators

Coordinate transformations must be first-class operations. The implementation needs separate operators for:

- membrane and bending strain components;
- membrane and bending resultants;
- transverse-shear strain components;
- transverse-shear resultants.

Nemeth explicitly uses distinct transformation matrices for stress, strain, and transverse-shear quantities in the direct derivation [Nemeth 2011]. The software should mirror that distinction rather than using a single generic rotation matrix.

For a rotation by angle $\psi$ from the local surface frame $(1,2,n)$ to the stiffener frame $(X,Y,Z)$, define:

$$
\boldsymbol\epsilon_P=\mathbf T_\epsilon(\psi)\boldsymbol\epsilon_p,
\qquad
\mathbf N_P=\mathbf T_\sigma(\psi)\mathbf N_p,
\qquad
\boldsymbol\gamma_P=\mathbf T_\tau(\psi)\boldsymbol\gamma_p.
$$

The exact matrices depend on engineering-shear convention. They must be generated from `StrainConvention`, not copied ad hoc into unrelated modules.

### 10.2 Objectivity requirement

A rotated cell should homogenize to a rotated wall law. Homogenizing a cell after rotation and rotating the resulting stiffness back should recover the original law:

$$
\mathcal R(-\alpha)
\left[\text{Homogenize}(\mathcal R(\alpha)\text{Cell})\right]
\approx
\text{Homogenize}(\text{Cell}).
$$

This should be a property-based test over random angles and representative cells.

### 10.3 Why this matters

Nemeth's report discusses discrepancies in previous literature associated with shear/twist averaging factors and notes that omitting certain $1/2$ factors can break constitutive symmetry [Nemeth 2011]. This is a direct warning for software design. A plausible matrix is not necessarily a correct matrix. Objectivity, symmetry, and energy tests should be mandatory.

---

## 11. Geometry Embedding

### 11.1 Geometry does not own the wall law

For tangent-plane homogenization, geometry supplies the local tangent frame, metric, curvature, Jacobian, and shell strain-displacement operator. It does not modify the local homogenization unless an explicitly curved-cell theory is selected.

In finite-element or weak-form notation:

$$
\mathbf K
=
\int_{\Omega}
\mathbf B_\text{shell}^T
\mathbf C_\text{wall}
\mathbf B_\text{shell}
\,d\Omega.
$$

The constitutive law $\mathbf C_\text{wall}$ is local material-structure information. The operator $\mathbf B_\text{shell}$ is geometry and kinematics.

### 11.2 Parametric surface representation

A smooth shell midsurface is represented parametrically:

$$
\mathbf r=\mathbf r(u,v).
$$

The covariant tangent vectors are:

$$
\mathbf a_1=\frac{\partial\mathbf r}{\partial u},
\qquad
\mathbf a_2=\frac{\partial\mathbf r}{\partial v}.
$$

The metric tensor is:

$$
g_{\alpha\beta}=\mathbf a_\alpha\cdot\mathbf a_\beta.
$$

The unit normal is:

$$
\mathbf n=\frac{\mathbf a_1\times\mathbf a_2}{\|\mathbf a_1\times\mathbf a_2\|}.
$$

The curvature tensor is:

$$
b_{\alpha\beta}=\mathbf n\cdot
\frac{\partial^2\mathbf r}{\partial\xi^\alpha\partial\xi^\beta}.
$$

The geometry layer should compute these quantities and provide a local orthonormal frame. The constitutive kernel should not depend on shell geometry classes.

### 11.3 Flat plate

For a plate:

$$
\mathbf r(x,y)=x\mathbf e_x+y\mathbf e_y,
$$

with zero curvature. The local wall law is used directly in the plate frame.

### 11.4 Cylindrical barrel

For a cylinder of radius $R$:

$$
\mathbf r(x,\theta)=
\begin{bmatrix}
x \\
R\cos\theta \\
R\sin\theta
\end{bmatrix}.
$$

Using circumferential arc coordinate $s=R\theta$, the principal curvatures are:

$$
k_x=0,
\qquad
k_s=\frac{1}{R}.
$$

The wall law is unchanged. Curvature enters shell strain-displacement relations, for example through the normal-displacement contribution to circumferential strain in cylindrical-shell kinematics. The chosen shell theory must be explicit: Donnell, Sanders-Koiter, Reissner-Mindlin shell, or another model [Flügge 1934; Sanders 1963; Koiter 1966; Reddy 2004].

### 11.5 Spherical cap

A spherical cap of radius $R$ can be parameterized as:

$$
\mathbf r(\phi,\theta)=R
\begin{bmatrix}
\sin\phi\cos\theta \\
\sin\phi\sin\theta \\
\cos\phi
\end{bmatrix}.
$$

Both principal curvatures have magnitude $1/R$. If stiffener spacing and orientation are locally uniform, a constant wall field may be adequate. If meridional stiffeners converge, hoop spacing changes, or local cell shape changes, a spatially varying wall field is required.

### 11.6 Ellipsoid

An ellipsoid can be represented as:

$$
\mathbf r(\phi,\theta)=
\begin{bmatrix}
a\sin\phi\cos\theta \\
b\sin\phi\sin\theta \\
c\cos\phi
\end{bmatrix}.
$$

The metric, curvature, and local principal directions vary with position. Tangent-plane homogenization remains local, but wall fields must be evaluated pointwise if stiffener spacing, orientation, or section properties vary over the surface.

---

## 12. Wall Fields and Atlases

### 12.1 Constant wall field

A uniform barrel or flat coupon can use a constant wall field:

```python
@dataclass(frozen=True, slots=True)
class ConstantWallField:
    law: ConstitutiveLaw

    def law_at(self, u: float, v: float) -> ConstitutiveLaw:
        return self.law
```

### 12.2 Homogenized wall field

A spatially varying dome or ellipsoid should use a wall field that constructs a local cell and homogenizes it:

```python
@dataclass(frozen=True, slots=True)
class HomogenizedWallField:
    surface: Surface
    pattern: SurfacePattern
    homogenizer: Homogenizer
    cache: WallCache | None = None

    def law_at(self, u: float, v: float) -> ConstitutiveLaw:
        cell = self.pattern.local_cell_at(self.surface, u, v)
        return self.homogenizer.compute(cell).law
```

### 12.3 Wall atlas

For finite-element integration, repeated pointwise homogenization may be expensive. A `WallAtlas` should store sampled wall laws, interpolation rules, validity reports, and cache keys. It should never hide interpolation error. Metadata should record:

- sampling coordinates;
- interpolation method;
- maximum observed property gradient;
- maximum validity warning severity;
- source homogenizer and version;
- input hash or provenance record.

---

## 13. Verification and Validation

Correctness is a primary feature of the library.

### 13.1 Constitutive symmetry

For a conservative linear elastic wall law:

$$
\mathbf C_\text{wall}=\mathbf C_\text{wall}^T.
$$

Any significant asymmetry should fail verification unless the user has explicitly selected a nonconservative or nonsymmetric law.

### 13.2 Positive semidefiniteness

For any generalized strain state:

$$
\boldsymbol\eta^T\mathbf C_\text{wall}\boldsymbol\eta\ge 0.
$$

A complete nonmechanism cell should usually be positive definite on the modeled strain subspace. Near-zero eigenvalues may indicate a legitimate mechanism, incomplete transverse-shear modeling, invalid section properties, or a bug.

### 13.3 Energy consistency

For random generalized strain states, compare homogenized energy with explicit cell energy:

$$
\frac{1}{2}A_\text{cell}\boldsymbol\eta^T\mathbf C_\text{wall}\boldsymbol\eta
\approx
U_\text{skin}(\boldsymbol\eta)+\sum_m U_m(\boldsymbol\eta).
$$

This is the defining test for the energy-equivalence homogenizer.

### 13.4 Rotation objectivity

The rotation objectivity test in Section 10 should be automated for every canonical cell family.

### 13.5 Symmetry identities for canonical grids

An ideal equilateral isogrid with identical members should be approximately isotropic in membrane response:

$$
A_{11}\approx A_{22},
\qquad
A_{16}\approx A_{26}\approx 0,
\qquad
A_{66}\approx\frac{A_{11}-A_{12}}{2}.
$$

Similar checks can be defined for bending and twisting terms where symmetry permits.

### 13.6 Regression against NASA cases

The first validation suite should reproduce canonical cases from Nemeth's report:

- unidirectional stiffened panel;
- orthogrid;
- singly and doubly braced orthogrid;
- isosceles-triangle and equilateral isogrid cells;
- Kagome grid;
- hexagonal grid;
- star-cell grid;
- sandwich-core variants [Nemeth 2011].

For cases where Nemeth provides expressions rather than numerical tables, tests can compare symbolic reductions, numerical substitution of published formulas, or independent direct-vs-energy equivalence.

### 13.7 Discrete finite-element comparison

Before broad user claims are made, the library should include at least a small set of discrete FE validation cases:

- a single repeating cell under generalized strain boundary conditions;
- a finite periodic patch compared to homogenized plate response;
- a cylindrical stiffened barrel segment compared to an equivalent shell model;
- a mode-wavelength sensitivity study showing breakdown as wavelength approaches pitch.

This step is essential for user confidence even if the underlying formulas are literature-based.

---

## 14. Validity and Warning System

### 14.1 Curvature ratios

At a surface point:

$$
\rho_h=\frac{h_s}{R_\text{min}},
\qquad
\rho_p=\frac{p}{R_\text{min}}.
$$

Recommended default interpretation:

| Ratio | Interpretation |
|---:|---|
| $<0.02$ | generally favorable for tangent-plane homogenization |
| $0.02$ to $0.10$ | use with caution; validate against a discrete or curved-cell model |
| $>0.10$ | tangent-plane homogenization may be inadequate for local cell behavior |

These are engineering heuristics, not universal laws. They should be configurable and clearly labeled.

### 14.2 Homogenization wavelength ratio

For global analysis:

$$
\rho_\lambda=\frac{p}{L_\text{response}}.
$$

Smeared wall models are least reliable when buckling or vibration modes have wavelengths comparable to stiffener pitch.

### 14.3 Coupling ratios

Membrane-bending coupling should be flagged when:

$$
\chi_{ij}=\frac{|B_{ij}|}{\sqrt{|A_{ii}D_{jj}|}}
$$

exceeds a configurable threshold. Strong coupling does not make the wall invalid, but it does make scalar equivalent engineering constants especially misleading.

### 14.4 Dome and closed-shell topology warnings

Curved closed or partially closed surfaces may not support globally periodic flat-grid topology without defects. The library should warn when:

- meridional stiffeners converge toward a pole;
- hoop spacing approaches zero;
- cell area changes rapidly;
- orientation fields are singular or discontinuous;
- the local wall field varies on a length scale comparable to the structural response wavelength.

---

## 15. Engineering Constants and Equivalent Thickness

The library should report stiffness matrices first and engineering constants second.

For membrane-only apparent constants, let:

$$
\mathbf a=\mathbf A^{-1}.
$$

Given an explicitly selected equivalent thickness $h_\text{eq}$:

$$
E_1^\text{mem}=\frac{1}{a_{11}h_\text{eq}},
\qquad
E_2^\text{mem}=\frac{1}{a_{22}h_\text{eq}},
$$

$$
G_{12}^\text{mem}=\frac{1}{a_{66}h_\text{eq}},
\qquad
\nu_{12}^\text{mem}=-\frac{a_{12}}{a_{11}},
\qquad
\nu_{21}^\text{mem}=-\frac{a_{12}}{a_{22}}.
$$

But these are interpretations, not the constitutive truth. Nemeth explicitly discusses multiple equivalent-thickness criteria, and the ambiguity is inherent: a thickness that matches mass need not match $A_{11}$, $D_{11}$, or isotropic least-squares behavior [Nemeth 2011].

Recommended API:

```python
wall.equivalent_thickness(method="mass")
wall.equivalent_thickness(method="membrane_A11")
wall.equivalent_thickness(method="bending_D11")
wall.equivalent_thickness(method="bending_D22")
wall.equivalent_thickness(method="least_squares_isotropic")
```

Every returned engineering constant object should include:

```python
@dataclass(frozen=True, slots=True)
class EngineeringConstants:
    E1: float
    E2: float
    G12: float
    nu12: float
    nu21: float
    thickness: float
    thickness_method: str
    source: str
    warnings: tuple[str, ...]
```

---

## 16. Software Architecture

### 16.1 Dependency direction

The dependency graph should be one-way:

$$
\text{materials}\rightarrow\text{sections}\rightarrow\text{cells}\rightarrow\text{homogenizers}\rightarrow\text{constitutive laws}.
$$

Geometry and shell adapters should depend on constitutive laws, not the reverse:

$$
\text{geometry}\rightarrow\text{shell adapter}\rightarrow\text{analysis/export}.
$$

The homogenization layer must not import barrel, dome, or finite-element solver modules.

### 16.2 Recommended package layout

```text
tensyl/
    core/
        conventions.py
        frames.py
        strain_state.py
        resultants.py
        constitutive.py
        units.py

    materials/
        isotropic.py
        orthotropic.py
        laminate.py

    sections/
        beam_section.py
        rectangular.py
        thin_wall.py
        composite_section.py
        section_integration.py

    cells/
        graph_cell.py
        canonical_cells.py
        families.py
        canonicalize.py

    homogenizers/
        energy.py
        direct_ec.py
        rve.py
        transforms.py

    verification/
        invariants.py
        literature_cases.py
        property_tests.py
        diagnostics.py

    fields/
        wall_field.py
        atlas.py
        cache.py

    geometry/
        surface.py
        plate.py
        cylinder.py
        sphere.py
        spherical_cap.py
        ellipsoid.py
        parametric.py

    adapters/
        shell_kinematics.py
        fe_export.py
        nastran.py
        scikit_fem.py
        dolfinx.py
        sfepy.py

    io/
        schema.py
        json.py
        yaml.py

    optimize/
        sizing.py
        sensitivities.py
```

### 16.3 Kernel versus adapters

The kernel should have minimal dependencies: Python standard library, NumPy, and optionally a units package if adopted. Numba, FEM frameworks, and solver exporters should be optional extras:

```text
tensyl[numba]
tensyl[fem]
tensyl[nastran]
tensyl[dev]
```

This keeps the core lightweight and avoids imposing heavy solver stacks on users who only need stiffness calculations.

---

## 17. Numerical Backend Strategy

### 17.1 NumPy as the reference backend

NumPy should be the reference backend. Its array model is the standard foundation of scientific Python, and the local homogenization problem mostly uses small dense matrices and repeated array operations [van der Walt et al. 2011; Harris et al. 2020]. The reference implementation should be clear, tested, and easy to inspect.

Public typing should use `numpy.typing.NDArray` and `ArrayLike` carefully. NumPy's typing documentation notes that the typed API is intentionally stricter than some runtime behavior, which is helpful for a mechanics library where object arrays and ambiguous dtypes should be avoided [NumPy typing docs].

### 17.2 Numba for profiled kernels

Numba should be introduced only for measured hot spots. Candidate kernels include:

- repeated homogenization over large design sweeps;
- wall-field evaluation over quadrature grids;
- section-property numerical integration;
- small-matrix transformations inside optimization loops;
- repeated validity calculations over surface meshes.

Numba's performance guidance emphasizes no-Python mode and notes that explicit loops are acceptable in Numba-compiled functions [Numba docs]. Therefore, the design should keep object-heavy orchestration in Python and move only pure numerical kernels into Numba-compatible functions.

### 17.3 JAX is out of scope

JAX is fully descoped for Tensyl. Do not add a `tensyl[jax]` extra, pytree
registration, JAX-specific kernels, or JAX-oriented API constraints. Gradient
based workflows should use the NumPy reference implementation and explicit
finite-difference or analytic sensitivities until the project direction is
formally reopened.

### 17.4 Symbolic computation

Symbolic computation is useful for derivation, regression, and documentation, particularly because Nemeth provides a Mathematica program for the basic-cell energy-equivalence method [Nemeth 2011]. Runtime use should not depend on symbolic packages. Symbolic tools should live in `verification/` or a separate development notebook suite.

---

## 18. Testing, Packaging, and Reproducibility

### 18.1 Project layout

Use a `src` layout:

```text
pyproject.toml
src/tensyl/...
tests/...
benchmarks/...
docs/...
```

Pytest recommends a `src` layout and `importlib` import mode for new projects to avoid import-path ambiguity in larger packages [pytest docs].

### 18.2 Property-based tests

Hypothesis should be used for invariants such as:

- symmetry of the tangent;
- nonnegative strain energy;
- objectivity under rotation;
- equivalence between direct and energy methods for canonical cells;
- canonicalization idempotence, `canon(canon(x)) == canon(x)`;
- isotropy identities for ideal equilateral isogrid;
- consistency of `energy`, `resultants`, and `tangent`.

Hypothesis is well suited because many mechanics correctness properties are universal rather than example-specific [Hypothesis docs].

### 18.3 Static typing

Use strict type checking for the public API. Type annotations will not prove mechanics correctness, but they catch many category errors: passing a surface where a cell is expected, passing an uncanonicalized cell to a homogenizer, returning a raw array where a constitutive law is required, or confusing resultants with strains. Generalized strains and generalized resultants should be distinct public boundary types, even if they unwrap to NumPy arrays internally. Python's `typing` module supports type hints and Protocol-based interfaces, and static checkers can use these annotations even though Python does not enforce them at runtime [Python typing docs].

### 18.4 Packaging

Use `pyproject.toml` for build-system and tool configuration. The Python Packaging User Guide describes `pyproject.toml` as the standard configuration file for package build metadata and tool configuration [Python Packaging User Guide].

Recommended baseline:

```toml
[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"

[project]
name = "tensyl"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["numpy>=2.0"]

[dependency-groups]
dev = ["pytest", "hypothesis", "ruff", "ty", "mkdocs"]

[tool.pytest.ini_options]
addopts = ["--import-mode=importlib"]
testpaths = ["tests"]

[tool.ruff]
line-length = 100

[tool.ty.environment]
python-version = "3.12"
```

### 18.5 Benchmarking

Use an airspeed velocity (`asv`) benchmark suite to track performance regressions for:

- single cell homogenization;
- batched homogeneous cells;
- wall-field evaluation over a grid;
- direct versus energy method performance;
- Numba kernel speedups;
- sensitivity and optimization driver evaluation time.

Performance should be measured after correctness is established, not before.

---

## 19. Public API Example

A user-facing workflow should look like this:

```python
from tensyl.materials import IsotropicMaterial
from tensyl.sections import RectangularBeamSection
from tensyl.cells import IsogridCell
from tensyl.homogenizers import EnergyHomogenizer
from tensyl.geometry import Cylinder, SphericalCap
from tensyl.fields import ConstantWallField
from tensyl.adapters import ShellSectionExporter

aluminum = IsotropicMaterial(E=10.3e6, nu=0.33, rho=0.100)
skin = aluminum.plate(thickness=0.080)

rib = RectangularBeamSection(
    material=aluminum,
    width=0.100,
    height=1.000,
)

cell = IsogridCell(
    skin=skin,
    member_section=rib,
    pitch=6.0,
    eccentricity=0.540,
)

result = EnergyHomogenizer().compute(cell)
wall = result.law

assert result.diagnostics["symmetric"]
assert result.diagnostics["energy_consistent"]
assert wall.validity == result.validity

barrel = Cylinder(radius=120.0, length=300.0)
cap = SphericalCap(radius=120.0, half_angle_deg=35.0)

wall_field = ConstantWallField(wall)

barrel_section = ShellSectionExporter().for_surface(barrel, wall_field)
cap_section = ShellSectionExporter().for_surface(cap, wall_field)
```

The same wall law is consumed by multiple geometries. This is the core abstraction.

---

## 20. Development Roadmap

### Phase 0: project foundation

Deliver:

- `src` package layout;
- `pyproject.toml`;
- strict typing configuration;
- pytest and Hypothesis setup;
- baseline documentation;
- CI for linting, tests, and type checking.

Exit criterion: a minimal package can be installed, tested, typed, and documented reproducibly.

### Phase 1: constitutive kernel

Deliver:

- `StrainConvention`, `Frame2D`, and resultants/strain vector objects;
- `ConstitutiveLaw` protocol;
- `LinearABDWall` implementation;
- isotropic and orthotropic skin models;
- laminate ABD calculation;
- section-property model;
- stiffness rotation utilities.

Exit criterion: skin-only isotropic and laminate cases match known plate stiffnesses and pass objectivity tests.

### Phase 2: tangent-plane homogenization

Deliver:

- `CanonicalUnitCell` and graph-cell canonicalization;
- energy-equivalence homogenizer;
- direct equilibrium-compatibility homogenizer for unidirectional and orthogrid families;
- named cell constructors for orthogrid and isogrid;
- diagnostics and `ValidityReport`.

Exit criterion: direct and energy methods agree for canonical cases; NASA-derived benchmarks are reproduced.

### Phase 3: extended canonical cells and verification suite

Deliver:

- braced orthogrids;
- isosceles-triangle grid;
- Kagome grid;
- hexagonal grid;
- star-cell grid;
- sandwich-core variants;
- full literature regression suite.

Exit criterion: all canonical configurations pass symmetry, energy, objectivity, and regression tests.

### Phase 4: geometry and wall fields

Deliver:

- flat plate surface;
- cylinder;
- spherical cap;
- ellipsoid;
- constant wall field;
- homogenized wall field;
- wall atlas and caching.

Exit criterion: a single wall law can be embedded in multiple geometries and validity ratios are reported pointwise.

### Phase 5: adapters and external workflows

Deliver:

- FE property export;
- simple shell-section adapter;
- Nastran or solver-neutral JSON/YAML export;
- explicit serialization schema version and documented migration policy;
- basic optimization workflow;
- benchmark suite.

Exit criterion: an analyst can compute a wall law, validate it, and export it to an external solver through a versioned schema.

### Phase 6: advanced research extensions

Deliver selectively:

- FE-RVE homogenizer;
- nonlinear or temperature-dependent constitutive laws;
- higher-order or strain-gradient prototypes;
- micropolar/rotational continuum experiments;

Exit criterion: each advanced feature satisfies the same operator and diagnostics contracts without destabilizing the tangent-plane core.

---

## 21. Risks and Mitigations

### Risk 1: convention errors produce plausible but wrong matrices

**Mitigation:** encode conventions as value objects, separate transformation matrices by physical quantity, require objectivity tests, and regression-test against NASA cases.

### Risk 2: users overinterpret engineering constants

**Mitigation:** make $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$ the primary output. Require explicit thickness methods and warnings when $\mathbf B$ coupling is significant.

### Risk 3: tangent-plane homogenization is used outside its scale-separation envelope

**Mitigation:** attach validity reports to results and expose configurable warning thresholds for $h_s/R$, $p/R$, and $p/L_\text{response}$.

### Risk 4: direct formulas drift from the reference theory

**Mitigation:** use the energy method as the oracle. Direct formulas are accelerators only and must be tested against energy-equivalent cells.

### Risk 5: shell analysis logic contaminates the constitutive kernel

**Mitigation:** separate `core`, `homogenizers`, `fields`, `geometry`, and `adapters`. The kernel must not import solver or shell modules.

### Risk 6: premature backend complexity

**Mitigation:** keep NumPy as the reference implementation; add Numba only after profiling; keep JAX out of scope; add FEM backends only as optional extras.

---

## 22. Recommended Minimum Viable Product

The MVP should demonstrate the complete constitutive pipeline without overcommitting to shell-solver scope.

MVP capabilities:

1. Define isotropic material and plate skin.
2. Define a rectangular or property-based beam section.
3. Define unidirectional, orthogrid, and equilateral isogrid cells.
4. Canonicalize input geometry and conventions.
5. Compute $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$ using the energy-equivalence oracle.
6. Compute the same canonical cases using direct formulas where available.
7. Verify symmetry, positive semidefiniteness, energy equivalence, rotation objectivity, and isotropy identities.
8. Report $h_s/R$, $p/R$, coupling ratios, assumptions, and warnings.
9. Embed the same wall in a flat plate and cylinder adapter.
10. Export the wall law to a solver-neutral JSON/YAML schema.

The MVP should not attempt to solve every shell problem. It should prove that the constitutive kernel is reliable.

---

## 23. Conclusion

The proposed library should be built around a solver-agnostic equivalent-wall constitutive kernel. The kernel computes local wall laws from materials, skins, stiffeners, and cells. Geometry then embeds those laws into shell kinematics. This architecture preserves the mathematical separation between constitutive behavior and geometric strain-displacement operators.

The tangent-plane implementation should remain faithful to Nemeth's equivalent-plate stiffness theory: first-approximation, Reissner--Mindlin-type shear-deformation plate kinematics, shear-deformable beam stiffeners, and equivalent stiffnesses in $\mathbf A$, $\mathbf B$, $\mathbf D$, and $\mathbf A_s$ notation [Nemeth 2011]. The main improvement over a formula collection is software architecture: explicit conventions, canonicalization, an energy-equivalence oracle, verification diagnostics, validity reports, wall fields, and adapters.

For the motivating regime of roughly 1 inch stiffeners on radii greater than 100 inches, tangent-plane homogenization is a defensible starting point. Curvature should be retained in shell kinematics and validity reports, but not inserted into the local wall homogenizer unless the user selects a higher-fidelity curved-cell or RVE model.

The central rule remains:

$$
\boxed{
\text{Equivalent wall stiffness is local; shell geometry enters through kinematics, metrics, and curvature.}
}
$$

Everything in the proposed architecture follows from that rule.

---

# References

## Primary technical basis

**Nemeth, M. P. (2011).** *A Treatise on Equivalent-Plate Stiffnesses for Stiffened Laminated-Composite Plates and Plate-Like Lattices*. NASA/TP-2011-216882, Langley Research Center. NASA Technical Reports Server record commonly associated with document ID 20110004039.

**Reissner, E. (1945).** The effect of transverse shear deformation on the bending of elastic plates. *Journal of Applied Mechanics*, 12, A69--A77.

**Mindlin, R. D. (1951).** Influence of rotatory inertia and shear on flexural motions of isotropic, elastic plates. *Journal of Applied Mechanics*, 18, 31--38.

**Flügge, W. (1934/1960).** *Stresses in Shells*. Springer.

**Sanders, J. L. (1963).** Nonlinear theories for thin shells. *Quarterly of Applied Mathematics*, 21(1), 21--36.

**Koiter, W. T. (1966).** On the nonlinear theory of thin elastic shells. *Proceedings of the Koninklijke Nederlandse Akademie van Wetenschappen* and related IUTAM shell theory publications.

**Jones, R. M. (1975).** *Mechanics of Composite Materials*. McGraw-Hill; later Taylor & Francis editions.

**Reddy, J. N. (2004).** *Mechanics of Laminated Composite Plates and Shells: Theory and Analysis*. CRC Press.

**Libove, C., and Hubka, R. E. (1951).** Elastic constants for corrugated-core sandwich plates. NACA/TN work cited and surveyed by Nemeth.

**Chen, H. C., and Tsai, S. W. (1996).** Analysis and optimum design of composite grid structures. Work cited and surveyed by Nemeth.

**Wodesenbet, E., Kidane, S., and Pang, S. S. (2003).** Optimization for buckling loads of grid stiffened composite panels. Work cited and surveyed by Nemeth.

**Vasiliev, V. V., Barynin, V. A., and Rasin, A. F. (2001).** Anisogrid lattice structures: survey of development and application. *Composite Structures*, 54(2--3), 361--370.

## Homogenization and multiscale modeling

**Bensoussan, A., Lions, J.-L., and Papanicolaou, G. (1978).** *Asymptotic Analysis for Periodic Structures*. North-Holland.

**Sanchez-Palencia, E. (1980).** *Non-Homogeneous Media and Vibration Theory*. Springer.

**Bakhvalov, N. S., and Panasenko, G. P. (1989).** *Homogenisation: Averaging Processes in Periodic Media*. Kluwer.

**De Souza Neto, E. A., and Feijóo, R. A. (2008).** Variational foundations of multi-scale constitutive models of solid: small and large strain kinematical formulation. In *Computational Methods for Microstructure-Property Relationships*. Springer.

**Ye, Y., Audoly, B., and Lestringant, C. (2024).** Asymptotic, second-order homogenization of linear elastic beam networks. arXiv:2404.11316.

**Danesh, H., Heußen, L., Montáns, F. J., Reese, S., and Brepols, T. (2024).** A two-scale computational homogenization approach for elastoplastic truss-based lattice structures. arXiv:2409.17293.

**Guo, T., Kouznetsova, V. G., Geers, M. G. D., Veroy, K., and Rokoš, O. (2024).** Reduced-order modeling for second-order computational homogenization with applications to geometrically parameterized elastomeric metamaterials. arXiv:2405.00437.

**Nassar, H., and Weber, A. (2023).** Effective isometries of periodic shells. arXiv:2310.08531.

## Scientific Python and software engineering

**Python Software Foundation.** `typing` documentation, including Protocols and type hints. https://docs.python.org/3/library/typing.html

**Python Software Foundation.** `dataclasses` documentation, including frozen and slots options. https://docs.python.org/3/library/dataclasses.html

**NumPy Developers.** `numpy.typing` documentation. https://numpy.org/doc/stable/reference/typing.html

**van der Walt, S., Colbert, S. C., and Varoquaux, G. (2011).** The NumPy array: a structure for efficient numerical computation. *Computing in Science & Engineering*, 13(2), 22--30.

**Harris, C. R., et al. (2020).** Array programming with NumPy. *Nature*, 585, 357--362.

**Numba Developers.** Performance tips documentation. https://numba.readthedocs.io/en/stable/user/performance-tips.html

**pytest Developers.** Good integration practices. https://docs.pytest.org/en/stable/explanation/goodpractices.html

**Hypothesis Developers.** Hypothesis documentation. https://hypothesis.readthedocs.io/

**Python Packaging Authority.** Writing your `pyproject.toml`. https://packaging.python.org/en/latest/guides/writing-pyproject-toml/

**DOLFINx/FEniCSx Developers.** DOLFINx Python documentation. https://docs.fenicsproject.org/dolfinx/main/python/

**scikit-fem Developers.** scikit-fem documentation. https://scikit-fem.readthedocs.io/

**SfePy Developers.** SfePy documentation. https://sfepy.org/doc-devel/

**airspeed velocity Developers.** asv documentation. https://asv.readthedocs.io/

---

# Appendix A. Canonical Data Model Sketch

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Protocol
import numpy as np
import numpy.typing as npt
from typing import NewType

FloatArray = npt.NDArray[np.float64]
GeneralizedStrain = NewType("GeneralizedStrain", FloatArray)
GeneralizedResultant = NewType("GeneralizedResultant", FloatArray)


@dataclass(frozen=True, slots=True)
class StrainConvention:
    membrane_order: tuple[str, str, str] = ("e11", "e22", "g12")
    bending_order: tuple[str, str, str] = ("k11", "k22", "k12")
    shear_order: tuple[str, str] = ("g13", "g23")
    engineering_shear: bool = True
    reference_surface: str = "wall_mid_surface"


@dataclass(frozen=True, slots=True)
class Frame2D:
    e1: FloatArray
    e2: FloatArray
    n: FloatArray
    label: str = "local_tangent"


class HyperelasticLaw(Protocol):
    frame: Frame2D
    convention: StrainConvention

    def energy(self, eta: GeneralizedStrain) -> float: ...
    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant: ...
    def tangent(self, eta: GeneralizedStrain) -> FloatArray: ...


class LinearLaw(HyperelasticLaw, Protocol):
    @property
    def constant_tangent(self) -> FloatArray: ...


@dataclass(frozen=True, slots=True)
class LinearABDWall:
    C8: FloatArray
    frame: Frame2D
    convention: StrainConvention
    areal_mass: float | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def constant_tangent(self) -> FloatArray:
        return self.C8

    def tangent(self, eta: GeneralizedStrain) -> FloatArray:
        return self.C8

    def resultants(self, eta: GeneralizedStrain) -> GeneralizedResultant:
        return self.C8 @ eta

    def energy(self, eta: GeneralizedStrain) -> float:
        return 0.5 * float(eta @ self.C8 @ eta)


@dataclass(frozen=True, slots=True)
class BeamSection:
    EA: float
    EIy: float
    EIz: float
    GJ: float
    kGAy: float | None = None
    kGAz: float | None = None
    EIyz: float = 0.0
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class BeamMember:
    section: BeamSection
    length: float
    angle_rad: float
    eccentricity: float
    multiplicity: float = 1.0
    label: str = ""


@dataclass(frozen=True, slots=True)
class CanonicalUnitCell:
    area: float
    skin: Any
    members: tuple[BeamMember, ...]
    frame: Frame2D
    convention: StrainConvention
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ValidityReport:
    h_over_R: float | None
    p_over_R: float | None
    p_over_L_response: float | None
    warnings: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class HomogenizationResult:
    law: ConstitutiveLaw
    validity: ValidityReport
    diagnostics: Mapping[str, Any]
    assumptions: tuple[str, ...]
    source: Literal["energy", "direct_ec", "rve", "imported"]


class Homogenizer(Protocol):
    def compute(self, cell: CanonicalUnitCell) -> HomogenizationResult: ...
```

---

# Appendix B. Verification Checklist

- Constitutive matrix symmetry.
- Positive semidefiniteness or controlled semidefiniteness with mechanism explanation.
- Energy equivalence between homogenized law and explicit cell energy.
- Rotation objectivity over random angles.
- Direct-method agreement with energy method for canonical rectilinear cases.
- Isotropy identities for ideal equilateral isogrid.
- Orthotropy identities for orthogrids with symmetric properties.
- Transverse-shear ordering checks against Nemeth convention.
- Reference-surface translation checks for $\mathbf A$, $\mathbf B$, and $\mathbf D$.
- Unit consistency checks for $\mathbf A$, $\mathbf B$, $\mathbf D$, $\mathbf A_s$, $\mathbf N$, $\mathbf M$, and $\mathbf Q$.
- Regression against NASA-derived examples.
- Discrete FE patch comparison for at least one orthogrid and one isogrid case.
- Validity warning generation for large $h_s/R$, large $p/R$, large $p/L_\text{response}$, and large coupling ratios.
- Metadata provenance for source equations, homogenizer type, assumptions, version, and input hash.

---

# Appendix C. Recommended Document Changes Relative to the Previous Draft

The rewritten paper makes the following major changes:

1. Reframes the project as a **constitutive-kernel architecture** rather than a geometry-specific equivalent-wall library.
2. Makes the **energy-equivalence method** the reference implementation and direct formulas validated specializations.
3. Replaces matrix-only thinking with a **`ConstitutiveLaw` protocol**.
4. Adds explicit **canonicalization** before homogenization.
5. Adds **validity reports** and machine-readable diagnostics as returned results.
6. Separates **kernel**, **fields**, **geometry**, and **adapters**.
7. Adds named model families from skin-only laws to tangent-plane homogenization, spatial wall fields, FE-RVE methods, and future higher-order models.
8. Clarifies that the project is not proposing a new homogenization theory in the MVP, but a rigorous software realization and extension architecture grounded in NASA's equivalent-plate framework.
9. Adds current scientific Python best practices for typing, dataclasses, NumPy, optional Numba, pytest, Hypothesis, `pyproject.toml`, and benchmarking.
10. Strengthens warnings about scalar engineering constants and equivalent thickness.
