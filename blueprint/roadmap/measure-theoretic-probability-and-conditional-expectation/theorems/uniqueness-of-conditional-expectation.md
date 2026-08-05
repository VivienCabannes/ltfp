---
kind: node
declaration: theorem
mathlib: true
---

# Uniqueness of conditional expectation

Let `E` be a complete real normed space, let `m <= m0`, suppose that `mu.trim` along this inclusion is sigma-finite, and let `f` be Bochner integrable. Suppose that `g` is `m`-almost-everywhere strongly measurable, is integrable on every `m`-measurable set of finite `mu`-measure, and has the same set integral as `f` on every such set. Then `g = mu[f | m]` almost everywhere with respect to `mu`.

## Mathlib

Declarations: `MeasureTheory.ae_eq_condExp_of_forall_setIntegral_eq`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`.

Verified in the pinned checkout. Under m <= m0, sigma-finiteness of the trimmed measure, completeness of the real normed codomain, and Integrable f mu, the theorem assumes that g is almost-everywhere strongly measurable with respect to m and integrable on every m-measurable finite-mu-measure set, with the same set integrals as f there. It concludes g = mu[f | m] almost everywhere with respect to mu. The previously guessed ae_eq_condExp_iff_eq_setIntegral declaration does not exist; an iff is derivable using setIntegral_condExp but is not a named theorem.

## Depends on

- [Strong measurability of conditional expectation](strong-measurability-of-conditional-expectation.md)
- [Integrability of conditional expectation](integrability-of-conditional-expectation.md)
- [Conditional expectation set-integral identity](conditional-expectation-set-integral-identity.md)
