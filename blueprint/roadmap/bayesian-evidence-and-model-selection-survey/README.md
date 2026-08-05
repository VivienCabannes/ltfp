---
kind: roadmap
status: mapped
---

# Bayesian evidence and model-selection survey

Marginal likelihood and the book's brief survey of evidence-based hyperparameter and model selection, including BIC, ARD, and Gaussian-process examples.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Bayesian posterior updating and prediction](../bayesian-posterior-updating-and-prediction/README.md)
- [Posterior computation and approximation survey](../posterior-computation-and-approximation-survey/README.md)
- [Hierarchical sparse priors](../hierarchical-sparse-priors/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Marginal likelihood or evidence
- Empirical-Bayes hyperparameter selection
- Finite-model evidence selection
- Laplace approximation of marginal likelihood (survey)
- Bayesian information criterion (survey)
- Automatic relevance determination (survey)
- Gaussian-process prior model (survey)

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.3.2, printed pages 422-423

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `MeasureTheory.integral`
- `ProbabilityTheory.multivariateGaussian`
- `RKHS`
- `RKHS.kernel`

Primary file: `Mathlib/Analysis/InnerProductSpace/Reproducing.lean`.

Pinned Mathlib supplies integration, Gaussian measures, and RKHS kernels as substrate, but no marginal-likelihood, empirical-Bayes, BIC, ARD, or Gaussian-process Bayesian-model-selection API was found. The source presents the Laplace/BIC, ARD, and Gaussian-process material as a short survey and does not prove convergence or approximation guarantees.
