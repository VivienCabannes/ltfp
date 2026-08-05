---
kind: node
declaration: theorem
mathlib: true
---

# Radon-Nikodym representation theorem

Let `mu` and `nu` be measures with `HaveLebesgueDecomposition mu nu`. Then `mu` is absolutely continuous with respect to the reference measure `nu` if and only if weighting `nu` by the `ENNReal`-valued density `mu.rnDeriv nu` recovers `mu`:

`nu.withDensity (mu.rnDeriv nu) = mu`.

The standard decomposition instance is available when `mu` is s-finite and `nu` is sigma-finite; in particular, two sigma-finite measures suffice. Although `rnDeriv` is totalized outside this setting, the representation theorem still requires the decomposition instance.

## Mathlib

Declarations: `MeasureTheory.Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq`, `MeasureTheory.Measure.withDensity_rnDeriv_eq`, `MeasureTheory.Measure.haveLebesgueDecomposition_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/RadonNikodym.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Decomposition/RadonNikodym.lean`.

Verified in the pinned checkout. Under HaveLebesgueDecomposition mu nu, the theorem states that mu is absolutely continuous with respect to nu exactly when nu.withDensity (mu.rnDeriv nu) = mu, where mu.rnDeriv nu is ENNReal-valued. The standard instance requires SFinite mu and SigmaFinite nu; two sigma-finite measures are a special case. Although rnDeriv is totalized to zero without a decomposition, this representation theorem is not unconditional.

## Depends on

- [Radon-Nikodym derivative of measures](../definitions/radon-nikodym-derivative-of-measures.md)
