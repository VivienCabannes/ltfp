---
kind: node
declaration: definition
mathlib: true
---

# Continuous linear maps

Let `R` be a semiring and let `E` and `F` be topological additive commutative monoids equipped with `R`-module structures. A continuous linear map from `E` to `F` is an `R`-linear map bundled with continuity of its underlying function. The type of these maps is written `E ->L[R] F`.

More generally, let `R` and `S` be semirings, let `sigma : R ->+* S`, let `E` carry separate topology, additive-commutative-monoid, and `R`-module structures, and let `F` carry the corresponding structures over `S`. The type `E ->SL[sigma] F` bundles `sigma`-semilinear maps whose underlying functions are continuous. Its definition requires no topology on `R` or `S`; addition and the scalar actions need not be continuous.

## Mathlib

Declarations: `ContinuousLinearMap`, `ContinuousLinearMap.mk`, `ContinuousLinearMap.toLinearMap`, `ContinuousLinearMap.cont`, `ContinuousLinearMap.continuous`, `ContinuousLinearMap.continuous_toLinearMap`, `ContinuousLinearMap.coe_mk`, `ContinuousLinearMap.coe_mk'`
File: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`.

Verified in the pinned checkout. For semirings R and S, a ring homomorphism sigma : R ->+* S, topological additive commutative monoids M and N, and module structures, ContinuousLinearMap bundles a sigma-semilinear map with continuity. The basic structure requires no topology on R or S and no compatibility between scalar multiplication, topology, or addition. The semilinear notation is M ->SL[sigma] N; M ->L[R] N specializes to the identity homomorphism. The listed constructors, coercion lemmas, and continuity projections expose the bundle's exact interface.

## Depends on

This node has no prerequisites.
