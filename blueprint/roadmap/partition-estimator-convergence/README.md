---
kind: roadmap
status: mapped
---

# Partition-estimator convergence

Finite-sample partition-regression bounds and the Lipschitz rate obtained by balancing cell diameter and count.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Generic local-smoother bias and variance](../generic-local-smoother-bias-and-variance/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Bounded differences and Bernstein concentration](../bounded-differences-and-bernstein-concentration/README.md)

## Candidate contents

- Partition-estimator convergence theorem
- Partition variance bound
- Partition empty-cell bias bound
- Cube-partition bandwidth balance
- Lipschitz nonparametric rate
- Curse-of-dimensionality consequence

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.3.1, printed pages 165-168

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Partition-estimator convergence theorem; Partition variance bound; Partition empty-cell bias bound; Cube-partition bandwidth balance; Lipschitz nonparametric rate; Curse-of-dimensionality consequence.
