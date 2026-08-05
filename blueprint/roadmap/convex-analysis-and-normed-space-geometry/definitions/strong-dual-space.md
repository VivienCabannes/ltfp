---
kind: node
declaration: definition
mathlib: true
---

# Strong dual space

Let `R` be a semiring with a topology and let `E` be a topological additive commutative monoid that is an `R`-module. The abbreviation `StrongDual R E` is the type `E ->L[R] R` of continuous `R`-linear functionals on `E`.

The definition itself requires no compatibility between the topology and the algebraic operations. It is distinct from the algebraic dual `Module.Dual R E`. Under the additional commutativity and continuity hypotheses required to form it, `WeakDual R E` is a type synonym for the same continuous functionals equipped with the weak-star topology.

## Mathlib

Declarations: `StrongDual`
File: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`


## Roadmap and coverage

- [Convex analysis and normed-space geometry](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean`.

Verified in the pinned checkout. StrongDual R E is the abbreviation E ->L[R] R under Semiring R, TopologicalSpace R, TopologicalSpace E, AddCommMonoid E, and Module R E. Its definition requires no topology-algebra compatibility assumptions. It is distinct from the algebraic dual Module.Dual R E and from WeakDual R E, which equips the same continuous functionals with the weak-star topology.

## Depends on

- [Continuous linear maps](continuous-linear-maps.md)
