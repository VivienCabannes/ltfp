---
kind: roadmap
status: mapped
---

# Ordinary differential equations and gradient flows

Existence, uniqueness, invariance, and convergence tools for ordinary differential equations and continuous-time gradient dynamics.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Ordinary differential equation solution
- Local existence and uniqueness
- Invariant subspace and cone arguments
- Gradient-flow energy identity
- Linear gradient-flow solution

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `IsPicardLindelof`
- `IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt`
- `IsPicardLindelof.exists_forall_mem_closedBall_eq_hasDerivWithinAt_lipschitzOnWith`
- `ContDiffAt.exists_forall_mem_closedBall_exists_eq_forall_mem_Ioo_hasDerivAt`
- `ODE_solution_unique_of_mem_Icc`

Primary file: `Mathlib/Analysis/ODE/ExistUnique.lean`.

Pinned Mathlib covers local existence, uniqueness, continuous-time integral curves, and Lipschitz dependence on initial data for Banach-space ODEs. Dedicated invariant-subspace/cone lemmas and gradient-flow energy and convergence interfaces were not found and still require assembly or new formalization.
