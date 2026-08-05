---
kind: roadmap
status: mapped
---

# Posterior mean and posterior mode

Bayes-optimal posterior means, maximum-a-posteriori modes, and their identities and contrasts in Gaussian denoising models.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Bayesian posterior updating and prediction](../bayesian-posterior-updating-and-prediction/README.md)
- [Likelihood-loss and MAP-regularization correspondences](../likelihood-loss-and-map-regularization-correspondences/README.md)
- [Hierarchical sparse priors](../hierarchical-sparse-priors/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Additive Gaussian denoising model
- Posterior density by Bayes rule
- Posterior mean as MMSE estimator
- Posterior mode as MAP estimator
- Gaussian-prior equality of MMSE and MAP
- Tweedie formula for the posterior mean
- Posterior covariance differential identity (Exercise 14.5)
- Poisson and geometric posterior-mean identities (Exercise 14.6)
- Proximal form of the MAP estimator
- MAP fixed-point identity
- MMSE as MAP for a transformed prior (Exercise 14.7)
- Spike-and-slab posterior estimator (Exercise 14.8)
- Laplace-prior posterior estimator (Exercise 14.9)
- Gaussian covariance MMSE and MAP (Exercise 14.10)
- Marginal-density calculations (Exercises 14.9 and 14.11)

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.1.4 and Exercises 14.5-14.11, printed pages 413-417

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.posterior`
- `ProbabilityTheory.posterior_eq_withDensity`
- `ProbabilityTheory.IsBayesEstimator`
- `ProbabilityTheory.IsArgminEstimator`
- `ProbabilityTheory.IsArgminEstimator.isBayesEstimator`
- `ProbabilityTheory.multivariateGaussian`
- `ProbabilityTheory.integral_id_multivariateGaussian`

Primary file: `Mathlib/Probability/Kernel/Posterior.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: ProbabilityTheory.posterior and posterior_eq_withDensity give a generic posterior and a Bayes-rule density representation. ProbabilityTheory.IsArgminEstimator and IsArgminEstimator.isBayesEstimator formalize posterior expected-loss minimizers as Bayes estimators; multivariateGaussian and integral_id_multivariateGaussian supply Gaussian model/mean ingredients. Supporting declarations are in Mathlib/Probability/Decision/BayesEstimator.lean and Mathlib/Probability/Distributions/Gaussian/Multivariate.lean. There is no square-loss theorem identifying the posterior mean, no density-mode/MAP or proximal API, and no density differentiation theorem specialized to this model. Materially uncovered members: Additive Gaussian denoising model; Posterior mean as MMSE estimator; Posterior mode as MAP estimator; Gaussian-prior equality of MMSE and MAP; Tweedie formula for the posterior mean; Posterior covariance differential identity (Exercise 14.5); Poisson and geometric posterior-mean identities (Exercise 14.6); Proximal form of the MAP estimator; MAP fixed-point identity; MMSE as MAP for a transformed prior (Exercise 14.7); Spike-and-slab posterior estimator; Laplace-prior posterior estimator; Gaussian covariance MMSE and MAP (Exercise 14.10); Marginal-density calculations (Exercises 14.9 and 14.11).
