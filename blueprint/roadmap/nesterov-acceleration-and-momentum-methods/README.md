---
kind: roadmap
status: mapped
---

# Nesterov acceleration and momentum methods

Momentum-style Nesterov recurrences attain optimal accelerated rates for smooth convex and strongly convex objectives.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Smooth convex gradient-descent rates](../smooth-convex-gradient-descent-rates/README.md)

## Candidate contents

- Strongly convex Nesterov iteration
- Accelerated strongly convex rate
- Strongly convex acceleration Lyapunov exercise (Exercise 5.14)
- Convex Nesterov iteration
- Accelerated convex one-over-time-squared rate
- Convex acceleration Lyapunov exercise (Exercise 5.15)

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.2.5, Nesterov acceleration, printed pages 126-127; Exercises 5.14-5.15

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib search found no Nesterov-acceleration, momentum-iteration, or accelerated-gradient optimization declaration. Generic smoothness and convexity APIs are available through prerequisite clusters, but the recurrences and rates are project-local.
