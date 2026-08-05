---
kind: roadmap
status: mapped
---

# Stochastic gradient descent and generalization

Unbiased stochastic gradients, convex Lipschitz convergence, and single-pass expected-risk generalization.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Empirical-risk decomposition and approximation](../empirical-risk-decomposition-and-approximation/README.md)
- [Nonconvex gradient descent and stationarity guarantees](../nonconvex-gradient-descent-and-stationarity-guarantees/README.md)

## Candidate contents

- Conditionally unbiased stochastic gradient
- Stochastic gradient descent algorithm
- Empirical-risk sampling mode
- Expected-risk single-pass mode
- Unbiased-gradient assumption
- Bounded-gradient assumption
- Convex stochastic-gradient convergence theorem
- Constant-step averaged stochastic-gradient bound
- Single-pass stochastic-gradient generalization bound
- Projected high-probability stochastic-gradient exercise (Exercise 5.26)
- Martingale-difference stochastic-gradient analysis exercise (Exercise 5.26)
- Minibatch stochastic-gradient exercise (Exercise 5.27)
- Smooth stochastic-gradient exercise (Exercise 5.28)
- Smooth minibatch improvement exercise (Exercise 5.28)
- Nonuniform importance-sampling exercise (Exercise 5.29)
- Support-vector importance-sampling specialization exercise (Exercise 5.29)
- Nonconvex stochastic small-gradient exercise (Exercise 5.30)

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.4 before 5.4.1, printed pages 134-139

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Conditionally unbiased stochastic gradient; Stochastic gradient descent algorithm; Empirical-risk sampling mode; Expected-risk single-pass mode; Unbiased-gradient assumption; Bounded-gradient assumption; Convex stochastic-gradient convergence theorem; Constant-step averaged stochastic-gradient bound; Single-pass stochastic-gradient generalization bound; Projected high-probability stochastic-gradient exercise; Martingale-difference stochastic-gradient analysis exercise; Minibatch stochastic-gradient exercise; Smooth stochastic-gradient exercise; Smooth minibatch improvement exercise; Nonuniform importance-sampling exercise; Support-vector importance-sampling specialization exercise; Nonconvex stochastic small-gradient exercise.
