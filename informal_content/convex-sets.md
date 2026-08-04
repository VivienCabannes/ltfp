# Convex sets

Let `R` carry a semiring structure and a separate partial order, let `E` be an additive commutative monoid with an `R`-scalar action, and let `s` be a subset of `E`. The set `s` is convex over `R` when, for every `x` and `y` in `s` and all nonnegative `a, b : R` with `a + b = 1`, the point `a • x + b • y` belongs to `s`.

Equivalently, `s` contains the segment between each pair of its points. Empty and universal sets are convex under these weak assumptions; singleton and general subsingleton convexity use a module structure.

When `R` is also a linearly ordered field with a strict ordered-ring structure and `E` is an additive commutative group and an `R`-module, the same condition has a normalized form. For nonnegative `a` and `b` with `0 < a + b`, convexity is equivalent to membership of

`(a / (a + b)) • x + (b / (a + b)) • y`.

This is the two-point normalization used in the finite center-of-mass argument.

## Mathlib

Declarations: `Convex`, `Convex.starConvex`, `convex_iff_add_mem`, `convex_iff_div`, `convex_iff_segment_subset`, `Convex.segment_subset`, `Convex.openSegment_subset`, `convex_iff_pointwise_add_subset`, `Convex.set_combo_subset`, `convex_empty`, `convex_univ`, `Set.Subsingleton.convex`, `convex_singleton`
File: `Mathlib/Analysis/Convex/Basic.lean`
