---
kind: node
declaration: theorem
mathlib: true
---

# Taylor expansion with little-o remainder

Let `E` be a normed real vector space, let `s` be a convex subset of the scalar domain `Real`, let `x0` belong to `s`, and let `f : Real -> E` be `n` times continuously differentiable on `s`. As `x` tends to `x0` within `s`,

`f x - taylorWithinEval f n s x0 x = o((x - x0)^n)`.

The polynomial uses the within-set iterated derivatives through order `n`, so this is an actual local Taylor expansion rather than only derivative-jet data.

## Mathlib

Declarations: `taylor_isLittleO`
File: `Mathlib/Analysis/Calculus/Taylor.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/Taylor.lean`.

Verified in the pinned checkout for f : Real -> E with E a normed real vector space. On a convex set s containing x0, ContDiffOn of natural order n yields little-o within the filter nhdsWithin x0 s relative to (x - x0)^n; no completeness or openness assumption is required.

## Depends on

- [Convex sets](../../convex-analysis-and-normed-space-geometry/definitions/convex-sets.md)
- [Iterated Frechet derivative](../definitions/iterated-frechet-derivative.md)
- [Taylor polynomial on a set](../definitions/taylor-polynomial-on-a-set.md)
