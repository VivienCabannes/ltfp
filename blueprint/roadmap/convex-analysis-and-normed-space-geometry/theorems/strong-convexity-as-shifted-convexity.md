---
kind: node
declaration: theorem
mathlib: true
---

# Strong convexity as shifted convexity

Let `E` be a real inner product space, let `s` be a set in `E`, let `m` be an arbitrary real number, and let `f : E -> Real`. Then `f` is `m`-strongly convex on `s` if and only if the function

`x |-> f x - (m / 2) * ||x||^2`

is `ConvexOn Real s`.

No positivity assumption on `m`, separate convexity assumption on `s`, or completeness assumption on `E` is required.

## Mathlib

Declarations: `strongConvexOn_iff_convex`
File: `Mathlib/Analysis/Convex/Strong.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Strong.lean`.

Verified in the pinned checkout. For a real inner-product space, arbitrary set s, arbitrary real modulus m, and f : E -> Real, strongConvexOn_iff_convex states that StrongConvexOn s m f is equivalent to ConvexOn Real s (fun x => f x - m / 2 * norm x ^ 2). No positivity, separate convex-set, or completeness premise is required.

## Depends on

- [Convex functions on a set](../definitions/convex-functions-on-a-set.md)
- [Strong convexity on a set](../definitions/strong-convexity-on-a-set.md)
- [Squared-norm sum and difference expansions](squared-norm-sum-and-difference-expansions.md)
