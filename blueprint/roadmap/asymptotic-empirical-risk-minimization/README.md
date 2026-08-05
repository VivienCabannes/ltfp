---
kind: roadmap
status: mapped
---

# Asymptotic empirical-risk minimization

Classical smooth finite-dimensional M-estimation, asymptotic normality, and the leading excess-risk trace formula.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Empirical-risk decomposition and approximation](../empirical-risk-decomposition-and-approximation/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Smooth M-estimator consistency heuristic
- Score Taylor expansion
- Hessian information matrix
- Fisher information matrix
- Multivariate central limit theorem for score averages
- Asymptotic normality of the empirical minimizer
- Asymptotic parameter mean-square error
- Asymptotic excess-risk trace formula
- Well-specified linear-regression specialization

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Section 4.7, printed pages 105-107

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`

Primary file: `Mathlib/Probability/CentralLimitTheorem.lean`.

Pinned Mathlib's tendstoInDistribution_inv_sqrt_mul_sum_sub proves only the one-dimensional i.i.d. central limit theorem; the file explicitly documents dimension 1. The source needs a multivariate CLT for random score vectors, Hessian convergence, and a full M-estimation Taylor/delta argument. No complete M-estimation theorem was found, and the book itself cites van der Vaart Theorems 5.21/5.41 while giving only an intuitive justification.
