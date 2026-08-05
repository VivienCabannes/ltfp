---
kind: roadmap
status: mapped
---

# Ridge regression and dimension-free control

Closed-form ridge regression, exact fixed-design bias-variance risk, effective dimension, and a dimension-free tuning bound.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)

## Candidate contents

- Ridge estimator
- Closed-form ridge solution
- Primal-dual Woodbury form (Exercise 3.5)
- Fixed-design ridge excess risk
- Ridge bias and variance monotonicity
- Degrees of freedom
- Optimized regularization and dimension-free risk
- Feature-trace bound
- Rayleigh and trace eigenvalue inequalities
- Generalized quadratic-penalty risk (Exercise 3.6)
- Leave-one-out hat-matrix identity (Exercise 3.7)

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Section 3.6, printed pages 56-60

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Matrix.invOf_add_mul_mul`
- `Matrix.add_mul_mul_inv_eq_sub`
- `Matrix.trace_mul_comm`
- `Matrix.IsHermitian.trace_eq_sum_eigenvalues`
- `ContinuousLinearMap.rayleighQuotient_le_norm`

Primary file: `Mathlib/LinearAlgebra/Matrix/NonsingularInverse.lean`.

Pinned Mathlib supplies Woodbury identities, cyclic trace, Hermitian trace as the sum of eigenvalues, spectral decomposition, and Rayleigh-quotient norm bounds. Searches found no ridge-regression estimator or statistical analysis, effective degrees of freedom, bias/variance monotonicity, optimized dimension-free bound, generalized-penalty theorem, hat matrix, or leave-one-out identity. Closed forms and spectral inequalities can be assembled from existing matrix APIs; the estimator-specific risk package is new.
