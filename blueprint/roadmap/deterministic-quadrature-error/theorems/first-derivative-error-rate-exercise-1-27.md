---
kind: node
declaration: theorem
statement: formalized
proof: formalized
lean: abs_trapezoidal_error_le_of_deriv_bound, abs_trapezoidal_integral_sub_integral_le_of_deriv_bound, abs_trapezoidal_integral_sub_integral_unitInterval_le_of_deriv_bound, isBigO_trapezoidal_error_of_deriv_bound
---

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


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 19, Exercise 1.27
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.27, printed page 4

## Planning record

Legacy Mathlib assessment: `partial`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean`.

Verified by a compiled Lean assembly in the pinned checkout. It suffices that a < b, 0 < N, f is DifferentiableOn Real on Set.Icc a b, and abs (derivWithin f (Set.Icc a b) x) <= L throughout the interval. No ContDiffOn or separate integrability hypothesis is needed: aemeasurable_fderivWithin and bounded domination give interval integrability of the derivative. Integration by parts with the midpoint kernel and sum_trapezoidal_error_adjacent_intervals give exactly abs (trapezoidal_error f N a b) <= L * (b-a)^2 / (4*N). No named first-derivative trapezoidal-rate theorem was found.

## Depends on

- [Exact trapezoidal error decomposition](exact-trapezoidal-error-decomposition.md)
- [Frechet derivative](../../differential-and-integral-calculus/definitions/frechet-derivative.md)
- [Fundamental theorem of calculus for interval integrals](../../differential-and-integral-calculus/theorems/fundamental-theorem-of-calculus-for-interval-integrals.md)
