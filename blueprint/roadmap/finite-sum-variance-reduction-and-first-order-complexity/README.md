---
kind: roadmap
status: mapped
---

# Finite-sum variance reduction and first-order complexity

SAGA control-variate gradients, exponential finite-sum convergence, and deterministic and stochastic oracle-rate comparisons.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Strongly convex and adaptive stochastic gradients](../strongly-convex-and-adaptive-stochastic-gradients/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Nesterov acceleration and momentum methods](../nesterov-acceleration-and-momentum-methods/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)

## Candidate contents

- Smooth strongly convex finite-sum setup
- SAGA update
- Unbiased SAGA gradient estimator
- SAGA convergence theorem
- SAGA Lyapunov function
- Sum-versus-product condition-number improvement
- Convex first-order rate table
- Strongly convex first-order rate table
- Gradient-oracle complexity table
- Dimensional-homogeneity exercise (Exercise 5.36)
- Rademacher-versus-single-pass stochastic-gradient comparison

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Sections 5.4.4-5.5, printed pages 146-153

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Smooth strongly convex finite-sum setup; SAGA update; Unbiased SAGA gradient estimator; SAGA convergence theorem; SAGA Lyapunov function; Sum-versus-product condition-number improvement; Convex first-order rate table; Strongly convex first-order rate table; Gradient-oracle complexity table; Dimensional-homogeneity exercise; Rademacher-versus-single-pass stochastic-gradient comparison.
