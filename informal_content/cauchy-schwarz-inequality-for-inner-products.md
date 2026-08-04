# Cauchy-Schwarz inequality for inner products

Let `K` be an `RCLike` scalar field and let `E` be a seminormed inner-product space over `K`. For all `x, y : E`,

`||<x, y>_K|| <= ||x|| ||y||`.

Mathlib takes the inner product to be conjugate-linear in `x` and linear in `y`. The inequality requires neither norm separation nor completeness.

## Mathlib

Declarations: `norm_inner_le_norm`
File: `Mathlib/Analysis/InnerProductSpace/Basic.lean`
