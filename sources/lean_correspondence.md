# Lean Correspondence

This file records which Lean declaration discharges which tier-2 graph node. The graph schema in
`graph.json` is closed and has no field for project declarations, and `sources/phase2_content_scope.json`
fingerprints the reviewed node records and prose byte for byte, so this correspondence is tracked
here instead of in the graph.

A node listed in one of the per-module tables below is *formalized*: the Lean statement transcribes
the reviewed statement in the node's `content` file, the declaration compiles on the pinned
toolchain, and its axiom set is exactly `[propext, Classical.choice, Quot.sound]`. It is not a claim
that an independent human review has taken place; see `formalization.yaml`. The closing sections
list nodes that are deliberately *not* formalized here because pinned Mathlib already proves them.

Environment: Lean `v4.32.2`, Mathlib `v4.32.2` at commit
`905b95818eb32af7874a58b427f50c1711a5e96c`.

Every module listed below lives under `LearningTheoryFromFirstPrinciples/Mathlib/`, the folder
reserved for declarations missing from the pinned Mathlib checkout, and is therefore a candidate for
upstreaming.

## Deterministic quadrature error

Module `Mathlib/MeasureTheory/Integral/IntervalIntegral/AffineInterpolation.lean`:

| Tier-2 node | Lean declarations |
| --- | --- |
| Affine panel interpolant | `affinePanelInterp`, `affinePanelInterp_apply`, `affinePanelInterp_eq_of_ne`, `affinePanelInterp_left`, `affinePanelInterp_right`, `affinePanelInterp_self`, `affinePanelInterp_self_eq_const`, `affinePanelInterp_zero_one` |
| Affine panel integral identity | `integral_affinePanelInterp`, `integral_affinePanelInterp_eq_trapezoidal_integral_one`, `integral_affinePanelInterp_zero_one`, `continuous_affinePanelInterp`, `intervalIntegrable_affinePanelInterp` |
| Piecewise-affine integral identity | `sum_integral_affinePanelInterp`, `trapezoidal_uniform_grid_last_point` |
| Exact trapezoidal error decomposition | `integral_sub_trapezoidal_integral_eq_sum_panel_error`, `integral_sub_trapezoidal_integral_eq_sum_integral_residual`, `trapezoidal_error_eq_neg_sum_integral_residual`, `abs_trapezoidal_error_eq_abs_sum_integral_residual`, `IntervalIntegrable.uniform_grid_panel` |

Module `Mathlib/MeasureTheory/Integral/IntervalIntegral/AffineInterpolationError.lean`:

| Tier-2 node | Lean declarations |
| --- | --- |
| Affine interpolation local error (Exercise 1.26) | `abs_sub_affinePanelInterp_le`, `abs_sub_affinePanelInterp_le_unitInterval`, `exists_sub_affinePanelInterp_eq`, `hasDerivAt_affinePanelInterp` |

Module `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalFirstDerivRate.lean`:

| Tier-2 node | Lean declarations |
| --- | --- |
| First-derivative error rate (Exercise 1.27) | `abs_trapezoidal_error_le_of_deriv_bound`, `abs_trapezoidal_integral_sub_integral_le_of_deriv_bound`, `abs_trapezoidal_integral_sub_integral_unitInterval_le_of_deriv_bound`, `isBigO_trapezoidal_error_of_deriv_bound` |

Module `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalBernoulliKernel.lean`:

| Tier-2 node | Lean declarations |
| --- | --- |
| Periodic Bernoulli-kernel trapezoidal identity | `trapezoidal_error_eq_bernoulli_kernel` |

Module `Mathlib/MeasureTheory/Integral/IntervalIntegral/TrapezoidalPeriodicRate.lean`:

| Tier-2 node | Lean declarations |
| --- | --- |
| Periodic smooth-function error rate (Exercise 1.28) | `trapezoidalPeriodicConst`, `trapezoidalPeriodicConst_one`, `abs_trapezoidal_error_le_of_periodic`, `isBigO_trapezoidal_error_of_periodic` |

## Elementary probability and convexity bounds

Module `Mathlib/Probability/SampleMean.lean` (namespace `ProbabilityTheory`):

| Tier-2 node | Lean declarations |
| --- | --- |
| Variance of an iid sample mean | `variance_sampleMean`, with `sampleMean`, `sampleMean_eq_smul_sum`, `memLp_sampleMean` |
| Mean-square error identity for an iid sample mean | `integral_sampleMean_sub_integral_sq`, with `integral_sampleMean` |
| Finite deviation bound for an iid sample mean | `measureReal_abs_sampleMean_sub_integral_gt_le`, with the closed-threshold `measureReal_abs_sampleMean_sub_integral_ge_le` |
| Convergence in probability of iid sample means | `tendstoInMeasure_sampleMean` |

Module `Mathlib/Probability/TailBound.lean` (namespace `MeasureTheory`):

| Tier-2 node | Lean declarations |
| --- | --- |
| Threshold indicator bound for Markov's inequality | `ae_mul_indicator_lt_le_of_ae_nonneg`, with the general `ae_mul_indicator_le_of_ae_nonneg` |
| Supremum tail union bound | `measure_lt_sSup_range_le_tsum'`, with the general `measure_lt_sSup_range_le_tsum` |

## Neighbouring nodes that pinned Mathlib already proves

Two `in-mathlib` tier-2 nodes sit directly next to the sample-mean statements above and are
therefore worth naming, so that a reader does not look for a project declaration that should not
exist:

| Tier-2 node | Pinned Mathlib declaration | Used by this project |
| --- | --- | --- |
| Variance of a finite sum of pairwise independent random variables | `ProbabilityTheory.IndepFun.variance_sum` | yes, in `variance_sampleMean` |
| Mean-square convergence of iid sample means | `ProbabilityTheory.strong_law_Lp` | no; the node needs no project declaration, and `tendstoInMeasure_sampleMean` deliberately follows the book's Chebyshev route instead |

## Coverage

The seven content-complete clusters contain 111 tier-2 nodes. Of these, 97 are `in-mathlib` and need
no project declaration; the other 14 are exactly the `partial` and `missing` nodes, and they are
exactly the 14 nodes tabulated above. The other 109 tier-1 clusters of the graph have no tier-2
children yet, so no statement of theirs is formalized.

## Statement conventions

* Where the reviewed statement is the source-facing one and the compiled argument proves something
  stronger, both are recorded: the general lemma and the exact source-facing statement derived from
  it. This applies to the two tail bounds and to the closed-threshold Chebyshev bound.
* Hypotheses that the source lists but the Lean proof does not consume are kept and their binders
  are underscore-prefixed, so the transcription stays complete without disabling a linter.
* Mathlib's `trapezoidal_error` is the estimator minus the integral, the opposite orientation to the
  book's error. Both signed forms are recorded where relevant; the absolute errors agree.
