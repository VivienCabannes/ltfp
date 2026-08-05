---
kind: node
declaration: definition
mathlib: true
---

# Bochner integral

Let `G` be a real normed vector space, let `mu` be an arbitrary measure on a measurable space `A`, and let `f : A -> G`. The predicate `Integrable f mu` combines almost-everywhere strong measurability with finiteness of the `lintegral` of the extended norm.

When `G` is complete and `f` is integrable, `MeasureTheory.integral mu f` sends `f` to its `L1` class and applies the continuous `L1` integral, extending the integral of simple functions. The public definition itself requires neither completeness nor integrability. It is totalized to zero when the codomain is incomplete or when `f` is not integrable, including the case where `f` is not almost everywhere strongly measurable. No finite-measure or sigma-finiteness assumption is required.

## Mathlib

Declarations: `MeasureTheory.AEStronglyMeasurable`, `MeasureTheory.HasFiniteIntegral`, `MeasureTheory.Integrable`, `MeasureTheory.Integrable.toL1`, `MeasureTheory.SimpleFunc.integral`, `MeasureTheory.L1.SimpleFunc.integral`, `MeasureTheory.L1.integral`, `MeasureTheory.integral`, `MeasureTheory.integral_eq`, `MeasureTheory.integral_undef`, `MeasureTheory.integral_non_aestronglyMeasurable`, `MeasureTheory.integral_of_not_completeSpace`, `MeasureTheory.SimpleFunc.integral_eq_integral`
File: `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`.

Verified in the pinned checkout. Integrable is the conjunction of AEStronglyMeasurable and HasFiniteIntegral, the latter meaning that the lintegral of the extended norm is finite. With a complete real normed codomain, an integrable function is sent through Integrable.toL1 and L1.integral; the construction extends simple-function integration. The public integral assumes neither completeness nor integrability and is zero for a nonintegrable or non-almost-everywhere-strongly-measurable function or an incomplete codomain. No finite-measure or sigma-finiteness assumption is imposed.

## Depends on

This node has no prerequisites.
