---
kind: roadmap
status: mapped
---

# Mirror descent geometry

Strongly convex mirror maps and Bregman divergences replace Euclidean projection, yielding entropy-based multiplicative updates on the simplex.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Online convex regret with projected gradients](../online-convex-regret-with-projected-gradients/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)

## Candidate contents

- Mirror map
- Relative strong convexity
- Entropy mirror map
- Online mirror-descent recursion
- Mirror-descent regret theorem
- Entropy multiplicative update
- Stochastic mirror descent for l1 regularization (Exercise 11.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Section 11.1.3, printed pages 319-321

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no mirror-map, relative-strong-convexity, mirror-descent recursion or regret theorem, multiplicative-weights update, or stochastic mirror-descent API. The standard simplex, logarithm and scalar entropy functions, convexity, and dual-norm tools exist only as assembly substrate; all seven source members remain project-local.
