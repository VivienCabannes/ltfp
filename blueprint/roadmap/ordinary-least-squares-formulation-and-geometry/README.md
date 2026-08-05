---
kind: roadmap
status: mapped
---

# Ordinary least-squares formulation and geometry

Linear-in-parameter square-loss empirical risk minimization, its closed form, projection geometry, and numerical formulations.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Learning rules, capacity, and risk decomposition](../learning-rules-capacity-and-risk-decomposition/README.md)

## Candidate contents

- Feature map and linear predictor
- Response vector and design matrix
- Empirical square-risk matrix form
- Full-column-rank and overdetermined assumptions
- Ordinary least-squares estimator
- Normal equations
- Closed-form ordinary least-squares solution
- Noncentered empirical covariance
- Projection characterization
- QR triangular solution
- Gradient-descent fixed-point formulation
- Fixed-design and random-design distinction
- Fixed-design in-sample risk

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Sections 3.1-3.4, printed pages 45-50

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Submodule.orthogonalProjectionOnto`
- `Submodule.exists_norm_eq_iInf_of_complete_subspace`
- `Submodule.norm_eq_iInf_iff_inner_eq_zero`
- `hasStrictFDerivAt_norm_sq`
- `fderiv_norm_sq_apply`
- `gramSchmidt`
- `gramSchmidtOrthonormalBasis`

Primary file: `Mathlib/Analysis/InnerProductSpace/Projection/Minimal.lean`.

Pinned Mathlib supplies Hilbert-space orthogonal projections with minimizer and orthogonality characterizations, squared-norm Frechet derivatives, Gram-Schmidt orthonormalization, matrix inversion, and finite-dimensional linear algebra. Searches found no least-squares/normal-equations API, closed-form OLS estimator, QR factorization theorem, empirical covariance convention, fixed/random-design statistical wrapper, or in-sample-risk interface. The projection and derivative foundations are reusable, but the source's matrix estimator layer and its algebraic specializations require new formalization.
