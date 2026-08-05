---
kind: node
declaration: definition
mathlib: true
---

# Taylor polynomial on a set

Let `E` be a normed real vector space, let `f : Real -> E`, let `s` be an arbitrary set of real numbers, let `x0 : Real`, and let `n` be a natural number. The order-`n` Taylor polynomial of `f` at `x0`, using totalized derivatives within `s`, has coefficient

`(k! : Real)^-1 smul iteratedDerivWithin k f s x0`

on the shifted power `(X - x0)^k`. It is a member of `PolynomialModule Real E`. Its value at `x` is

`sum k in range (n + 1), (((k! : Real)^-1 * (x - x0)^k) smul iteratedDerivWithin k f s x0)`.

No differentiability, convexity, openness, membership, or completeness hypothesis is needed for these definitions because `iteratedDerivWithin` is totalized. The polynomial definition alone asserts no approximation or remainder property.

## Mathlib

Declarations: `taylorCoeffWithin`, `taylorWithin`, `taylorWithinEval`, `taylor_within_apply`
File: `Mathlib/Analysis/Calculus/Taylor.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/Taylor.lean`.

Verified in the pinned checkout. For f : Real -> E, where E is any normed real vector space, taylorCoeffWithin is (k! : Real)^-1 smul iteratedDerivWithin k f s x0; taylorWithin lies in PolynomialModule Real E and uses powers of X - x0; taylorWithinEval evaluates it; and taylor_within_apply gives the sum over Finset.range (n + 1). There are no smoothness or completeness hypotheses because iteratedDerivWithin is totalized. These declarations provide no remainder theorem.

## Depends on

- [Iterated Frechet derivative](iterated-frechet-derivative.md)
