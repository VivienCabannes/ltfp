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
