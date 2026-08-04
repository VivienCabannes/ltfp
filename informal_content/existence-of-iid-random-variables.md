# Existence of iid random variables

Let `I` be any index type and let `mu` be a probability measure on an arbitrary measurable space `E`. There exist a measurable space `Omega`, a probability measure `P` on it, and a family `X i : Omega -> E` such that every `X i` is measurable, every `X i` has law `mu` under `P`, and the family is independent under `P`.

The index type may be empty or uncountable. No topology, countable-generation, standard-Borel, or nonemptiness hypothesis is required. The noncomputable construction uses the full product space, its Pi measurable structure, the infinite product measure, and coordinate evaluation maps. Pairwise identical distribution follows from the common law but is not a separate conclusion of the theorem.

## Mathlib

Declarations: `ProbabilityTheory.exists_iid`, `ProbabilityTheory.exists_hasLaw_indepFun`
File: `Mathlib/Probability/HasLawExists.lean`
