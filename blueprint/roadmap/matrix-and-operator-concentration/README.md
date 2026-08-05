---
kind: roadmap
status: mapped
---

# Matrix and operator concentration

Hoeffding and Bernstein inequalities for symmetric matrices, rectangular dilations, and Hilbert-space operators.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Bounded differences and Bernstein concentration](../bounded-differences-and-bernstein-concentration/README.md)

## Candidate contents

- Positive-semidefinite order
- Largest eigenvalue and operator norm
- Matrix Hoeffding inequality
- Matrix Bernstein inequality
- Hermitian dilation
- Rectangular matrix Hoeffding and Bernstein (Exercise 1.29)
- Intrinsic-dimension ratio
- Intrinsic-dimension matrix Bernstein inequality
- Simplified large-deviation intrinsic bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.6, printed pages 19-20

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches for matrix/operator Hoeffding, Bernstein, intrinsic-dimension concentration, Hermitian dilation concentration, and sample covariance bounds found no matching declaration. Positive-semidefinite order, eigenvalues, and operator norms exist in prerequisite clusters, but no member providing matrix concentration itself is in Mathlib. The complete theorem package and its trace-exponential proof machinery must be developed or sourced independently.
