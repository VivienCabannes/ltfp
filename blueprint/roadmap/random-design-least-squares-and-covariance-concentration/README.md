---
kind: roadmap
status: mapped
---

# Random-design least-squares and covariance concentration

Population-covariance risk formulas, exact Gaussian-design behavior, and high-probability covariance control.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Matrix and operator concentration](../matrix-and-operator-concentration/README.md)
- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)

## Candidate contents

- Random-design well-specified linear model
- Population-covariance excess risk
- Expected ordinary least-squares risk
- Random-design ridge risk (Exercise 3.8)
- Inverse-Wishart expectation
- Exact Gaussian-design risk
- Matrix Bernstein restatement
- Covariance fourth-moment assumption
- Normalized moment parameter
- Gaussian normalized-moment verification
- Empirical covariance lower bound
- High-probability ordinary least-squares risk bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Sections 3.8-3.8.2, printed pages 63-66

## Mathlib assessment

Legacy assessment: `missing`.

A pinned-checkout search found no Wishart or inverse-Wishart distribution/expectation, random-design regression API, sample/empirical covariance concentration, matrix Bernstein theorem, normalized fourth-moment package, or random-design OLS/ridge risk theorem. General multivariate Gaussian and covariance-operator foundations live in prerequisite clusters, but no declaration directly covers a member of this statistical concentration cluster.
