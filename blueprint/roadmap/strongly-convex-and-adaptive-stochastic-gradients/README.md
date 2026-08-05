---
kind: roadmap
status: mapped
---

# Strongly convex and adaptive stochastic gradients

One-over-time stochastic convergence under strong convexity and preconditioned coordinatewise geometries for adaptive methods.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Newton and preconditioned gradient methods](../newton-and-preconditioned-gradient-methods/README.md)

## Candidate contents

- Regularized strongly convex stochastic-gradient recursion
- Strongly convex stochastic-gradient convergence theorem
- Noisy quadratic constant-step exercise (Exercise 5.31)
- Averaged noisy quadratic exercise (Exercise 5.31)
- Log-free weighted strongly convex exercise (Exercise 5.32)
- Sample-mean recursion exercise (Exercise 5.33)
- Blended-step-size strongly convex exercise (Exercise 5.34)
- Preconditioned stochastic-gradient complexity bound
- Optimal diagonal stochastic preconditioner
- Adagrad covariance motivation
- Adam covariance motivation

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Sections 5.4.1-5.4.2, printed pages 139-143

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Regularized strongly convex stochastic-gradient recursion; Strongly convex stochastic-gradient convergence theorem; Noisy quadratic constant-step exercise; Averaged noisy quadratic exercise; Log-free weighted strongly convex exercise; Sample-mean recursion exercise; Blended-step-size strongly convex exercise; Preconditioned stochastic-gradient complexity bound; Optimal diagonal stochastic preconditioner; Adagrad covariance motivation; Adam covariance motivation.
