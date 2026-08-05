---
kind: node
declaration: definition
mathlib: true
---

# Frechet derivative

Let `K` be a nontrivially normed field, let `E` and `F` be normed vector spaces over `K`, let `f : E -> F`, let `x : E`, and let `A : E ->L[K] F`. The relation `HasFDerivAt f A x` says that

`f x' - f x - A (x' - x) = o(x' - x)`

as `x'` tends to `x`. The value `fderiv K f x` is the continuous linear derivative selected when a derivative exists and is zero when `f` is not differentiable at `x`.

## Mathlib

Declarations: `HasFDerivAt`, `fderiv`, `hasFDerivAt_iff_isLittleO`, `DifferentiableAt.hasFDerivAt`, `HasFDerivAt.fderiv`, `fderiv_zero_of_not_differentiableAt`
File: `Mathlib/Analysis/Calculus/FDeriv/Defs.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/FDeriv/Defs.lean`.

Verified in the pinned checkout. HasFDerivAt has the stated little-o characterization in normed spaces; fderiv selects the unique derivative when differentiable and is zero otherwise. No completeness assumption is required; supporting totalization theorems are imported from FDeriv/Basic.

## Depends on

- [Continuous linear maps](../../convex-analysis-and-normed-space-geometry/definitions/continuous-linear-maps.md)
