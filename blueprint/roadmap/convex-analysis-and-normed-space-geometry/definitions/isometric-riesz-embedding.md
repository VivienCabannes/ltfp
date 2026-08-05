---
kind: node
declaration: definition
mathlib: true
---

# Isometric Riesz embedding

Let `K` be an `RCLike` scalar field and let `E` be a normed inner product space over `K`. The map sending `x : E` to the continuous functional `y |-> <x, y>` is the conjugate-linear isometric embedding

`InnerProductSpace.toDualMap K E : E →ₗᵢ⋆[K] StrongDual K E`.

Completeness is not needed for this embedding; it is needed only for surjectivity.

The same declaration is available for a seminormed inner product space and remains norm-preserving there. Norm separation makes it injective and hence an embedding in the usual sense.

## Mathlib

Declarations: `InnerProductSpace.toDualMap`, `InnerProductSpace.toDualMap_apply_apply`, `InnerProductSpace.toContinuousLinearMap_toDualMap`
File: `Mathlib/Analysis/InnerProductSpace/Dual.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Dual.lean`.

Verified in the pinned checkout. For an RCLike field K, a seminormed additive commutative group E, and InnerProductSpace K E, toDualMap is the conjugate-linear norm-preserving map x |-> (y |-> inner K x y) into StrongDual K E. It is built from innerSL and innerSL_apply_norm. When E is a normed additive commutative group, norm preservation gives injectivity and the usual isometric embedding. No completeness is required; completeness enters only for InnerProductSpace.toDual and its surjectivity. The StrongDual codomain is definitionally E ->L[K] K.

## Depends on

- [Norm of the inner product functional](../theorems/norm-of-the-inner-product-functional.md)
- [Strong dual space](strong-dual-space.md)
- [Inner product as a continuous sesquilinear map](inner-product-as-a-continuous-sesquilinear-map.md)
