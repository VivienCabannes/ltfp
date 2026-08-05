---
kind: node
declaration: theorem
mathlib: true
---

# Variance of a finite sum of pairwise independent random variables

Let `mu` be an arbitrary measure on a measurable space `Omega`, let `s` be a `Finset` in an arbitrary index type, and let `X i : Omega -> Real`. Assume

`forall i in s, MemLp (X i) 2 mu`

and assume pairwise independence on `s`, expressed exactly as

`Set.Pairwise (s : Set _) (fun i j => IndepFun (X i) (X j) mu)`.

Then

`variance (sum i in s, X i) mu = sum i in s, variance (X i) mu`.

No probability-measure or finite-measure instance is required. The index type need not be finite, since finiteness is supplied by `s`, and no identical-distribution hypothesis is used. Mathlib's variance is a total definition; the `MemLp` assumptions provide the square-integrability and measurability regularity required by this theorem.

## Mathlib

Declarations: `ProbabilityTheory.IndepFun.variance_sum`
File: `Mathlib/Probability/Moments/Variance.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, independent-sum variance display

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/Moments/Variance.lean`.

Verified in the pinned checkout. For an arbitrary measure mu, arbitrary index type, Finset s, and real-valued family X, the theorem assumes MemLp (X i) 2 mu only for i in s and Set.Pairwise on s of binary IndepFun. It requires no IsProbabilityMeasure, IsFiniteMeasure, Fintype, or identical-distribution hypothesis. Variance is total; MemLp supplies the regularity required by this theorem.

## Depends on

- [Pairwise independence on a finite index set](../definitions/pairwise-independence-on-a-finite-index-set.md)
