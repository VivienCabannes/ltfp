---
kind: roadmap
status: mapped
---

# RKHS foundations and representer principles

Finite representability of regularized Hilbert-space models and the canonical reproducing-kernel Hilbert space associated with a positive-semidefinite kernel.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Learning rules, capacity, and risk decomposition](../learning-rules-capacity-and-risk-decomposition/README.md)

## Candidate contents

- Feature-map linear predictors
- Kernel and Gram matrix
- Representer theorem
- Supervised representer theorem
- Kernel trick and finite-dimensional empirical-risk minimization
- Minimum-norm interpolation
- Positive-definite kernel
- Aronszajn feature-map and RKHS characterization
- Reproducing properties and canonical feature map
- Kernel cone and product calculus
- Bounded evaluations characterize RKHSs (Exercise 7.1)
- Exponentials of kernels (Exercise 7.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Sections 7.1-7.3 through kernel calculus, printed pages 179-186

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `RKHS`
- `RKHS.kernel`
- `RKHS.kerFun_dense`
- `RKHS.posSemidef_kernel`
- `RKHS.OfKernel`
- `RKHS.kernel_ofKernel`

Primary file: `Mathlib/Analysis/InnerProductSpace/Reproducing.lean`.

The pinned checkout has a recent RKHS construction and kernel theorem; the optimization representer theorems are not part of that file and require new formalization.
