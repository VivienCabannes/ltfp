# Fundamental theorem of calculus for interval integrals

Let `E` be a complete real normed vector space, let `f f' : Real -> E`, and let `a b : Real`. Suppose that `HasDerivAt f (f' x) x` holds at every `x` in `Set.uIcc a b`, and suppose that `f'` is interval integrable from `a` to `b` with respect to volume. Then the oriented interval integral satisfies

`integral x in a..b of f' x = f b - f a`.

The derivative hypothesis is an ambient derivative, including at both endpoints. No order on `a` and `b` and no separate continuity hypothesis is required.

## Mathlib

Declarations: `intervalIntegral.integral_eq_sub_of_hasDerivAt`, `intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le`, `intervalIntegral.integral_eq_sub_of_hasDeriv_right`, `intervalIntegral.integral_eq_sub_of_hasDeriv_right_of_le`, `intervalIntegral.integral_deriv_eq_sub`, `intervalIntegral.integral_deriv_eq_sub'`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean`
