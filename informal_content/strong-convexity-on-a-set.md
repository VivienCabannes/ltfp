# Strong convexity on a set

Let `E` be a real normed vector space, let `s` be a set in `E`, let `m` be a real number, and let `f : E -> Real`. The predicate `StrongConvexOn s m f` is defined as `UniformConvexOn s (fun r => (m / 2) * r^2) f`. Equivalently, `s` is convex and, for `x, y` in `s` and nonnegative `a, b` with `a + b = 1`,

`f (a • x + b • y) <= a * f x + b * f y - a * b * (m / 2) * ||x - y||^2`.

This definition is meaningful for every real modulus; the usual strong-convexity regime has `m > 0`.

## Mathlib

Declarations: `StrongConvexOn`, `UniformConvexOn`
File: `Mathlib/Analysis/Convex/Strong.lean`
