---
kind: roadmap
status: mapped
---

# Hoeffding and sub-Gaussian concentration

Bounded-variable, martingale, Laplace-transform, tail, sum, and moment formulations of sub-Gaussian concentration.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Hoeffding Laplace lemma
- One-sided Hoeffding inequality
- Gaussian tail sandwich (Exercise 1.12)
- Two-sided Hoeffding inequality
- Arbitrary-range and heterogeneous-range Hoeffding bounds
- Hoeffding confidence forms
- One-sided confidence bound (Exercise 1.13)
- Azuma inequality (Exercise 1.14)
- Sub-Gaussian definition
- Bounded implies sub-Gaussian
- Sub-Gaussian tail and confidence equivalence
- Gaussian sub-Gaussianity (Exercise 1.15)
- Concentration of sub-Gaussian averages (Exercise 1.16)
- Even-moment bound (Exercise 1.17)
- Moment-bound converse (Exercise 1.18)
- Negative-Laplace bound for nonnegative variables (Exercise 1.19)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.1, printed pages 10-13

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.Kernel.HasSubgaussianMGF`
- `ProbabilityTheory.HasCondSubgaussianMGF`
- `ProbabilityTheory.HasCondSubgaussianMGF.ae_condExp_le`
- `ProbabilityTheory.HasSubgaussianMGF`
- `ProbabilityTheory.HasSubgaussianMGF.measure_ge_le`
- `ProbabilityTheory.HasSubgaussianMGF.neg`
- `ProbabilityTheory.HasSubgaussianMGF.const_mul`
- `ProbabilityTheory.HasSubgaussianMGF.memLp`
- `ProbabilityTheory.HasSubgaussianMGF.sum_of_iIndepFun`
- `ProbabilityTheory.HasSubgaussianMGF.measure_sum_ge_le_of_iIndepFun`
- `ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun`
- `ProbabilityTheory.mgf_le_of_mem_Icc_of_integral_eq_zero`
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero`
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc`
- `ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF`
- `ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF`
- `ProbabilityTheory.mgf_gaussianReal`
- `ProbabilityTheory.mgf_id_gaussianReal`
- `ProbabilityTheory.integrable_exp_mul_gaussianReal`
- `ProbabilityTheory.gaussianReal_map_sub_const`

Primary file: `Mathlib/Probability/Moments/SubGaussian.lean`.

Pinned revision 905b958 provides the MGF predicate, Hoeffding's bounded-variable Laplace lemma, centered bounded-variable sub-Gaussianity, one-sided tails for independent and conditionally sub-Gaussian sums, scaling, negation, and Gaussian MGF identities. The book's bounded-average and two-sided confidence forms require rescaling and union-bound assembly. No exact Gaussian tail sandwich, quantitative even-moment/converse package, negative-Laplace inequality, or conditional bounded-difference Hoeffding lemma was found. Mathlib parameter c corresponds to the book's tau^2.
