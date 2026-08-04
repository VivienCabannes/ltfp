# Random variable

Let `Omega` and `E` be types with measurable-space structures. A function `X : Omega -> E` is measurable when the inverse image under `X` of every measurable subset of `E` is measurable in `Omega`. This predicate requires no measure or probability-measure assumption. Measurable functions are closed under composition and are almost everywhere measurable with respect to any chosen measure.

Mathlib has no separate `RandomVariable` alias; the canonical predicate for this concept is `Measurable`. Its measure-dependent relaxation `AEMeasurable` is distinct from strong measurability, which also requires topological structure.

## Mathlib

Declarations: `Measurable`, `Measurable.comp`, `AEMeasurable`, `Measurable.aemeasurable`
File: `Mathlib/MeasureTheory/MeasurableSpace/Defs.lean`
