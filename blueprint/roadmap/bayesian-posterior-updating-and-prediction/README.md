---
kind: roadmap
status: mapped
---

# Bayesian posterior updating and prediction

Bayes-rule posterior updating and posterior prediction from a prior and likelihood, including the posterior-draw interface used by Thompson sampling.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Likelihood and prior modeling foundations](../likelihood-and-prior-modeling-foundations/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)

## Candidate contents

- Prior, likelihood, evidence, and posterior distributions
- Bayes-rule posterior normalization
- Iid posterior update
- Posterior mean
- Posterior predictive distribution
- Bayesian model averaging
- Independent posterior draws for Thompson sampling

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.3 opening, printed pages 420-421
- `sources/ltfp_book.pdf` — Chapter 11, Section 11.3.3, printed pages 338-339

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.posterior`
- `ProbabilityTheory.compProd_posterior_eq_map_swap`
- `ProbabilityTheory.posterior_eq_withDensity`
- `ProbabilityTheory.condDistrib`
- `ProbabilityTheory.IsBayesEstimator`
- `ProbabilityTheory.IsArgminEstimator.isBayesEstimator`

Primary file: `Mathlib/Probability/Kernel/Posterior.lean`.

Pinned Mathlib directly provides a generic posterior kernel, its joint-law characterization, a density representation under absolute continuity, regular conditional distributions, and Bayes-estimator foundations. The book's parameterized iid posterior formulas, posterior predictive mixtures, model averaging, and posterior-draw algorithmic interface still require project-local definitions and proofs.
