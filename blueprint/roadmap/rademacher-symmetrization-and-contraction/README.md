---
kind: roadmap
status: mapped
---

# Rademacher symmetrization and contraction

Population and empirical Rademacher complexity, symmetrization, finite-class bounds, and Lipschitz contraction.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Uniform deviations, finite classes, and coverings](../uniform-deviations-finite-classes-and-coverings/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Maxima and smooth-sum expectation bounds](../maxima-and-smooth-sum-expectation-bounds/README.md)

## Candidate contents

- Rademacher complexity
- Rademacher monotonicity exercise (Exercise 4.9)
- Rademacher Minkowski-sum exercise (Exercise 4.9)
- Rademacher homogeneity exercise (Exercise 4.9)
- Translation invariance exercise (Exercise 4.9)
- Convex-hull invariance exercise (Exercise 4.9)
- Massart finite-class lemma exercise (Exercise 4.10)
- Symmetrization theorem
- Gaussian complexity
- Gaussian-Rademacher comparison exercise (Exercise 4.11)
- Empirical Rademacher complexity
- Data-dependent Rademacher generalization bound
- Lipschitz contraction principle
- Loss-class contraction bound
- Absolute-value contraction principle

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Sections 4.5-4.5.2, printed pages 91-96

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Rademacher complexity; Rademacher monotonicity exercise; Rademacher Minkowski-sum exercise; Rademacher homogeneity exercise; Translation invariance exercise; Convex-hull invariance exercise; Massart finite-class lemma exercise; Symmetrization theorem; Gaussian complexity; Gaussian-Rademacher comparison exercise; Empirical Rademacher complexity; Data-dependent Rademacher generalization bound; Lipschitz contraction principle; Loss-class contraction bound; Absolute-value contraction principle. Mathlib/Analysis/Calculus/Rademacher.lean concerns almost-everywhere differentiability and is unrelated to Rademacher complexity.
