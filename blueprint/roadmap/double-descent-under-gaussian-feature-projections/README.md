---
kind: roadmap
status: mapped
---

# Double descent under Gaussian feature projections

A varying Gaussian random-feature dimension yields a full double-descent curve via conditional Gaussian and inverse-Wishart identities.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Randomized least-squares compression and embeddings](../randomized-least-squares-compression-and-embeddings/README.md)
- [Minimum-norm interpolation by gradient methods](../minimum-norm-interpolation-by-gradient-methods/README.md)
- [Gaussian linear double descent](../gaussian-linear-double-descent/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Gaussian projection model
- Projected-estimator bias-variance decomposition
- Underparameterized projected risk
- Gaussian-projection bias bound
- Overparameterized projected estimator
- Overparameterized projected risk
- Infinite-feature limiting risk

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.2.4, printed pages 360-365

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no Gaussian random-feature projection model, projected-estimator bias-variance theorem, inverse-Wishart expectation, finite-feature double-descent formula, or infinite-feature risk limit. Generic Gaussian and linear-map APIs are reusable prerequisites, but none of the seven cluster members is directly covered.
