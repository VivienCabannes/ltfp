---
kind: node
declaration: theorem
mathlib: true
---

# Cauchy-Schwarz inequality for inner products

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`,

`||<x, y>_K|| <= ||x|| ||y||`.

Mathlib takes the inner product to be conjugate-linear in `x` and linear in `y`. The inequality requires neither norm separation nor completeness.

## Mathlib

Declarations: `norm_inner_le_norm`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Basic.lean`.

Verified in the pinned checkout. Under RCLike scalars, SeminormedAddCommGroup E, and InnerProductSpace K E, norm_inner_le_norm states norm (inner K x y) <= norm x * norm y. It requires neither completeness nor norm separation. Mathlib uses it to construct innerSL as a continuous map and for the upper operator-norm bound in innerSL_apply_norm.

## Depends on

This node has no prerequisites.
