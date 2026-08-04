# Integrability of conditional expectation

Let `m0` be the measurable structure underlying a measure `mu`, let `m` be another measurable structure on the same type, let `E` be a complete real normed space, and let `f` take values in `E`. The conditional expectation `mu[f | m]` is Bochner integrable with respect to `mu`.

No input-integrability, inclusion `m <= m0`, or trimmed sigma-finiteness hypothesis is required. In every invalid branch of the totalized definition, the conditional expectation is the zero function. Completeness of `E` is an assumption of the integrability theorem itself.

## Mathlib

Declarations: `MeasureTheory.integrable_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`
