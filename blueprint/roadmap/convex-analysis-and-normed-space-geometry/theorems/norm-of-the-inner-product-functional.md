---
kind: node
declaration: theorem
mathlib: true
---

# Norm of the inner product functional

Let `K` be an `RCLike` scalar field, let `E` be a seminormed additive commutative group with an `InnerProductSpace K E` structure, and let `x : E`. The continuous functional `y |-> <x, y>` has operator norm exactly `||x||`:

`||innerSL K x|| = ||x||`.

No completeness, nontriviality, or norm-separation assumption on `E` is required. This theorem concerns the functional obtained after applying `innerSL` to `x`, not the norm of the whole outer conjugate-linear map.

## Mathlib

Declarations: `innerSL_apply_norm`
File: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`.

Verified in the pinned checkout. For an RCLike field K, a seminormed additive commutative group E, InnerProductSpace K E, and x : E, innerSL_apply_norm states norm (innerSL K x) = norm x. No CompleteSpace, Nontrivial, or NormedAddCommGroup assumption is required. The argument order is conjugate-linear in x and linear in the functional argument. This is distinct from InnerProductSpace.innerSL_norm, which concerns the whole outer map and has stronger assumptions. Its proof explicitly invokes opNorm_le_bound, le_opNorm, norm_inner_le_norm, and inner_self_eq_norm_sq_to_K, and the graph records those proof dependencies.

## Depends on

- [Inner product as a continuous sesquilinear map](../definitions/inner-product-as-a-continuous-sesquilinear-map.md)
- [Operator norm of a continuous linear map](../definitions/operator-norm-of-a-continuous-linear-map.md)
- [Pointwise bound controls the operator norm](pointwise-bound-controls-the-operator-norm.md)
- [Operator norm controls evaluation](operator-norm-controls-evaluation.md)
- [Self-inner-product and norm definiteness](self-inner-product-and-norm-definiteness.md)
- [Cauchy-Schwarz inequality for inner products](cauchy-schwarz-inequality-for-inner-products.md)
