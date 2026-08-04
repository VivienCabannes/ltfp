# Norm of the inner product functional

Let `K` be an `RCLike` scalar field, let `E` be a seminormed additive commutative group with an `InnerProductSpace K E` structure, and let `x : E`. The continuous functional `y |-> <x, y>` has operator norm exactly `||x||`:

`||innerSL K x|| = ||x||`.

No completeness, nontriviality, or norm-separation assumption on `E` is required. This theorem concerns the functional obtained after applying `innerSL` to `x`, not the norm of the whole outer conjugate-linear map.

## Mathlib

Declarations: `innerSL_apply_norm`
File: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`
