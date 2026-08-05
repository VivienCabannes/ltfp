---
kind: node
declaration: definition
mathlib: true
---

# Positive semidefinite matrices

Let `R` be a ring equipped with a partial order and a star-ring structure, and let `M` be a square matrix over `R`. The matrix `M` is positive semidefinite when it is Hermitian and, for every finitely supported coordinate vector `x`, the quadratic expression

`sum_i sum_j star (x i) * M i j * x j`

is nonnegative.

## Mathlib

Declarations: `Matrix.PosSemidef`
File: `Mathlib/LinearAlgebra/Matrix/PosDef.lean`


## Roadmap and coverage

- [Finite-dimensional linear algebra and spectral theory](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.1.4, printed page 6

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/LinearAlgebra/Matrix/PosDef.lean`.

Verified in the pinned checkout. Matrix.PosSemidef assumes independent Ring, PartialOrder, and StarRing structures, with no additional order compatibility; it quantifies over finitely supported vectors on an arbitrary index type.

## Depends on

This node has no prerequisites.
