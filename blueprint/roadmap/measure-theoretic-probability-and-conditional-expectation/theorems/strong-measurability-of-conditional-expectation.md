---
kind: node
declaration: theorem
mathlib: true
---

# Strong measurability of conditional expectation

Let `m0` be the measurable structure underlying a measure `mu`, let `m` be another measurable structure on the same type, let `E` be a real normed space, and let `f` take values in `E`. The conditional expectation `mu[f | m]` is strongly measurable with respect to `m`.

No inclusion `m <= m0`, trimmed sigma-finiteness, integrability, or completeness assumption is needed. The statement remains true in every invalid branch of the totalized definition because the conditional expectation is then zero.

## Mathlib

Declarations: `MeasureTheory.stronglyMeasurable_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. For measurable structures m and m0 on alpha, mu : Measure[m0] alpha, f : alpha -> E, and a real normed-space codomain E, stronglyMeasurable_condExp proves StronglyMeasurable[m] (mu[f | m]). It requires neither m <= m0, trimmed sigma-finiteness, integrability, nor completeness because every invalid branch of the totalized conditional expectation is zero.

## Depends on

- [Conditional expectation](../definitions/conditional-expectation.md)
