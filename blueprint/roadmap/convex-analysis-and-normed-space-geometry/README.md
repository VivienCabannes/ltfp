---
kind: roadmap
status: detailed
---

# Convex analysis and normed-space geometry

Mathlib foundations for convex functions and sets, strong convexity, finite Jensen inequalities, norms, duality, and Hilbert-space geometry.

## Planning status

This milestone is decomposed into 22 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

This milestone has no coarse prerequisites.

## Candidate contents

- Convex sets and convex functions
- Strong convexity
- Finite convex combinations and finite Jensen inequality
- Norms and dual norms
- Hilbert spaces and continuous linear maps

## Detailed nodes

- [Convex sets](definitions/convex-sets.md)
- [Convex functions on a set](definitions/convex-functions-on-a-set.md)
- [Strong convexity on a set](definitions/strong-convexity-on-a-set.md)
- [Strong convexity as shifted convexity](theorems/strong-convexity-as-shifted-convexity.md)
- [Finite Jensen inequality](theorems/finite-jensen-inequality.md)
- [Continuous linear maps](definitions/continuous-linear-maps.md)
- [Strong dual space](definitions/strong-dual-space.md)
- [Operator norm of a continuous linear map](definitions/operator-norm-of-a-continuous-linear-map.md)
- [Pointwise bound controls the operator norm](theorems/pointwise-bound-controls-the-operator-norm.md)
- [Operator norm controls evaluation](theorems/operator-norm-controls-evaluation.md)
- [Inner product as a continuous sesquilinear map](definitions/inner-product-as-a-continuous-sesquilinear-map.md)
- [Norm of the inner product functional](theorems/norm-of-the-inner-product-functional.md)
- [Isometric Riesz embedding](definitions/isometric-riesz-embedding.md)
- [Hilbert projection theorem for complete convex sets](theorems/hilbert-projection-theorem-for-complete-convex-sets.md)
- [Orthogonal projection onto a closed subspace](theorems/orthogonal-projection-onto-a-closed-subspace.md)
- [Frechet-Riesz representation theorem](theorems/frechet-riesz-representation-theorem.md)
- [Finite convex combinations in convex sets](theorems/finite-convex-combinations-in-convex-sets.md)
- [Self-inner-product and norm definiteness](theorems/self-inner-product-and-norm-definiteness.md)
- [Cauchy-Schwarz inequality for inner products](theorems/cauchy-schwarz-inequality-for-inner-products.md)
- [Squared-norm sum and difference expansions](theorems/squared-norm-sum-and-difference-expansions.md)
- [Parallelogram and Pythagorean identities](theorems/parallelogram-and-pythagorean-identities.md)
- [Minimizer characterizations for convex sets and subspaces](theorems/minimizer-characterizations-for-convex-sets-and-subspaces.md)

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `in-mathlib`.

Relevant declarations:

- `ConvexOn`
- `StrongConvexOn`
- `ConvexOn.map_sum_le`
- `StrongDual`
- `ContinuousLinearMap.opNorm_le_bound`
- `innerSL`

Primary file: `Mathlib/Analysis/Convex/Function.lean`.

Verified in the pinned checkout. Strong convexity and finite Jensen results are in adjacent Mathlib/Analysis/Convex files; StrongDual is in Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean; ContinuousLinearMap.opNorm_le_bound is defined in Mathlib/Analysis/Normed/Operator/Basic.lean; and the Hilbert-space Riesz map innerSL is in Mathlib/Analysis/InnerProductSpace/LinearMap.lean. Integral Jensen is assigned to the probability-and-expectation foundation because its statement depends on both a probability measure and Bochner integration. Mathlib's strong-convexity file does not supply the derivative characterizations needed downstream, which remain project-local assembly or proofs.
