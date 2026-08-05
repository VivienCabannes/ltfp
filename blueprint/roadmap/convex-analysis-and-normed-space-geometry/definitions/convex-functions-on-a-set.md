---
kind: node
declaration: definition
mathlib: true
---

# Convex functions on a set

Let `R` be a semiring with a partial order, let `E` and `B` be additive commutative monoids with scalar actions by `R`, and let `B` carry a partial order. For a set `s` in `E` and a function `f : E -> B`, the predicate `ConvexOn R s f` says that `s` is convex and, whenever `x, y` belong to `s` and `a, b : R` are nonnegative with `a + b = 1`,

`f (a • x + b • y) <= a • f x + b • f y`.

The definition itself requires no module laws or compatibility between the scalar action and either order.

## Mathlib

Declarations: `ConvexOn`
File: `Mathlib/Analysis/Convex/Function.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Function.lean`.

Verified in the pinned checkout. ConvexOn assumes Semiring R, PartialOrder R, AddCommMonoid E, AddCommMonoid B, PartialOrder B, SMul R E, and SMul R B. It bundles Convex R s with the nonnegative two-point inequality. The definition requires no module laws, ordered-semiring compatibility, topology, norm, or completeness. Its only foundation dependency here is Convex sets.

## Depends on

- [Convex sets](convex-sets.md)
