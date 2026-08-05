---
kind: roadmap
status: mapped
---

# Atomic geometry and classical boosting

Boosting over symmetric weak learners is expressed through signed measures, atomic gauges, matching pursuit, and AdaBoost's exponential-risk updates.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Lasso geometry and optimization](../lasso-geometry-and-optimization/README.md)
- [Signed measures and variation norms](../signed-measures-and-variation-norms/README.md)
- [Variation spaces and neural approximation](../variation-spaces-and-neural-approximation/README.md)

## Candidate contents

- Weak-learner oracle (Exercise 10.6)
- Signed-measure predictor representation
- Variation and atomic norms
- Gauge and polar gauge
- Gauge-polar inequality
- Matching-pursuit iteration
- Gauge-controlled matching-pursuit rate
- Orthogonal matching-pursuit approximation rate (Exercise 10.7)
- AdaBoost update
- Weak-learnability convergence

## Sources

- `sources/ltfp_book.pdf` — Chapter 10, Sections 10.3.1-10.3.4, printed pages 298-304

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `gauge`
- `gauge_def`
- `gauge_nonneg`
- `gauge_add_le`
- `gauge_sum_le`
- `gaugeSeminorm`
- `LinearMap.polar`
- `LinearMap.polar_mem_iff`
- `LinearMap.subset_bipolar`

Primary file: `Mathlib/Analysis/Convex/Gauge.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched coverage: Gauge and polar gauge. gauge is the Minkowski functional, with nonnegativity, subadditivity, finite-sum control, and gaugeSeminorm; LinearMap.polar and LinearMap.polar_mem_iff in Mathlib/Analysis/LocallyConvex/Polar.lean define the absolute polar for a bilinear pairing, and subset_bipolar supplies one bipolar inclusion. These are generic geometric primitives, not the variation/atomic-norm identification or the requested gauge-polar inequality. Searches found no matching pursuit, orthogonal matching-pursuit approximation rate, AdaBoost, or weak-learnability convergence theorem. Materially uncovered members: Weak-learner oracle; Signed-measure predictor representation; Variation and atomic norms; Gauge-polar inequality; Matching-pursuit iteration; Gauge-controlled matching-pursuit rate; Orthogonal matching-pursuit approximation rate (Exercise 10.7); AdaBoost update; Weak-learnability convergence.
