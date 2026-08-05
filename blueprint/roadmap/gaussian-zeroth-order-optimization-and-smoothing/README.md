---
kind: roadmap
status: mapped
---

# Gaussian zeroth-order optimization and smoothing

Gaussian finite differences and convolution smoothing provide smooth and nonsmooth zeroth-order convergence rates, including noisy oracle tradeoffs.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Gaussian-smoothed objective
- Gaussian integration-by-parts gradient identity
- Smoothing bias
- Gradient-estimator second moment (Exercise 11.5)
- Gaussian moment bounds (Exercise 11.4)
- Smooth zeroth-order convergence (Exercise 11.6)
- Randomized smoothing
- Lipschitz Gaussian convolution
- Nonsmooth zeroth-order convergence

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Section 11.2, printed pages 323-331

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib supplies standard multivariate Gaussian measures, means and covariances, finite Gaussian moments, and general Frechet integration-by-parts lemmas. It does not supply the Gaussian-smoothing gradient identity, the dimension-dependent moment bounds used here, smoothing bias and estimator-variance bounds, randomized smoothing, or any smooth or nonsmooth zeroth-order convergence theorem. No cluster member is directly covered.
