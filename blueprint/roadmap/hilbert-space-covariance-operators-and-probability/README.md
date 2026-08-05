---
kind: roadmap
status: mapped
---

# Hilbert-space covariance operators and probability

Covariance bilinear forms and operators, trace-class spectral theory, and concentration interfaces for Hilbert-valued random variables.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Hilbert-valued random variables
- Covariance bilinear form
- Covariance operator
- Trace-class positive operators
- Compact self-adjoint spectral theorem
- Hilbert-valued concentration

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Exercise 7.7, printed page 190
- `sources/ltfp_book.pdf` — Chapter 7, Sections 7.6.2-7.6.6, printed pages 209-218

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

Pinned Mathlib provides uncentered Hilbert-space covariance operators with integral and positivity theorems, plus the compact self-adjoint spectral theorem in Mathlib/Analysis/InnerProductSpace/Spectrum.lean. Trace-class summability and the Hilbert-valued concentration estimates used in Chapter 7 are not supplied as a unified API.
