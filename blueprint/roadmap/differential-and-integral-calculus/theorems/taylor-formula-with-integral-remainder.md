---
kind: node
declaration: theorem
mathlib: true
---

# Taylor formula with integral remainder

Let `E` and `F` be normed real vector spaces, assume that only `F` is complete, let `f : E -> F`, let `x y : E`, and let `n` be a natural number. Suppose that `ContDiffAt Real (n + 1) f (x + t smul y)` holds for every real `t` in `Set.Icc 0 1`. Then

`f (x + y)`

is the sum, for `0 <= k <= n`, of

`(k!)^-1 smul iteratedFDeriv Real k f x (fun _ => y)`,

plus the integral remainder

`(n!)^-1 smul integral t in 0..1 of ((1 - t)^n smul iteratedFDeriv Real (n + 1) f (x + t smul y) (fun _ => y))`.

The sum ranges over orders zero through `n`. The remainder is the oriented volume interval integral from zero to one. No separate convexity, measurability, or integrability hypothesis is required.

## Mathlib

Declarations: `map_add_eq_sum_add_integral_iteratedFDeriv`
File: `Mathlib/Analysis/Calculus/TaylorIntegral.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/TaylorIntegral.lean`.

Verified in the pinned checkout for real normed domain and codomain, with completeness required only for the codomain. The exact hypothesis is ContDiffAt Real (n + 1) f (x + t smul y) for every t in Set.Icc 0 1. The finite sum uses orders 0 through n with inverse factorial coefficients; the remainder uses (n!)^-1, (1 - t)^n, derivative order n + 1, and the volume interval integral from 0 to 1. No separate convexity or integrability assumption occurs.

## Depends on

- [Interval integral](../definitions/interval-integral.md)
- [Iterated Frechet derivative](../definitions/iterated-frechet-derivative.md)
