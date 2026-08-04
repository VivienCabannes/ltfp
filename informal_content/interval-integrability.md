# Interval integrability

Let `E` be a topological extended-normed additive monoid, let `f : Real -> E`, let `mu` be an arbitrary measure on the real line, and let `a b : Real`. The predicate `IntervalIntegrable f mu a b` means that `f` is integrable on both `Set.Ioc a b` and `Set.Ioc b a`.

For a pseudometrizable codomain this is equivalent to integrability on the unordered half-open interval `Set.uIoc a b`, and the property is symmetric in `a` and `b`. Equivalence with the unordered closed interval `Set.uIcc a b`, or with `Set.Icc a b` when `a <= b`, additionally requires `NullSingletonClass mu` and finiteness of the extended norm at the relevant endpoint. Without the singleton-null assumption, integrability on the closed interval still implies interval integrability but need not be equivalent to it.

## Mathlib

Declarations: `IntervalIntegrable`, `intervalIntegrable_iff`, `IntervalIntegrable.def'`, `intervalIntegrable_iff_integrableOn_Ioc_of_le`, `intervalIntegrable_iff'`, `intervalIntegrable_iff_integrableOn_Icc_of_le`, `IntervalIntegrable.symm_iff`, `MeasureTheory.IntegrableOn.intervalIntegrable`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/Basic.lean`
