---
kind: roadmap
status: mapped
---

# Matrix algebra and Gaussian conditioning

Closed-form quadratic optimization, block-matrix inversion, and Gaussian conditioning through Schur complements.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Positive-definite quadratic minimum
- Completed-square identity
- Semidefinite unboundedness criterion
- Quadratic Fenchel-Young inequality
- Scalar Young inequality
- Two-by-two inverse
- Schur complements
- Block inverse formulas
- Woodbury identities
- Push-through identities
- Identity-plus-BB-transpose inverse
- Rank-one all-ones inverse (Exercise 1.1)
- Block LDU diagonalization (Exercise 1.2)
- Schur determinant factorization (Exercise 1.3)
- Block Gaussian density and marginal
- Conditional Gaussian mean and covariance
- Gaussian conditioning derivation (Exercise 1.4)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Sections 1.1.1-1.1.3, printed pages 3-6

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Matrix.PosSemidef`
- `Matrix.PosDef`
- `Matrix.PosSemidef.dotProduct_mulVec_nonneg`
- `Matrix.PosDef.dotProduct_mulVec_pos`
- `Matrix.PosDef.isUnit`
- `Matrix.PosDef.inv`
- `Matrix.schur_complement_eq₁₁`
- `Matrix.schur_complement_eq₂₂`
- `Matrix.PosDef.fromBlocks₁₁`
- `Matrix.PosDef.fromBlocks₂₂`
- `Matrix.fromBlocks_eq_of_invertible₁₁`
- `Matrix.fromBlocks_eq_of_invertible₂₂`
- `Matrix.invOf_fromBlocks₁₁_eq`
- `Matrix.invOf_fromBlocks₂₂_eq`
- `Matrix.det_fromBlocks₁₁`
- `Matrix.det_fromBlocks₂₂`
- `Matrix.invOf_add_mul_mul`
- `Matrix.add_mul_mul_inv_eq_sub`
- `Matrix.inv_def`
- `Matrix.adjugate_fin_two_of`
- `Matrix.det_fin_two_of`
- `two_mul_le_add_mul_sq`
- `Real.young_inequality`
- `ProbabilityTheory.multivariateGaussian`
- `ProbabilityTheory.integral_id_multivariateGaussian`
- `ProbabilityTheory.covarianceBilin_multivariateGaussian`
- `ProbabilityTheory.measurePreserving_restrict₂_multivariateGaussian`

Primary file: `Mathlib/LinearAlgebra/Matrix/SchurComplement.lean`.

Pinned Mathlib exactly covers scalar Young inequalities, operational Schur complements, both block inverse formulas, Woodbury, the identity-plus-BB-transpose inverse by specialization, Schur determinant factorizations, multivariate Gaussian means/covariance, and coordinate-block marginals. Quadratic minimization, completed-square and Fenchel-Young forms require assembly. The semidefinite range/unboundedness criterion, push-through and all-ones specializations, explicit two-by-two inverse theorem, Gaussian density factorization, and conditional Gaussian mean/covariance theorem are absent. Supporting files include Matrix/Invertible.lean, NonsingularInverse.lean, PosDef.lean, Adjugate.lean, Determinant/Basic.lean, and Probability/Distributions/Gaussian/Multivariate.lean.
