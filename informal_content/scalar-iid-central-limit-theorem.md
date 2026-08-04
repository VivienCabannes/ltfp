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
