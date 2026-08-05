---
kind: roadmap
status: mapped
---

# Kernel ridge covariance theory

Kernel ridge regression as a random-design linear smoother, with operator bias and variance bounds and empirical-population covariance comparison.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Finite kernel optimization and stochastic algorithms](../finite-kernel-optimization-and-stochastic-algorithms/README.md)
- [Lipschitz kernel learning and smoothness adaptation](../lipschitz-kernel-learning-and-smoothness-adaptation/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)
- [Matrix and operator concentration](../matrix-and-operator-concentration/README.md)
- [Hilbert-space covariance operators and probability](../hilbert-space-covariance-operators-and-probability/README.md)
- [Local-averaging estimator constructions](../local-averaging-estimator-constructions/README.md)

## Candidate contents

- Kernel ridge as a linear estimator
- Kernel-ridge smoothing matrix formula and symmetry
- Centered kernel ridge (Exercise 7.22)
- Periodic-kernel smoothing eigenvalues (Exercise 7.23)
- Empirical and population covariance operators
- RKHS-L2 covariance identity
- Kernel-ridge bias-variance decomposition
- Expected-risk upper bound
- Empirical-population covariance comparison
- Well-specified kernel-ridge bound
- High-probability kernel-ridge bound
- Variational bias identity
- Misspecified kernel-ridge bound
- Trace-class covariance eigendecomposition
- Degrees of freedom under eigenvalue decay
- Sobolev bias-variance balance

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Section 7.6, printed pages 208-218

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.covarianceOperator`
- `ProbabilityTheory.covarianceOperator_inner`
- `ProbabilityTheory.covarianceOperator_apply`
- `ProbabilityTheory.isPositive_covarianceOperator`
- `ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot`
- `ContinuousLinearMap.finite_dimensional_eigenspace`

Primary file: `Mathlib/Probability/Moments/CovarianceBilin.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Directly covered in part: the population half of Empirical and population covariance operators. ProbabilityTheory.covarianceOperator defines the uncentered covariance operator of a Hilbert-space measure; covarianceOperator_inner and covarianceOperator_apply give its integral formulas, and isPositive_covarianceOperator proves positivity. The empirical covariance operator and its link to this population operator are absent. Assembly-only support: ContinuousLinearMap.orthogonalComplement_iSup_eigenspaces_eq_bot and ContinuousLinearMap.finite_dimensional_eigenspace in Mathlib/Analysis/InnerProductSpace/Spectrum.lean give the compact self-adjoint spectral theorem, but not trace-class covariance or kernel-ridge theory. Materially uncovered members: Kernel ridge as a linear estimator; Kernel-ridge smoothing matrix formula and symmetry; Centered kernel ridge (Exercise 7.22); Periodic-kernel smoothing eigenvalues (Exercise 7.23); RKHS-L2 covariance identity; Kernel-ridge bias-variance decomposition; Expected-risk upper bound; Empirical-population covariance comparison; Well-specified kernel-ridge bound; High-probability kernel-ridge bound; Variational bias identity; Misspecified kernel-ridge bound; Trace-class covariance eigendecomposition; Degrees of freedom under eigenvalue decay; Sobolev bias-variance balance.
