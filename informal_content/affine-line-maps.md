# Affine line maps

Let `k` be a ring, let `V` be an additive commutative group and a `k`-module, and let `P` be an affine space modeled on `V`. For `p0, p1 : P`, the affine line map

`AffineMap.lineMap p0 p1 : k ->a[k] P`

has value `p0` at zero and `p1` at one. When `P = k`, its value at `c : k` is

`(1 - c) * p0 + c * p1`.

## Mathlib

Declarations: `AffineMap.lineMap`, `AffineMap.lineMap_apply_ring`, `AffineMap.lineMap_apply_zero`, `AffineMap.lineMap_apply_one`
File: `Mathlib/LinearAlgebra/AffineSpace/AffineMap.lean`
