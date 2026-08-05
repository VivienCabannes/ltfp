---
kind: node
declaration: theorem
mathlib: true
---

# Parallelogram and Pythagorean identities

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`, the parallelogram identity is

`||x + y|| ||x + y|| + ||x - y|| ||x - y|| = 2 (||x|| ||x|| + ||y|| ||y||)`.

If `<x, y>_K = 0`, the Pythagorean identity is

`||x + y|| ||x + y|| = ||x|| ||x|| + ||y|| ||y||`.

The cited Mathlib declarations use products of norms rather than powers. They are equivalent to the familiar squared-norm formulas, and they require neither norm separation nor completeness. Orthogonality in the reverse inner-product orientation suffices by conjugate symmetry.

## Mathlib

Declarations: `parallelogram_law_with_norm_mul`, `norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Basic.lean`.

Verified in the pinned checkout for seminormed RCLike inner-product spaces. parallelogram_law_with_norm_mul takes the scalar K explicitly and states the norm-product form used by the complete-convex minimizer proof. The Pythagorean declaration takes the directed premise inner K x y = 0 and also states products of norms; reverse orthogonality suffices by conjugate symmetry. It is used to bound projection onto a subspace along its orthogonal complement and establish continuity. Neither result requires norm separation or completeness.

## Depends on

This node has no prerequisites.
