---
kind: node
declaration: theorem
mathlib: true
---

# Conditional expectation set-integral identity

Let `E` be a complete real normed space, let `m <= m0`, suppose that `mu.trim` along this inclusion is sigma-finite, and let `f` be Bochner integrable with respect to `mu`. For every `m`-measurable set `s`, the set integrals agree:

`integral x in s, mu[f | m] x dmu = integral x in s, f x dmu`.

## Mathlib

Declarations: `MeasureTheory.setIntegral_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 2, Section 2.2.3, printed pages 28-30

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

The verified theorem retains m <= m0, SigmaFinite of the trimmed measure, Integrable f mu, completeness of the codomain, and MeasurableSet[m] s. Both set integrals use mu restricted to s; the theorem is not an invalid-case totalization identity.

## Depends on

- [Conditional expectation](../definitions/conditional-expectation.md)
- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
