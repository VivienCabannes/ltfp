---
kind: roadmap
status: mapped
---

# Learning rules, capacity, and risk decomposition

Local averaging and empirical risk minimization, together with approximation, estimation, optimization, and capacity control.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Supervised learning setup and evaluation](../supervised-learning-setup-and-evaluation/README.md)

## Candidate contents

- Local-averaging principle
- Nearest-neighbor classifier
- Nearest-neighbor sample-size behavior (Exercise 2.8)
- Empirical risk minimizer
- Approximation error
- Estimation error
- Approximation-estimation decomposition
- Uniform deviation
- Empirical optimization error
- Uniform-deviation optimization bound
- Constrained capacity control
- Regularized empirical risk minimization
- Ridge objective
- Underfitting and overfitting

## Sources

- `sources/ltfp_book.pdf` — Chapter 2, Sections 2.3-2.3.2, printed pages 30-35

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no empirical-risk, learning-rule, local-averaging, nearest-neighbor-classifier, capacity-control, approximation/estimation/optimization-error, underfitting, or overfitting API. Generic minimizer predicates such as IsMinOn and finite well-founded argmin utilities exist, but they do not cover real-valued ERM or any statistical risk decomposition. This cluster requires project-local definitions and theorems built on the supervised-learning and decision-theory layers.
