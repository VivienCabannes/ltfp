# Identically distributed random variables

Let `X : Omega -> E` and `Y : Omega' -> E` be functions from potentially different measurable source spaces into a common measurable codomain, with arbitrary measures `P` and `Q`. The proposition `IdentDistrib X Y P Q` requires that each function is almost everywhere measurable for its own measure and that their pushforward measures agree: `P.map X = Q.map Y`.

No probability or finiteness assumption is required. Identical distribution is reflexive for an almost-everywhere-measurable function, symmetric, and transitive. A common `HasLaw` witness implies identical distribution, and identical distribution transports any law from either function to the other.

## Mathlib

Declarations: `ProbabilityTheory.IdentDistrib`, `ProbabilityTheory.IdentDistrib.aemeasurable_fst`, `ProbabilityTheory.IdentDistrib.aemeasurable_snd`, `ProbabilityTheory.IdentDistrib.map_eq`, `ProbabilityTheory.IdentDistrib.refl`, `ProbabilityTheory.IdentDistrib.symm`, `ProbabilityTheory.IdentDistrib.trans`, `ProbabilityTheory.IdentDistrib.comp_of_aemeasurable`, `ProbabilityTheory.IdentDistrib.comp`, `ProbabilityTheory.IdentDistrib.measure_mem_eq`, `ProbabilityTheory.HasLaw.identDistrib`, `ProbabilityTheory.IdentDistrib.hasLaw`
File: `Mathlib/Probability/IdentDistrib.lean`
