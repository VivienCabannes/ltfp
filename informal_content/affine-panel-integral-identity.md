# Affine panel integral identity

Let `f : Real -> Real` and let `a, b : Real`. The affine panel interpolant is interval integrable and satisfies the oriented identity

`integral x in a..b, A[f; a, b](x) = (b - a) * (f a + f b) / 2`.

In particular,

`integral x in 0..1, ((1 - x) * f 0 + x * f 1) = (f 0 + f 1) / 2`.

No order assumption on the endpoints is needed. If `b < a`, both the interval integral and the factor `b - a` change sign. If `a = b`, Lean's totalized normalized interpolant still makes the displayed equality true because both sides are zero.

## Proof

For `a != b`, set `x = a + t * (b - a)`. With oriented intervals, `t` runs from `0` to `1` even when the endpoints are reversed, and

`A[f; a, b](a + t * (b - a)) = (1 - t) * f a + t * f b`.

The change of variables therefore gives

`integral x in a..b, A[f; a, b](x)`

`= (b - a) * integral t in 0..1, ((1 - t) * f a + t * f b)`

`= (b - a) * (f a / 2 + f b / 2)`.

The integrability used here is automatic because the interpolant is affine and hence continuous. The degenerate case `a = b` follows directly from the zero-length interval integral.

### Mathlib support

`AffineMap.lineMap_apply_ring` supplies the affine formula, `Continuous.intervalIntegrable` supplies integrability, and the standard interval-integral rules for addition, constant multiplication, constants, and the identity function prove the formula. `trapezoidal_integral_one` identifies the right-hand side as the one-panel trapezoidal approximation. There is no named declaration in the pinned checkout equating the interval integral of this normalized affine interpolant with that approximation.

Declarations: `AffineMap.lineMap_apply_ring`, `Continuous.intervalIntegrable`, `intervalIntegral.integral_add`, `intervalIntegral.integral_mul_const`, `intervalIntegral.integral_const`, `integral_id`, `trapezoidal_integral_one`
Files: `Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean`, `Mathlib/Analysis/SpecialFunctions/Integrals/Basic.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`, `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`
