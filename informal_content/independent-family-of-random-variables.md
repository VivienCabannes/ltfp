# Independent family of random variables

Let `X i : Omega -> E i` be a dependent family of functions into measurable spaces and let `P` be an arbitrary measure on `Omega`. The predicate `iIndepFun X P` says that the family of measurable-space structures obtained by pulling the structures on `E i` back along `X i` is independent under `P`. Equivalently, the measures of finite intersections of measurable preimage events factor as products.

The predicate itself does not assert that any `X i` is measurable; that remains a separate random-variable hypothesis. It also does not require a probability-measure instance, although the empty finite subfamily forces `P Set.univ = 1`, so independence supplies one. Independence is equivalent to independence of every finite restriction and is preserved by coordinatewise measurable composition.

## Mathlib

Declarations: `ProbabilityTheory.iIndep`, `ProbabilityTheory.iIndep_iff`, `ProbabilityTheory.iIndepFun`, `ProbabilityTheory.iIndepFun_iff_iIndep`, `ProbabilityTheory.iIndepFun_iff`, `ProbabilityTheory.iIndepFun_iff_measure_inter_preimage_eq_mul`, `ProbabilityTheory.iIndepFun_iff_finset`, `ProbabilityTheory.iIndepFun.restrict`, `ProbabilityTheory.iIndepFun.comp`, `ProbabilityTheory.iIndepFun.comp₀`, `ProbabilityTheory.iIndepFun.isProbabilityMeasure`
File: `Mathlib/Probability/Independence/Basic.lean`
