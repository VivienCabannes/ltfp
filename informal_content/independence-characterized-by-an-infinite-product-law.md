# Independence characterized by an infinite product law

Let `I` be an arbitrary index type, let `E i` be dependent measurable codomains, and let `P` be a probability measure. Suppose that every `X i : Omega -> E i` has law `mu i` under `P` and that the joint map `omega |-> fun i => X i omega` is `P`-almost-everywhere measurable. Then `X` is an independent family under `P` if and only if the joint map has law `Measure.infinitePi mu` under `P`.

There is no countability or finiteness assumption on `I` and no separate probability assumption on the marginal measures. The full joint almost-everywhere-measurability hypothesis is essential for arbitrary uncountable products and does not follow from the coordinate laws alone.

## Mathlib

Declarations: `ProbabilityTheory.iIndepFun_iff_hasLaw_Pi_infinitePi`
File: `Mathlib/Probability/Independence/InfinitePi.lean`
