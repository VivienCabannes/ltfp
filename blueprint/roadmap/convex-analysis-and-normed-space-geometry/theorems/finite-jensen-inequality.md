---
kind: node
declaration: theorem
mathlib: true
---

# Finite Jensen inequality

Let `K` be a strict linearly ordered field, let `E` be a `K`-module, and let `B` be a partially ordered `K`-module with ordered addition and strictly ordered scalar multiplication. Suppose `f : E -> B` is convex on `s`. For a finite set of indices `t`, assume `0 <= w i` and `p i` belongs to `s` for every `i` in `t`, and that `sum i in t, w i = 1`. Then

`f (sum i in t, w i • p i) <= sum i in t, w i • f (p i)`.

No finite-type structure on the ambient index and no condition on weights outside `t` is required.

## Mathlib

Declarations: `ConvexOn.map_sum_le`
File: `Mathlib/Analysis/Convex/Jensen.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Convex/Jensen.lean`.

Verified in the pinned checkout. For a field with a linear order and strict ordered-ring structure, module domains and codomains, and a partially ordered codomain whose addition and scalar multiplication respect order, ConvexOn.map_sum_le uses an arbitrary finite index set t. It assumes nonnegative weights on t, sum one on t, and membership of all indexed points in the convex domain, then gives the weighted-sum inequality. There is no Fintype, continuity, completeness, separate convex-set, or finite-support hypothesis; weights outside t are unrestricted.

## Depends on

- [Convex functions on a set](../definitions/convex-functions-on-a-set.md)
- [Finite convex combinations in convex sets](finite-convex-combinations-in-convex-sets.md)
