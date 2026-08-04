# Integral Jensen inequality

Let `E` be a complete real normed vector space, let `mu` be a probability measure on a measurable space, let `s` be a closed convex subset of `E`, and let `g : E -> Real` be convex and continuous on `s`. Suppose `f x` belongs to `s` for `mu`-almost every `x` and both `f` and `g ∘ f` are Bochner integrable with respect to `mu`. Then

`g (integral x, f x dmu) <= integral x, g (f x) dmu`.

No separate hypothesis says that the integral of `f` belongs to `s`; that membership follows from convexity, closedness, almost-everywhere membership, and integrability. A finite nonzero measure version uses normalized averages instead of integrals.

No separate measurability or sigma-finiteness assumption is needed. For a probability measure, `MeasureTheory.average_eq_integral` identifies the normalized average with the integral for every function. That supporting declaration is defined in `Mathlib/MeasureTheory/Integral/Average.lean`; the primary Jensen declarations listed below are in `Mathlib/Analysis/Convex/Integral.lean`.

## Mathlib

Declarations: `ConvexOn.map_average_le`, `ConvexOn.map_integral_le`, `Convex.integral_mem`, `MeasureTheory.average_eq_integral`
File: `Mathlib/Analysis/Convex/Integral.lean`
