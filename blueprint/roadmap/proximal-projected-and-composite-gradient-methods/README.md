---
kind: roadmap
status: mapped
---

# Proximal, projected, and composite gradient methods

Proximal-gradient majorization handles smooth-plus-nonsmooth composite objectives, specializing to projected gradient descent and l1 soft thresholding.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Proximal-gradient iteration
- Projected gradient descent
- l1 soft-thresholding proximal map
- Proximal-gradient convergence exercise (Exercise 5.17)

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.2.5, Proximal gradient descent, printed pages 128-129; Exercise 5.17

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib search found no proximal-gradient, proximal-map, soft-thresholding, or projected-gradient optimization declaration. Convexity, norms, and projection foundations are available through prerequisite clusters.
