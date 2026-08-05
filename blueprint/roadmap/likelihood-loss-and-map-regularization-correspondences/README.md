---
kind: roadmap
status: mapped
---

# Likelihood-loss and MAP-regularization correspondences

Negative log-likelihood and negative log-prior calculations identify standard empirical losses and regularizers, including Gaussian-ridge and Laplace-Lasso correspondences.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Likelihood and prior modeling foundations](../likelihood-and-prior-modeling-foundations/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)

## Candidate contents

- Regularized empirical-risk exponential factorization
- Negative log-likelihood as empirical risk
- Gaussian likelihood and square loss
- Bernoulli likelihood and logistic loss
- Maximum-a-posteriori estimator
- Negative log-prior as regularizer
- Gaussian prior and squared l2 penalty
- Laplace prior and l1 penalty
- Student prior and logarithmic penalty
- Gaussian negative log-density (Exercise 14.1)
- Laplace variance (Exercise 14.2)
- Gaussian-inverse-Gamma mixture gives a Student prior (Exercise 14.3)

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Sections 14.1-14.1.2 and Exercises 14.1-14.3, printed pages 409-412

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.multivariateGaussian`
- `MeasureTheory.Measure.rnDeriv`

Primary file: `Mathlib/Probability/Distributions/Gaussian/Multivariate.lean`.

Pinned Mathlib supplies Gaussian measures and density primitives, but no exact maximum-likelihood, MAP, negative-log-likelihood/loss, Gaussian/ridge, or Laplace/Lasso correspondence declarations were found. The model-specific algebra and optimization identifications remain project-local.
