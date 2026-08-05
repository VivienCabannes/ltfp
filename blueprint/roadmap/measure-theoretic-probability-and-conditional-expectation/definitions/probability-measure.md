---
kind: node
declaration: definition
mathlib: true
---

# Probability measure

Let `alpha` be an arbitrary measurable space and let `mu` be a measure on `alpha`. The proposition-valued typeclass `IsProbabilityMeasure mu` has the single defining condition `mu Set.univ = 1`, where the equality is in `ENNReal`.

This condition implies that the underlying type is nonempty and that `mu` is finite and nonzero. The default-measure notation does not by itself provide a probability-measure instance; that property remains a separate assumption. Mathlib also has a bundled `ProbabilityMeasure` subtype whose coercion to `Measure` supplies this typeclass.

## Mathlib

Declarations: `MeasureTheory.IsProbabilityMeasure`, `MeasureTheory.IsProbabilityMeasure.measure_univ`, `MeasureTheory.isProbabilityMeasure_iff`, `MeasureTheory.isProbabilityMeasure_iff_real`, `MeasureTheory.nonempty_of_isProbabilityMeasure`, `MeasureTheory.instIsZeroOrProbabilityMeasureOfIsProbabilityMeasure`, `MeasureTheory.IsZeroOrProbabilityMeasure.toIsFiniteMeasure`, `MeasureTheory.IsProbabilityMeasure.neZero`, `MeasureTheory.IsProbabilityMeasure.ae_neBot`
File: `Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.2 opening, printed page 25

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Measure/Typeclasses/Probability.lean`.

Verified in the pinned checkout. IsProbabilityMeasure is a Prop-valued typeclass on a measure over an arbitrary measurable space, with sole field measure_univ : mu univ = 1 in ENNReal. It requires no topology, nonemptiness, or finiteness assumption; it implies nonemptiness, IsZeroOrProbabilityMeasure and hence IsFiniteMeasure, NeZero mu, and a nontrivial ae filter. The default measure notation P denotes MeasureSpace.volume and is not automatically probabilistic. The separately bundled ProbabilityMeasure type coerces to Measure and supplies this class.

## Depends on

This node has no prerequisites.
