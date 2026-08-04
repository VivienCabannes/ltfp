# Operator norm of a continuous linear map

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L`, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. Its operator norm is the infimum of the nonnegative constants `C` such that

`||f x|| <= C * ||x||`

for every `x : E`. This quantity is installed as the norm of `f`, so `||f||` is definitionally `ContinuousLinearMap.opNorm f`.

The definition itself does not require `sigma` to preserve norms. That isometry assumption is needed later to prove that continuity supplies a global bound and hence that this infimum has the expected evaluation property.

## Mathlib

Declarations: `ContinuousLinearMap.opNorm`, `ContinuousLinearMap.hasOpNorm`, `ContinuousLinearMap.norm_def`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`
