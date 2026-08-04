# Finite deviation bound for an iid sample mean

Let `mu` be a probability measure. Under the remaining hypotheses of the variance formula for an iid sample mean, let `n` be positive, let `epsilon > 0`, and put

`A_n(omega) = (n : Real)^(-1) * sum i in range n, X i omega`.

Then

`mu.real {omega | epsilon < abs (A_n omega - integral omega, X 0 omega dmu)}`

`<= Var[X 0; mu] / ((n : Real) * epsilon^2)`.

The deviation event is strict, matching the source. The verified Mathlib assembly proves the stronger closed-threshold bound, from which this display follows by event inclusion.

## Proof

Square-integrability of `X 0` transfers to every sampled `X i` by identical distribution. On the probability space this also gives integrability. Finite-sum and scalar linearity therefore show that the expectation of `A_n` is the expectation of `X 0`. The same `L^2` closure facts make `A_n` square-integrable, so Chebyshev's inequality gives

`mu.real {omega | epsilon < abs (A_n omega - integral omega, A_n omega dmu)}`

`<= Var[A_n; mu] / epsilon^2`.

Replace the expectation of `A_n` by the expectation of `X 0`, and replace its variance by `Var[X 0; mu] / n`. Associativity of division yields the stated bound.

Both positivity hypotheses are essential: `n > 0` gives a genuine sample mean and the variance scaling, while `epsilon > 0` is required by the real-valued Chebyshev bound.

### Mathlib support

Declarations: `ProbabilityTheory.meas_ge_le_variance_div_sq`, `ProbabilityTheory.IdentDistrib.integral_eq`, `ProbabilityTheory.IdentDistrib.memLp_snd`, `MeasureTheory.integral_finsetSum`, `MeasureTheory.integral_smul`, `MeasureTheory.memLp_finsetSum'`, `MeasureTheory.MemLp.const_smul`
Files: `Mathlib/Probability/Moments/Variance.lean`, `Mathlib/Probability/IdentDistrib.lean`, `Mathlib/MeasureTheory/Integral/Bochner/Basic.lean`, `Mathlib/MeasureTheory/Function/LpSeminorm/TriangleInequality.lean`, `Mathlib/MeasureTheory/Function/LpSeminorm/SMul.lean`
