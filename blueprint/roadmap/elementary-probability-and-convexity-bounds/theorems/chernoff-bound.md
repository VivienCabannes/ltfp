---
kind: node
declaration: theorem
mathlib: true
---

# Chernoff bound

Let `mu` be a probability measure, let `X : Omega -> Real` be measurable, let `t : Real`, and let `s > 0`. Suppose `omega |-> exp (s * X omega)` is integrable. Then

`mu.real {omega | t < X omega}`

`<= exp (-s * t) * integral omega, exp (s * X omega) dmu`.

The event is strict, as in the source. The exponential integrability hypothesis makes the real-valued expectation on the right meaningful; without it, Mathlib's total Bochner integral would not represent an infinite moment-generating function.

Mathlib writes the expectation factor as `mgf X mu s`; its definition is exactly the displayed integral. Its theorem bounds the stronger closed-threshold event, so the displayed strict-event bound follows by inclusion. The theorem only needs a finite measure and `0 <= s`; the probability-space and strictly positive parameter assumptions are the source specialization.

## Mathlib

Declarations: `ProbabilityTheory.mgf`, `ProbabilityTheory.measure_ge_le_exp_mul_mgf`
File: `Mathlib/Probability/Moments/Basic.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, Exercise 1.10, printed page 9
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.10, printed page 2

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/Moments/Basic.lean`.

Verified in the pinned checkout. Under IsFiniteMeasure mu, 0 <= s, and Integrable (fun omega => exp (s * X omega)), measure_ge_le_exp_mul_mgf proves the closed-threshold upper-tail bound with factor exp (-s*t) * mgf X mu s. The source's strict event is a subset. The definition mgf is the displayed Bochner integral. A probability measure supplies finiteness; the source's s > 0 is a specialization. No separate measurability premise is needed beyond exponential integrability.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/random-variable.md)
- [Markov's inequality](markovs-inequality.md)
