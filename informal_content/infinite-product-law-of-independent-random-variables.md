# Infinite product law of independent random variables

Let `I` be an arbitrary index type and let `E i` be dependent measurable codomains. Suppose that every `X i : Omega -> E i` has law `mu i` under `P`, the family `X` is independent under `P`, and the joint map `omega |-> fun i => X i omega` is `P`-almost-everywhere measurable. Then this joint map has law `Measure.infinitePi mu` under `P`.

No countability, finiteness, or explicit probability-measure hypothesis is required. The separate joint measurability assumption cannot in general be recovered from the coordinate laws for an arbitrary uncountable index type.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun.hasLaw_infinitePi`
File: `Mathlib/Probability/Independence/InfinitePi.lean`
