---
kind: node
declaration: theorem
mathlib: true
---

# Integral Jensen inequality

Let `E` be a complete real normed vector space, let `mu` be a probability measure on a measurable space, let `s` be a closed convex subset of `E`, and let `g : E -> Real` be convex and continuous on `s`. Suppose `f x` belongs to `s` for `mu`-almost every `x` and both `f` and `g ∘ f` are Bochner integrable with respect to `mu`. Then

`g (integral x, f x dmu) <= integral x, g (f x) dmu`.

No separate hypothesis says that the integral of `f` belongs to `s`; that membership follows from convexity, closedness, almost-everywhere membership, and integrability. A finite nonzero measure version uses normalized averages instead of integrals.

No separate measurability or sigma-finiteness assumption is needed. For a probability measure, `MeasureTheory.average_eq_integral` identifies the normalized average with the integral for every function. That supporting declaration is defined in `Mathlib/MeasureTheory/Integral/Average.lean`; the primary Jensen declarations listed below are in `Mathlib/Analysis/Convex/Integral.lean`.

## Mathlib

Declarations: `ConvexOn.map_average_le`, `ConvexOn.map_integral_le`, `Convex.integral_mem`, `MeasureTheory.average_eq_integral`
File: `Mathlib/Analysis/Convex/Integral.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Integral.lean`.

Verified in the pinned checkout. ConvexOn.map_integral_le is for a complete real normed space E, a probability measure mu, f : alpha -> E, and a real-valued g : E -> Real. It assumes ConvexOn Real s g, ContinuousOn g s, IsClosed s, almost-everywhere membership f x in s, Integrable f mu, and Integrable (g composed with f) mu. There is no separate sigma-finiteness, measurability, or integral-membership hypothesis; Convex.integral_mem derives that the Bochner integral lies in s. The finite nonzero measure variant is map_average_le and uses normalized averages. MeasureTheory.average_eq_integral is the supporting normalization declaration defined in Mathlib/MeasureTheory/Integral/Average.lean; the recorded mathlib_file is the primary home of the Jensen theorems.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../definitions/probability-measure.md)
- [Convex functions on a set](../../convex-analysis-and-normed-space-geometry/definitions/convex-functions-on-a-set.md)
- [Finite convex combinations in convex sets](../../convex-analysis-and-normed-space-geometry/theorems/finite-convex-combinations-in-convex-sets.md)
