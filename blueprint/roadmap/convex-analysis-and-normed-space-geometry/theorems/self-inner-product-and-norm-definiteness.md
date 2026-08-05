---
kind: node
declaration: theorem
mathlib: true
---

# Self-inner-product and norm definiteness

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For every `x : E`,

`<x, x>_K = (||x|| : K)^2`.

If the seminorm on `E` is a norm, this identity detects zero vectors:

`<x, x>_K = 0` if and only if `x = 0`,

and equivalently `<x, x>_K != 0` if and only if `x != 0`. The first identity needs no norm separation, while the two equivalences do. None of the statements requires completeness or a separate nontriviality assumption.

## Mathlib

Declarations: `inner_self_eq_norm_sq_to_K`, `inner_self_eq_zero`, `inner_self_ne_zero`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Basic.lean`.

Verified in the pinned checkout. For an RCLike scalar field and a seminormed inner-product space, inner_self_eq_norm_sq_to_K states that the self-inner-product is the square in K of the coerced norm, (norm x : K) ^ 2. The equivalences inner_self_eq_zero and inner_self_ne_zero require NormedAddCommGroup, exactly where norm separation is needed. The norm-functional proof uses the squared-norm identity, orthogonal-projection uniqueness uses the zero equivalence, and Frechet-Riesz surjectivity uses the nonzero equivalence. No completeness or separate Nontrivial assumption is required.

## Depends on

This node has no prerequisites.
