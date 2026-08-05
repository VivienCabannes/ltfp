---
kind: roadmap
status: mapped
---

# Margin surrogates and support-vector geometry

Real-valued binary scores, convex margin losses, and hard- and soft-margin support-vector formulations, duality, and sparsity.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Real-valued score classifier
- Randomized sign convention at zero
- Margin-based zero-one loss
- Phi-risk
- Square surrogate
- Logistic surrogate
- Hinge surrogate
- Squared-hinge surrogate
- Exponential surrogate
- Separable maximum-margin support-vector machine
- Slack-variable soft-margin support-vector machine
- Regularized hinge-loss equivalence
- Support-vector-machine Lagrange dual
- SVM strong duality and complementary slackness
- Support-vector representation

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Sections 4.1-4.1.2, printed pages 72-76

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found convex-cone and Farkas-lemma primitives but no general finite-dimensional Lagrangian strong-duality, KKT, or complementary-slackness API. The SVM dual and support-vector argument therefore need a project-local specialization; closed-form minimization of the quadratic Lagrangian can reuse the matrix-quadratic prerequisite.
