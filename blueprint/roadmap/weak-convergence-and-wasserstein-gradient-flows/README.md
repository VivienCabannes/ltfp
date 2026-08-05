---
kind: roadmap
status: mapped
---

# Weak convergence and Wasserstein gradient flows

Weak convergence of probability measures, Wasserstein distance, continuity equations, and measure-valued gradient-flow foundations.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Weak convergence of probability measures
- Empirical-measure convergence (Exercise 12.6)
- Wasserstein distance
- Continuity equation
- Wasserstein proximal step
- Measure-valued gradient flow

## Sources

- `sources/ltfp_book.pdf` — Chapter 12, Section 12.3.1, printed pages 365-370

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `MeasureTheory.FiniteMeasure.tendsto_iff_forall_integral_tendsto`
- `MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto`
- `MeasureTheory.TendstoInDistribution`
- `MeasureTheory.levyProkhorovDist`
- `MeasureTheory.LevyProkhorov.eq_convergenceInDistribution`

Primary file: `Mathlib/MeasureTheory/Measure/LevyProkhorovMetric.lean`.

Pinned Mathlib covers weak convergence of finite and probability measures, convergence in distribution, and the Levy-Prokhorov metric that metrizes weak convergence on separable spaces. No Wasserstein declaration was found; Wasserstein distance, continuity equations, and Wasserstein gradient flows remain missing.
