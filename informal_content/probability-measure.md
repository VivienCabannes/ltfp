# Probability measure

Let `alpha` be an arbitrary measurable space and let `mu` be a measure on `alpha`. The proposition-valued typeclass `IsProbabilityMeasure mu` has the single defining condition `mu Set.univ = 1`, where the equality is in `ENNReal`.

This condition implies that the underlying type is nonempty and that `mu` is finite and nonzero. The default-measure notation does not by itself provide a probability-measure instance; that property remains a separate assumption. Mathlib also has a bundled `ProbabilityMeasure` subtype whose coercion to `Measure` supplies this typeclass.

## Mathlib

Declarations: `MeasureTheory.IsProbabilityMeasure`, `MeasureTheory.IsProbabilityMeasure.measure_univ`, `MeasureTheory.isProbabilityMeasure_iff`, `MeasureTheory.isProbabilityMeasure_iff_real`, `MeasureTheory.nonempty_of_isProbabilityMeasure`, `MeasureTheory.instIsZeroOrProbabilityMeasureOfIsProbabilityMeasure`, `MeasureTheory.IsZeroOrProbabilityMeasure.toIsFiniteMeasure`, `MeasureTheory.IsProbabilityMeasure.neZero`, `MeasureTheory.IsProbabilityMeasure.ae_neBot`
File: `Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean`
