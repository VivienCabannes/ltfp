---
kind: roadmap
status: mapped
---

# Structured surrogate generalization

Generalization guarantees for quadratic and smooth structured surrogates under linear parameterizations, with kernel and structured-regularization extensions.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Vector-valued learning bounds](../vector-valued-learning-bounds/README.md)
- [Smooth structured surrogates](../smooth-structured-surrogates/README.md)
- [Least-squares stochastic-gradient bias and variance](../least-squares-stochastic-gradient-bias-and-variance/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Structured sparsity and low-rank regularization](../structured-sparsity-and-low-rank-regularization/README.md)

## Candidate contents

- Structured surrogate estimation-error decomposition
- Lipschitz constants for structured decoding losses
- Stochastic-gradient structured prediction bound
- Quadratic-surrogate least-squares bound
- Kernel-method extension (discussion)
- Trace-norm regularization extension (discussion)
- Calibration transfer to target structured risk
- Alternative smooth surrogate bound (Exercise 13.10)
- Robust-regression specialization
- Ranking specialization

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Sections 13.6-13.7 and Exercise 13.10, printed pages 402-407

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: RKHS, matrix, probability, and convex-analysis foundations exist, but there is no structured-prediction risk, vector-valued learning-bound, trace-norm generalization, robust-regression/ranking specialization, or calibration-transfer assembly. Materially uncovered members: Structured surrogate estimation-error decomposition; Lipschitz constants for structured decoding losses; Stochastic-gradient structured prediction bound; Quadratic-surrogate least-squares bound; Kernel-method extension (discussion); Trace-norm regularization extension (discussion); Calibration transfer to target structured risk; Alternative smooth surrogate bound (Exercise 13.10); Robust-regression specialization; Ranking specialization.
