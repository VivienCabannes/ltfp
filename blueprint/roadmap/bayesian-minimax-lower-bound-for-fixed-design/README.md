---
kind: roadmap
status: mapped
---

# Bayesian minimax lower bound for fixed design

A Gaussian-prior Bayes reduction proving that the ordinary least-squares rate is worst-case optimal.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)
- [Consistency, minimax limits, and adaptivity](../consistency-minimax-limits-and-adaptivity/README.md)

## Candidate contents

- Supremum-to-prior-average lower bound
- Gaussian prior for the regression parameter
- Posterior mean as squared-error Bayes estimator
- Gaussian posterior mean-mode equivalence
- Ridge as Gaussian posterior estimator
- Rank-sensitive fixed-design lower bound
- Full-rank minimax lower bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Section 3.7, printed pages 60-63

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.minimaxRisk`
- `ProbabilityTheory.iSup_bayesRisk_le_minimaxRisk`
- `ProbabilityTheory.bayesRisk`
- `ProbabilityTheory.IsBayesEstimator`
- `ProbabilityTheory.IsArgminEstimator.isBayesEstimator`
- `ProbabilityTheory.multivariateGaussian`

Primary file: `Mathlib/Probability/Decision/Risk/Basic.lean`.

Pinned Mathlib directly supplies generic minimax and Bayes risks, the supremum-of-Bayes-risks lower bound, measurable posterior argmin estimators, and multivariate Gaussian measures. It does not provide Gaussian linear-regression conjugacy, posterior mean/mode formulas, ridge-as-posterior estimation, or the rank-sensitive fixed-design lower bound. The abstract Bayes reduction is reusable; the Gaussian conditioning and regression calculation remain new.
