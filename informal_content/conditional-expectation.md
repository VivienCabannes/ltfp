# Conditional expectation

Let `E` be a real normed space, let `mu` be a measure for a measurable structure `m0` on `alpha`, let `m` be another measurable structure on `alpha`, and let `f : alpha -> E`. The noncomputable function `mu[f | m]` is the pointwise representative of the conditional expectation of `f` with respect to `m`. The definition itself does not require `E` to be complete.

This totalized definition is zero if `m` is not below `m0`, if the trimmed measure along that inclusion is not sigma-finite, or if `f` is not Bochner integrable. Under the valid hypotheses it returns `f` when `f` is already strongly measurable with respect to `m`; otherwise it chooses the strongly measurable representative constructed through `condExpL1`.

## Mathlib

Declarations: `MeasureTheory.condExp`, `MeasureTheory.condExpL1`, `MeasureTheory.condExp_of_not_le`, `MeasureTheory.condExp_of_not_sigmaFinite`, `MeasureTheory.condExp_of_not_integrable`, `MeasureTheory.condExp_of_sigmaFinite`, `MeasureTheory.condExp_of_stronglyMeasurable`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`
