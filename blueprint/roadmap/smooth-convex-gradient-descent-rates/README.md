---
kind: roadmap
status: mapped
---

# Smooth convex gradient-descent rates

Exponential convergence under smooth strong convexity, one-over-time convergence under smooth convexity, and statistical early stopping.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)
- [Ridge regression and dimension-free control](../ridge-regression-and-dimension-free-control/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)

## Candidate contents

- Smooth strongly convex gradient-descent convergence theorem
- Regularized logistic and ridge constants exercise (Exercise 5.9)
- Smooth convex gradient-descent convergence theorem
- Lyapunov proof for smooth convex descent
- Alternative smooth-descent proof exercise (Exercise 5.12)
- Reciprocal-gap smooth-descent proof exercise (Exercise 5.13)
- Comparator inequality for early stopping
- Early-stopped batch generalization bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Sections 5.2.3-5.2.4, printed pages 122-126

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Smooth strongly convex gradient-descent convergence theorem; Regularized logistic and ridge constants exercise; Smooth convex gradient-descent convergence theorem; Lyapunov proof for smooth convex descent; Alternative smooth-descent proof exercise; Reciprocal-gap smooth-descent proof exercise; Comparator inequality for early stopping; Early-stopped batch generalization bound.
