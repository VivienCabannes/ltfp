---
kind: roadmap
status: mapped
---

# Slow Lasso rates

Dimension-logarithmic, square-root-sample guarantees in random and fixed designs without restrictive covariance assumptions.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Sparse least-squares proof and probability toolkit](../sparse-least-squares-proof-and-probability-toolkit/README.md)
- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Rademacher symmetrization and contraction](../rademacher-symmetrization-and-contraction/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)
- [Maxima and smooth-sum expectation bounds](../maxima-and-smooth-sum-expectation-bounds/README.md)

## Candidate contents

- Random-design l1 Rademacher bound
- Dual norm
- General regularized least-squares inequality
- Duality of lp norms (Exercise 8.7)
- High-probability slow Lasso rate
- Square-root Lasso
- Expected slow Lasso rate (Exercise 8.8)

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Sections 8.3.2-8.3.3, printed pages 234-238

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `lp.dualPairing`
- `lp.dualPairing_apply`
- `lp.norm_dualPairing`
- `lp.tsum_mul_le_mul_norm`
- `lp.tsum_mul_le_mul_norm'`

Primary file: `Mathlib/Analysis/Normed/Lp/lpHolder.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched coverage: Dual norm and the core Holder-duality ingredient for Duality of lp norms (Exercise 8.7). lp.dualPairing constructs the conjugate-lp pairing and lp.norm_dualPairing bounds its operator norm; lp.tsum_mul_le_mul_norm in Mathlib/Analysis/Normed/Lp/lpSpace.lean proves Holder's inequality. The source TODO notes that the latter formulation does not uniformly cover the p = 1, q = infinity endpoint, so the finite l1/linfinity exercise still needs specialization and a norm-attainment argument. No Lasso risk theorem was found. Materially uncovered members: Duality of lp norms (Exercise 8.7) at the l1/linfinity endpoint; Random-design l1 Rademacher bound; General regularized least-squares inequality; High-probability slow Lasso rate; Square-root Lasso; Expected slow Lasso rate (Exercise 8.8).
