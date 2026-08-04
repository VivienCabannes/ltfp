# Jensen's inequality on the real line

Let `mu` be a probability measure, let `X : Omega -> Real` be integrable, and let `F : Real -> Real` be convex on all of `Real`. Suppose `F composed with X` is integrable. Then

`F (integral omega, X omega dmu)`

`<= integral omega, F (X omega) dmu`.

A finite real-valued convex function on the whole real line is continuous, so no separate continuity hypothesis is needed in this scalar specialization. This result is the one-dimensional specialization of the existing integral Jensen inequality, with the closed convex domain chosen to be `Set.univ`.

## Mathlib

Declarations: `ConvexOn.map_integral_le`, `ConvexOn.continuousOn`
File: `Mathlib/Analysis/Convex/Integral.lean`
