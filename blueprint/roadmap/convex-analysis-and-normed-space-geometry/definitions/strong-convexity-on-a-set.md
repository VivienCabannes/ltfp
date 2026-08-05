---
kind: node
declaration: definition
mathlib: true
---

# Strong convexity on a set

Let `E` be a real normed vector space, let `s` be a set in `E`, let `m` be a real number, and let `f : E -> Real`. The predicate `StrongConvexOn s m f` is defined as `UniformConvexOn s (fun r => (m / 2) * r^2) f`. Equivalently, `s` is convex and, for `x, y` in `s` and nonnegative `a, b` with `a + b = 1`,

`f (a • x + b • y) <= a * f x + b * f y - a * b * (m / 2) * ||x - y||^2`.

This definition is meaningful for every real modulus; the usual strong-convexity regime has `m > 0`.

## Mathlib

Declarations: `StrongConvexOn`, `UniformConvexOn`
File: `Mathlib/Analysis/Convex/Strong.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Strong.lean`.

Verified in the pinned checkout. StrongConvexOn is defined for a real normed space and a real-valued function, with no completeness, inner-product, or sign assumption on the real modulus m. It is definitionally UniformConvexOn s (fun r => m / 2 * r^2) f and bundles Convex Real s with the nonnegative two-point inequality whose correction term is a * b * (m / 2) * norm(x - y)^2. The definition does not use ConvexOn directly; ordinary and strict convexity consequences require the usual sign hypotheses.

## Depends on

- [Convex sets](convex-sets.md)
