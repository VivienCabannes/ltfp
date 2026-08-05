---
kind: roadmap
status: mapped
---

# Gaussian linear double descent

Minimum-norm Gaussian linear regression has exact finite-sample risk formulas on both sides of the interpolation threshold, producing double descent.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Minimum-norm interpolation by gradient methods](../minimum-norm-interpolation-by-gradient-methods/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Random-design least-squares and covariance concentration](../random-design-least-squares-and-covariance-concentration/README.md)

## Candidate contents

- Double-descent phenomenon
- Interpolation threshold
- Isotropic Gaussian regression model
- Underparameterized expected risk
- Overparameterized variance
- Overparameterized bias
- Combined Gaussian double-descent formula
- Overparameterized risk minimizer (Exercise 12.5)

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Sections 12.2-12.2.3, printed pages 355-360

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib provides multivariate Gaussian measures and matrix/covariance foundations, but searches found no Wishart or inverse-Wishart distribution or expectation, random-design least-squares risk formula, interpolation-threshold analysis, or double-descent theorem. The eight exact finite-sample risk members are absent.
