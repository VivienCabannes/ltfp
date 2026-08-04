# Convex functions on a set

Let `R` be a semiring with a partial order, let `E` and `B` be additive commutative monoids with scalar actions by `R`, and let `B` carry a partial order. For a set `s` in `E` and a function `f : E -> B`, the predicate `ConvexOn R s f` says that `s` is convex and, whenever `x, y` belong to `s` and `a, b : R` are nonnegative with `a + b = 1`,

`f (a • x + b • y) <= a • f x + b • f y`.

The definition itself requires no module laws or compatibility between the scalar action and either order.

## Mathlib

Declarations: `ConvexOn`
File: `Mathlib/Analysis/Convex/Function.lean`
