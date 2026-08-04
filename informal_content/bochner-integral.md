# Bochner integral

Let `G` be a real normed vector space, let `mu` be an arbitrary measure on a measurable space `A`, and let `f : A -> G`. The predicate `Integrable f mu` combines almost-everywhere strong measurability with finiteness of the `lintegral` of the extended norm.

When `G` is complete and `f` is integrable, `MeasureTheory.integral mu f` sends `f` to its `L1` class and applies the continuous `L1` integral, extending the integral of simple functions. The public definition itself requires neither completeness nor integrability. It is totalized to zero when the codomain is incomplete or when `f` is not integrable, including the case where `f` is not almost everywhere strongly measurable. No finite-measure or sigma-finiteness assumption is required.

## Mathlib

Declarations: `MeasureTheory.AEStronglyMeasurable`, `MeasureTheory.HasFiniteIntegral`, `MeasureTheory.Integrable`, `MeasureTheory.Integrable.toL1`, `MeasureTheory.SimpleFunc.integral`, `MeasureTheory.L1.SimpleFunc.integral`, `MeasureTheory.L1.integral`, `MeasureTheory.integral`, `MeasureTheory.integral_eq`, `MeasureTheory.integral_undef`, `MeasureTheory.integral_non_aestronglyMeasurable`, `MeasureTheory.integral_of_not_completeSpace`, `MeasureTheory.SimpleFunc.integral_eq_integral`
File: `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`
