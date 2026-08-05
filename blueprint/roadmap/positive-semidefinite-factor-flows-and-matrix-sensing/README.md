---
kind: roadmap
status: mapped
---

# Positive-semidefinite factor flows and matrix sensing

Gradient flow for a factorized positive-semidefinite matrix preserves rank and gives conditional global convergence, with Oja flow and matrix sensing as examples.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Ordinary differential equations and gradient flows](../ordinary-differential-equations-and-gradient-flows/README.md)
- [Bregman and multiplicative implicit bias](../bregman-and-multiplicative-implicit-bias/README.md)
- [Structured sparsity and low-rank regularization](../structured-sparsity-and-low-rank-regularization/README.md)

## Candidate contents

- Factorized convex matrix objective
- Factor and induced PSD matrix flows
- Rank preservation (Exercise 12.7)
- PSD optimality conditions
- Conditional global convergence
- Local minima are global (Exercise 12.8)
- Oja flow and closed-form solution
- Incremental eigenvalue learning
- Matrix-sensing mirror flow (Exercise 12.9)
- Nuclear-norm implicit bias (Exercise 12.9)

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Sections 12.3.2-12.3.4, printed pages 370-375

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib supplies positive-semidefinite matrices, spectral calculus, ranks, traces, and general ODE foundations. Searches found no factorized PSD gradient flow, rank-preservation theorem, matrix-flow optimality and convergence package, Oja flow, matrix-sensing mirror flow, or nuclear-norm implicit-bias result. None of the ten cluster members is direct.
