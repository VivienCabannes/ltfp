---
kind: roadmap
status: mapped
---

# Shallow ReLU models and norm-controlled estimation

Single-hidden-layer networks and width-independent estimation bounds obtained from ReLU homogeneity and l1-type norm control.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)
- [Nonconvex gradient descent and stationarity guarantees](../nonconvex-gradient-descent-and-stationarity-guarantees/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)

## Candidate contents

- Single-hidden-layer neural network
- Standard activation functions
- Cross-entropy and logistic-loss equivalence
- Optimization-estimation-approximation decomposition
- Nonconvex empirical-risk minimization and stationarity
- Infinite-width global-convergence claim
- ReLU positive homogeneity
- Scale balancing of squared weight decay
- Normalized incoming weights and l1 output penalty
- Neural-network Rademacher bound
- Estimation-error bound
- l1-normalized incoming weights (Exercise 9.1)
- Deep-network Rademacher recursion (Exercise 9.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 9, Sections 9.1-9.2.3, printed pages 247-256

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Real.sigmoid`
- `Real.sigmoid_def`
- `Real.hasDerivAt_sigmoid`
- `lipschitzWith_posPart`

Primary file: `Mathlib/Analysis/SpecialFunctions/Sigmoid.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Directly covered in part: Standard activation functions. Real.sigmoid defines the logistic sigmoid and Real.hasDerivAt_sigmoid gives its derivative; the scalar specialization of posPart is ReLU, and lipschitzWith_posPart proves it is 1-Lipschitz in Mathlib/Analysis/Normed/Order/Lattice.lean. Mathlib has no named neural-network or ReLU learning interface, and the positive-homogeneity, scale-balancing, risk, stationarity, infinite-width, and Rademacher statements are absent. Materially uncovered members: Single-hidden-layer neural network; Cross-entropy and logistic-loss equivalence; Optimization-estimation-approximation decomposition; Nonconvex empirical-risk minimization and stationarity; Infinite-width global-convergence claim; ReLU positive homogeneity; Scale balancing of squared weight decay; Normalized incoming weights and l1 output penalty; Neural-network Rademacher bound; Estimation-error bound; l1-normalized incoming weights (Exercise 9.1); Deep-network Rademacher recursion (Exercise 9.2).
