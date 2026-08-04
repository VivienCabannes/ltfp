# Independence characterized by a finite product law

Let `I` carry a `Fintype` instance, let `E i` be dependent measurable codomains, and let `P` be a probability measure. If every `X i : Omega -> E i` has law `mu i` under `P`, then the family `X` is independent under `P` if and only if the joint function `omega |-> fun i => X i omega` has law `Measure.pi mu` under `P`.

The marginal laws supply all coordinatewise almost-everywhere measurability hypotheses. No separate joint-measurability or marginal probability assumption is required. The empty finite index type is allowed.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_iff_hasLaw_pi_pi`
File: `Mathlib/Probability/HasLaw.lean`
