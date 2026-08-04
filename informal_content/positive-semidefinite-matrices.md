# Positive semidefinite matrices

Let `R` be a ring equipped with a partial order and a star-ring structure, and let `M` be a square matrix over `R`. The matrix `M` is positive semidefinite when it is Hermitian and, for every finitely supported coordinate vector `x`, the quadratic expression

`sum_i sum_j star (x i) * M i j * x j`

is nonnegative.

## Mathlib

Declarations: `Matrix.PosSemidef`
File: `Mathlib/LinearAlgebra/Matrix/PosDef.lean`
