# Operator norm controls evaluation

Let `K` and `L` be nontrivially normed fields, let `sigma : K ->+* L` preserve norms, and let `f : E ->SL[sigma] F` be a continuous semilinear map between seminormed spaces over those fields. For every `x : E`,

`||f x|| <= ||f|| * ||x||`.

For an ordinary continuous linear map `f : E ->L[K] F`, the scalar homomorphism is the identity and its isometry condition is automatic. No completeness or norm-separation hypothesis is required.

## Mathlib

Declarations: `ContinuousLinearMap.le_opNorm`
File: `Mathlib/Analysis/Normed/Operator/Basic.lean`
