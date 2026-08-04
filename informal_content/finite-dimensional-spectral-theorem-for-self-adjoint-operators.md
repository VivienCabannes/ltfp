# Finite-dimensional spectral theorem for self-adjoint operators

Let `E` be a finite-dimensional inner-product space over a real or complex scalar field, and let `T : E -> E` be a self-adjoint linear map. If the dimension of `E` is `n`, then `E` has an orthonormal basis indexed by `Fin n` whose vectors are eigenvectors of `T`. The corresponding eigenvalues are real, and the matrix of `T` in this basis is diagonal.

## Mathlib

Declarations: `LinearMap.IsSymmetric.eigenvectorBasis`, `LinearMap.IsSymmetric.eigenvalues`, `LinearMap.IsSymmetric.apply_eigenvectorBasis`, `LinearMap.IsSymmetric.hasEigenvector_eigenvectorBasis`, `LinearMap.IsSymmetric.toMatrix_eigenvectorBasis`, `LinearMap.isSymmetric_iff_isSelfAdjoint`
File: `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`
