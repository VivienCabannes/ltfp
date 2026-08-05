---
kind: node
declaration: theorem
mathlib: true
---

# Measurability of the Radon-Nikodym derivative

For any measures `mu` and `nu` on the same measurable space, the `ENNReal`-valued function `mu.rnDeriv nu` is measurable.

## Mathlib

Declarations: `MeasureTheory.Measure.measurable_rnDeriv`
File: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`.

The verified theorem is unconditional because the definition is zero when no decomposition instance exists.

## Depends on

- [Radon-Nikodym derivative of measures](../definitions/radon-nikodym-derivative-of-measures.md)
