---
kind: node
declaration: lemma
mathlib: true
---

# Independent coordinates on an infinite product space

For each `i : I`, let `P i` be a probability measure on a measurable space `Omega i`, and let `X i : Omega i -> E i` be measurable, with both families of spaces allowed to depend on `i`. On the product space equipped with `Measure.infinitePi P`, the lifted coordinate functions `omega |-> X i (omega i)` form an independent family.

The index type is arbitrary: no countability, finite-generation, topology, joint measurability, or prior independence assumption is needed. Taking every `X i` to be the identity gives the bare coordinate projections; their marginal maps preserve the corresponding coordinate measures.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_infinitePi`, `MeasureTheory.Measure.infinitePi`, `measurable_pi_apply`, `measurePreserving_eval_infinitePi`, `MeasureTheory.Measure.infinitePi_map_eval`, `MeasureTheory.Measure.infinitePi_map_pi`
File: `Mathlib/Probability/Independence/InfinitePi.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.1, printed pages 22-24

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/Independence/InfinitePi.lean`.

Verified in the pinned checkout. The theorem allows an arbitrary index type and dependent coordinate and codomain types with only measurable-space structures. It requires every P i to be a probability measure and every X i to be measurable, and concludes independence of the lifted maps under the explicit measure Measure.infinitePi P. It assumes no countability, countable-generation, topology, joint measurability, or prior independence. Bare projections follow by taking X i = id and are measurable by measurable_pi_apply. Measure.infinitePi is zero outside its probability-measure branch; the theorem's hypotheses select the product probability measure.

## Depends on

- [Probability measure](../definitions/probability-measure.md)
- [Random variable](../definitions/random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
- [Independence characterized by an infinite product law](independence-characterized-by-an-infinite-product-law.md)
