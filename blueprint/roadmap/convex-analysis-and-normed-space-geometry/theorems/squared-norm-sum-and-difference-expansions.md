---
kind: node
declaration: theorem
mathlib: true
---

# Squared-norm sum and difference expansions

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`,

`||x + y||^2 = ||x||^2 + 2 Re(<x, y>_K) + ||y||^2`,

`||x - y||^2 = ||x||^2 - 2 Re(<x, y>_K) + ||y||^2`.

For a real inner-product space, the real-part terms reduce to the real inner product itself. These identities need neither norm separation nor completeness.

## Mathlib

Declarations: `norm_add_sq`, `norm_add_sq_real`, `norm_sub_sq`, `norm_sub_sq_real`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Basic.lean`.

Verified in the pinned checkout for seminormed RCLike inner-product spaces. norm_add_sq and norm_sub_sq use RCLike.re of inner K x y; norm_add_sq_real and norm_sub_sq_real are the corresponding real-scalar formulas. All four statements use powers ^ 2 and require neither norm separation nor completeness. strongConvexOn_iff_convex uses the real formulas through its auxiliary calculation, while norm_eq_iInf_iff_real_inner_le_zero directly uses norm_sub_sq.

## Depends on

This node has no prerequisites.
