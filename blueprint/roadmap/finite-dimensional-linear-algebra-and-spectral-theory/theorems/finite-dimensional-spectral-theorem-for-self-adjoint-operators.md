---
kind: node
declaration: theorem
mathlib: true
---

# Finite-dimensional spectral theorem for self-adjoint operators

Let `E` be a finite-dimensional inner-product space over a real or complex scalar field, and let `T : E -> E` be a self-adjoint linear map. If the dimension of `E` is `n`, then `E` has an orthonormal basis indexed by `Fin n` whose vectors are eigenvectors of `T`. The corresponding eigenvalues are real, and the matrix of `T` in this basis is diagonal.

## Mathlib

Declarations: `LinearMap.IsSymmetric.eigenvectorBasis`, `LinearMap.IsSymmetric.eigenvalues`, `LinearMap.IsSymmetric.apply_eigenvectorBasis`, `LinearMap.IsSymmetric.hasEigenvector_eigenvectorBasis`, `LinearMap.IsSymmetric.toMatrix_eigenvectorBasis`, `LinearMap.isSymmetric_iff_isSelfAdjoint`
File: `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`


## Roadmap and coverage

- [Finite-dimensional linear algebra and spectral theory](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.1.4, printed page 6

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`.

Verified in the pinned checkout over RCLike scalars and finite-dimensional inner-product spaces. The isSymmetric/isSelfAdjoint equivalence bridges terminology; the eigenbasis has real eigenvalues and toMatrix_eigenvectorBasis supplies the literal diagonal representation.

## Depends on

- [Matrix representations of linear maps](../definitions/matrix-representations-of-linear-maps.md)
