---
kind: node
declaration: theorem
mathlib: true
---

# Mean-square convergence of iid sample means

Let `mu` be a probability measure and let `X : Nat -> Omega -> Real`. Suppose `X 0` belongs to `L^2(mu)`, the sequence is pairwise independent, and every `X i` is identically distributed with `X 0`. Then the sample means converge in `L^2(mu)` to the constant expectation of `X 0`:

`eLpNorm (fun omega => (n : Real)^(-1) * sum i in range n, X i omega`

`  - integral omega, X 0 omega dmu) 2 mu -> 0`

as `n -> infinity`.

The value chosen for the zero-sample average does not affect this limit. This is mean-square convergence; squaring the `L^2` seminorm gives the expected squared error whenever the functions are in `L^2`.

The source route uses the preceding mean-square error identity. For every positive `n`, the square of the displayed `L^2` seminorm is `Var[X 0; mu] / n`, which tends to zero. Nonnegativity then forces the seminorm itself to tend to zero. Mathlib's theorem below proves the same conclusion directly.

## Mathlib

Declarations: `ProbabilityTheory.strong_law_Lp`
File: `Mathlib/Probability/StrongLaw.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, paragraph following equation (1.4)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/StrongLaw.lean`.

Verified by a compiled specialization of ProbabilityTheory.strong_law_Lp in the pinned checkout. At p = 2 and E = Real, MemLp (X 0) 2 mu, global pairwise independence Pairwise ((fun i j => IndepFun (X i) (X j) mu) on X), and IdentDistrib (X i) (X 0) mu mu for every i give Tendsto of the L2 seminorm of the centered Finset.range n average to zero. The source dependency route instead squares the seminorm, applies the upstream mean-square identity Var[X 0; mu] / n, and uses its limit. The theorem needs no explicit IsProbabilityMeasure mu instance. Its n = 0 average is totalized to zero and is irrelevant to the atTop limit.

## Depends on

- [Mean-square error identity for an iid sample mean](mean-square-error-identity-for-an-iid-sample-mean.md)
