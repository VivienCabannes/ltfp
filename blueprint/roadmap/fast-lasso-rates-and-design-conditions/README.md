---
kind: roadmap
status: mapped
---

# Fast Lasso rates and design conditions

Cone inequalities and restricted covariance conditions yielding k log(d)/n rates and their random-design transfer.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Slow Lasso rates](../slow-lasso-rates/README.md)
- [Sparse least-squares proof and probability toolkit](../sparse-least-squares-proof-and-probability-toolkit/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Lasso cone and support inequality
- Restricted eigenvalue property
- Fixed-design fast Lasso rate
- Expected fast rate (Exercise 8.9)
- Mutual incoherence condition
- Restricted isometry property
- Gaussian-design restricted eigenvalue property
- Gaussian mutual incoherence (Exercise 8.10)
- Irrepresentable condition
- Random-design fast Lasso rate
- Recovery of the slow rate without strong convexity (Exercise 8.11)

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Sections 8.3.4-8.3.6, printed pages 238-243

## Mathlib assessment

Legacy assessment: `missing`.

Proposition 8.5 is unproved in the source and needs a complete proof source or independent development.
