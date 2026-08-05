---
kind: roadmap
status: mapped
---

# Combinatorial sparse model selection

Near-oracle rates for known and unknown sparsity using l0 constraints and penalties.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Sparse least-squares proof and probability toolkit](../sparse-least-squares-proof-and-probability-toolkit/README.md)
- [Complexity-aware model selection](../complexity-aware-model-selection/README.md)
- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)

## Candidate contents

- l0 pseudonorm and support
- Sparsity oracle and logarithmic adaptivity price
- Known-sparsity model-selection bound
- Approximate constrained minimization (Exercise 8.2)
- Finite-design orthogonal matching-pursuit support-selection algorithm
- Iterative sorting
- Sparse Lipschitz model selection (Exercise 8.3)
- l0-penalized estimator
- Adaptive l0 bound
- Cardinality-dependent penalty (Exercise 8.4)
- Forward-backward subset selection
- Iterative hard thresholding

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Section 8.2, printed pages 226-230

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: Finsupp.support, Finset.card, and generic finite-set minimization primitives can encode supports and cardinalities, but no listed sparse-model-selection result is present. Searches for l0 pseudonorms and penalties, finite-design orthogonal matching-pursuit support selection, iterative sorting, forward-backward selection, and iterative hard thresholding found no relevant declaration. Materially uncovered members: l0 pseudonorm and support; Sparsity oracle and logarithmic adaptivity price; Known-sparsity model-selection bound; Approximate constrained minimization (Exercise 8.2); Finite-design orthogonal matching-pursuit support-selection algorithm; Iterative sorting; Sparse Lipschitz model selection (Exercise 8.3); l0-penalized estimator; Adaptive l0 bound; Cardinality-dependent penalty (Exercise 8.4); Forward-backward subset selection; Iterative hard thresholding.
