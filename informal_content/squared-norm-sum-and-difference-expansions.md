# Squared-norm sum and difference expansions

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`,

`||x + y||^2 = ||x||^2 + 2 Re(<x, y>_K) + ||y||^2`,

`||x - y||^2 = ||x||^2 - 2 Re(<x, y>_K) + ||y||^2`.

For a real inner-product space, the real-part terms reduce to the real inner product itself. These identities need neither norm separation nor completeness.

## Mathlib

Declarations: `norm_add_sq`, `norm_add_sq_real`, `norm_sub_sq`, `norm_sub_sq_real`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`
