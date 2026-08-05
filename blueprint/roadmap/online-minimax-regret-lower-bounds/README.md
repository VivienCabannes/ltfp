---
kind: roadmap
status: mapped
---

# Online minimax regret lower bounds

Random hypercube linear losses and a prior-average reduction yield matching square-root minimax lower bounds for online convex regret.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Online convex regret with projected gradients](../online-convex-regret-with-projected-gradients/README.md)
- [Khintchine inequalities for Rademacher sums](../khintchine-inequalities-for-rademacher-sums/README.md)
- [Bayesian minimax lower bound for fixed design](../bayesian-minimax-lower-bound-for-fixed-design/README.md)

## Candidate contents

- Hypercube linear-loss adversary
- Minimax online-regret lower bound
- Weighted-regret upper and lower bounds (Exercise 11.3)

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Section 11.1.4 and Exercise 11.3, printed pages 321-323

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib has no online minimax-regret reduction or hypercube adversary theorem. The source explicitly reuses the supremum-to-prior-average Bayesian reduction from Section 3.7 and the Khintchine lower bound; the remaining online argument requires a project-local proof.
