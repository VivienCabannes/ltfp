# Mean-square error identity for an iid sample mean

Let `mu` be a probability measure and let the positive natural number `n` and the family `X : Nat -> Omega -> Real` satisfy the hypotheses of the variance formula for an iid sample mean: `X 0` belongs to `L^2(mu)`, the variables indexed by `Finset.range n` are pairwise independent, and `X 0` is identically distributed with every `X i` for `i < n`. Let

`A_n(omega) = (n : Real)^(-1) * sum i in range n, X i omega`.

Then

`integral omega, (A_n omega - integral omega, X 0 omega dmu)^2 dmu`

`= Var[X 0; mu] / n`.

## Proof

On a probability space, membership in `L^2(mu)` implies integrability. Identical distribution gives

`integral omega, X i omega dmu = integral omega, X 0 omega dmu`

for every `i < n`. Linearity of the integral and positivity of `n` therefore give

`integral omega, A_n omega dmu = integral omega, X 0 omega dmu`.

The variance integral identity applied to `A_n` now identifies the left-hand side with `Var[A_n; mu]`. The variance formula for the iid sample mean evaluates this variance as `Var[X 0; mu] / n`.

The positivity of `n` is essential here. At `n = 0`, the right-hand side totalizes to zero, while the left-hand side is generally the square of the expectation of `X 0`.

### Mathlib support

Declarations: `ProbabilityTheory.variance_eq_integral`, `ProbabilityTheory.IdentDistrib.integral_eq`, `MeasureTheory.integral_finsetSum`, `MeasureTheory.integral_smul`
Files: `Mathlib/Probability/Moments/Variance.lean`, `Mathlib/Probability/IdentDistrib.lean`, `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`
