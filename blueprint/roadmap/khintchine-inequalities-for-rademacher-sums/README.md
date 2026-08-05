---
kind: roadmap
status: mapped
---

# Khintchine inequalities for Rademacher sums

Upper and lower moment bounds compare Rademacher sums with the Euclidean norm of their coefficients, including the first-moment form used in vector contraction.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)

## Candidate contents

- Khintchine upper moment bound
- Khintchine lower moment bound
- Optimal lower first-moment constant used in vector contraction

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Section 11.1.4, Lemma 11.1, printed pages 322-323
- `sources/ltfp_book.pdf` — Chapter 13, Section 13.1.3, Lemma 13.1, printed pages 385-386

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib searches found no Khintchine or Khinchin inequality declaration for Rademacher sums. Tail, moment-integration, and sub-Gaussian ingredients exist in the dependency nodes, but the stated upper, lower, and optimal first-moment bounds require project-local proofs.
