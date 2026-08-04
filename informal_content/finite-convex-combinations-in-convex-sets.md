# Finite convex combinations in convex sets

Let `R` be a field and let `E` be an additive commutative group and an `R`-module. For a finite index set `t`, weights `w`, and points `z`, Mathlib defines

`centerMass t w z = (sum i in t, w i)^(-1) • (sum i in t, w i • z i)`.

The definition requires no order, sign condition, or normalization of the weights. For its convex-closure theorem, additionally let `R` carry a linear order and a strict ordered-ring structure, and let `s` be convex over `R`. If every weight indexed by `t` is nonnegative, their sum is positive, and every indexed point belongs to `s`, then `centerMass t w z` belongs to `s`. In particular, when the weights sum to one, the unnormalized weighted sum belongs to `s`:

`sum i in t, w i • z i ∈ s`.

The index type may be arbitrary; only the explicit finite set `t` matters. Values outside `t` are unrestricted, while membership is required at every index in `t`, including indices whose weight is zero.

## Mathlib

Declarations: `Finset.centerMass`, `Convex.centerMass_mem`, `Convex.sum_mem`
File: `Mathlib/Analysis/Convex/Combination.lean`
