# Taylor remainder bound

Let `E` be a normed real vector space, let `a <= b`, let `x` belong to `Set.Icc a b`, and let `f : Real -> E` be `n + 1` times continuously differentiable on `Set.Icc a b`. Suppose that

`norm (iteratedDerivWithin (n + 1) f (Set.Icc a b) y) <= C`

for every `y` in `Set.Icc a b`. Then

`norm (f x - taylorWithinEval f n (Set.Icc a b) a x) <= C * (x - a)^(n + 1) / n!`.

## Mathlib

Declarations: `taylor_mean_remainder_bound`
File: `Mathlib/Analysis/Calculus/Taylor.lean`
