---
kind: roadmap
status: mapped
---

# Derivative-free nonconvex lower bounds

Covering-radius and indistinguishability lower bounds for zeroth-order global optimization of Lipschitz and smooth nonconvex functions.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)

## Candidate contents

- Deterministic zeroth-order oracle model
- Hidden-well family of nonconvex functions
- Query-value indistinguishability argument
- Covering-radius lower bound for query complexity
- Lipschitz nonconvex optimization lower bound
- First-order-oracle extension for differentiable Lipschitz objectives (Exercise 15.2)
- Random-query covering lower bound (Exercise 15.3)
- Smooth hidden-well construction
- Gradient-Lipschitz zeroth-order lower bound (Exercise 15.4)
- Curse of dimensionality for global optimization

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Section 15.2.2 and Exercises 15.2-15.4, printed pages 443-447

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: Metric.coveringNumber and ContDiffBump/ContDiffBump.support_eq provide covering and compactly supported smooth-bump primitives, but Mathlib has no zeroth-order oracle/query model, hidden-well family, indistinguishability reduction, random-query argument, or quantitative global-optimization lower bound. The bump-function API does not itself establish the derivative constants required by the book's hidden wells. Materially uncovered members: Deterministic zeroth-order oracle model; Hidden-well family of nonconvex functions; Query-value indistinguishability argument; Covering-radius lower bound for query complexity; Lipschitz nonconvex optimization lower bound; First-order-oracle extension for differentiable Lipschitz objectives (Exercise 15.2); Random-query covering lower bound (Exercise 15.3); Smooth hidden-well construction; Gradient-Lipschitz zeroth-order lower bound (Exercise 15.4); Curse of dimensionality for global optimization.
