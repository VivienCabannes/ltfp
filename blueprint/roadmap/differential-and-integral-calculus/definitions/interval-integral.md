---
kind: node
declaration: definition
mathlib: true
---

# Interval integral

Let `E` be a real normed vector space, let `f : Real -> E`, let `mu` be an arbitrary measure on the real line, and let `a b : Real`. The oriented interval integral is defined by

`integral (mu.restrict (Set.Ioc a b)) f - integral (mu.restrict (Set.Ioc b a)) f`.

Reversing the endpoints negates the value. When the endpoints are ordered, only the corresponding half-open interval remains, and in general the result is a sign times the integral over `Set.uIoc a b`. No completeness or integrability hypothesis is required to form the expression. It is zero when `f` is not interval integrable; totalization of the underlying Bochner integrals also makes it zero for an incomplete codomain.

## Mathlib

Declarations: `intervalIntegral`, `intervalIntegral.integral_of_le`, `intervalIntegral.integral_of_ge`, `intervalIntegral.integral_symm`, `intervalIntegral.intervalIntegral_eq_integral_uIoc`, `intervalIntegral.integral_undef`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`.

Verified in the pinned checkout for f : Real -> E into any real normed vector space and an arbitrary measure mu on Real. The definition is the difference of the Bochner integrals against mu restricted to Ioc a b and Ioc b a. Endpoint reversal and the ordered-endpoint formulas require no integrability or completeness hypotheses, and the value is a sign times the integral over uIoc a b. The construction is totalized: it is zero when interval integrability fails, and the underlying Bochner integrals are zero for an incomplete codomain.

## Depends on

- [Bochner integral](bochner-integral.md)
- [Interval integrability](interval-integrability.md)
