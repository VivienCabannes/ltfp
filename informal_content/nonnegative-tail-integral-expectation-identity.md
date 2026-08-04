# Nonnegative tail-integral expectation identity

Let `mu` be a probability measure and let `Y : Omega -> Real` be measurable, integrable, and nonnegative almost everywhere. Then

`integral omega, Y omega dmu`

`= integral t in Set.Ioi 0, mu.real {omega | t < Y omega}`.

Thus the expectation of a nonnegative integrable random variable is the integral over positive thresholds of its strict upper-tail probability. The strict event is essential to the displayed form; the non-strict version has the same integral only after an almost-everywhere-in-threshold argument.

## Mathlib

Declarations: `MeasureTheory.Integrable.integral_eq_integral_meas_lt`, `MeasureTheory.Integrable.integral_eq_integral_meas_le`
File: `Mathlib/MeasureTheory/Integral/Layercake.lean`
