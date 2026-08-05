---
kind: node
declaration: definition
mathlib: true
---

# Law of a random variable

Let `P` be an arbitrary measure on a measurable space `Omega`, let `mu` be an arbitrary measure on a measurable space `E`, and let `X : Omega -> E`. The proposition `HasLaw X mu P` consists of both `P`-almost-everywhere measurability of `X` and the pushforward identity `P.map X = mu`.

Neither measure is assumed finite or probabilistic. The explicit measurability field is essential because `Measure.map` is totalized to zero outside the almost-everywhere-measurable case. A law transports finiteness and the probability-measure property between `P` and `mu`; the API also provides event-measure identities, almost-everywhere congruence, measure-preserving bridges, and composition laws.

## Mathlib

Declarations: `ProbabilityTheory.HasLaw`, `ProbabilityTheory.HasLaw.aemeasurable`, `ProbabilityTheory.HasLaw.map_eq`, `ProbabilityTheory.HasLaw.measure_eq`, `ProbabilityTheory.HasLaw.measureReal_eq`, `ProbabilityTheory.HasLaw.comp_of_hasLaw_comp`, `ProbabilityTheory.HasLaw.congr`, `ProbabilityTheory.hasLaw_congr`, `MeasureTheory.MeasurePreserving.hasLaw`, `ProbabilityTheory.HasLaw.measurePreserving`, `ProbabilityTheory.HasLaw.id`, `ProbabilityTheory.HasLaw.ae_iff`, `ProbabilityTheory.HasLaw.isFiniteMeasure_iff`, `ProbabilityTheory.HasLaw.isProbabilityMeasure_iff`, `ProbabilityTheory.HasLaw.comp`, `ProbabilityTheory.HasLaw.fun_comp`
File: `Mathlib/Probability/HasLaw.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.1, printed pages 22-24

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/HasLaw.lean`.

Verified in the pinned checkout. HasLaw X mu P is a Prop structure with fields AEMeasurable X P and P.map X = mu. It assumes only measurable-space structures and arbitrary source and target measures; neither measure must initially be finite or probabilistic. Measure.map is totalized to zero for non-almost-everywhere-measurable functions, so the explicit measurability field is essential. HasLaw.isProbabilityMeasure_iff transfers the probability-measure property between P and mu. Law uniqueness follows immediately from the map_eq projections, although no dedicated uniqueness declaration was found. The core API also supplies event-measure identities, almost-everywhere congruence, MeasurePreserving bridges, identity and composition laws.

## Depends on

- [Random variable](random-variable.md)
