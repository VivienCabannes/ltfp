---
kind: roadmap
status: mapped
---

# Stochastic multiarmed bandits

Explore-then-commit and upper-confidence-bound policies for sub-Gaussian arms receive gap-dependent and gap-free regret bounds.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Online convex regret with projected gradients](../online-convex-regret-with-projected-gradients/README.md)
- [Bayesian posterior updating and prediction](../bayesian-posterior-updating-and-prediction/README.md)

## Candidate contents

- Sub-Gaussian bandit model
- Pull-count regret decomposition
- Explore-then-commit algorithm
- Gap-dependent explore-then-commit bound
- Gap-free explore-then-commit bound (Exercise 11.8)
- Epsilon-greedy policy
- Upper-confidence-bound algorithm
- UCB pull-count bound
- UCB regret bounds
- Thompson sampling
- Pure-exploitation linear-regret lower bound (Exercise 11.7)

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Sections 11.3-11.3.3, printed pages 331-339

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no multiarmed-bandit model, pull-count regret decomposition, explore-then-commit, epsilon-greedy, UCB, Thompson-sampling, pure-exploitation lower bound, or bandit-regret API. Sub-Gaussian concentration and generic posterior kernels are reusable prerequisites, but all eleven bandit-specific members require project-local definitions and proofs.
