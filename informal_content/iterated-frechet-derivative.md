# Iterated Frechet derivative

Let `K` be a nontrivially normed field, let `E` and `F` be normed vector spaces over `K`, and let `f : E -> F`. For every natural number `n`, `iteratedFDeriv K n f x` is the continuous `n`-linear map obtained by repeatedly taking the Frechet derivative and uncurrying the new linear argument. The within-set variant uses `fderivWithin` at every stage; unique-differentiability hypotheses are needed when it is identified with an intrinsic derivative on the set. Both definitions are totalized, so a stage at which the required derivative does not exist contributes zero. On the scalar line, `iteratedDeriv` and `iteratedDerivWithin` evaluate these multilinear maps on the repeated unit direction. At order two this is the coordinate-free second Frechet derivative; for a sufficiently differentiable real-valued function it is the bilinear Hessian form, while a Hessian matrix requires finite-dimensional coordinate choices.

## Mathlib

Declarations: `iteratedFDeriv`, `iteratedFDerivWithin`, `iteratedFDeriv_two_apply`, `iteratedFDerivWithin_two_apply`, `iteratedDeriv`, `iteratedDerivWithin`
File: `Mathlib/Analysis/Calculus/ContDiff/FTaylorSeries.lean`
