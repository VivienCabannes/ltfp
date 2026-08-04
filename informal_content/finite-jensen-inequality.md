# Finite Jensen inequality

Let `K` be a strict linearly ordered field, let `E` be a `K`-module, and let `B` be a partially ordered `K`-module with ordered addition and strictly ordered scalar multiplication. Suppose `f : E -> B` is convex on `s`. For a finite set of indices `t`, assume `0 <= w i` and `p i` belongs to `s` for every `i` in `t`, and that `sum i in t, w i = 1`. Then

`f (sum i in t, w i • p i) <= sum i in t, w i • f (p i)`.

No finite-type structure on the ambient index and no condition on weights outside `t` is required.

## Mathlib

Declarations: `ConvexOn.map_sum_le`
File: `Mathlib/Analysis/Convex/Jensen.lean`
