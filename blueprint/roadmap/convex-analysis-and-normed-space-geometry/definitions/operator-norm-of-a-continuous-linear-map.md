---
kind: node
declaration: definition
mathlib: true
---

# Operator norm of a continuous linear map

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L`, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. Its operator norm is the infimum of the nonnegative constants `C` such that

`||f x|| <= C * ||x||`

for every `x : E`. This quantity is installed as the norm of `f`, so `||f||` is definitionally `ContinuousLinearMap.opNorm f`.

The definition itself does not require `sigma` to preserve norms. That isometry assumption is needed later to prove that continuity supplies a global bound and hence that this infimum has the expected evaluation property.

## Mathlib

Declarations: `ContinuousLinearMap.opNorm`, `ContinuousLinearMap.hasOpNorm`, `ContinuousLinearMap.norm_def`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Normed/Operator/Basic.lean`.

Verified in the pinned checkout. ContinuousLinearMap.opNorm is a namespace definition, not a structure field or protected definition. For seminormed additive commutative groups over nontrivially normed fields and a ring homomorphism sigma, it is the infimum of nonnegative constants giving a global pointwise norm bound. Neither opNorm, hasOpNorm, nor norm_def requires RingHomIsometric sigma; norm_def identifies the installed norm definitionally with opNorm. Isometry is needed only for downstream existence, least-bound, evaluation, and seminorm-structure results. Norm separation is unnecessary.

## Depends on

- [Continuous linear maps](continuous-linear-maps.md)
