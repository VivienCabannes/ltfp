---
kind: node
declaration: theorem
mathlib: true
---

# Pointwise bound controls the operator norm

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L`, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. Let `C` be nonnegative. If

`||f x|| <= C * ||x||`

for every `x : E`, then `||f|| <= C`.

The scalar homomorphism need not preserve norms. The theorem allows `C = 0` and subsingleton domain or codomain spaces, and requires no completeness or norm-separation hypothesis.

## Mathlib

Declarations: `ContinuousLinearMap.opNorm_le_bound`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Normed/Operator/Basic.lean`.

Verified in the pinned checkout. ContinuousLinearMap.opNorm_le_bound holds for continuous semilinear maps between seminormed additive commutative groups over nontrivially normed fields, with normed-space scalar structures and an arbitrary scalar ring homomorphism. It requires 0 <= M and a pointwise bound norm (f x) <= M * norm x, and concludes norm f <= M. RingHomIsometric is not required; M = 0 and subsingleton spaces are allowed. There is no completeness or norm-separation assumption.

## Depends on

- [Operator norm of a continuous linear map](../definitions/operator-norm-of-a-continuous-linear-map.md)
