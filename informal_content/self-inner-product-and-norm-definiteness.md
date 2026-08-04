# Self-inner-product and norm definiteness

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For every `x : E`,

`<x, x>_K = (||x|| : K)^2`.

If the seminorm on `E` is a norm, this identity detects zero vectors:

`<x, x>_K = 0` if and only if `x = 0`,

and equivalently `<x, x>_K != 0` if and only if `x != 0`. The first identity needs no norm separation, while the two equivalences do. None of the statements requires completeness or a separate nontriviality assumption.

## Mathlib

Declarations: `inner_self_eq_norm_sq_to_K`, `inner_self_eq_zero`, `inner_self_ne_zero`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`
