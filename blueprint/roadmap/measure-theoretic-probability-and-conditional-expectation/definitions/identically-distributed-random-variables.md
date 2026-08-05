---
kind: node
declaration: definition
mathlib: true
---

# Identically distributed random variables

Let `X : Omega -> E` and `Y : Omega' -> E` be functions from potentially different measurable source spaces into a common measurable codomain, with arbitrary measures `P` and `Q`. The proposition `IdentDistrib X Y P Q` requires that each function is almost everywhere measurable for its own measure and that their pushforward measures agree: `P.map X = Q.map Y`.

No probability or finiteness assumption is required. Identical distribution is reflexive for an almost-everywhere-measurable function, symmetric, and transitive. A common `HasLaw` witness implies identical distribution, and identical distribution transports any law from either function to the other.

## Mathlib

Declarations: `ProbabilityTheory.IdentDistrib`, `ProbabilityTheory.IdentDistrib.aemeasurable_fst`, `ProbabilityTheory.IdentDistrib.aemeasurable_snd`, `ProbabilityTheory.IdentDistrib.map_eq`, `ProbabilityTheory.IdentDistrib.refl`, `ProbabilityTheory.IdentDistrib.symm`, `ProbabilityTheory.IdentDistrib.trans`, `ProbabilityTheory.IdentDistrib.comp_of_aemeasurable`, `ProbabilityTheory.IdentDistrib.comp`, `ProbabilityTheory.IdentDistrib.measure_mem_eq`, `ProbabilityTheory.HasLaw.identDistrib`, `ProbabilityTheory.IdentDistrib.hasLaw`
File: `Mathlib/Probability/IdentDistrib.lean`


## Roadmap and coverage

- [Measure-theoretic probability and conditional expectation](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10
- `sources/ltfp_book.pdf` — Chapter 2, Section 2.1, printed pages 22-24

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/IdentDistrib.lean`.

Verified in the pinned checkout. IdentDistrib f g mu nu is a Prop structure for functions from potentially different measurable source spaces into one common measurable codomain. It requires AEMeasurable f mu, AEMeasurable g nu, and Measure.map f mu = Measure.map g nu. The measures are arbitrary and need not be probability or finite measures. Reflexivity requires almost-everywhere measurability; symmetry and transitivity are available. Common HasLaw witnesses imply IdentDistrib, while IdentDistrib transports any law in either direction using symmetry. No separately named HasLaw equivalence declaration exists.

## Depends on

- [Random variable](random-variable.md)
- [Law of a random variable](law-of-a-random-variable.md)
