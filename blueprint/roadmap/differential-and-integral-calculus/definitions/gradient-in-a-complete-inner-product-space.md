---
kind: node
declaration: definition
mathlib: true
---

# Gradient in a complete inner product space

Let `K` be `Real` or `Complex`, let `H` be a complete inner-product space over `K`, let `f : H -> K`, and let `x g : H`. The relation `HasGradientAt f g x` says that the Frechet derivative of `f` at `x` maps every direction `h` to the inner product of `g` with `h`. The value `gradient f x` is obtained from `fderiv K f x` through the inverse conjugate-linear Frechet-Riesz isometry. It is zero when `f` is not `K`-differentiable at `x`.

## Mathlib

Declarations: `HasGradientAt`, `gradient`, `hasGradientAt_iff_hasFDerivAt`, `toDual_gradient`, `gradient_eq_zero_of_not_differentiableAt`, `InnerProductSpace.toDual`, `InnerProductSpace.toDual_apply_apply`
File: `Mathlib/Analysis/Calculus/Gradient/Basic.lean`


## Roadmap and coverage

- [Differential and integral calculus](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- [Adopted source map](../../../sources/README.md)

## Planning record

Legacy Mathlib assessment: `in-mathlib`.
Primary supporting file: `Mathlib/Analysis/Calculus/Gradient/Basic.lean`.

Verified in the pinned checkout for RCLike scalars and complete inner-product spaces. HasGradientAt represents Df(x)(h) as inner g h; gradient applies the inverse conjugate-linear Frechet-Riesz equivalence to fderiv and is zero when f is not scalar-Fréchet differentiable.

## Depends on

- [Frechet derivative](frechet-derivative.md)
- [Frechet-Riesz representation theorem](../../convex-analysis-and-normed-space-geometry/theorems/frechet-riesz-representation-theorem.md)
