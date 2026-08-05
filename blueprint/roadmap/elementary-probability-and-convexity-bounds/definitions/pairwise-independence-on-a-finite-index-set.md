---
kind: node
declaration: definition
mathlib: true
---

# Pairwise independence on a finite index set

Let `X i : Omega -> E i` be a family of functions into measurable spaces, let `mu` be an arbitrary measure on `Omega`, and let `s` be a finite set of indices. Pairwise independence on `s` means

`Set.Pairwise (s : Set _) (fun i j => IndepFun (X i) (X j) mu)`.

Thus, for any distinct `i` and `j` belonging to `s`, the two functions `X i` and `X j` are independent under `mu`. This condition is weaker than mutual independence of the whole family. If `iIndepFun X mu` holds, `ProbabilityTheory.iIndepFun.indepFun` supplies each required binary-independence statement and hence pairwise independence on every finite `s`.

Neither predicate itself asserts measurability of the functions, and no probability-measure instance is an assumption.

## Mathlib

Declarations: `ProbabilityTheory.IndepFun`, `ProbabilityTheory.iIndepFun.indepFun`
File: `Mathlib/Probability/Independence/Basic.lean`


## Roadmap and coverage

- [Elementary probability and convexity bounds](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2, printed page 8, independent-sum variance display

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Probability/Independence/Basic.lean`.

Verified in the pinned checkout. Pairwise independence on a Finset s is Set.Pairwise on the coerced set with binary IndepFun as the relation. The theorem iIndepFun.indepFun turns mutual independence into each binary independence statement for distinct indices, and therefore into the finite-set pairwise condition. Neither predicate includes function measurability, and no probability-measure instance is assumed.

## Depends on

- [Independent family of random variables](../../measure-theoretic-probability-and-conditional-expectation/definitions/independent-family-of-random-variables.md)
