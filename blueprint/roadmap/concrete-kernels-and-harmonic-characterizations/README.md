---
kind: roadmap
status: mapped
---

# Concrete kernels and harmonic characterizations

Polynomial, periodic, Mercer, and translation-invariant kernels characterized through Fourier and Sobolev norms.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Fourier analysis and Sobolev approximation](../fourier-analysis-and-sobolev-approximation/README.md)
- [Hilbert-space covariance operators and probability](../hilbert-space-covariance-operators-and-probability/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Linear kernel
- Homogeneous polynomial kernel
- Inhomogeneous polynomial feature space (Exercise 7.3)
- Periodic Fourier RKHS characterization
- Derivative and Sobolev penalties
- Bernoulli-polynomial kernels
- Order-two Bernoulli kernel (Exercise 7.4)
- Periodic exponential kernel
- Periodic exponential closed form (Exercise 7.5)
- Mercer-kernel construction (Exercise 7.6)
- Mercer decomposition (Exercise 7.7)
- Bochner theorem
- Fourier-domain RKHS norm
- Exponential kernel and first-order Sobolev norm
- Gaussian-kernel smoothness
- Matern kernels and Sobolev spaces
- Density in L2
- Kernels beyond vectorial inputs

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Sections 7.3.1-7.3.4, printed pages 186-195

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: RKHS and RKHS.kernel in Mathlib/Analysis/InnerProductSpace/Reproducing.lean, Fourier-transform APIs, TemperedDistribution.MemSobolev and TemperedDistribution.memSobolev_two_iff_fourier, and MeasureTheory.Lp.dense_hasCompactSupport_contDiff supply general RKHS, Fourier, Sobolev, and density infrastructure, but do not state a listed concrete-kernel result. Searches for linear and polynomial kernels, periodic/Bernoulli kernels, Mercer decomposition, positive-definite Bochner theory, Matern kernels, and the listed Fourier/Sobolev kernel characterizations found no matching declaration. Materially uncovered members: Linear kernel; Homogeneous polynomial kernel; Inhomogeneous polynomial feature space (Exercise 7.3); Periodic Fourier RKHS characterization; Derivative and Sobolev penalties; Bernoulli-polynomial kernels; Order-two Bernoulli kernel (Exercise 7.4); Periodic exponential kernel; Periodic exponential closed form (Exercise 7.5); Mercer-kernel construction (Exercise 7.6); Mercer decomposition (Exercise 7.7); Bochner theorem; Fourier-domain RKHS norm; Exponential kernel and first-order Sobolev norm; Gaussian-kernel smoothness; Matern kernels and Sobolev spaces; Density in L2; Kernels beyond vectorial inputs.
