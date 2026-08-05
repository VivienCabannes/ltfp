---
kind: roadmap
status: mapped
---

# Generic local-smoother bias and variance

A universal local-smoother bias-variance bound in terms of locality and squared weights under bounded noise and Lipschitz targets.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Local-averaging estimator constructions](../local-averaging-estimator-constructions/README.md)
- [Classification calibration and surrogate-risk transfer](../classification-calibration-and-surrogate-risk-transfer/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Bounded-noise assumption
- Lipschitz-target assumption
- Conditional local-smoother bias-variance identity
- Generic local-smoother excess-risk bound
- Squared-weight variance criterion
- Weighted-distance bias criterion
- Overfitting and underfitting weight extremes
- Classification majority-vote calibration exercise (Exercise 6.2)

## Sources

- `sources/ltfp_book.pdf` — Chapter 6, Section 6.3 before 6.3.1, printed pages 163-165

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `LipschitzWith`
- `MeasureTheory.condExp`
- `ProbabilityTheory.variance_eq_integral`

Primary file: `Mathlib/Topology/EMetricSpace/Lipschitz.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: Lipschitz-target assumption. Assembly ingredients and limits: LipschitzWith directly states the target regularity. MeasureTheory.condExp and ProbabilityTheory.variance_eq_integral are genuine ingredients for conditional bias-variance calculations, but there is no weighted local-smoother identity, squared-weight variance criterion, weighted-distance bias bound, excess-risk theorem, or majority-vote calibration result. Supporting files are Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean and Mathlib/Probability/Moments/Variance.lean. Materially uncovered members: Bounded-noise assumption; Conditional local-smoother bias-variance identity; Generic local-smoother excess-risk bound; Squared-weight variance criterion; Weighted-distance bias criterion; Overfitting and underfitting weight extremes; Classification majority-vote calibration exercise.
