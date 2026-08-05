---
kind: node
declaration: theorem
mathlib: true
---

# Operator norm controls evaluation

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L` preserve norms, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. For every `x : E`,

`||f x|| <= ||f|| * ||x||`.

For an ordinary continuous linear map `f : E ->L[K] F`, the scalar homomorphism is the identity and its isometry condition is automatic. No completeness or norm-separation hypothesis is required.

## Mathlib

Declarations: `ContinuousLinearMap.le_opNorm`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Normed/Operator/Basic.lean`.

Verified in the pinned checkout. ContinuousLinearMap.le_opNorm applies to continuous semilinear maps between seminormed additive commutative groups over nontrivially normed fields, with normed-space structures and RingHomIsometric sigma. It states norm (f x) <= norm f * norm x. For ordinary continuous linear maps the identity scalar homomorphism is automatically isometric. No completeness or norm-separation assumption is required. The installed norm is definitionally opNorm; similarly named ContinuousMap and BoundedContinuousFunction results are unrelated.

## Depends on

- [Operator norm of a continuous linear map](../definitions/operator-norm-of-a-continuous-linear-map.md)
