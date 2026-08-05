---
kind: roadmap
status: detailed
---

# Elementary probability and convexity bounds

Moment identities and basic devices underlying all later concentration arguments.

## Planning status

This milestone is decomposed into 16 reviewed theorem-sized nodes in the current Autoform DAG.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Variance of an independent sample mean
- Mean-square law of large numbers
- Sample-mean central limit theorem
- Markov inequality (Exercise 1.9)
- Chebyshev inequality
- Convergence-in-probability bound
- Countable union bound
- Supremum tail union bound
- Chernoff bound (Exercise 1.10)
- Tail-integral expectation identity (Exercise 1.11)
- Jensen inequality on the real line

## Detailed nodes

- [Variance of a finite sum of pairwise independent random variables](theorems/variance-of-a-finite-sum-of-pairwise-independent-random-variables.md)
- [Variance of an iid sample mean](theorems/variance-of-an-iid-sample-mean.md)
- [Mean-square error identity for an iid sample mean](theorems/mean-square-error-identity-for-an-iid-sample-mean.md)
- [Mean-square convergence of iid sample means](theorems/mean-square-convergence-of-iid-sample-means.md)
- [Finite deviation bound for an iid sample mean](theorems/finite-deviation-bound-for-an-iid-sample-mean.md)
- [Convergence in probability of iid sample means](theorems/convergence-in-probability-of-iid-sample-means.md)
- [Scalar iid central limit theorem](theorems/scalar-iid-central-limit-theorem.md)
- [Threshold indicator bound for Markov's inequality](theorems/threshold-indicator-bound-for-markovs-inequality.md)
- [Markov's inequality](theorems/markovs-inequality.md)
- [Chebyshev's inequality](theorems/chebyshevs-inequality.md)
- [Countable union bound](theorems/countable-union-bound.md)
- [Supremum tail union bound](theorems/supremum-tail-union-bound.md)
- [Chernoff bound](theorems/chernoff-bound.md)
- [Nonnegative tail-integral expectation identity](theorems/nonnegative-tail-integral-expectation-identity.md)
- [Jensen's inequality on the real line](theorems/jensens-inequality-on-the-real-line.md)
- [Pairwise independence on a finite index set](definitions/pairwise-independence-on-a-finite-index-set.md)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2 opening, printed pages 7-10

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.variance_eq_integral`
- `ProbabilityTheory.variance_smul`
- `ProbabilityTheory.IndepFun.variance_sum`
- `ProbabilityTheory.IdentDistrib.variance_eq`
- `ProbabilityTheory.strong_law_Lp`
- `ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub`
- `MeasureTheory.mul_meas_ge_le_integral_of_nonneg`
- `ProbabilityTheory.meas_ge_le_variance_div_sq`
- `MeasureTheory.tendstoInMeasure_of_tendsto_eLpNorm`
- `MeasureTheory.tendstoInMeasure_iff_measureReal_dist`
- `MeasureTheory.measure_iUnion_le`
- `ProbabilityTheory.measure_ge_le_exp_mul_mgf`
- `MeasureTheory.Integrable.integral_eq_integral_meas_lt`
- `ConvexOn.map_integral_le`

Primary file: `Mathlib/Probability/Moments/Variance.lean`.

Pinned Mathlib directly covers Markov, Chebyshev, the sample-mean CLT, a stronger Lp law of large numbers, countable union bounds, generic Chernoff, tail integration, and vector-valued Jensen under explicit hypotheses. Variance scaling, independent-sum variance, and identical-distribution invariance assemble the exact sigma^2/n sample-mean variance; combining this with Chebyshev gives the book's finite convergence-in-probability estimate. The supremum-tail result is a countable-union corollary with nonempty/boundedness conditions, not a dedicated theorem.
