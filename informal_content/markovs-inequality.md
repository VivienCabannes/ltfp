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
