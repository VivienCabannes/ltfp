# Radon-Nikodym derivative of measures

For measures `mu` and `nu` on the same measurable space, `mu.rnDeriv nu` is a noncomputable, total `ENNReal`-valued function. The definition internally tests whether `HaveLebesgueDecomposition mu nu` holds. When it does, the function is the selected measurable density in

`mu = mu.singularPart nu + nu.withDensity (mu.rnDeriv nu)`.

When no such decomposition exists, the derivative is exactly the zero function. The public definition itself has no finiteness assumptions; `SFinite mu` together with `SigmaFinite nu` supplies the standard decomposition instance.

## Mathlib

Declarations: `MeasureTheory.Measure.HaveLebesgueDecomposition`, `MeasureTheory.Measure.rnDeriv`, `MeasureTheory.Measure.rnDeriv_of_not_haveLebesgueDecomposition`, `MeasureTheory.Measure.haveLebesgueDecomposition_spec`, `MeasureTheory.Measure.haveLebesgueDecomposition_of_sigmaFinite`
File: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`
