---
kind: roadmap
status: mapped
---

# Bregman and multiplicative implicit bias

Mirror flow selects a Bregman-nearest interpolator, and a diagonal two-layer parameterization interpolates between l2 and l1 implicit bias as initialization changes.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Minimum-norm interpolation by gradient methods](../minimum-norm-interpolation-by-gradient-methods/README.md)
- [Mirror descent geometry](../mirror-descent-geometry/README.md)
- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Ordinary differential equations and gradient flows](../ordinary-differential-equations-and-gradient-flows/README.md)

## Candidate contents

- Mirror-flow equation
- Bregman projection of initialization
- Dual-variable limit
- Bregman Pythagorean identity (Exercise 12.3)
- Discrete mirror-descent implicit bias (Exercise 12.4)
- Diagonal linear network
- Squared-weight invariant
- Induced mirror potential
- Large-initialization l2 asymptotic
- Small-initialization l1 asymptotic

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Sections 12.1.3-12.1.4, printed pages 351-355

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no Bregman divergence or projection, mirror-flow implicit-bias theorem, diagonal linear-network dynamics, induced mirror potential, or small/large-initialization asymptotics. General convex calculus and ODE tools are only prerequisites; all ten members remain project-local.
