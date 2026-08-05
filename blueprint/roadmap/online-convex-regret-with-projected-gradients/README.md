---
kind: roadmap
status: mapped
---

# Online convex regret with projected gradients

Projected online stochastic gradient descent controls regret for convex and strongly convex loss sequences and admits online-to-batch conversion.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Strongly convex and adaptive stochastic gradients](../strongly-convex-and-adaptive-stochastic-gradients/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Normalized and adversarial regret
- Oblivious and adaptive adversaries
- Projected online stochastic gradient descent
- Convex online-regret theorem (Exercise 11.1)
- Online-to-batch conversion
- Adaptive pseudo-regret
- Strongly convex online-regret theorem

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Sections 11.1-11.1.2, printed pages 313-319

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no online-regret, adversary, projected online-gradient, online-to-batch, pseudo-regret, or strongly-convex online-regret API. Mathlib's convexity, orthogonal-projection, conditional-expectation, and finite-sum infrastructure can support the development, but none of the seven cluster members is directly available.
