# Interval integral

Let `E` be a real normed vector space, let `f : Real -> E`, let `mu` be an arbitrary measure on the real line, and let `a b : Real`. The oriented interval integral is defined by

`integral (mu.restrict (Set.Ioc a b)) f - integral (mu.restrict (Set.Ioc b a)) f`.

Reversing the endpoints negates the value. When the endpoints are ordered, only the corresponding half-open interval remains, and in general the result is a sign times the integral over `Set.uIoc a b`. No completeness or integrability hypothesis is required to form the expression. It is zero when `f` is not interval integrable; totalization of the underlying Bochner integrals also makes it zero for an incomplete codomain.

## Mathlib

Declarations: `intervalIntegral`, `intervalIntegral.integral_of_le`, `intervalIntegral.integral_of_ge`, `intervalIntegral.integral_symm`, `intervalIntegral.intervalIntegral_eq_integral_uIoc`, `intervalIntegral.integral_undef`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`
