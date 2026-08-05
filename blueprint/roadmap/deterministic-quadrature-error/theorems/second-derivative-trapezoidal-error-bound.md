---
kind: node
declaration: theorem
mathlib: true
---

# Second-derivative trapezoidal error bound

Let `f : Real -> Real`, let `a, b : Real`, let `N` be a positive natural number, and let `0 <= L`. Suppose `f` is differentiable on the unordered interval `Set.uIcc a b` and its within derivative

`derivWithin f (Set.uIcc a b)`

is differentiable there. Suppose also that

`abs (iteratedDerivWithin 2 f (Set.uIcc a b) x) <= L`

for every `x` in `Set.uIcc a b`. Then

`abs (T_N(f; a, b) - integral x in a..b, f x) <= abs (b - a)^3 * L / (12 * N^2)`.

No endpoint order is required. For `a = 0` and `b = 1`, this becomes

`abs ((integral x in 0..1, f x) - T_N(f; 0, 1)) <= L / (12 * N^2)`.

The sign in the last display is reversed relative to Mathlib's `trapezoidal_error`, but the absolute value removes that difference. No separate interval-integrability assumption is needed.

## Mathlib

Declarations: `trapezoidal_error_le`, `trapezoidal_error_le_of_c2`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 19

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`.

Verified by compiled applications in the pinned checkout. The primary theorem trapezoidal_error_le assumes differentiability of f and its within derivative on Set.uIcc a b, a uniform bound on iteratedDerivWithin 2, and 0 < N; it gives exactly abs (b-a)^3 * L / (12 * N^2). An interval-only bound with 0 <= L extends to Mathlib's all-real bound because the totalized within derivative vanishes off the interval. Arbitrary endpoint orientation, the [0,1] specialization, and reversal from estimator-minus-integral to the source sign all compile. No separate integrability hypothesis is needed. trapezoidal_error_le_of_c2 is only a stronger-hypothesis convenience corollary.

## Depends on

- [Exact trapezoidal error decomposition](exact-trapezoidal-error-decomposition.md)
- [Affine interpolation local error (Exercise 1.26)](affine-interpolation-local-error-exercise-1-26.md)
