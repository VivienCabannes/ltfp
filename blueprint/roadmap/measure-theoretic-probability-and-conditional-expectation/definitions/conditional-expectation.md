---
kind: node
declaration: definition
mathlib: true
---

# Conditional expectation

Let `E` be a real normed space, let `mu` be a measure for a measurable structure `m0` on `alpha`, let `m` be another measurable structure on `alpha`, and let `f : alpha -> E`. The noncomputable function `mu[f | m]` is the pointwise representative of the conditional expectation of `f` with respect to `m`. The definition itself does not require `E` to be complete.

This totalized definition is zero if `m` is not below `m0`, if the trimmed measure along that inclusion is not sigma-finite, or if `f` is not Bochner integrable. Under the valid hypotheses it returns `f` when `f` is already strongly measurable with respect to `m`; otherwise it chooses the strongly measurable representative constructed through `condExpL1`.

## Mathlib

Declarations: `MeasureTheory.condExp`, `MeasureTheory.condExpL1`, `MeasureTheory.condExp_of_not_le`, `MeasureTheory.condExp_of_not_sigmaFinite`, `MeasureTheory.condExp_of_not_integrable`, `MeasureTheory.condExp_of_sigmaFinite`, `MeasureTheory.condExp_of_stronglyMeasurable`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 2, Section 2.2.3, printed pages 28-30

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. For mu with underlying measurable structure m0, condExp takes an explicit measurable structure m and has type alpha -> E for any real normed-space codomain E; the scoped notation mu[f | m] expands to condExp m mu f. The definition requires neither completeness nor a probability or finite-measure assumption. It is exactly zero when m is not below m0, when SigmaFinite of the trimmed measure fails, or when f is not Bochner integrable. Under valid hypotheses, it returns f if f is strongly measurable with respect to m, and otherwise returns the strongly measurable representative built from condExpL1. Completeness and integral-characterization laws belong to downstream nodes.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
