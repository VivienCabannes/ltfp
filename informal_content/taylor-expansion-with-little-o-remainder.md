# Taylor expansion with little-o remainder

Let `E` be a normed real vector space, let `s` be a convex subset of the scalar domain `Real`, let `x0` belong to `s`, and let `f : Real -> E` be `n` times continuously differentiable on `s`. As `x` tends to `x0` within `s`,

`f x - taylorWithinEval f n s x0 x = o((x - x0)^n)`.

The polynomial uses the within-set iterated derivatives through order `n`, so this is an actual local Taylor expansion rather than only derivative-jet data.

## Mathlib

Declarations: `taylor_isLittleO`
File: `Mathlib/Analysis/Calculus/Taylor.lean`
