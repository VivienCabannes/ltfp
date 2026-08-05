---
kind: roadmap
status: mapped
---

# Averaging and bagging of predictors

Independent averaging preserves bias while reducing variance, while bootstrap and subsample bagging trade bias for variance reduction in nearest-neighbor and ridge estimators.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Classification calibration and surrogate-risk transfer](../classification-calibration-and-surrogate-risk-transfer/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Nearest-neighbor geometry and convergence](../nearest-neighbor-geometry-and-convergence/README.md)
- [Kernel ridge covariance theory](../kernel-ridge-covariance-theory/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)

## Candidate contents

- Weighted-dataset ensemble construction
- Regression averaging and classification voting
- Independent-ensemble bias-variance decomposition
- Distributed nearest-neighbor rate (Exercise 10.1)
- Replicated ridge-regression rate (Exercise 10.2)
- Independent majority-vote error bound (Exercise 10.3)
- Bootstrap and subsampling bagging (Exercise 10.4)
- Infinite-replication stabilization
- Bagged one-nearest-neighbor weights
- Bagged one-nearest-neighbor risk bound
- Random forests

## Sources

- `sources/ltfp_book.pdf` — Chapter 10, Sections 10.1-10.2, printed pages 283-289

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: ProbabilityTheory.IndepFun.variance_add and ProbabilityTheory.IndepFun.variance_sum in Mathlib/Probability/Moments/Variance.lean can support an independent-average variance calculation, and generic Hoeffding bounds can support voting estimates, but neither is an ensemble or bagging theorem. Searches for averaging ensembles, bagging, bootstrap predictors, majority votes, bagged nearest neighbors, and random forests found no member-level declaration. Materially uncovered members: Weighted-dataset ensemble construction; Regression averaging and classification voting; Independent-ensemble bias-variance decomposition; Distributed nearest-neighbor rate; Replicated ridge-regression rate; Independent majority-vote error bound; Bootstrap and subsampling bagging; Infinite-replication stabilization; Bagged one-nearest-neighbor weights; Bagged one-nearest-neighbor risk bound; Random forests.
