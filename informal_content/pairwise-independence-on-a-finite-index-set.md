# Pairwise independence on a finite index set

Let `X i : Omega -> E i` be a family of functions into measurable spaces, let `mu` be an arbitrary measure on `Omega`, and let `s` be a finite set of indices. Pairwise independence on `s` means

`Set.Pairwise (s : Set _) (fun i j => IndepFun (X i) (X j) mu)`.

Thus, for any distinct `i` and `j` belonging to `s`, the two functions `X i` and `X j` are independent under `mu`. This condition is weaker than mutual independence of the whole family. If `iIndepFun X mu` holds, `ProbabilityTheory.iIndepFun.indepFun` supplies each required binary-independence statement and hence pairwise independence on every finite `s`.

Neither predicate itself asserts measurability of the functions, and no probability-measure instance is an assumption.

## Mathlib

Declarations: `ProbabilityTheory.IndepFun`, `ProbabilityTheory.iIndepFun.indepFun`
File: `Mathlib/Probability/Independence/Basic.lean`
