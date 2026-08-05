---
kind: node
declaration: definition
mathlib: true
---

# Radon-Nikodym derivative of measures

For measures `mu` and `nu` on the same measurable space, `mu.rnDeriv nu` is a noncomputable, total `ENNReal`-valued function. The definition internally tests whether `HaveLebesgueDecomposition mu nu` holds. When it does, the function is the selected measurable density in

`mu = mu.singularPart nu + nu.withDensity (mu.rnDeriv nu)`.

When no such decomposition exists, the derivative is exactly the zero function. The public definition itself has no finiteness assumptions; `SFinite mu` together with `SigmaFinite nu` supplies the standard decomposition instance.

## Mathlib

Declarations: `MeasureTheory.Measure.HaveLebesgueDecomposition`, `MeasureTheory.Measure.rnDeriv`, `MeasureTheory.Measure.rnDeriv_of_not_haveLebesgueDecomposition`, `MeasureTheory.Measure.haveLebesgueDecomposition_spec`, `MeasureTheory.Measure.haveLebesgueDecomposition_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`.

Verified in the pinned checkout. For measures mu and nu on the same measurable space, rnDeriv mu nu : alpha -> ENNReal is a noncomputable irreducible total definition. It has no finiteness or decomposition typeclass parameter: it internally tests the proposition HaveLebesgueDecomposition mu nu, classically chooses its measurable density when true, and is exactly the zero function when false. Under HaveLebesgueDecomposition mu nu, haveLebesgueDecomposition_spec gives measurability, mutual singularity of the selected singular part with nu, and mu = mu.singularPart nu + nu.withDensity (mu.rnDeriv nu). The standard instance assumes SFinite mu and SigmaFinite nu. The argument order is the density component of mu relative to reference measure nu; this node does not assert absolute-continuity recovery or almost-everywhere uniqueness.

## Depends on

This node has no prerequisites.
