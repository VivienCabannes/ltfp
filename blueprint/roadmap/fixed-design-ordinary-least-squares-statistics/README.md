---
kind: roadmap
status: mapped
---

# Fixed-design ordinary least-squares statistics

Bias, covariance, risk, training error, and noise generalizations under a well-specified fixed design.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)

## Candidate contents

- Well-specified homoscedastic linear model
- Gaussian maximum-likelihood interpretation
- Noise-variance maximum likelihood estimator (Exercise 3.1)
- Fixed-design risk decomposition
- Mahalanobis norm
- Estimator bias-variance decomposition
- Ordinary least-squares unbiasedness and covariance
- Exact ordinary least-squares excess risk
- Expected training risk and unbiased noise estimator (Exercise 3.2)
- Train-test optimism
- General-noise covariance risk (Exercise 3.3)
- Multivariate ordinary least-squares risk (Exercise 3.4)

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Sections 3.5-3.5.2, printed pages 50-56

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.covariance`
- `ProbabilityTheory.covarianceBilin`
- `ProbabilityTheory.covarianceOperator`
- `ProbabilityTheory.covarianceOperator_inner`
- `ProbabilityTheory.covarianceOperator_apply`
- `ProbabilityTheory.IndepFun.variance_sum`

Primary file: `Mathlib/Probability/Moments/CovarianceBilin.lean`.

Pinned Mathlib supplies scalar and Hilbert-space covariance, a positive covariance operator with integral formulas, variance of independent sums, and Gaussian distributions. Searches found no fixed-design linear-model or ordinary-least-squares statistical API, Mahalanobis loss wrapper, OLS unbiasedness/covariance/risk theorem, noise-variance MLE, expected training-error correction, optimism identity, or multivariate OLS result. The probability-moment substrate is reusable, but all estimator-specific statements require assembly or new formalization.
