---
kind: roadmap
status: mapped
---

# Gradient descent on quadratic objectives

Batch gradient descent solved exactly on least-squares quadratics through spectral recurrences, condition numbers, and line searches.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Empirical-risk decomposition and approximation](../empirical-risk-decomposition-and-approximation/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Spectral and differential matrix tools](../spectral-and-differential-matrix-tools/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Optimization-error decomposition for approximate empirical-risk minimization
- Derivative oracle hierarchy
- Gradient descent algorithm
- Least-squares quadratic objective
- Hessian spectral constants
- Closed-form gradient-descent recurrence
- Optimal constant step size
- Exponential distance convergence
- Exponential function-value convergence
- Semidefinite quadratic one-over-time convergence
- Smallest-positive-eigenvalue convergence exercise (Exercise 5.1)
- Exact-line-search and Kantorovich exercise (Exercise 5.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Sections 5.1-5.2.1, printed pages 109-116

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Optimization-error decomposition for approximate empirical-risk minimization; Derivative oracle hierarchy; Gradient descent algorithm; Least-squares quadratic objective; Hessian spectral constants; Closed-form gradient-descent recurrence; Optimal constant step size; Exponential distance convergence; Exponential function-value convergence; Semidefinite quadratic one-over-time convergence; Smallest-positive-eigenvalue convergence exercise; Exact-line-search and Kantorovich exercise.
