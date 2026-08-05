---
kind: roadmap
status: mapped
---

# Local-averaging estimator constructions

Plug-in local averaging through partition estimators, nearest neighbors, and Nadaraya-Watson kernel regression.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Learning rules, capacity, and risk decomposition](../learning-rules-capacity-and-risk-decomposition/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)

## Candidate contents

- Plug-in conditional-distribution estimator
- Linear local-averaging estimator
- Simplex weight conditions
- Weighted majority vote
- Weighted regression estimate
- Smoothing matrix
- Partition estimator
- Empty-cell convention
- Partition estimator and least-squares equivalence
- Regressogram
- Decision-tree partition
- Nearest-neighbor ordering
- k-nearest-neighbor estimator
- Voronoi one-neighbor partition
- Smoothing-matrix sparsity exercise (Exercise 6.1)
- Nadaraya-Watson estimator
- Box kernel window
- Gaussian kernel window

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Sections 6.1-6.2.4, printed pages 155-163

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `stdSimplex`
- `stdSimplex_eq_inter`
- `ProbabilityTheory.gaussianPDFReal`
- `ProbabilityTheory.integral_gaussianPDFReal_eq_one`

Primary file: `Mathlib/Analysis/Convex/StdSimplex.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: Simplex weight conditions; Gaussian kernel window. Assembly ingredients and limits: stdSimplex exactly packages nonnegative finite weights summing to one. ProbabilityTheory.gaussianPDFReal and its unit-integral theorem supply the one-dimensional Gaussian-window instance; a multivariate window still needs assembly. Indicators and metric balls can define a box window, but no named statistical window, local-averaging estimator, partition estimator, nearest-neighbor estimator, smoothing matrix, or Nadaraya-Watson API was found. The Gaussian declarations are in Mathlib/Probability/Distributions/Gaussian/Real.lean. Materially uncovered members: Plug-in conditional-distribution estimator; Linear local-averaging estimator; Weighted majority vote; Weighted regression estimate; Smoothing matrix; Partition estimator; Empty-cell convention; Partition estimator and least-squares equivalence; Regressogram; Decision-tree partition; Nearest-neighbor ordering; k-nearest-neighbor estimator; Voronoi one-neighbor partition; Smoothing-matrix sparsity exercise; Nadaraya-Watson estimator; Box kernel window.
