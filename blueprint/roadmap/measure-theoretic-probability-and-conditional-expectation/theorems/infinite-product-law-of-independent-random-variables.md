---
kind: node
declaration: lemma
mathlib: true
---

# Infinite product law of independent random variables

Let `I` be an arbitrary index type and let `E i` be dependent measurable codomains. Suppose that every `X i : Omega -> E i` has law `mu i` under `P`, the family `X` is independent under `P`, and the joint map `omega |-> fun i => X i omega` is `P`-almost-everywhere measurable. Then this joint map has law `Measure.infinitePi mu` under `P`.

No countability, finiteness, or explicit probability-measure hypothesis is required. The separate joint measurability assumption cannot in general be recovered from the coordinate laws for an arbitrary uncountable index type.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun.hasLaw_infinitePi`
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

Verified in the pinned checkout. For an arbitrary index type and dependent measurable codomains, iIndepFun.hasLaw_infinitePi takes marginal HasLaw hypotheses, independence iIndepFun X P, and almost-everywhere measurability of the joint map, and concludes that the joint map has law Measure.infinitePi mu under P. There is no Countable or Fintype assumption and no explicit probability, finite-measure, or sigma-finite instance: independence entails IsProbabilityMeasure P. Coordinatewise HasLaw supplies only coordinatewise almost-everywhere measurability, which is insufficient to infer joint almost-everywhere measurability for an arbitrary uncountable index. The separate converse theorem iIndepFun_iff_hasLaw_Pi_infinitePi requires IsProbabilityMeasure P.

## Depends on

- [Law of a random variable](../definitions/law-of-a-random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
- [Finite product law of independent random variables](finite-product-law-of-independent-random-variables.md)
