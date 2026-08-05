---
kind: node
declaration: lemma
mathlib: true
---

# Finite product law of independent random variables

Let `I` be a finite index type and let `E i` be a dependent family of measurable codomains. Suppose that each `X i : Omega -> E i` has law `mu i` under an arbitrary measure `P` and that the family `X` is independent under `P`. Then the joint function `omega |-> fun i => X i omega` has law `Measure.pi mu` under `P`.

The marginal-law hypotheses already supply almost-everywhere measurability. No separate joint-measurability, probability, finite-measure, or sigma-finiteness assumption is required; independence itself normalizes `P`. Here `Measure.pi mu` is the coordinate-indexed finite Pi product.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun.hasLaw_pi`
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

Verified in the pinned checkout. For a Fintype-indexed family with dependent measurable codomains, iIndepFun.hasLaw_pi takes marginal HasLaw hypotheses and iIndepFun X P and concludes that the joint map has law Measure.pi mu. Each HasLaw hypothesis already supplies P-almost-everywhere measurability, so no separate coordinatewise or joint measurability hypothesis is needed. The theorem has no explicit probability, finite-measure, or sigma-finite instance: iIndepFun itself entails IsProbabilityMeasure P. Measure.pi mu is the coordinate-indexed finite Pi product. The converse iIndepFun_iff_hasLaw_pi_pi is a distinct theorem and requires IsProbabilityMeasure P.

## Depends on

- [Law of a random variable](../definitions/law-of-a-random-variable.md)
- [Independent family of random variables](../definitions/independent-family-of-random-variables.md)
