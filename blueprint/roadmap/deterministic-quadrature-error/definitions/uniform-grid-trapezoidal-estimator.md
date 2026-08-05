---
kind: node
declaration: definition
mathlib: true
---

# Uniform-grid trapezoidal estimator

Let `f : Real -> Real`, let `N` be a natural number, and let `a, b : Real`. When `N > 0`, put

`h = (b - a) / N`.

The uniform-grid trapezoidal estimator of the oriented integral of `f` from `a` to `b` is

`T_N(f; a, b) = h * ((f a + f b) / 2 + sum k in {1, ..., N - 1}, f (a + k * h))`.

The raw definition is total for every `N`; at `N = 0` it is exactly zero. For `N > 0`, it has the displayed grid interpretation. It is meaningful for either endpoint order, and reversing the endpoints reverses its sign. On the unit interval it becomes

`T_N(f; 0, 1) = (1 / N) * (f 0 / 2 + sum k in {1, ..., N - 1}, f (k / N) + f 1 / 2)`.

In Mathlib this is `trapezoidal_integral f N a b`. The named symmetry theorem and the nontrivial grid-decomposition and error-bound theorems require `N > 0`.

## Mathlib

Declarations: `trapezoidal_integral`, `trapezoidal_integral_symm`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 18

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`.

Verified in the pinned checkout. trapezoidal_integral is the total real-valued uniform-grid expression for an arbitrary function Real -> Real, with no regularity assumption. At N = 0 totalized division makes the estimator exactly zero. trapezoidal_integral_symm requires 0 < N and negates the value under endpoint reversal; the nontrivial grid-decomposition and error-bound results likewise require positivity.

## Depends on

This node has no prerequisites.
