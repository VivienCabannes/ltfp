# Matrix representations of linear maps

Let `R` be a commutative semiring, and let `M` and `N` be additive commutative monoids with `R`-module structures and finite bases indexed by `n` and `m`, respectively. Sending an `R`-linear map from `M` to `N` to its coefficient matrix in these bases is an `R`-linear equivalence with `Matrix m n R`. Its inverse sends a matrix to the linear map whose coordinate vector is obtained by multiplying that matrix by the coordinate vector of the input.

## Mathlib

Declarations: `LinearMap.toMatrix`, `Matrix.toLin`, `Matrix.toLin_toMatrix`, `LinearMap.toMatrix_toLin`, `Matrix.repr_toLin`
File: `Mathlib/LinearAlgebra/Matrix/ToLin.lean`
