---
kind: roadmap
status: mapped
---

# Loss risk and Bayes decision theory

Formal performance criteria and pointwise optimal prediction under common losses.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Supervised learning setup and evaluation](../supervised-learning-setup-and-evaluation/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Loss function
- Binary and multicategory zero-one losses
- Square and absolute regression losses
- Structured-output losses
- Expected risk
- Empirical risk
- Conditional risk
- Bayes predictor and Bayes risk
- Excess risk
- Binary and multicategory Bayes classifiers
- Square-loss conditional-mean predictor
- Cost-sensitive Bayes classifier (Exercise 2.1)
- Absolute-loss Bayes predictor (Exercise 2.2)
- Pinball-loss quantile predictor (Exercise 2.3)
- Epsilon-insensitive Bayes predictors (Exercise 2.4)
- Inverted-classifier risk (Exercise 2.5)
- Chance-prediction risk (Exercise 2.6)
- Posterior-sampling optimality (Exercise 2.7)

## Sources

- `sources/ltfp_book.pdf` — Chapter 2, Sections 2.2-2.2.3, printed pages 25-30

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.avgRisk`
- `ProbabilityTheory.bayesRisk`
- `ProbabilityTheory.IsBayesEstimator`
- `ProbabilityTheory.IsArgminEstimator`
- `ProbabilityTheory.HasArgminEstimator`
- `ProbabilityTheory.lintegral_iInf_posterior_le_bayesRisk`
- `ProbabilityTheory.IsArgminEstimator.isBayesEstimator`
- `ProbabilityTheory.HasArgminEstimator.bayesRisk_eq`

Primary file: `Mathlib/Probability/Decision/BayesEstimator.lean`.

Pinned Mathlib has a generic kernel-valued decision-theory API with extended-nonnegative losses, average and Bayes risk, posterior expected loss, measurable argmin estimators, and the theorem that such an estimator is Bayes. The file explicitly leaves general measurable selection as a TODO. No prediction-specific zero-one, square, absolute, pinball, or epsilon-insensitive loss library, empirical/conditional/excess-risk API, or the book's classifier/regression Bayes-characterization theorems were found. Adapting the generic estimator API to supervised prediction and real-valued risks remains project work.
