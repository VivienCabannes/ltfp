---
kind: node
declaration: theorem
mathlib: true
---

# Minimizer characterizations for convex sets and subspaces

Let `F` be a real normed inner-product space, let `C` be convex, let `u : F`, and let `v` belong to `C`. Then `v` minimizes distance from `u` over `C` exactly when

`<u - v, w - v>_R <= 0`

for every `w` in `C`. The infimum is indexed by the subtype `C`, with its elements coerced into `F` inside the norm.

Let `K` be an `RCLike` scalar field, let `E` be a normed inner-product space over `K`, let `U` be a linear subspace of `E`, and let `u : E`. The corresponding condition is residual orthogonality: a point `v` in `U` minimizes distance from `u` exactly when

`<u - v, w>_K = 0`

for every `w` in `U`. If the carrier of `U` is complete, such a minimizer exists without requiring the ambient space to be complete. Completeness is needed for this existence result, but not for the variational or orthogonality equivalences.

## Mathlib

Declarations: `Submodule.exists_norm_eq_iInf_of_complete_subspace`, `norm_eq_iInf_iff_real_inner_le_zero`, `Submodule.norm_eq_iInf_iff_real_inner_eq_zero`, `Submodule.norm_eq_iInf_iff_inner_eq_zero`
File: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`.

Verified in the pinned checkout. The complete-subspace existence theorem assumes only completeness of the subspace and derives convexity and nonemptiness before applying complete-convex minimizer existence; ambient completeness is unnecessary. The real convex-set theorem characterizes a minimizer by inner Real (u - v) (w - v) <= 0 and uses norm_sub_sq. The real and RCLike submodule variants characterize minimizers by inner K (u - v) w = 0. Only existence needs completeness. HasOrthogonalProjection.ofCompleteSpace uses the existence theorem and RCLike equivalence; starProjection_minimal directly uses the RCLike equivalence.

## Depends on

- [Hilbert projection theorem for complete convex sets](hilbert-projection-theorem-for-complete-convex-sets.md)
- [Convex sets](../definitions/convex-sets.md)
- [Squared-norm sum and difference expansions](squared-norm-sum-and-difference-expansions.md)
