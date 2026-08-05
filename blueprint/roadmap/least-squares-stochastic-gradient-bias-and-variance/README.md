---
kind: roadmap
status: mapped
---

# Least-squares stochastic-gradient bias and variance

Least-mean-squares recursion as a random linear system with initialization-bias and observation-noise variance bounds.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Least-mean-squares recursion
- Classical averaged least-mean-squares excess-risk bound
- Explicit least-mean-squares bias-variance decomposition
- Weaker regression-noise assumption exercise (Exercise 5.35)
- Additive-noise simplified recursion
- Unrolled averaged recursion
- Averaged constant-step bias bound
- Averaged constant-step variance bound
- Comparison with least-squares empirical minimization

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.4.3, printed pages 143-146

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Least-mean-squares recursion; Classical averaged least-mean-squares excess-risk bound; Explicit least-mean-squares bias-variance decomposition; Weaker regression-noise assumption exercise; Additive-noise simplified recursion; Unrolled averaged recursion; Averaged constant-step bias bound; Averaged constant-step variance bound; Comparison with least-squares empirical minimization.
