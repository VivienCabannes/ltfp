---
kind: node
declaration: theorem
mathlib: true
---

# Law of total expectation

Let `E` be a complete real normed space, let `mu` be an arbitrary measure, let `m <= m0`, and suppose that the corresponding trimmed measure is sigma-finite. Then the Bochner integral of a conditional expectation equals the integral of the original function:

`integral x, mu[f | m] x dmu = integral x, f x dmu`.

No probability or finite-measure assumption is required. The equality also covers nonintegrable `f` through the totalized conventions for conditional expectation and the Bochner integral.

## Mathlib

Declarations: `MeasureTheory.integral_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 2, Section 2.2.3, printed pages 28-30

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. For an arbitrary measure mu, a complete real normed-space codomain E, m <= m0, and sigma-finiteness of the trimmed measure, integral_condExp states that the integral of mu[f | m] with respect to mu equals the integral of f. It assumes neither Integrable f mu nor a probability or finite-measure structure. The integrable branch specializes setIntegral_condExp to Set.univ; in the nonintegrable branch, both condExp and the Bochner integral are zero by their totalized definitions.

## Depends on

- [Conditional expectation set-integral identity](conditional-expectation-set-integral-identity.md)
- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
