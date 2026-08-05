---
kind: node
declaration: theorem
statement: formalized
proof: formalized
lean: ProbabilityTheory.variance_sampleMean, ProbabilityTheory.sampleMean, ProbabilityTheory.sampleMean_eq_smul_sum, ProbabilityTheory.memLp_sampleMean
---

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


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, sample-mean variance display

## Planning record

Legacy Mathlib assessment: `partial`.
Primary supporting file: `Mathlib/Probability/Moments/Variance.lean`.

Verified by a compiled Lean assembly in the pinned checkout. For arbitrary mu and positive n, it suffices to assume MemLp (X 0) 2 mu, IdentDistrib (X 0) (X i) mu mu for i < n, and pairwise IndepFun on Finset.range n. IdentDistrib.memLp_snd transports MemLp, IndepFun.variance_sum adds variances, IdentDistrib.variance_eq identifies them, and variance_smul supplies inverse-square scaling. No probability- or finite-measure instance is needed. IdentDistrib declarations are in Mathlib/Probability/IdentDistrib.lean.

## Depends on

- [Identically distributed random variables](../../measure-theoretic-probability-and-conditional-expectation/definitions/identically-distributed-random-variables.md)
- [Variance of a finite sum of pairwise independent random variables](variance-of-a-finite-sum-of-pairwise-independent-random-variables.md)
