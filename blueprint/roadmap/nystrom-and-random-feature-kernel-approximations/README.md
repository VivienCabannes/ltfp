---
kind: roadmap
status: mapped
---

# Nystrom and random-feature kernel approximations

Column sampling and random features provide low-dimensional approximations of kernel matrices and feature maps for scalable learning.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Finite kernel optimization and stochastic algorithms](../finite-kernel-optimization-and-stochastic-algorithms/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Nystrom column sampling
- Random-feature approximation
- Fourier random features
- Random-ReLU features
- Column sampling as optimal feature projection (Exercise 7.8)
- Positive-semidefinite Nystrom residual (Exercise 7.9)
- Random features for Mercer kernels (Exercise 7.10)

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Sections 7.4.2-7.4.3 and Exercises 7.8-7.10, printed pages 197-199

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `RKHS`
- `RKHS.kernel`
- `RKHS.posSemidef_kernel`
- `Matrix.gram`
- `Matrix.submatrix_gram`
- `Matrix.posSemidef_gram`
- `Matrix.PosSemidef.submatrix`
- `Matrix.PosSemidef.fromBlocks₁₁`
- `Matrix.PosSemidef.fromBlocks₂₂`
- `Matrix.PosDef.isUnit`
- `CFC.sqrt`
- `CFC.sq_sqrt`

Primary file: `Mathlib/Analysis/InnerProductSpace/GramMatrix.lean`.

Pinned Mathlib supplies Gram matrices and principal submatrices, positive-semidefinite Schur-complement equivalences, positive-definite invertibility, RKHS kernel positivity, and matrix square roots. These cover the matrix substrate for column sampling and the core Schur-complement fact behind the invertible-principal-block Nystrom residual, which still needs reindexing and assembly. No Nystrom algorithm, random-feature construction, or associated learning guarantee was found.
