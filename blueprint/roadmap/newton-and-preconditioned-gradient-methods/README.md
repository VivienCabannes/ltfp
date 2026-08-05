---
kind: roadmap
status: mapped
---

# Newton and preconditioned gradient methods

Newton's Hessian-scaled iteration has local quadratic convergence under Hessian regularity, while linear changes of variables motivate condition-number preconditioning.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Newton iteration
- Local quadratic convergence
- Newton Hessian-Lipschitz exercise (Exercise 5.16)
- Linear preconditioning equivalence

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.2.5, Newton method and Preconditioning, printed pages 127-129; Exercise 5.16

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib search found only polynomial Newton-map dynamics, not Newton optimization, Hessian-preconditioned gradient descent, or local quadratic convergence. Matrix inverse, derivative, Hessian, and spectral APIs are available through prerequisite clusters.
