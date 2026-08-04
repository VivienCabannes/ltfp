# Independent coordinates on an infinite product space

For each `i : I`, let `P i` be a probability measure on a measurable space `Omega i`, and let `X i : Omega i -> E i` be measurable, with both families of spaces allowed to depend on `i`. On the product space equipped with `Measure.infinitePi P`, the lifted coordinate functions `omega |-> X i (omega i)` form an independent family.

The index type is arbitrary: no countability, finite-generation, topology, joint measurability, or prior independence assumption is needed. Taking every `X i` to be the identity gives the bare coordinate projections; their marginal maps preserve the corresponding coordinate measures.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_infinitePi`, `MeasureTheory.Measure.infinitePi`, `measurable_pi_apply`, `measurePreserving_eval_infinitePi`, `MeasureTheory.Measure.infinitePi_map_eval`, `MeasureTheory.Measure.infinitePi_map_pi`
File: `Mathlib/Probability/Independence/InfinitePi.lean`
