---
kind: roadmap
status: mapped
---

# Mean-field limits for wide one-hidden-layer models

Wide one-hidden-layer networks become empirical measures of particles whose limiting dynamics satisfy a Wasserstein continuity equation.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Variation spaces and neural approximation](../variation-spaces-and-neural-approximation/README.md)
- [Weak convergence and Wasserstein gradient flows](../weak-convergence-and-wasserstein-gradient-flows/README.md)
- [Ordinary differential equations and gradient flows](../ordinary-differential-equations-and-gradient-flows/README.md)

## Candidate contents

- Particle representation of a two-layer network
- Probability-measure reformulation
- Convex risk over probability measures
- Particle gradient flow
- Wasserstein proximal flow
- Finite-particle mean-field convergence
- Conditional homogeneous global convergence

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.3.1, printed pages 365-370

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib has weak convergence and Levy-Prokhorov infrastructure for probability measures, but searches found no particle neural-network flow, Wasserstein proximal flow, empirical-measure mean-field limit, or homogeneous global-convergence theorem. All seven neural mean-field members remain project-local, and the source's final convergence claim is itself conditional.
