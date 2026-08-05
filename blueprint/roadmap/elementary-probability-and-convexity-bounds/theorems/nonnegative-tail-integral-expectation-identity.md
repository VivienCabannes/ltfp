---
kind: node
declaration: theorem
mathlib: true
---

# Nonnegative tail-integral expectation identity

Let `mu` be a probability measure and let `Y : Omega -> Real` be measurable, integrable, and nonnegative almost everywhere. Then

`integral omega, Y omega dmu`

`= integral t in Set.Ioi 0, mu.real {omega | t < Y omega}`.

Thus the expectation of a nonnegative integrable random variable is the integral over positive thresholds of its strict upper-tail probability. The strict event is essential to the displayed form; the non-strict version has the same integral only after an almost-everywhere-in-threshold argument.

## Mathlib

Declarations: `MeasureTheory.Integrable.integral_eq_integral_meas_lt`, `MeasureTheory.Integrable.integral_eq_integral_meas_le`
File: `Mathlib/MeasureTheory/Integral/Layercake.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, Exercise 1.11, printed page 9
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.11, printed page 2

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/Layercake.lean`.

Verified in the pinned checkout. For an arbitrary measure and an integrable almost-everywhere nonnegative real function, integral_eq_integral_meas_lt is exactly the strict-tail Bochner layer-cake identity in the source; integral_eq_integral_meas_le supplies the non-strict companion. Integrable provides the needed almost-everywhere measurability and tail finiteness. No probability- or finite-measure instance is required by the Mathlib theorem.

## Depends on

- [Bochner integral](../../differential-and-integral-calculus/definitions/bochner-integral.md)
- [Probability measure](../../measure-theoretic-probability-and-conditional-expectation/definitions/probability-measure.md)
- [Random variable](../../measure-theoretic-probability-and-conditional-expectation/definitions/random-variable.md)
