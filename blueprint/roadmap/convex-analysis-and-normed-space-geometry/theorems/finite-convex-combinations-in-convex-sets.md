---
kind: node
declaration: theorem
mathlib: true
---

# Finite convex combinations in convex sets

Let `R` be a field and let `E` be an additive commutative group and an `R`-module. For a finite index set `t`, weights `w`, and points `z`, Mathlib defines

`centerMass t w z = (sum i in t, w i)^(-1) • (sum i in t, w i • z i)`.

The definition requires no order, sign condition, or normalization of the weights. For its convex-closure theorem, additionally let `R` carry a linear order and a strict ordered-ring structure, and let `s` be convex over `R`. If every weight indexed by `t` is nonnegative, their sum is positive, and every indexed point belongs to `s`, then `centerMass t w z` belongs to `s`. In particular, when the weights sum to one, the unnormalized weighted sum belongs to `s`:

`sum i in t, w i • z i ∈ s`.

The index type may be arbitrary; only the explicit finite set `t` matters. Values outside `t` are unrestricted, while membership is required at every index in `t`, including indices whose weight is zero.

## Mathlib

Declarations: `Finset.centerMass`, `Convex.centerMass_mem`, `Convex.sum_mem`
File: `Mathlib/Analysis/Convex/Combination.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Combination.lean`.

Verified in the pinned checkout. Finset.centerMass is the inverse total weight acting on the weighted finite sum and itself requires only a field, an additive commutative group, and a module. Under a linear order and strict ordered-ring structure, Convex.centerMass_mem assumes nonnegative weights on the explicit Finset, positive total mass, and membership of every indexed point. Convex.sum_mem specializes to total weight one and concludes membership of the raw weighted sum. The index type is arbitrary, values outside the Finset are irrelevant, and no topology, norm, completeness, finite-dimensionality, Fintype, or global finite-support assumption is required.

## Depends on

- [Convex sets](../definitions/convex-sets.md)
