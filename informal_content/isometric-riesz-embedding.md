# Isometric Riesz embedding

Let `K` be an `RCLike` scalar field and let `E` be a normed inner product space over `K`. The map sending `x : E` to the continuous functional `y |-> <x, y>` is the conjugate-linear isometric embedding

`InnerProductSpace.toDualMap K E : E →ₗᵢ⋆[K] StrongDual K E`.

Completeness is not needed for this embedding; it is needed only for surjectivity.

The same declaration is available for a seminormed inner product space and remains norm-preserving there. Norm separation makes it injective and hence an embedding in the usual sense.

## Mathlib

Declarations: `InnerProductSpace.toDualMap`, `InnerProductSpace.toDualMap_apply_apply`, `InnerProductSpace.toContinuousLinearMap_toDualMap`
File: `Mathlib/Analysis/InnerProductSpace/Dual.lean`
