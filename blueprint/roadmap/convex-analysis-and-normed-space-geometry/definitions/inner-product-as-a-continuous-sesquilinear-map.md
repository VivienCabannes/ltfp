---
kind: node
declaration: definition
mathlib: true
---

# Inner product as a continuous sesquilinear map

Let `K` be an `RCLike` scalar field, let `E` be a seminormed additive commutative group, and equip `E` with an `InnerProductSpace K E` structure. The assignment

`x |-> (y |-> <x, y>)`

is a continuous conjugate-linear map from `E` to its strong dual, bundled as

`innerSL K : E →L⋆[K] (E →L[K] K)`.

Its value satisfies `innerSL K x y = <x, y>`. Thus the outer argument is conjugate-linear and the inner argument is linear. Over `Real` the conjugation is trivial; over `Complex` it is genuine. No completeness, norm-separation, finite-dimensionality, or nontriviality assumption on `E` is required.

## Mathlib

Declarations: `innerSL`, `coe_innerSL_apply`, `innerSL_apply_apply`
File: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`.

Verified in the pinned checkout. For an RCLike field K, a seminormed additive commutative group E, and InnerProductSpace K E, innerSL K has type E ->L*[K] (E ->L[K] K), whose codomain is definitionally StrongDual K E. It sends x and y to inner K x y. The outer map is semilinear over starRingEnd K and hence conjugate-linear, while each inner functional is K-linear. Over Real the star is trivial; over Complex it is genuine. No completeness, finite-dimensionality, or nontriviality assumption on E is required.

## Depends on

- [Continuous linear maps](continuous-linear-maps.md)
- [Strong dual space](strong-dual-space.md)
- [Cauchy-Schwarz inequality for inner products](../theorems/cauchy-schwarz-inequality-for-inner-products.md)
