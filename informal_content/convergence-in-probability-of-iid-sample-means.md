# Convergence in probability of iid sample means

Let `mu` be a probability measure and let `X : Nat -> Omega -> Real`. Suppose `X 0` belongs to `L^2(mu)`, the sequence is pairwise independent, and every `X i` is identically distributed with `X 0`. Define the sample mean by

`A_n(omega) = (n : Real)^(-1) * sum i in range n, X i omega`.

Then `A_n` converges in probability to the constant expectation of `X 0`. In Mathlib notation,

`TendstoInMeasure mu A_n atTop (fun _ => integral omega, X 0 omega dmu)`.

## Proof

Fix `epsilon > 0`. For every positive `n`, apply the strict finite deviation bound at `epsilon / 2`. Since

`{omega | epsilon <= abs (A_n omega - integral omega, X 0 omega dmu)}`

is contained in

`{omega | epsilon / 2 < abs (A_n omega - integral omega, X 0 omega dmu)}`,

its probability is at most

`Var[X 0; mu] / ((n : Real) * (epsilon / 2)^2)`.

The right-hand side tends to zero as `n` tends to infinity. The probabilities on the left are nonnegative, so they also tend to zero by comparison. The characterization of convergence in measure for a finite measure and a real-valued metric target now gives the claimed convergence in probability.

The totalized inverse and empty sum make `A_0 = 0`. The finite deviation bound is needed only eventually, for positive `n`, so this initial value does not affect the `atTop` limit.

### Mathlib support

Declarations: `MeasureTheory.tendstoInMeasure_iff_measureReal_dist`, `MeasureTheory.tendstoInMeasure_of_tendsto_eLpNorm`, `ProbabilityTheory.strong_law_Lp`
Files: `Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean`, `Mathlib/Probability/StrongLaw.lean`
