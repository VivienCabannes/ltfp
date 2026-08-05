---
kind: node
declaration: theorem
mathlib: true
---

# Hilbert projection theorem for complete convex sets

Let `E` be a real inner product space, let `C` be a nonempty complete convex subset of `E`, and let `u : E`. There exists `v` in `C` such that

`||u - v|| = iInf (fun w : C => ||u - w||)`.

Thus the distance from `u` to `C` is attained without requiring the ambient space itself to be complete.

The theorem asserts existence of a minimizer. Uniqueness is not part of this declaration's conclusion; it follows separately from the inner-product characterization of minimizers.

## Mathlib

Declarations: `exists_norm_eq_iInf_of_complete_convex`
File: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`.

Verified in the pinned checkout. For a normed additive commutative group F with InnerProductSpace Real F, the theorem assumes K.Nonempty, IsComplete K, and Convex Real K. For every u it returns v in K satisfying norm (u - v) = iInf over w : K of norm (u - w). No ambient CompleteSpace F is required. Its type asserts existence rather than uniqueness; norm_eq_iInf_iff_real_inner_le_zero supplies the minimizer characterization from which uniqueness can be derived.

## Depends on

- [Convex sets](../definitions/convex-sets.md)
- [Parallelogram and Pythagorean identities](parallelogram-and-pythagorean-identities.md)
