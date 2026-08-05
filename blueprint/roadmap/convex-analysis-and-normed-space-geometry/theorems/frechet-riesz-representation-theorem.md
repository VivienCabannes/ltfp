---
kind: node
declaration: theorem
mathlib: true
---

# Frechet-Riesz representation theorem

Let `K` be an `RCLike` scalar field and let `E` be a complete normed inner product space over `K`. The isometric Riesz embedding is surjective and therefore gives a conjugate-linear isometric equivalence

`InnerProductSpace.toDual K E : E ≃ₗᵢ⋆[K] StrongDual K E`.

Consequently, for every continuous linear functional `ell` on `E`, there is a unique `x : E` such that `ell y = <x, y>` for every `y : E`, and `||ell|| = ||x||`. No `Nontrivial E` assumption is required.

The representative is `(InnerProductSpace.toDual K E).symm ell`. Uniqueness and the norm identity follow from the generic injectivity and norm-preservation APIs of the equivalence; they are not separate named Riesz declarations.

## Mathlib

Declarations: `InnerProductSpace.toDual`, `InnerProductSpace.toDual_apply_apply`, `InnerProductSpace.toDual_symm_apply`, `InnerProductSpace.toLinearIsometry_toDual`, `InnerProductSpace.toDual_apply_eq_toDualMap_apply`
File: `Mathlib/Analysis/InnerProductSpace/Dual.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Dual.lean`.

Verified in the pinned checkout. For an RCLike field K, NormedAddCommGroup E, InnerProductSpace K E, and CompleteSpace E, InnerProductSpace.toDual K E has type E equivalent conjugate-linearly and isometrically to StrongDual K E. It is built from toDualMap by surjectivity; Mathlib proves surjectivity using orthogonal-projection machinery for the kernel of a functional. toDual_symm_apply identifies the representing vector. Uniqueness and norm equality are generic consequences of equivalence injectivity and norm_map rather than separate named Riesz theorems. No Nontrivial E assumption is required.

## Depends on

- [Isometric Riesz embedding](../definitions/isometric-riesz-embedding.md)
- [Orthogonal projection onto a closed subspace](orthogonal-projection-onto-a-closed-subspace.md)
- [Self-inner-product and norm definiteness](self-inner-product-and-norm-definiteness.md)
