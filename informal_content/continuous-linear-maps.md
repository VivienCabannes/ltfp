# Continuous linear maps

Let `R` be a semiring and let `E` and `F` be topological additive commutative monoids equipped with `R`-module structures. A continuous linear map from `E` to `F` is an `R`-linear map bundled with continuity of its underlying function. The type of these maps is written `E ->L[R] F`.

More generally, let `R` and `S` be semirings, let `sigma : R ->+* S`, let `E` carry separate topology, additive-commutative-monoid, and `R`-module structures, and let `F` carry the corresponding structures over `S`. The type `E ->SL[sigma] F` bundles `sigma`-semilinear maps whose underlying functions are continuous. Its definition requires no topology on `R` or `S`; addition and the scalar actions need not be continuous.

## Mathlib

Declarations: `ContinuousLinearMap`, `ContinuousLinearMap.mk`, `ContinuousLinearMap.toLinearMap`, `ContinuousLinearMap.cont`, `ContinuousLinearMap.continuous`, `ContinuousLinearMap.continuous_toLinearMap`, `ContinuousLinearMap.coe_mk`, `ContinuousLinearMap.coe_mk'`
File: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`
