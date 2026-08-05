---
kind: roadmap
status: mapped
---

# Nearest-neighbor geometry and convergence

Euclidean nearest-neighbor distance bounds and the resulting k-nearest-neighbor regression rate.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Generic local-smoother bias and variance](../generic-local-smoother-bias-and-variance/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Nearest-neighbor distance lemma
- Disjoint-neighborhood volume argument
- kth-nearest-neighbor distance lemma
- Random-block reduction to first neighbors
- k-nearest-neighbor convergence theorem
- Optimal neighbor-count balance
- Noiseless one-nearest-neighbor consistency exercise (Exercise 6.3)

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.3.2, printed pages 168-170

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Nearest-neighbor distance lemma; Disjoint-neighborhood volume argument; kth-nearest-neighbor distance lemma; Random-block reduction to first neighbors; k-nearest-neighbor convergence theorem; Optimal neighbor-count balance; Noiseless one-nearest-neighbor consistency exercise.
