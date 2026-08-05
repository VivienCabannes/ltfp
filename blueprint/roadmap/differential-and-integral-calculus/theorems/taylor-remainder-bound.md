---
kind: node
declaration: theorem
mathlib: true
---

# Taylor remainder bound

Let `E` be a normed real vector space, let `a <= b`, let `x` belong to `Set.Icc a b`, and let `f : Real -> E` be `n + 1` times continuously differentiable on `Set.Icc a b`. Suppose that

`norm (iteratedDerivWithin (n + 1) f (Set.Icc a b) y) <= C`

for every `y` in `Set.Icc a b`. Then

`norm (f x - taylorWithinEval f n (Set.Icc a b) a x) <= C * (x - a)^(n + 1) / n!`.

## Mathlib

Declarations: `taylor_mean_remainder_bound`
File: `Mathlib/Analysis/Calculus/Taylor.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/Taylor.lean`.

Verified in the pinned checkout for f : Real -> E with E a normed real vector space. Given a <= b, x in Set.Icc a b, ContDiffOn order n+1, and a uniform bound C on iteratedDerivWithin order n+1, the remainder norm is at most C * (x-a)^(n+1) / n!; no completeness or explicit nonnegativity assumption on C is required.

## Depends on

- [Iterated Frechet derivative](../definitions/iterated-frechet-derivative.md)
- [Taylor polynomial on a set](../definitions/taylor-polynomial-on-a-set.md)
