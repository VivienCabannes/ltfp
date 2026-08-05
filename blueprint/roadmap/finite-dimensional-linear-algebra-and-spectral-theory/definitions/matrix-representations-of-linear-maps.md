---
kind: node
declaration: definition
mathlib: true
---

# Matrix representations of linear maps

Let `R` be a commutative semiring, and let `M` and `N` be additive commutative monoids with `R`-module structures and finite bases indexed by `n` and `m`, respectively. Sending an `R`-linear map from `M` to `N` to its coefficient matrix in these bases is an `R`-linear equivalence with `Matrix m n R`. Its inverse sends a matrix to the linear map whose coordinate vector is obtained by multiplying that matrix by the coordinate vector of the input.

## Mathlib

Declarations: `LinearMap.toMatrix`, `Matrix.toLin`, `Matrix.toLin_toMatrix`, `LinearMap.toMatrix_toLin`, `Matrix.repr_toLin`
File: `Mathlib/LinearAlgebra/Matrix/ToLin.lean`


## Roadmap and coverage

- [Finite-dimensional linear algebra and spectral theory](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/LinearAlgebra/Matrix/ToLin.lean`.

Verified in the pinned checkout. LinearMap.toMatrix and Matrix.toLin are inverse linear equivalences already over a commutative semiring; Matrix.toLin_toMatrix and LinearMap.toMatrix_toLin state the inverse laws, and Matrix.repr_toLin states the coordinate-vector multiplication formula.

## Depends on

This node has no prerequisites.
