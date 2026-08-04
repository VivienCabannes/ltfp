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
