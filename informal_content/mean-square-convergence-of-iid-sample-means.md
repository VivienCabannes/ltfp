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
