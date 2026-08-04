# Chernoff bound

Let `mu` be a probability measure, let `X : Omega -> Real` be measurable, let `t : Real`, and let `s > 0`. Suppose `omega |-> exp (s * X omega)` is integrable. Then

`mu.real {omega | t < X omega}`

`<= exp (-s * t) * integral omega, exp (s * X omega) dmu`.

The event is strict, as in the source. The exponential integrability hypothesis makes the real-valued expectation on the right meaningful; without it, Mathlib's total Bochner integral would not represent an infinite moment-generating function.

Mathlib writes the expectation factor as `mgf X mu s`; its definition is exactly the displayed integral. Its theorem bounds the stronger closed-threshold event, so the displayed strict-event bound follows by inclusion. The theorem only needs a finite measure and `0 <= s`; the probability-space and strictly positive parameter assumptions are the source specialization.

## Mathlib

Declarations: `ProbabilityTheory.mgf`, `ProbabilityTheory.measure_ge_le_exp_mul_mgf`
File: `Mathlib/Probability/Moments/Basic.lean`
