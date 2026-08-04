# Periodic Bernoulli-kernel trapezoidal identity

For `r >= 1`, let `B_r` be the Bernoulli polynomial normalized by

`B_1(t) = t - 1 / 2`, `B_(r+1)'(t) = (r + 1) * B_r(t)`,

and `B_r(1) = B_r(0)` for `r != 1`.

Let `s : Nat` satisfy `1 <= s`, let `N` be a positive natural number, and let `f : Real -> Real` satisfy `ContDiff Real s f`. Suppose

`iteratedDeriv r f 1 = iteratedDeriv r f 0`

for every natural number `r` with `1 <= r < s`. Then

`T_N(f; 0, 1) - integral x in 0..1, f x`

`= (-1)^(s - 1) * sum k in {0, ..., N - 1},`

`    integral x in k/N..(k+1)/N,`

`      (bernoulliFun s (N*x - k) / (s! * N^s)) * iteratedDeriv s f x`.

For `s = 1`, the endpoint-matching condition is empty.

## Proof

On the `k`-th panel define

`P_(r,k)(x) = B_r(N*x - k) / (r! * N^r)`.

For `r = 1`, this is

`P_(1,k)(x) = x - (k + 1/2) / N`,

the displacement from the panel midpoint. Integration by parts therefore gives

`integral x in k/N..(k+1)/N, P_(1,k)(x) * f'(x)`

`= (f(k/N) + f((k+1)/N)) / (2*N)`

`  - integral x in k/N..(k+1)/N, f x`.

Summing these equalities over the panels produces exactly

`T_N(f; 0, 1) - integral x in 0..1, f x`.

The Bernoulli derivative identity gives

`P_(r+1,k)' = P_(r,k)`.

Integrating by parts once more replaces the integral of `P_(r,k) * f^(r)` by the negative integral of `P_(r+1,k) * f^(r+1)`, plus boundary terms. For `r + 1 >= 2`, the equality `B_(r+1)(1) = B_(r+1)(0)` gives the same coefficient at both ends of every panel. After summation, the boundary terms telescope to that common coefficient times `f^(r)(1) - f^(r)(0)`, which vanishes by the endpoint hypothesis.

Repeating this step for `r = 1, ..., s - 1` introduces `s - 1` minus signs and yields the displayed identity.

### Mathlib status

The pinned checkout contains the required Bernoulli-polynomial derivative, endpoint, continuity, and integral facts, but no theorem connecting them to trapezoidal quadrature was found.

Supporting declarations: `trapezoidal_error`, `sum_trapezoidal_error_adjacent_intervals`, `bernoulliFun`, `bernoulliFun_one`, `hasDerivAt_bernoulliFun`, `contDiff_bernoulliFun`, `bernoulliFun_endpoints_eq_of_ne_one`, `intervalIntegral.integral_mul_deriv_eq_deriv_mul`, `iteratedDeriv`, `iteratedDeriv_succ`, `ContDiff.continuous_iteratedDeriv`, `ContDiff.differentiable_iteratedDeriv`
Files: `Mathlib/NumberTheory/ZetaValues.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/IntegrationByParts.lean`, `Mathlib/Analysis/Calculus/IteratedDeriv/Defs.lean`
