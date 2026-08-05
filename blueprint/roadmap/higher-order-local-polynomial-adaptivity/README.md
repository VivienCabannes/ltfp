---
kind: roadmap
status: mapped
---

# Higher-order local-polynomial adaptivity

The smoothness ceiling for nonnegative averaging weights and locally affine and polynomial estimators for higher regularity.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Local-averaging estimator constructions](../local-averaging-estimator-constructions/README.md)
- [Generic local-smoother bias and variance](../generic-local-smoother-bias-and-variance/README.md)
- [Kernel-regression convergence](../kernel-regression-convergence/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Nonnegative-weight second-order cancellation barrier
- Twice-smooth local-averaging rate
- Locally affine regression
- Local polynomial regression
- Second-order Nadaraya-Watson bias exercise (Exercise 6.6)
- Optimal twice-smooth bandwidth exercise (Exercise 6.6)

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.5, printed pages 177-178

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Nonnegative-weight second-order cancellation barrier; Twice-smooth local-averaging rate; Locally affine regression; Local polynomial regression; Second-order Nadaraya-Watson bias exercise; Optimal twice-smooth bandwidth exercise.
