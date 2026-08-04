# Radon-Nikodym representation theorem

Let `mu` and `nu` be measures with `HaveLebesgueDecomposition mu nu`. Then `mu` is absolutely continuous with respect to the reference measure `nu` if and only if weighting `nu` by the `ENNReal`-valued density `mu.rnDeriv nu` recovers `mu`:

`nu.withDensity (mu.rnDeriv nu) = mu`.

The standard decomposition instance is available when `mu` is s-finite and `nu` is sigma-finite; in particular, two sigma-finite measures suffice. Although `rnDeriv` is totalized outside this setting, the representation theorem still requires the decomposition instance.

## Mathlib

Declarations: `MeasureTheory.Measure.absolutelyContinuous_iff_withDensity_rnDeriv_eq`, `MeasureTheory.Measure.withDensity_rnDeriv_eq`, `MeasureTheory.Measure.haveLebesgueDecomposition_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/RadonNikodym.lean`
