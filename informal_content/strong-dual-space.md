# Strong dual space

Let `R` be a semiring with a topology and let `E` be a topological additive commutative monoid that is an `R`-module. The abbreviation `StrongDual R E` is the type `E ->L[R] R` of continuous `R`-linear functionals on `E`.

The definition itself requires no compatibility between the topology and the algebraic operations. It is distinct from the algebraic dual `Module.Dual R E`. Under the additional commutativity and continuity hypotheses required to form it, `WeakDual R E` is a type synonym for the same continuous functionals equipped with the weak-star topology.

## Mathlib

Declarations: `StrongDual`
File: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`
