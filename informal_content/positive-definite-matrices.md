# Positive definite matrices

Let `R` be a ring equipped with a partial order and a star-ring structure, and let `M` be a square matrix over `R`. The matrix `M` is positive definite when it is Hermitian and, for every nonzero finitely supported coordinate vector `x`, the quadratic expression

`sum_i sum_j star (x i) * M i j * x j`

is strictly positive.

## Mathlib

Declarations: `Matrix.PosDef`
File: `Mathlib/LinearAlgebra/Matrix/PosDef.lean`
