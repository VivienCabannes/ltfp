---
kind: roadmap
status: mapped
---

# Gradient boosting convergence and early stopping

Smooth-loss gradient boosting receives gauge-controlled optimization rates, path-norm bounds, and Rademacher-based consistency under early stopping.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Atomic geometry and classical boosting](../atomic-geometry-and-classical-boosting/README.md)
- [Smooth convex gradient-descent rates](../smooth-convex-gradient-descent-rates/README.md)
- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)

## Candidate contents

- Generic gradient-boosting algorithm
- Smooth quadratic upper-bound update
- Gradient-boosting convergence theorem (Exercise 10.8)
- Boosting gauge-growth bound
- Scalar nonlinear-recurrence lemma
- Rademacher complexity of variation balls (Exercise 10.9)
- Boosting expected-risk guarantee
- Early-stopping schedule
- Finite-variation Bayes consistency

## Sources

- `sources/ltfp_book.pdf` — Chapter 10, Sections 10.3.5-10.3.6, printed pages 304-309

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: generic smooth-convex descent, gauge, recurrence, and Rademacher prerequisites exist, but do not state a boosting result. Searches for gradient boosting, functional gradient descent over weak learners, boosting gauge growth, variation-ball complexity, early stopping, and Bayes consistency found no member-level declaration. Materially uncovered members: Generic gradient-boosting algorithm; Smooth quadratic upper-bound update; Gradient-boosting convergence theorem; Boosting gauge-growth bound; Scalar nonlinear-recurrence lemma; Rademacher complexity of variation balls; Boosting expected-risk guarantee; Early-stopping schedule; Finite-variation Bayes consistency.
