# Frechet Taylor derivative jet

Let `K` be a nontrivially normed field, let `E` and `F` be normed vector spaces over `K`, let `f : E -> F`, and let `p` assign to every `x : E` and natural number `m` a continuous `m`-linear map from `E` to `F`. The predicate `HasFTaylorSeriesUpTo n f p` records that the order-zero term, after evaluation as a zero-linear map, is `f`; that the first currying of the order-`m + 1` term is the Frechet derivative of the parameterized order-`m` term whenever `m < n`; and that each parameterized order-`m` term is continuous whenever `m <= n`. The index `n` may be a natural number, infinity, or omega. This is only a derivative-jet condition; it asserts neither factorial normalization nor convergence of a series to `f`.

## Mathlib

Declarations: `HasFTaylorSeriesUpTo`
File: `Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean`
