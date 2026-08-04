# Second-derivative trapezoidal error bound

Let `f : Real -> Real`, let `a, b : Real`, let `N` be a positive natural number, and let `0 <= L`. Suppose `f` is differentiable on the unordered interval `Set.uIcc a b` and its within derivative

`derivWithin f (Set.uIcc a b)`

is differentiable there. Suppose also that

`abs (iteratedDerivWithin 2 f (Set.uIcc a b) x) <= L`

for every `x` in `Set.uIcc a b`. Then

`abs (T_N(f; a, b) - integral x in a..b, f x) <= abs (b - a)^3 * L / (12 * N^2)`.

No endpoint order is required. For `a = 0` and `b = 1`, this becomes

`abs ((integral x in 0..1, f x) - T_N(f; 0, 1)) <= L / (12 * N^2)`.

The sign in the last display is reversed relative to Mathlib's `trapezoidal_error`, but the absolute value removes that difference. No separate interval-integrability assumption is needed.

## Mathlib

Declarations: `trapezoidal_error_le`, `trapezoidal_error_le_of_c2`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`
