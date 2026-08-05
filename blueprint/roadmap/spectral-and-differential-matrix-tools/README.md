---
kind: roadmap
status: mapped
---

# Spectral and differential matrix tools

Spectral decompositions and the matrix derivatives used throughout the estimators.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Symmetric spectral decomposition
- Positive-semidefinite eigenvalue criterion
- Economy singular value decomposition
- Singular-vector equations
- Gram squared-singular-value spectrum
- Symmetric dilation spectrum
- Gram eigenvectors (Exercise 1.5)
- Dilation eigenvectors (Exercise 1.6)
- Quadratic gradients and Hessians
- Least-squares gradient and Hessian
- Sigmoid definition
- Logistic gradient and Hessian (Exercise 1.7)
- Inverse-trace and log-determinant gradients (Exercise 1.8)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Sections 1.1.4-1.1.5, printed pages 6-7

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Matrix.isHermitian_iff_isSymm`
- `Matrix.IsHermitian.eigenvalues`
- `Matrix.IsHermitian.eigenvectorBasis`
- `Matrix.IsHermitian.mulVec_eigenvectorBasis`
- `Matrix.IsHermitian.eigenvectorUnitary`
- `Matrix.IsHermitian.spectral_theorem`
- `Matrix.IsHermitian.posSemidef_iff_eigenvalues_nonneg`
- `Matrix.PosSemidef.eigenvalues_nonneg`
- `Matrix.posSemidef_iff_isHermitian_and_spectrum_nonneg`
- `LinearMap.singularValues`
- `LinearMap.singularValues_nonneg`
- `LinearMap.singularValues_fin`
- `LinearMap.sq_singularValues_fin`
- `LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues`
- `Matrix.charpoly_mul_comm'`
- `Matrix.charpoly_mul_comm_of_le`
- `HasFDerivAt.inner`
- `fderiv_inner_apply`
- `hasStrictFDerivAt_norm_sq`
- `fderiv_norm_sq_apply`
- `HasFDerivAt.norm_sq`
- `Real.sigmoid`
- `Real.sigmoid_def`
- `Real.hasDerivAt_sigmoid`
- `Real.deriv_sigmoid`
- `hasFDerivAt_ringInverse`
- `fderiv_inverse`
- `Matrix.traceLinearMap`
- `Matrix.derivative_det_one_add_X_smul`

Primary file: `Mathlib/Analysis/Matrix/Spectrum.lean`.

At pinned Mathlib commit 905b95818eb32af7874a58b427f50c1711a5e96c, the real-symmetric spectral decomposition is covered through the Hermitian spectral theorem and Matrix.isHermitian_iff_isSymm; the positive-semidefinite eigenvalue criterion and sigmoid definition/derivative are also direct. LinearMap.sq_singularValues_fin and LinearMap.hasEigenvalue_adjoint_comp_self_sq_singularValues identify squared singular values with the spectrum of the domain Gram operator T* T, while the rectangular charpoly multiplication lemmas relate the two Gram spectra; completing the codomain Gram statement still requires assembly. No economy-SVD factorization or singular-vector API was found, leaving the economy SVD, singular-vector equations, Gram eigenvectors (Exercise 1.5), symmetric dilation spectrum, and dilation eigenvectors (Exercise 1.6) uncovered. Inner-product and squared-norm Frechet derivative lemmas support assembly of the quadratic and least-squares gradients, but no dedicated gradient formulas or Hessian theorems were found. Sigmoid differentiation is present, but the logistic gradient and Hessian (Exercise 1.7) are uncovered. Ring-inverse differentiation, trace linearity, and the polynomial derivative of det(I + tM) at zero provide ingredients for Exercise 1.8, but no exact inverse-trace or log-determinant matrix-gradient theorem was found. Supporting files are Mathlib/Analysis/Matrix/PosDef.lean, Mathlib/Analysis/Matrix/Order.lean, Mathlib/Analysis/InnerProductSpace/SingularValues.lean, Mathlib/LinearAlgebra/Matrix/Charpoly/Basic.lean, Mathlib/Analysis/InnerProductSpace/Calculus.lean, Mathlib/Analysis/SpecialFunctions/Sigmoid.lean, Mathlib/Analysis/Calculus/FDeriv/Mul.lean, Mathlib/LinearAlgebra/Matrix/Trace.lean, and Mathlib/LinearAlgebra/Matrix/Charpoly/Coeff.lean.
