# Law of a random variable

Let `P` be an arbitrary measure on a measurable space `Omega`, let `mu` be an arbitrary measure on a measurable space `E`, and let `X : Omega -> E`. The proposition `HasLaw X mu P` consists of both `P`-almost-everywhere measurability of `X` and the pushforward identity `P.map X = mu`.

Neither measure is assumed finite or probabilistic. The explicit measurability field is essential because `Measure.map` is totalized to zero outside the almost-everywhere-measurable case. A law transports finiteness and the probability-measure property between `P` and `mu`; the API also provides event-measure identities, almost-everywhere congruence, measure-preserving bridges, and composition laws.

## Mathlib

Declarations: `ProbabilityTheory.HasLaw`, `ProbabilityTheory.HasLaw.aemeasurable`, `ProbabilityTheory.HasLaw.map_eq`, `ProbabilityTheory.HasLaw.measure_eq`, `ProbabilityTheory.HasLaw.measureReal_eq`, `ProbabilityTheory.HasLaw.comp_of_hasLaw_comp`, `ProbabilityTheory.HasLaw.congr`, `ProbabilityTheory.hasLaw_congr`, `MeasureTheory.MeasurePreserving.hasLaw`, `ProbabilityTheory.HasLaw.measurePreserving`, `ProbabilityTheory.HasLaw.id`, `ProbabilityTheory.HasLaw.ae_iff`, `ProbabilityTheory.HasLaw.isFiniteMeasure_iff`, `ProbabilityTheory.HasLaw.isProbabilityMeasure_iff`, `ProbabilityTheory.HasLaw.comp`, `ProbabilityTheory.HasLaw.fun_comp`
File: `Mathlib/Probability/HasLaw.lean`
