---
kind: roadmap
status: mapped
---

# Principal components and low-rank regression

Principal component analysis as optimal low-rank reconstruction and its bias-variance relationship with ridge regression.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)

## Candidate contents

- Principal component reconstruction objective
- Centered affine and linear principal components
- Trace maximization formulation
- Top-eigenspace solution
- Alternating matrix-factorization convergence (Exercise 3.9)
- K-means alternating updates (Exercise 3.10)
- Principal-component-preprocessed ordinary least-squares predictor
- Principal-component ordinary least-squares excess-risk identity
- Rank-dependent risk bound
- Optimized-rank equivalence with ridge

## Sources

- `sources/ltfp_book.pdf` — Chapter 3, Section 3.9, printed pages 66-68

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Matrix.IsHermitian.eigenvectorBasis`
- `Matrix.IsHermitian.mulVec_eigenvectorBasis`
- `Matrix.IsHermitian.trace_eq_sum_eigenvalues`
- `Submodule.orthogonalProjectionOnto`
- `LinearMap.singularValues`

Primary file: `Mathlib/Analysis/Matrix/Spectrum.lean`.

Pinned Mathlib supplies Hermitian eigenspaces, trace as the sum of eigenvalues, orthogonal projection, and singular values. Searches found no PCA API, Eckart-Young/best-low-rank approximation theorem, trace-maximization/top-eigenspace result, centered affine PCA, alternating factorization or k-means convergence, principal-component regression estimator, or its risk comparison with ridge. The spectral substrate is reusable but every PCA/statistical statement needs assembly or new proof.
