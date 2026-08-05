---
kind: roadmap
status: mapped
---

# Structured sparsity and low-rank regularization

Group and structured supports, low-rank matrices, multiple-kernel learning, elastic nets, and concave penalties.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Finite kernel optimization and stochastic algorithms](../finite-kernel-optimization-and-stochastic-algorithms/README.md)

## Candidate contents

- Group penalties
- Orthogonal-design group thresholding (Exercise 8.12)
- Structured sparsity
- Nested-group support patterns (Exercise 8.13)
- Nuclear norm
- Nuclear-norm proximal problem (Exercise 8.14)
- Nuclear-norm factorization (Exercise 8.15)
- Multiple-kernel learning
- Multiple-kernel variational equivalence (Exercise 8.16)
- Elastic net
- Concave sparsity penalties and debiasing
- Concave-penalty variational identity (Exercise 8.17)

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Section 8.5, printed pages 243-245

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: matrix singular-value, generic convex-proximal, RKHS, and group-indexing APIs provide prerequisites only. Searches for group Lasso or group thresholding, nuclear or trace norms and their proximal maps, multiple-kernel learning, elastic net, and concave sparsity penalties found no member-level declarations. Materially uncovered members: Group penalties; Orthogonal-design group thresholding (Exercise 8.12); Structured sparsity; Nested-group support patterns (Exercise 8.13); Nuclear norm; Nuclear-norm proximal problem (Exercise 8.14); Nuclear-norm factorization (Exercise 8.15); Multiple-kernel learning; Multiple-kernel variational equivalence (Exercise 8.16); Elastic net; Concave sparsity penalties and debiasing; Concave-penalty variational identity (Exercise 8.17).
