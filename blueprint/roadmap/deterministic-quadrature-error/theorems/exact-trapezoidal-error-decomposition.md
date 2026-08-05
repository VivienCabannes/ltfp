---
kind: node
declaration: proposition
statement: formalized
proof: formalized
lean: integral_sub_trapezoidal_integral_eq_sum_panel_error, integral_sub_trapezoidal_integral_eq_sum_integral_residual, trapezoidal_error_eq_neg_sum_integral_residual, abs_trapezoidal_error_eq_abs_sum_integral_residual, IntervalIntegrable.uniform_grid_panel
---

# Exact trapezoidal error decomposition

Let `a, b : Real`, let `N` be a positive natural number, and put

`h = (b - a) / N`, `x_i = a + i * h` for `0 <= i <= N`.

Suppose `f : Real -> Real` is interval integrable on `[a, b]`. For `i < N`, let `A_i` be the affine interpolant of `f` at `x_i` and `x_(i+1)`. Then

`(integral x in a..b, f x) - T_N(f; a, b)`

`= sum i in {0, ..., N - 1}, ((integral x in x_i..x_(i+1), f x) - h * (f x_i + f x_(i+1)) / 2)`

`= sum i in {0, ..., N - 1}, (integral x in x_i..x_(i+1), (f x - A_i(x)))`.

## Proof

Interval integrability on `[a, b]` restricts to every panel. Additivity over adjacent intervals gives

`integral x in a..b, f x = sum i, integral x in x_i..x_(i+1), f x`.

The piecewise-affine integral identity gives

`T_N(f; a, b) = sum i, integral x in x_i..x_(i+1), A_i(x)`.

Subtract these finite sums term by term. Linearity of the interval integral then turns each difference into the integral of `f - A_i`, proving both equalities. The argument is oriented and requires no order on `a` and `b`; it also remains valid when `a = b`.

Mathlib defines

`trapezoidal_error f N a b = T_N(f; a, b) - integral x in a..b, f x`.

Therefore its signed error is the negative of the one displayed above. The absolute errors are identical.

The assumption `0 < N` is essential. At `N = 0`, the estimator and the panel sum are zero, while the integral of `f` need not vanish, so the displayed decomposition generally fails.

### Mathlib support

Declarations: `trapezoidal_error`, `trapezoidal_integral_one`, `sum_trapezoidal_integral_adjacent_intervals`, `sum_trapezoidal_error_adjacent_intervals`, `intervalIntegral.sum_integral_adjacent_intervals`, `intervalIntegral.integral_sub`, `IntervalIntegrable.mono`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 19

## Planning record

Legacy Mathlib assessment: `partial`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`.

Verified by a compiled Lean assembly in the pinned checkout. For 0 < N and IntervalIntegrable f volume a b, negating sum_trapezoidal_error_adjacent_intervals gives the source sign integral-minus-estimator as the sum of panel errors. Panel restriction, finite interval additivity, integral_sub, and the affine-panel identity give the residual form. No endpoint order is required. At N = 0 the decomposition is generally false because the estimator and panel sum are zero but the integral need not be. Generic interval declarations are in Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean.

## Depends on

- [Piecewise-affine integral identity](piecewise-affine-integral-identity.md)
- [Interval integrability](../../differential-and-integral-calculus/definitions/interval-integrability.md)
- [Interval integral](../../differential-and-integral-calculus/definitions/interval-integral.md)
