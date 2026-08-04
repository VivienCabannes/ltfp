# Rolle's theorem for real derivatives

Let `f : Real -> Real`, let `a < b`, suppose `f` is continuous on `Set.Icc a b`, and suppose `f a = f b`. If a function `f'` is a derivative of `f` at every point of `Set.Ioo a b`, then there exists `c` in that open interval such that

`f' c = 0`.

Mathlib also provides a version stated with the totalized `deriv f`. That version needs no explicit differentiability hypothesis because `deriv f c` is defined to be zero when `f` is not differentiable at `c`. Proofs that need a genuine derivative value should use the `HasDerivAt` version and supply the interior derivative hypotheses.

## Mathlib

Declarations: `exists_hasDerivAt_eq_zero`, `exists_deriv_eq_zero`
File: `Mathlib/Analysis/Calculus/LocalExtr/Rolle.lean`
