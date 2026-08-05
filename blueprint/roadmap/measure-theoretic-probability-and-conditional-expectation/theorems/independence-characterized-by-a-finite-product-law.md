---
kind: node
declaration: lemma
mathlib: true
---

# Independence characterized by a finite product law

Let `I` carry a `Fintype` instance, let `E i` be dependent measurable codomains, and let `P` be a probability measure. If every `X i : Omega -> E i` has law `mu i` under `P`, then the family `X` is independent under `P` if and only if the joint function `omega |-> fun i => X i omega` has law `Measure.pi mu` under `P`.

The marginal laws supply all coordinatewise almost-everywhere measurability hypotheses. No separate joint-measurability or marginal probability assumption is required. The empty finite index type is allowed.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_iff_hasLaw_pi_pi`
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

Verified exactly in the pinned checkout. For dependent measurable codomains, a Fintype index, a probability source measure, arbitrary fixed marginal measures mu i, and hypotheses that every X i has law mu i under P, iIndepFun_iff_hasLaw_pi_pi states that iIndepFun X P is equivalent to the joint function having law Measure.pi mu under P. The marginal HasLaw hypotheses supply coordinatewise almost-everywhere measurability, so no separate measurable, joint-measurable, or marginal probability assumptions are required. Measure.pi is the finite dependent product measure. The forward direction is iIndepFun.hasLaw_pi and does not itself require an explicit probability-measure instance; this theorem is not the arbitrary-index infinitePi variant.

## Depends on

- [Probability measure](../definitions/probability-measure.md)
- [Law of a random variable](../definitions/law-of-a-random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
- [Finite product law of independent random variables](finite-product-law-of-independent-random-variables.md)
