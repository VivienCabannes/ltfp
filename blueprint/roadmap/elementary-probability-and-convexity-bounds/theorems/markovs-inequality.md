---
kind: node
declaration: theorem
mathlib: true
---

# Markov's inequality

Let `mu` be a probability measure, let `Y : Omega -> Real` be measurable, integrable, and nonnegative almost everywhere, and let `epsilon > 0`. Then

`mu.real {omega | epsilon < Y omega}`

`<= (integral omega, Y omega dmu) / epsilon`.

This is the strict event stated in the source. Mathlib proves the stronger multiplied form

`epsilon * mu.real {omega | epsilon <= Y omega} <= integral omega, Y omega dmu`

for the closed-threshold event, under an arbitrary measure and arbitrary real `epsilon`. The strict event is a subset of that event; positivity is needed only to divide by `epsilon`.

## Mathlib

Declarations: `MeasureTheory.mul_meas_ge_le_integral_of_nonneg`
File: `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, equation (1.5) and Exercise 1.9, printed pages 8-9
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.9, printed page 2

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`.

Verified in the pinned checkout. For an arbitrary measure, an almost-everywhere nonnegative integrable real function, and an arbitrary real epsilon, mul_meas_ge_le_integral_of_nonneg proves epsilon * mu.real {x | epsilon <= f x} <= integral f. The source uses the strict event {epsilon < f x}, whose bound follows by event inclusion, specialization to a probability measure and positive epsilon, and ordered-field division. Integrability already supplies the needed almost-everywhere measurability.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/random-variable.md)
- [Threshold indicator bound for Markov's inequality](threshold-indicator-bound-for-markovs-inequality.md)
