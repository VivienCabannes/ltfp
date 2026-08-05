---
kind: roadmap
status: mapped
---

# Randomized least-squares compression and embeddings

Gaussian sketches and random feature projections are analyzed through random projectors and Wishart moments, with extensions to kernels and Johnson-Lindenstrauss embeddings.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Random-design least-squares and covariance concentration](../random-design-least-squares-and-covariance-concentration/README.md)
- [Averaging and bagging of predictors](../averaging-and-bagging-of-predictors/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Nystrom and random-feature kernel approximations](../nystrom-and-random-feature-kernel-approximations/README.md)
- [Sparse least-squares proof and probability toolkit](../sparse-least-squares-proof-and-probability-toolkit/README.md)

## Candidate contents

- Observation sketching
- Feature random projection
- Gaussian sketch estimator
- Averaged Gaussian-sketch risk
- Expected random projector
- Projected least-squares bias-variance decomposition
- Gaussian projection risk bound
- Coordinate-sampling sketch moments (Exercise 10.5)
- Kernel random projection
- Random-feature sketch bound
- Johnson-Lindenstrauss lemma

## Sources

- `sources/ltfp_book.pdf` — Chapter 10, Section 10.2, printed pages 288-297

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: multivariate Gaussian, matrix, orthogonal-projection, least-squares, and RKHS APIs provide only prerequisites. Searches for Gaussian sketches, Wishart or expected random projectors, observation and feature sketching, randomized least-squares risk, random-feature sketch bounds, and the Johnson-Lindenstrauss lemma found no matching declaration. Materially uncovered members: Observation sketching; Feature random projection; Gaussian sketch estimator; Averaged Gaussian-sketch risk; Expected random projector; Projected least-squares bias-variance decomposition; Gaussian projection risk bound; Coordinate-sampling sketch moments; Kernel random projection; Random-feature sketch bound; Johnson-Lindenstrauss lemma.
