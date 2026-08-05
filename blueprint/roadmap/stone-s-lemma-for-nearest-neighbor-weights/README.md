---
kind: roadmap
status: mapped
---

# Stone's lemma for nearest-neighbor weights

The finite-dimensional geometric bound that gives Stone's weighted-integrability condition for k-nearest-neighbor weights.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Nearest-neighbor geometry and convergence](../nearest-neighbor-geometry-and-convergence/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Stone neighbor-count lemma
- k-nearest-neighbor weighted-integrability inequality

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.4, condition (6.13) and the k-nearest-neighbor discussion, printed pages 174-177
- `sources/formalization_notes.md` — External-source gaps: nearest-neighbor universal-consistency argument

## Mathlib assessment

Legacy assessment: `missing`.

No nearest-neighbor or Stone-lemma declaration was found in the pinned Mathlib checkout. The book cites Biau and Devroye (2015), Lemma 10.7, without proving the result, so this needs an independently reviewed external source or a full project-local proof.
