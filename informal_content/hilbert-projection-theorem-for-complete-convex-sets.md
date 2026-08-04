# Hilbert projection theorem for complete convex sets

Let `E` be a real inner product space, let `C` be a nonempty complete convex subset of `E`, and let `u : E`. There exists `v` in `C` such that

`||u - v|| = iInf (fun w : C => ||u - w||)`.

Thus the distance from `u` to `C` is attained without requiring the ambient space itself to be complete.

The theorem asserts existence of a minimizer. Uniqueness is not part of this declaration's conclusion; it follows separately from the inner-product characterization of minimizers.

## Mathlib

Declarations: `exists_norm_eq_iInf_of_complete_convex`
File: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`
