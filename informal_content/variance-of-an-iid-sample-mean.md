# Variance of an iid sample mean

Let `mu` be an arbitrary measure, let `n` be a positive natural number, and let `X : Nat -> Omega -> Real`. Suppose that `X 0` belongs to `L^2(mu)`, that

`Set.Pairwise (Finset.range n : Set Nat) (fun i j => IndepFun (X i) (X j) mu)`,

and that `IdentDistrib (X 0) (X i) mu mu` for every `i < n`. Identical distribution transports the `L^2` hypothesis from `X 0` to each sampled variable, so no separate family of square-integrability assumptions is needed. Define

`A_n(omega) = (n : Real)^(-1) * sum i in range n, X i omega`.

Then

`Var[A_n; mu] = Var[X 0; mu] / n`.

## Proof

Variance scales quadratically under multiplication by a real scalar, so

`Var[A_n; mu] = (n : Real)^(-2) * Var[sum i in range n, X i; mu]`.

The finite independent-sum variance formula turns the variance on the right into the sum of the `n` individual variances. Identical distribution makes every summand equal to `Var[X 0; mu]`. Hence

`Var[A_n; mu] = (n : Real)^(-2) * n * Var[X 0; mu]`.

Since `n` is positive, its real coercion is nonzero, and the displayed expression simplifies to `Var[X 0; mu] / n`. None of these ingredients requires `mu` to be a probability or finite measure. Lean's totalized inverse also makes the algebraic equality true when `n = 0`, but that case is excluded because it is not a sample mean.

### Mathlib support

Declarations: `ProbabilityTheory.variance_smul`, `ProbabilityTheory.IndepFun.variance_sum`, `ProbabilityTheory.IdentDistrib.variance_eq`, `ProbabilityTheory.IdentDistrib.memLp_snd`
Files: `Mathlib/Probability/Moments/Variance.lean`, `Mathlib/Probability/IdentDistrib.lean`
