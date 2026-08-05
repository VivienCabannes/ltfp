---
kind: roadmap
status: mapped
---

# Lipschitz kernel learning and smoothness adaptation

Kernel risk decomposition, universal consistency, and Sobolev-smoothness-adaptive approximation and estimation rates.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Fourier analysis and Sobolev approximation](../fourier-analysis-and-sobolev-approximation/README.md)
- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)

## Candidate contents

- Lipschitz excess-risk-to-L2 bound
- Constrained RKHS empirical-risk bound
- Optimized constrained risk bound
- Approximation functional
- Well-specified, misspecified, and projection cases
- Regularized RKHS empirical-risk bound
- Spectral solution of translation-invariant approximation
- Universal approximation of translation-invariant kernels
- Matern-Sobolev approximation rate
- Smoothness-adaptive Lipschitz excess-risk rate
- Approximation-error-to-RKHS-norm conversion
- Lipschitz-to-Sobolev extension on a ball
- Gaussian-kernel approximation error (Exercise 7.21)

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Section 7.5, printed pages 202-208

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: generic RKHS, Lipschitz, convexity, Rademacher, Fourier, and Sobolev APIs can support later assembly, but none implements a listed kernel-learning or approximation member. Searches for constrained or regularized RKHS risk bounds, approximation functionals, universal translation-invariant kernels, Matern adaptation, and Gaussian-kernel approximation rates found no relevant theorem. Materially uncovered members: Lipschitz excess-risk-to-L2 bound; Constrained RKHS empirical-risk bound; Optimized constrained risk bound; Approximation functional; Well-specified, misspecified, and projection cases; Regularized RKHS empirical-risk bound; Spectral solution of translation-invariant approximation; Universal approximation of translation-invariant kernels; Matern-Sobolev approximation rate; Smoothness-adaptive Lipschitz excess-risk rate; Approximation-error-to-RKHS-norm conversion; Lipschitz-to-Sobolev extension on a ball; Gaussian-kernel approximation error (Exercise 7.21).
