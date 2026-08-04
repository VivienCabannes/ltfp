# Parallelogram and Pythagorean identities

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`, the parallelogram identity is

`||x + y|| ||x + y|| + ||x - y|| ||x - y|| = 2 (||x|| ||x|| + ||y|| ||y||)`.

If `<x, y>_K = 0`, the Pythagorean identity is

`||x + y|| ||x + y|| = ||x|| ||x|| + ||y|| ||y||`.

The cited Mathlib declarations use products of norms rather than powers. They are equivalent to the familiar squared-norm formulas, and they require neither norm separation nor completeness. Orthogonality in the reverse inner-product orientation suffices by conjugate symmetry.

## Mathlib

Declarations: `parallelogram_law_with_norm_mul`, `norm_add_sq_eq_norm_sq_add_norm_sq_of_inner_eq_zero`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`
