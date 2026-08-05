---
kind: roadmap
status: detailed
---

# Finite-dimensional linear algebra and spectral theory

Mathlib foundations for matrices, positive definiteness, inner products, eigenspaces, and singular values.

## Planning status

This milestone is decomposed into 5 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

This milestone has no coarse prerequisites.

## Candidate contents

- Matrices and linear maps
- Positive semidefinite and positive definite matrices
- Finite-dimensional spectral theorem
- Singular values
- Orthogonal projections

## Detailed nodes

- [Matrix representations of linear maps](definitions/matrix-representations-of-linear-maps.md)
- [Positive semidefinite matrices](definitions/positive-semidefinite-matrices.md)
- [Positive definite matrices](definitions/positive-definite-matrices.md)
- [Finite-dimensional spectral theorem for self-adjoint operators](theorems/finite-dimensional-spectral-theorem-for-self-adjoint-operators.md)
- [Singular values of finite-dimensional linear maps](definitions/singular-values-of-finite-dimensional-linear-maps.md)

## Sources

- [Adopted source map](../../sources/README.md)

## Mathlib assessment

Legacy assessment: `in-mathlib`.

Relevant declarations:

- `Matrix.PosSemidef`
- `Matrix.PosDef`
- `LinearMap.IsSymmetric.eigenvectorBasis`
- `LinearMap.singularValues`
- `Submodule.orthogonalProjectionOnto`

Primary file: `Mathlib/Analysis/InnerProductSpace/Spectrum.lean`.

Verified in the pinned checkout. Matrix positivity is defined in Mathlib/LinearAlgebra/Matrix/PosDef.lean, the symmetric spectral basis in Mathlib/Analysis/InnerProductSpace/Spectrum.lean, singular values in Mathlib/Analysis/InnerProductSpace/SingularValues.lean, and orthogonal projection in Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean. The singular-value API exposes Gram-spectrum values rather than a complete singular-vector decomposition. The generic projection declaration requires HasOrthogonalProjection; finite-dimensional completeness supplies the intended specialization.
