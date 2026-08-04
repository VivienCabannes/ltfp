# Orthogonal projection onto a closed subspace

Let `K` be an `RCLike` scalar field, let `E` be a complete normed inner product space over `K`, and let `U` be a closed linear subspace of `E`. There are two bundled forms of the projector:

- `U.orthogonalProjectionOnto : E ->L[K] U`, whose values carry membership in `U`;
- `U.starProjection : E ->L[K] E`, obtained by including those values into the ambient space.

For every `x : E`, `U.starProjection x` belongs to `U`, and the residual `x - U.starProjection x` belongs to `U`'s orthogonal complement. More precisely, if `v` belongs to `U` and

`<x - v, w>_K = 0`

for every `w` in `U`, then `U.starProjection x = v`; the equivalent hypothesis is `x - v` belonging to the orthogonal complement. The projector also minimizes distance to `x`:

`||x - U.starProjection x|| = iInf (fun u : U => ||x - u||)`.

More generally, the construction only needs the typeclass `U.HasOrthogonalProjection`. Ambient completeness together with closedness of `U` supplies that instance by making `U` complete.

Under the same typeclass, `U` has trivial orthogonal complement exactly when `U` is the whole space. The declaration `Submodule.orthogonal_eq_bot_iff` is defined in `Mathlib/Analysis/InnerProductSpace/Projection/Submodule.lean`; the primary projector API listed below is in `Projection/Basic.lean`.

## Mathlib

Declarations: `Submodule.HasOrthogonalProjection`, `Submodule.HasOrthogonalProjection.ofCompleteSpace`, `Submodule.orthogonalProjectionOnto`, `Submodule.starProjection`, `Submodule.starProjection_apply`, `Submodule.coe_orthogonalProjectionOnto_apply`, `Submodule.starProjection_apply_mem`, `Submodule.sub_starProjection_mem_orthogonal`, `Submodule.eq_starProjection_of_mem_of_inner_eq_zero`, `Submodule.eq_starProjection_of_mem_orthogonal`, `Submodule.starProjection_minimal`, `Submodule.orthogonal_eq_bot_iff`
File: `Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean`
