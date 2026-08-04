# Inner product as a continuous sesquilinear map

Let `K` be an `RCLike` scalar field, let `E` be a seminormed additive commutative group, and equip `E` with an `InnerProductSpace K E` structure. The assignment

`x |-> (y |-> <x, y>)`

is a continuous conjugate-linear map from `E` to its strong dual, bundled as

`innerSL K : E →L⋆[K] (E →L[K] K)`.

Its value satisfies `innerSL K x y = <x, y>`. Thus the outer argument is conjugate-linear and the inner argument is linear. Over `Real` the conjugation is trivial; over `Complex` it is genuine. No completeness, norm-separation, finite-dimensionality, or nontriviality assumption on `E` is required.

## Mathlib

Declarations: `innerSL`, `coe_innerSL_apply`, `innerSL_apply_apply`
File: `Mathlib/Analysis/InnerProductSpace/LinearMap.lean`
