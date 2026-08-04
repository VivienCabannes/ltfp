# Gradient in a complete inner product space

Let `K` be `Real` or `Complex`, let `H` be a complete inner-product space over `K`, let `f : H -> K`, and let `x g : H`. The relation `HasGradientAt f g x` says that the Frechet derivative of `f` at `x` maps every direction `h` to the inner product of `g` with `h`. The value `gradient f x` is obtained from `fderiv K f x` through the inverse conjugate-linear Frechet-Riesz isometry. It is zero when `f` is not `K`-differentiable at `x`.

## Mathlib

Declarations: `HasGradientAt`, `gradient`, `hasGradientAt_iff_hasFDerivAt`, `toDual_gradient`, `gradient_eq_zero_of_not_differentiableAt`, `InnerProductSpace.toDual`, `InnerProductSpace.toDual_apply_apply`
File: `Mathlib/Analysis/Calculus/Gradient/Basic.lean`
