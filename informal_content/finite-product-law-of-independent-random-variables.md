# Finite product law of independent random variables

Let `I` be a finite index type and let `E i` be a dependent family of measurable codomains. Suppose that each `X i : Omega -> E i` has law `mu i` under an arbitrary measure `P` and that the family `X` is independent under `P`. Then the joint function `omega |-> fun i => X i omega` has law `Measure.pi mu` under `P`.

The marginal-law hypotheses already supply almost-everywhere measurability. No separate joint-measurability, probability, finite-measure, or sigma-finiteness assumption is required; independence itself normalizes `P`. Here `Measure.pi mu` is the coordinate-indexed finite Pi product.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun.hasLaw_pi`
File: `Mathlib/Probability/HasLaw.lean`
