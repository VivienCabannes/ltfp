# Almost-everywhere uniqueness of the Radon-Nikodym derivative

Let `nu` be sigma-finite. If `f : alpha -> ENNReal` is measurable, `s` is mutually singular with `nu`, and `mu = s + nu.withDensity f`, then `f = mu.rnDeriv nu` almost everywhere with respect to `nu`. No sigma-finiteness assumption on `mu` is needed. An analogous theorem weakens measurability of `f` to almost-everywhere measurability.

Thus a density is determined only up to `nu`-almost-everywhere equality, not by unrestricted pointwise equality. A related measure-level theorem identifies the two weighted measures before sigma-finite uniqueness converts that equality back to equality of density functions.

## Mathlib

Declarations: `MeasureTheory.Measure.eq_rnDeriv`, `MeasureTheory.Measure.eq_rnDeriv₀`, `MeasureTheory.Measure.eq_withDensity_rnDeriv`, `MeasureTheory.Measure.eq_withDensity_rnDeriv₀`, `MeasureTheory.Measure.measurable_rnDeriv`, `MeasureTheory.withDensity_eq_iff_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`
