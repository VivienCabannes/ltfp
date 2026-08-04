# Frechet-Riesz representation theorem

Let `K` be an `RCLike` scalar field and let `E` be a complete normed inner product space over `K`. The isometric Riesz embedding is surjective and therefore gives a conjugate-linear isometric equivalence

`InnerProductSpace.toDual K E : E ≃ₗᵢ⋆[K] StrongDual K E`.

Consequently, for every continuous linear functional `ell` on `E`, there is a unique `x : E` such that `ell y = <x, y>` for every `y : E`, and `||ell|| = ||x||`. No `Nontrivial E` assumption is required.

The representative is `(InnerProductSpace.toDual K E).symm ell`. Uniqueness and the norm identity follow from the generic injectivity and norm-preservation APIs of the equivalence; they are not separate named Riesz declarations.

## Mathlib

Declarations: `InnerProductSpace.toDual`, `InnerProductSpace.toDual_apply_apply`, `InnerProductSpace.toDual_symm_apply`, `InnerProductSpace.toLinearIsometry_toDual`, `InnerProductSpace.toDual_apply_eq_toDualMap_apply`
File: `Mathlib/Analysis/InnerProductSpace/Dual.lean`
