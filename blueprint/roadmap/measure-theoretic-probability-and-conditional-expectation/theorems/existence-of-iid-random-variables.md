---
kind: node
declaration: lemma
mathlib: true
---

# Existence of iid random variables

Let `I` be any index type and let `mu` be a probability measure on an arbitrary measurable space `E`. There exist a measurable space `Omega`, a probability measure `P` on it, and a family `X i : Omega -> E` such that every `X i` is measurable, every `X i` has law `mu` under `P`, and the family is independent under `P`.

The index type may be empty or uncountable. No topology, countable-generation, standard-Borel, or nonemptiness hypothesis is required. The noncomputable construction uses the full product space, its Pi measurable structure, the infinite product measure, and coordinate evaluation maps. Pairwise identical distribution follows from the common law but is not a separate conclusion of the theorem.

## Mathlib

Declarations: `ProbabilityTheory.exists_iid`, `ProbabilityTheory.exists_hasLaw_indepFun`
File: `Mathlib/Probability/HasLawExists.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.1, printed pages 22-24

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/HasLawExists.lean`.

Verified in the pinned checkout. exists_iid allows an arbitrary, possibly empty or uncountable index type and assumes only a measurable-space structure on the target and IsProbabilityMeasure mu. It returns a source measurable space, a probability measure P, and measurable maps X i with common HasLaw mu and iIndepFun X P. Its implementation uses the full product space, MeasurableSpace.pi, Measure.infinitePi, and coordinate evaluations. No countability, nonemptiness, countable-generation, or standard-Borel hypotheses occur. IdentDistrib is not in the conclusion, although the common HasLaw witnesses imply pairwise IdentDistrib. The product-measure construction is noncomputable and transitively uses Classical.choice.

## Depends on

- [Probability measure](../definitions/probability-measure.md)
- [Random variable](../definitions/random-variable.md)
- [Law of a random variable](../definitions/law-of-a-random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
- [Independent coordinates on an infinite product space](independent-coordinates-on-an-infinite-product-space.md)
