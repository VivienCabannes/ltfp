---
kind: node
declaration: theorem
mathlib: true
---

# Rolle's theorem for real derivatives

Let `f : Real -> Real`, let `a < b`, suppose `f` is continuous on `Set.Icc a b`, and suppose `f a = f b`. If a function `f'` is a derivative of `f` at every point of `Set.Ioo a b`, then there exists `c` in that open interval such that

`f' c = 0`.

Mathlib also provides a version stated with the totalized `deriv f`. That version needs no explicit differentiability hypothesis because `deriv f c` is defined to be zero when `f` is not differentiable at `c`. Proofs that need a genuine derivative value should use the `HasDerivAt` version and supply the interior derivative hypotheses.

## Mathlib

Declarations: `exists_hasDerivAt_eq_zero`, `exists_deriv_eq_zero`
File: `Mathlib/Analysis/Calculus/LocalExtr/Rolle.lean`


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/LocalExtr/Rolle.lean`.

Verified in the pinned checkout. For a < b, continuity on Icc, equal endpoint values, and a HasDerivAt witness at every interior point, exists_hasDerivAt_eq_zero returns c in Ioo with the witnessed derivative equal to zero. exists_deriv_eq_zero uses totalized deriv and therefore omits an explicit differentiability premise; genuine-derivative arguments should use the HasDerivAt version.

## Depends on

- [Frechet derivative](../../differential-and-integral-calculus/definitions/frechet-derivative.md)
