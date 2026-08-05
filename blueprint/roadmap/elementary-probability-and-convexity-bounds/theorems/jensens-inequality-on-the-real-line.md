---
kind: node
declaration: proposition
mathlib: true
---

# Jensen's inequality on the real line

Let `mu` be a probability measure, let `X : Omega -> Real` be integrable, and let `F : Real -> Real` be convex on all of `Real`. Suppose `F composed with X` is integrable. Then

`F (integral omega, X omega dmu)`

`<= integral omega, F (X omega) dmu`.

A finite real-valued convex function on the whole real line is continuous, so no separate continuity hypothesis is needed in this scalar specialization. This result is the one-dimensional specialization of the existing integral Jensen inequality, with the closed convex domain chosen to be `Set.univ`.

## Mathlib

Declarations: `ConvexOn.map_integral_le`, `ConvexOn.continuousOn`
File: `Mathlib/Analysis/Convex/Integral.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, Proposition 1.1, printed pages 9-10

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Integral.lean`.

Verified in the pinned checkout. ConvexOn.map_integral_le specialized to E = Real and s = Set.univ gives the exact probability-measure Jensen inequality for Integrable X and Integrable (F composed with X). Global real ConvexOn supplies ContinuousOn by ConvexOn.continuousOn because Real is finite dimensional and univ is open; that continuity theorem is defined in Mathlib/Analysis/Convex/Continuous.lean.

## Depends on

- [Integral Jensen inequality](../../measure-theoretic-probability-and-conditional-expectation/theorems/integral-jensen-inequality.md)
- [Convex functions on a set](../../convex-analysis-and-normed-space-geometry/definitions/convex-functions-on-a-set.md)
