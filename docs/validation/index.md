# Validation Overview

Tensyl separates checks against published equations from comparisons with
physical tests or detailed finite-element models. Both matter, but they answer
different questions.

## Evidence Available Now

The [Nemeth cell verification](nemeth-cells.md) checks the named stiffener-cell
layouts and stiffness calculations against NASA/TP-2011-216882. Eight source
cases agree with a separately written calculation to floating-point rounding.
This is strong evidence that the source equations and cell definitions were
translated correctly.

The [SP-8007 reconciliation](sp8007-reconciliation.md) compares selected
orthogrid and isogrid stiffness terms with the elastic-constant formulas in
NASA SP-8007. It identifies which terms agree directly, one printed isogrid
term that needs correction, and the effect of an optional in-plane
member-bending extension.

These are literature checks. They do not replace a physical test campaign or
an independently meshed finite-element comparison.

## Evidence Still Planned

The independent FEM program remains planned work. It will compare Tensyl with
detailed models for:

- skin-only, unidirectional, orthogrid, eccentric-orthogrid, and isogrid cells;
- flat-panel and barrel response;
- cases near the limits of the repeating-cell approximation;
- sensitivity to joints, boundary conditions, and local effects that an
  equivalent stiffness cannot represent directly.

Each promoted case should include the input deck, solver version, extracted
results, comparison metrics, plots, and a manifest sufficient for another
engineer to repeat the work.

## How To Read the Evidence

A close literature comparison means the implementation follows the stated
source under the same assumptions. It does not prove that either model captures
every feature of a real structure.

Before using a result, check:

- whether the stiffener pattern and section idealization match the structure;
- whether pitch and stiffener height are small enough for the response being
  studied;
- whether joints, cutouts, local buckling, crippling, or load introduction need
  a more detailed model;
- whether the local frame, reference surface, and eccentricity signs match the
  downstream analysis.

That distinction keeps the claim proportional to the evidence: the current
source checks are useful and repeatable, while independent FEM correlation is
still to come.
