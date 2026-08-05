---
kind: node
declaration: theorem
mathlib: true
---

# Scalar iid central limit theorem

Let `mu` and `nu` be probability measures, let `X : Nat -> Omega -> Real`, and let `Y : Omega' -> Real`. Suppose `X 0` belongs to `L^2(mu)`, the family `X` is independent, and every `X i` is identically distributed with `X 0`. Suppose also that `Y` has the centered Gaussian law with variance `Var[X 0; mu]`. Then

`(sqrt n)^(-1) * (sum i in range n, X i - n * integral omega, X 0 omega dmu)`

converges in distribution under `mu` to `Y` under `nu` as `n -> infinity`.

Equivalently for positive `n`, this is the convergence of

`sqrt n * ((n : Real)^(-1) * sum i in range n, X i`

`  - integral omega, X 0 omega dmu)`.

The theorem includes the zero-variance case. In Mathlib the target law is written `gaussianReal 0 (Var[X 0; mu]).toNNReal`.

Both `mu` and `nu` carry probability-measure instances. The `IdentDistrib` hypotheses supply almost-everywhere measurability of the sample variables; no separate family of measurability assumptions appears in the Mathlib theorem.

## Mathlib

Declarations: `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`
File: `Mathlib/Probability/CentralLimitTheorem.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed pages 8-9, central-limit-theorem paragraph

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/CentralLimitTheorem.lean`.

Verified in the pinned checkout. With probability measures P and P', HasLaw Y (gaussianReal 0 Var[X 0; P].toNNReal) P', MemLp (X 0) 2 P, iIndepFun X P, and IdentDistrib (X i) (X 0) P P for every i, the exact n-indexed centered inverse-square-root sum tends to Y in distribution. IdentDistrib supplies sample measurability. The theorem includes n = 0 in the sequence and handles zero variance separately.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Law of a random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/law-of-a-random-variable.md)
- [Identically distributed random variables](../../measure-theoretic-probability-and-conditional-expectation/definitions/identically-distributed-random-variables.md)
- [Independent family of random variables](../../measure-theoretic-probability-and-conditional-expectation/definitions/independent-family-of-random-variables.md)
