---
kind: node
declaration: theorem
mathlib: true
---

# Integrability of conditional expectation

Let `m0` be the measurable structure underlying a measure `mu`, let `m` be another measurable structure on the same type, let `E` be a complete real normed space, and let `f` take values in `E`. The conditional expectation `mu[f | m]` is Bochner integrable with respect to `mu`.

No input-integrability, inclusion `m <= m0`, or trimmed sigma-finiteness hypothesis is required. In every invalid branch of the totalized definition, the conditional expectation is the zero function. Completeness of `E` is an assumption of the integrability theorem itself.

## Mathlib

Declarations: `MeasureTheory.integrable_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. For measurable structures m and m0, a measure mu with underlying structure m0, an arbitrary f : alpha -> E, and a complete real normed-space codomain E, integrable_condExp proves Integrable (mu[f | m]) mu. There is no hypothesis that f is integrable, that m <= m0, or that a trimmed measure is sigma-finite. Failure of any validity condition makes condExp zero; completeness is a theorem assumption rather than a totalization branch.

## Depends on

- [Conditional expectation](../definitions/conditional-expectation.md)
- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
