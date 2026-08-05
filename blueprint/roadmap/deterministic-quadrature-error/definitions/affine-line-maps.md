---
kind: node
declaration: definition
mathlib: true
---

# Affine line maps

Let `k` be a ring, let `V` be an additive commutative group and a `k`-module, and let `P` be an affine space modeled on `V`. For `p0, p1 : P`, the affine line map

`AffineMap.lineMap p0 p1 : k ->a[k] P`

has value `p0` at zero and `p1` at one. When `P = k`, its value at `c : k` is

`(1 - c) * p0 + c * p1`.

## Mathlib

Declarations: `AffineMap.lineMap`, `AffineMap.lineMap_apply_ring`, `AffineMap.lineMap_apply_zero`, `AffineMap.lineMap_apply_one`
File: `Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean`


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean`.

Verified in the pinned checkout. AffineMap.lineMap p0 p1 is the affine map taking parameter zero to p0 and one to p1. For points in the scalar ring, lineMap_apply_ring gives (1 - c) * p0 + c * p1. The definition requires a ring, a module over an additive commutative group, and an affine torsor; it has no distinct-endpoint premise.

## Depends on

This node has no prerequisites.
