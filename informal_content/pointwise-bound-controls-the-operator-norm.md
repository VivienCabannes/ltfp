# Pointwise bound controls the operator norm

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L`, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. Let `C` be nonnegative. If

`||f x|| <= C * ||x||`

for every `x : E`, then `||f|| <= C`.

The scalar homomorphism need not preserve norms. The theorem allows `C = 0` and subsingleton domain or codomain spaces, and requires no completeness or norm-separation hypothesis.

## Mathlib

Declarations: `ContinuousLinearMap.opNorm_le_bound`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`
