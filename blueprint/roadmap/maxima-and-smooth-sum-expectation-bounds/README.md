---
kind: roadmap
status: mapped
---

# Maxima and smooth-sum expectation bounds

Logarithmic maxima bounds and expectation control for smooth convex functions of independent sums.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)

## Candidate contents

- Expected sub-Gaussian maximum
- Maximum tail union bound
- Expected absolute maximum (Exercise 1.22)
- Gaussian maximum lower bound (Exercise 1.23)
- Weighted simultaneous confidence and penalized-selection bound (Exercise 1.24)
- Norm-relative smoothness definition
- Smooth convex independent-sum bound (Exercise 1.25)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.4, printed pages 16-18

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.HasSubgaussianMGF`
- `ProbabilityTheory.HasSubgaussianMGF.cgf_le`
- `ProbabilityTheory.HasSubgaussianMGF.measure_ge_le`
- `ProbabilityTheory.HasSubgaussianMGF.neg`
- `MeasureTheory.measure_iUnion_fintype_le`
- `MeasureTheory.Integrable.integral_eq_integral_meas_lt`
- `ProbabilityTheory.gaussianReal`
- `ProbabilityTheory.mgf_gaussianReal`
- `ConvexOn`
- `ContDiff`
- `StrongConcaveOn`
- `strongConcaveOn_iff_convex`
- `ProbabilityTheory.iIndepFun.indepFun_finsetSum_of_notMem₀`
- `ProbabilityTheory.IndepFun.integral_bilin_comp_comp`
- `ConvexOn.map_integral_le`

Primary file: `Mathlib/Probability/Moments/SubGaussian.lean`.

Pinned revision 905b958 provides centered sub-Gaussian MGF, CGF, and one-sided tail APIs; finite/countable set union bounds; the layer-cake tail-integral formula; Gaussian measures and MGFs; convexity, C1 calculus, and a chordal strong-concavity/semiconcavity surrogate; and independence plus bilinear-expectation factorization for partial sums. MeasureTheory.measure_iUnion_fintype_le covers the maximum tail union bound after rewriting the maximum event as a finite union. Uncovered as dedicated statements are: Expected sub-Gaussian maximum; Expected absolute maximum (Exercise 1.22); Gaussian maximum lower bound (Exercise 1.23); Weighted simultaneous confidence and penalized-selection bound (Exercise 1.24); Norm-relative smoothness definition; and Smooth convex independent-sum bound (Exercise 1.25). These require assembly or new theorems. StrongConcaveOn with negative modulus is related to the book's upper quadratic smoothness condition, but Mathlib/Analysis/Convex/Strong.lean explicitly leaves derivative properties as TODO, so no verified equivalence was found. Material ambiguity: Exercise 1.24 permits zero weights although its Real.log(1 / pi_i) penalty is not the intended extended-real infinity at pi_i = 0; a formal statement should require positive weights or use an extended-real penalty.
