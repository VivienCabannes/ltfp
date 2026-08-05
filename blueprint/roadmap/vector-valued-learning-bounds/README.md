---
kind: roadmap
status: mapped
---

# Vector-valued learning bounds

Optimization and generalization bounds for vector-valued predictors, including stochastic-gradient and vector-contraction arguments.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Multicategory convex surrogates](../multicategory-convex-surrogates/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)
- [Khintchine inequalities for Rademacher sums](../khintchine-inequalities-for-rademacher-sums/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Structured sparsity and low-rank regularization](../structured-sparsity-and-low-rank-regularization/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Shallow ReLU models and norm-controlled estimation](../shallow-relu-models-and-norm-controlled-estimation/README.md)
- [Mirror descent geometry](../mirror-descent-geometry/README.md)

## Candidate contents

- Vector-valued linear score models
- Euclidean and trace-norm parameter constraints
- Lipschitz constants for multicategory losses
- Stochastic-gradient multicategory excess-risk bound
- Mirror descent with trace-norm penalty (Exercise 13.4)
- Vector-valued Rademacher complexity
- One-step vector-valued Rademacher comparison lemma (Lemma 13.1)
- Vector-valued contraction principle
- Linear multicategory Rademacher bound
- Neural multicategory bound (Exercise 13.5)

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Sections 13.1.2-13.1.3 and Exercises 13.4-13.5, printed pages 383-387

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: finite-dimensional Euclidean spaces, matrices, norms, finite sums, and generic probability are available, but searches found no trace/nuclear-norm learning constraint, vector-valued Rademacher complexity, vector contraction, multicategory stochastic-gradient bound, mirror-descent trace-norm result, or neural multicategory bound. The Rademacher files in Mathlib concern almost-everywhere differentiability, not random-sign complexity. Materially uncovered members: Vector-valued linear score models; Euclidean and trace-norm parameter constraints; Lipschitz constants for multicategory losses; Stochastic-gradient multicategory excess-risk bound; Mirror descent with trace-norm penalty (Exercise 13.4); Vector-valued Rademacher complexity; One-step vector-valued Rademacher comparison lemma (Lemma 13.1); Vector-valued contraction principle; Linear multicategory Rademacher bound; Neural multicategory bound (Exercise 13.5).
