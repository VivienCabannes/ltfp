---
kind: roadmap
status: mapped
---

# Universal consistency of local averaging

Consistency for arbitrary square-integrable targets using density of Lipschitz functions and Stone's weighted-integrability condition.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Generic local-smoother bias and variance](../generic-local-smoother-bias-and-variance/README.md)
- [Partition-estimator convergence](../partition-estimator-convergence/README.md)
- [Stone's lemma for nearest-neighbor weights](../stone-s-lemma-for-nearest-neighbor-weights/README.md)
- [Kernel-regression convergence](../kernel-regression-convergence/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Universal-consistency weight condition
- Lipschitz density in L2
- Universal bias approximation bound
- Universal local-averaging consistency criterion
- Partition Stone condition
- Reciprocal Bernoulli-sum exercise (Exercise 6.5)
- Kernel-regression universal-consistency consequence
- Nearest-neighbor Stone lemma dependency

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.4, printed pages 174-177

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib proves that bounded continuous functions are dense in Lp under weak regularity, but no theorem making Lipschitz functions dense in L2 was found. That Lipschitz-approximation step still needs assembly or the source cited by the book. The nearest-neighbor specialization is separately blocked on the Stone-lemma node, whose proof is cited externally rather than supplied by the book.
