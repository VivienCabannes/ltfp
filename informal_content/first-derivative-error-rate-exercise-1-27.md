# First-derivative error rate (Exercise 1.27)

Let `a < b`, let `N` be a positive natural number, and let `f : Real -> Real` be differentiable on `Set.Icc a b`. Suppose

`abs (derivWithin f (Set.Icc a b) x) <= L`

for every `x` in `Set.Icc a b`. Then

`abs (T_N(f; a, b) - integral x in a..b, f x) <= L * (b - a)^2 / (4 * N)`.

In particular, on `[0, 1]` the error is at most `L / (4 * N)`, and hence is `O(1 / N)`, as requested by the source exercise.

## Proof

Put `h = (b - a) / N`, `x_i = a + i * h`, and let

`m_i = (x_i + x_(i+1)) / 2`.

The within derivative is almost everywhere measurable on the measurable compact interval. Its uniform bound therefore makes it interval integrable. Differentiability also makes `f` continuous and interval integrable. Integration by parts gives

`integral x in x_i..x_(i+1), ((x - m_i) * f'(x))`

`= (h / 2) * (f x_i + f x_(i+1)) - integral x in x_i..x_(i+1), f x`.

Thus this integral is exactly the signed one-panel trapezoidal error. Since `abs (x - m_i) <= h / 2` on the panel and `abs (f'(x)) <= L`,

`abs ((h / 2) * (f x_i + f x_(i+1)) - integral x in x_i..x_(i+1), f x)`

`<= L * integral x in x_i..x_(i+1), abs (x - m_i)`

`= L * h^2 / 4`.

The exact error decomposition and the triangle inequality now give

`abs (T_N(f; a, b) - integral x in a..b, f x) <= N * L * h^2 / 4`.

Substituting `h = (b - a) / N` proves the stated bound. Mathlib's error uses the estimator-minus-integral orientation, opposite to the book's `I - I_hat`, but their absolute values agree.

### Mathlib status

The pinned checkout provides interval integration by parts and the exact trapezoidal panel decomposition, but no named first-derivative trapezoidal-rate theorem was found.

Supporting declarations: `intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivWithinAt`, `sum_trapezoidal_error_adjacent_intervals`, `MeasureTheory.aemeasurable_fderivWithin`, `intervalIntegral.norm_integral_le_of_norm_le`, `derivWithin_subset`
Files: `Mathlib/MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`, `Mathlib/MeasureTheory/Function/Jacobian.lean`, `Mathlib/Analysis/Calculus/Deriv/Basic.lean`
