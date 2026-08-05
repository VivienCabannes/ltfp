---
kind: node
declaration: theorem
mathlib: true
---

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


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean`.

Verified in the pinned checkout under RCLike K, NormedAddCommGroup E, and InnerProductSpace K E. orthogonalProjectionOnto U : E ->L[K] U is subtype-valued, while starProjection U : E ->L[K] E is ambient-valued; bridge lemmas identify their values. Membership, residual orthogonality, uniqueness, and minimality are stated for starProjection, with minimality as an iInf over x : U. The generic construction assumes U.HasOrthogonalProjection. If E is complete and U is closed, U is complete and HasOrthogonalProjection.ofCompleteSpace supplies that instance. eq_starProjection_of_mem_of_inner_eq_zero exposes the self-inner-product uniqueness step. orthogonal_eq_bot_iff, defined in Projection/Submodule.lean, is the projection bridge used by Frechet-Riesz surjectivity. Older orthogonalProjection and orthogonalProjectionFn names are deprecated.

## Depends on

- [Continuous linear maps](../definitions/continuous-linear-maps.md)
- [Minimizer characterizations for convex sets and subspaces](minimizer-characterizations-for-convex-sets-and-subspaces.md)
- [Self-inner-product and norm definiteness](self-inner-product-and-norm-definiteness.md)
- [Parallelogram and Pythagorean identities](parallelogram-and-pythagorean-identities.md)
