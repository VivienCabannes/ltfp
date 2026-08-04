# Frechet derivative

Let `K` be a nontrivially normed field, let `E` and `F` be normed vector spaces over `K`, let `f : E -> F`, let `x : E`, and let `A : E ->L[K] F`. The relation `HasFDerivAt f A x` says that

`f x' - f x - A (x' - x) = o(x' - x)`

as `x'` tends to `x`. The value `fderiv K f x` is the continuous linear derivative selected when a derivative exists and is zero when `f` is not differentiable at `x`.

## Mathlib

Declarations: `HasFDerivAt`, `fderiv`, `hasFDerivAt_iff_isLittleO`, `DifferentiableAt.hasFDerivAt`, `HasFDerivAt.fderiv`, `fderiv_zero_of_not_differentiableAt`
File: `Mathlib/Analysis/Calculus/FDeriv/Defs.lean`
