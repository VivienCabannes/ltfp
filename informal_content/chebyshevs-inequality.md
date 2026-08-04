# Chebyshev's inequality

Let `mu` be a probability measure, let `X : Omega -> Real` belong to `L^2(mu)`, and let `epsilon > 0`. Then

`mu.real {omega | epsilon < abs (X omega - integral omega, X omega dmu)}`

`<= Var[X; mu] / epsilon^2`.

The deviation event is strict, as in the source. The `L^2` hypothesis supplies measurability, integrability, and the finite second moment. Mathlib bounds the stronger closed-threshold event by the measure-valued right-hand side `ENNReal.ofReal (Var[X; mu] / epsilon^2)`; event inclusion and finite real values give the displayed probability inequality.

## Mathlib

Declarations: `ProbabilityTheory.meas_ge_le_variance_div_sq`
File: `Mathlib/Probability/Moments/Variance.lean`
