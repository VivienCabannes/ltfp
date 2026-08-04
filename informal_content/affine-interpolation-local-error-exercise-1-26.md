# Affine interpolation local error (Exercise 1.26)

Let `a < b` and let `f : Real -> Real`. Assume that `f` is differentiable on `Set.Icc a b` and that `derivWithin f (Set.Icc a b)` is differentiable there. Let `L >= 0` and suppose

`abs (iteratedDerivWithin 2 f (Set.Icc a b) y) <= L`

for every `y` in `Set.Icc a b`. Then, for every `x` in `Set.Icc a b`,

`abs (f x - A[f; a, b](x)) <= (L / 2) * (x - a) * (b - x)`.

On `[0, 1]`, the right-hand side is `(L / 2) * x * (1 - x)`.

## Proof

Write `e = f - A[f; a, b]`. Since the affine interpolant agrees with `f` at the endpoints,

`e a = e b = 0`.

The claim is immediate when `x` is an endpoint. Suppose `a < x < b`, and define

`c = e x / ((x - a) * (x - b))`

and

`phi(t) = e t - c * (t - a) * (t - b)`.

The function `phi` vanishes at `a`, `x`, and `b`. Rolle's theorem on `[a, x]` and `[x, b]` gives points `u` and `v`, with `a < u < x < v < b`, such that `phi'(u) = phi'(v) = 0`. A second application of Rolle's theorem to `phi'` on `[u, v]` gives a point `xi` in `(u, v)` with `phi''(xi) = 0`.

The affine interpolant has zero second derivative, while the second derivative of `(t - a) * (t - b)` is `2`. At an interior point the closed interval is a neighborhood, so each within-derivative witness supplied by the hypotheses becomes an ordinary derivative witness. The identities `iteratedDerivWithin_one` and `iteratedDerivWithin_succ` express the bounded second within derivative as the within derivative of the first within derivative. Hence

`0 = phi''(xi) = f''(xi) - 2 * c`,

so `c = f''(xi) / 2`. Returning to the definition of `c` yields

`e x = (f''(xi) / 2) * (x - a) * (x - b)`.

Because `x` lies between `a` and `b`, taking absolute values and using the derivative bound gives

`abs (e x) <= (L / 2) * (x - a) * (b - x)`.

On the open interval, the second derivative used in this argument agrees with `iteratedDerivWithin 2 f (Set.Icc a b)`. The two differentiability-on hypotheses supply continuity of `f`, continuity of its first within derivative, and the genuine derivative witnesses required by the three applications of Rolle's theorem. Thus the statement uses twice differentiability, as in the source, rather than the stronger `C^2` assumption.

### Mathlib status

No named local affine-interpolation error theorem with this bound was found in the pinned checkout. `exists_hasDerivAt_eq_zero` supports the three Rolle steps, `iteratedDerivWithin_one`, `iteratedDerivWithin_succ`, and `HasDerivWithinAt.hasDerivAt` support the interior derivative bridge, and `AffineMap.hasDerivAt_lineMap` supplies the affine derivative. None packages the sharp interpolation estimate itself.
