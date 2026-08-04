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
