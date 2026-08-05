---
kind: roadmap
status: mapped
---

# Complexity-aware model selection

Structural-risk and held-out-validation selection among model classes with prior-weighted penalties and oracle inequalities.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)
- [Uniform deviations, finite classes, and coverings](../uniform-deviations-finite-classes-and-coverings/README.md)

## Candidate contents

- Simultaneous weighted model bounds
- Structural-risk-minimization criterion
- Structural-risk-minimization oracle inequality
- Validation-set selection criterion
- Validation-set oracle inequality

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Sections 4.6-4.6.2, printed pages 103-105

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Simultaneous weighted model bounds; Structural-risk-minimization criterion; Structural-risk-minimization oracle inequality; Validation-set selection criterion; Validation-set oracle inequality.
