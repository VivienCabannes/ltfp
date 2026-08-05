---
kind: node
declaration: definition
mathlib: true
---

# Convex sets

Let `R` carry a semiring structure and a separate partial order, let `E` be an additive commutative monoid with an `R`-scalar action, and let `s` be a subset of `E`. The set `s` is convex over `R` when, for every `x` and `y` in `s` and all nonnegative `a, b : R` with `a + b = 1`, the point `a • x + b • y` belongs to `s`.

Equivalently, `s` contains the segment between each pair of its points. Empty and universal sets are convex under these weak assumptions; singleton and general subsingleton convexity use a module structure.

When `R` is also a linearly ordered field with a strict ordered-ring structure and `E` is an additive commutative group and an `R`-module, the same condition has a normalized form. For nonnegative `a` and `b` with `0 < a + b`, convexity is equivalent to membership of

`(a / (a + b)) • x + (b / (a + b)) • y`.

This is the two-point normalization used in the finite center-of-mass argument.

## Mathlib

Declarations: `Convex`, `Convex.starConvex`, `convex_iff_add_mem`, `convex_iff_div`, `convex_iff_segment_subset`, `Convex.segment_subset`, `Convex.openSegment_subset`, `convex_iff_pointwise_add_subset`, `Convex.set_combo_subset`, `convex_empty`, `convex_univ`, `Set.Subsingleton.convex`, `convex_singleton`
File: `Mathlib/Analysis/Convex/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Basic.lean`.

Verified in the pinned checkout. The minimal assumptions for Convex, the two-point and segment equivalences, and segment closure are Semiring R, PartialOrder R, AddCommMonoid E, and SMul R E, with no module, ordered-semiring compatibility, topology, norm, or real-scalar assumption. Convex is defined through StarConvex; convex_iff_add_mem gives the nonnegative two-point formula, convex_iff_div supplies the normalized division form used by finite centers of mass, and convex_iff_segment_subset gives segment closure. Empty and universal sets use the same weak assumptions, while singleton and subsingleton convexity require Module R E. The distinct Convexity.IsConvexSet API is not substituted because downstream Analysis/Convex declarations use Convex.

## Depends on

This node has no prerequisites.
