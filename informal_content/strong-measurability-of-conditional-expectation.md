# Strong measurability of conditional expectation

Let `m0` be the measurable structure underlying a measure `mu`, let `m` be another measurable structure on the same type, let `E` be a real normed space, and let `f` take values in `E`. The conditional expectation `mu[f | m]` is strongly measurable with respect to `m`.

No inclusion `m <= m0`, trimmed sigma-finiteness, integrability, or completeness assumption is needed. The statement remains true in every invalid branch of the totalized definition because the conditional expectation is then zero.

## Mathlib

Declarations: `MeasureTheory.stronglyMeasurable_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`
