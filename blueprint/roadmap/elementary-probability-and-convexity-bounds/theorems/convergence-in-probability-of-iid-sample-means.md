---
kind: node
declaration: corollary
statement: formalized
proof: formalized
lean: ProbabilityTheory.tendstoInMeasure_sampleMean
---

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


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, sentence following the finite deviation bound

## Planning record

Legacy Mathlib assessment: `partial`.
Primary supporting file: `Mathlib/MeasureTheory/Function/ConvergenceInMeasure.lean`.

Verified by two compiled assemblies in the pinned checkout; no single dedicated weak-law declaration matches the node. The direct source route uses tendstoInMeasure_iff_measureReal_dist under the finite-measure instance supplied by a probability measure. For epsilon > 0, its closed-threshold event is contained in the source's strict event at epsilon/2, so the finite deviation bound eventually for n > 0 squeezes its probability below Var[X 0; mu] / ((n : Real) * (epsilon/2)^2), which tends to zero. The n = 0 average is totalized to zero and is irrelevant atTop. An alternative compiled route combines strong_law_Lp at p = 2 with tendstoInMeasure_of_tendsto_eLpNorm, but it is not the dependency route recorded here.

## Depends on

- [Finite deviation bound for an iid sample mean](finite-deviation-bound-for-an-iid-sample-mean.md)
