---
kind: roadmap
status: mapped
---

# Finite kernel optimization and stochastic algorithms

Representer reductions, finite kernel optimization, dual formulations, and stochastic-gradient algorithms for regularized kernel learning.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Concrete kernels and harmonic characterizations](../concrete-kernels-and-harmonic-characterizations/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)

## Candidate contents

- Regularized kernel empirical-risk minimization
- Kernel-ridge coefficient formula
- Kernel square-root formulation and conditioning
- Kernel Lagrange dual
- Kernel stochastic-gradient recursion and convergence
- Ridge duality and conditioning (Exercise 7.11)
- Logistic and hinge duals (Exercise 7.12)
- Unregularized constant term (Exercise 7.13)
- Infinite-bandwidth Gaussian limit (Exercise 7.14)
- Kernel optimization (Exercise 7.15)
- Unregularized stochastic-gradient bound (Exercise 7.16)

## Sources

- `sources/ltfp_book.pdf` — Chapter 7, Sections 7.4.1 and 7.4.4-7.4.5, printed pages 196-201

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `RKHS`
- `RKHS.kernel`
- `RKHS.kerFun`
- `RKHS.kerFun_dense`
- `RKHS.posSemidef_kernel`
- `RKHS.OfKernel`
- `RKHS.kernel_ofKernel`
- `Matrix.gram`
- `Matrix.posSemidef_gram`
- `Matrix.PosDef.isUnit`
- `CFC.sqrt`
- `CFC.sq_sqrt`

Primary file: `Mathlib/Analysis/InnerProductSpace/Reproducing.lean`.

Pinned Mathlib supplies RKHS kernels and positive-semidefinite Gram matrices, positive-definite invertibility, and continuous-functional-calculus matrix square roots, which directly support the finite representer and square-root formulations. No exact kernel empirical-risk optimizer, kernel-ridge coefficient or conditioning theorem, kernel-learning dual, or kernel stochastic-gradient result was found; those members require project-local assembly or proofs. Supporting files are Mathlib/Analysis/InnerProductSpace/GramMatrix.lean, Mathlib/LinearAlgebra/Matrix/PosDef.lean, and Mathlib/Analysis/Matrix/Order.lean.
