---
kind: roadmap
status: mapped
---

# Lazy training and neural tangent kernels

Diverging output scaling freezes parameter motion and makes training follow the tangent linear model, whose infinite-width limit is the neural tangent kernel.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Mean-field limits for wide one-hidden-layer models](../mean-field-limits-for-wide-one-hidden-layer-models/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Neural variation spaces and random-feature kernels](../neural-variation-spaces-and-random-feature-kernels/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Ordinary differential equations and gradient flows](../ordinary-differential-equations-and-gradient-flows/README.md)

## Candidate contents

- Mean-field, last-layer, and lazy scalings
- Lazy parameter and predictor flows
- Infinitesimal parameter displacement
- Equivalent tangent linear model
- Convexified lazy-regime convergence
- Neural tangent kernel
- One-hidden-layer tangent features
- Infinite-width neural tangent kernel
- Random-feature and derivative-kernel decomposition

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.4, printed pages 375-377

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no neural-network scaling, lazy-training flow, tangent linearization, neural tangent kernel, infinite-width NTK limit, or random-feature/derivative-kernel decomposition. RKHS and Gaussian/random-feature prerequisites exist elsewhere in the graph, but all nine members of this cluster require project-local definitions and proofs.
