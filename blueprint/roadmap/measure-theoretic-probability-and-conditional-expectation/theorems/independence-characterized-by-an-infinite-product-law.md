---
kind: node
declaration: lemma
mathlib: true
---

# Independence characterized by an infinite product law

Let `I` be an arbitrary index type, let `E i` be dependent measurable codomains, and let `P` be a probability measure. Suppose that every `X i : Omega -> E i` has law `mu i` under `P` and that the joint map `omega |-> fun i => X i omega` is `P`-almost-everywhere measurable. Then `X` is an independent family under `P` if and only if the joint map has law `Measure.infinitePi mu` under `P`.

There is no countability or finiteness assumption on `I` and no separate probability assumption on the marginal measures. The full joint almost-everywhere-measurability hypothesis is essential for arbitrary uncountable products and does not follow from the coordinate laws alone.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_iff_hasLaw_Pi_infinitePi`
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

Verified in the pinned checkout. For an arbitrary index type and dependent measurable codomains, iIndepFun_iff_hasLaw_Pi_infinitePi assumes IsProbabilityMeasure P, marginal HasLaw hypotheses, and almost-everywhere measurability of the complete joint map. It states both directions between iIndepFun X P and the joint map having law Measure.infinitePi mu. There is no Countable or Fintype assumption and no explicit marginal probability-measure assumption. The forward implication is iIndepFun.hasLaw_infinitePi; coordinatewise almost-everywhere measurability from the marginal laws does not imply joint almost-everywhere measurability for an arbitrary uncountable index. This is distinct from the Fintype theorem iIndepFun_iff_hasLaw_pi_pi, whose target is Measure.pi mu and which needs no separate joint-measurability hypothesis.

## Depends on

- [Probability measure](../definitions/probability-measure.md)
- [Law of a random variable](../definitions/law-of-a-random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
- [Infinite product law of independent random variables](infinite-product-law-of-independent-random-variables.md)
- [Independence characterized by a finite product law](independence-characterized-by-a-finite-product-law.md)
