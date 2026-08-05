---
kind: roadmap
status: mapped
---

# Regression minimax lower bounds

Fano and packing lower bounds for finite-dimensional and smooth nonparametric Gaussian regression.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Minimax reduction and packing](../minimax-reduction-and-packing/README.md)
- [Entropy, data processing, and Fano inequalities](../entropy-data-processing-and-fano-inequalities/README.md)
- [Relative entropy and Gibbs variational principles](../relative-entropy-and-gibbs-variational-principles/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Kernel ridge covariance theory](../kernel-ridge-covariance-theory/README.md)
- [Hilbert-space covariance operators and probability](../hilbert-space-covariance-operators-and-probability/README.md)
- [Fourier analysis and Sobolev approximation](../fourier-analysis-and-sobolev-approximation/README.md)

## Candidate contents

- Gaussian regression testing family
- Prediction-distance and KL identities
- Dense linear-regression minimax lower bound
- Euclidean-ball packing lower bound (Exercise 15.1)
- Orthogonal series regression family
- Sobolev ellipsoid packing
- Smooth nonparametric minimax lower rate
- Kernel-eigenvalue lower-bound construction
- Match to kernel-ridge upper rates
- Dependence on noise, dimension, smoothness, and sample size

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Section 15.1.5 and Exercise 15.1, printed pages 436-438

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: multivariate Gaussian measures, metric packing numbers, matrix/Hilbert-space operators, Fourier analysis, and Sobolev regularity exist in prerequisite areas, but searches found no Gaussian regression experiment, Gaussian-regression KL identity, regression minimax theorem, orthogonal-series hard family, Sobolev packing lower bound, or kernel-eigenvalue lower-rate construction. Materially uncovered members: Gaussian regression testing family; Prediction-distance and KL identities; Dense linear-regression minimax lower bound; Euclidean-ball packing lower bound (Exercise 15.1); Orthogonal series regression family; Sobolev ellipsoid packing; Smooth nonparametric minimax lower rate; Kernel-eigenvalue lower-bound construction; Match to kernel-ridge upper rates; Dependence on noise, dimension, smoothness, and sample size.
