# Piecewise-affine integral identity

Let `a, b : Real`, let `N` be a positive natural number, and put

`h = (b - a) / N`, `x_i = a + i * h` for `0 <= i <= N`.

For each `i < N`, let `A_i = A[f; x_i, x_(i+1)]`. Then

`sum i in {0, ..., N - 1}, (integral x in x_i..x_(i+1), A_i(x)) = T_N(f; a, b)`.

This statement sums the separate affine-panel integrals. Interpreting it as the integral of one global continuous piecewise-affine function additionally requires defining that stitched function, proving panelwise agreement and continuity, and applying interval-integral additivity; those stronger obligations are not part of this proposition.

## Proof

Every oriented panel has signed width `h`. The affine panel integral identity gives

`integral x in x_i..x_(i+1), A_i(x) = h * (f x_i + f x_(i+1)) / 2`.

After summing over the panels, each interior value `f x_i`, with `1 <= i < N`, appears in two adjacent half-weight terms, while the two endpoint values appear once. Hence the sum is

`h * (f a / 2 + sum i in {1, ..., N - 1}, f x_i + f b / 2)`,

which is `T_N(f; a, b)` by definition. No endpoint order is needed: for `b < a` the panel integrals and `h` are both oriented, and for `a = b` both sides vanish. The narrow algebraic sum also vanishes at `N = 0`, but positivity is retained because only then does the uniform grid have final point `x_N = b` for arbitrary endpoints.

### Mathlib support

Declarations: `trapezoidal_integral_one`, `sum_trapezoidal_integral_adjacent_intervals`
File: `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalRule.lean`

The second declaration performs the grid summation for one-panel trapezoidal approximations. The identification of each approximation with the integral of its affine interpolant is the preceding node, not a named theorem in this file. No global interval-additivity theorem is needed for the displayed sum of different panel functions.
