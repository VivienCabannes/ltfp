---
kind: node
declaration: theorem
mathlib: true
---

# Almost-everywhere uniqueness of the Radon-Nikodym derivative

Let `nu` be sigma-finite. If `f : alpha -> ENNReal` is measurable, `s` is mutually singular with `nu`, and `mu = s + nu.withDensity f`, then `f = mu.rnDeriv nu` almost everywhere with respect to `nu`. No sigma-finiteness assumption on `mu` is needed. An analogous theorem weakens measurability of `f` to almost-everywhere measurability.

Thus a density is determined only up to `nu`-almost-everywhere equality, not by unrestricted pointwise equality. A related measure-level theorem identifies the two weighted measures before sigma-finite uniqueness converts that equality back to equality of density functions.

## Mathlib

Declarations: `MeasureTheory.Measure.eq_rnDeriv`, `MeasureTheory.Measure.eq_rnDeriv₀`, `MeasureTheory.Measure.eq_withDensity_rnDeriv`, `MeasureTheory.Measure.eq_withDensity_rnDeriv₀`, `MeasureTheory.Measure.measurable_rnDeriv`, `MeasureTheory.withDensity_eq_iff_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`.

Verified in the pinned checkout. With SigmaFinite nu, a measurable f : alpha -> ENNReal, s mutually singular with nu, and mu = s + nu.withDensity f, eq_rnDeriv proves f = mu.rnDeriv nu almost everywhere with respect to nu. No sigma-finiteness assumption on mu or pre-existing decomposition instance is required. The eq_rnDeriv₀ variant needs only AEMeasurable f nu. Measure-level withDensity uniqueness does not require sigma-finiteness; the function-level result uses withDensity_eq_iff_of_sigmaFinite and measurable_rnDeriv. This is distinct from the absolute-continuity reconstruction theorem.

## Depends on

- [Radon-Nikodym derivative of measures](../definitions/radon-nikodym-derivative-of-measures.md)
- [Measurability of the Radon-Nikodym derivative](measurability-of-the-radon-nikodym-derivative.md)
