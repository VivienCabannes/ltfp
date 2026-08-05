---
kind: roadmap
status: mapped
---

# Nonconvex gradient descent and stationarity guarantees

Smooth nonconvex gradient descent guarantees that some iterate has a small gradient norm, without claiming convergence to a stationary point.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Nonconvex small-gradient iterate bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.2.6, Nonconvex Objective Functions, printed pages 129-130

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib search found no nonconvex gradient-descent stationarity or small-gradient iterate theorem. Frechet calculus and smoothness foundations are available through prerequisite clusters.
