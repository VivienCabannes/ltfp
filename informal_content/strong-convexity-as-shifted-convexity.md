# Strong convexity as shifted convexity

Let `E` be a real inner product space, let `s` be a set in `E`, let `m` be an arbitrary real number, and let `f : E -> Real`. Then `f` is `m`-strongly convex on `s` if and only if the function

`x |-> f x - (m / 2) * ||x||^2`

is `ConvexOn Real s`.

No positivity assumption on `m`, separate convexity assumption on `s`, or completeness assumption on `E` is required.

## Mathlib

Declarations: `strongConvexOn_iff_convex`
File: `Mathlib/Analysis/Convex/Strong.lean`
