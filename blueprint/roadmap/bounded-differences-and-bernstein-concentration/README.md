---
kind: roadmap
status: mapped
---

# Bounded differences and Bernstein concentration

Function-level bounded differences and variance-sensitive scalar concentration.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)

## Candidate contents

- Bounded-variation definition
- McDiarmid inequality
- Bounded-difference martingale decomposition
- Conditional Hoeffding lemma
- Vector Hoeffding bound (Exercise 1.20)
- Centered Bernstein Laplace lemma
- Bernstein tail and confidence bounds
- Noncentered Bernstein extension
- Proof of noncentered Bernstein (Exercise 1.21)

## Sources

- `sources/ltfp_book.pdf` — Chapter 1, Sections 1.2.2-1.2.3, printed pages 13-16

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `LipschitzWith`
- `hammingDist`
- `Hamming`
- `MeasureTheory.Martingale`
- `MeasureTheory.martingale_condExp`
- `MeasureTheory.Filtration.natural`
- `ProbabilityTheory.HasCondSubgaussianMGF`
- `ProbabilityTheory.HasCondSubgaussianMGF.ae_condExp_le`
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero`
- `ProbabilityTheory.HasSubgaussianMGF.sum_of_hasCondSubgaussianMGF`
- `ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF`
- `ProbabilityTheory.mgf`
- `ProbabilityTheory.iIndepFun.mgf_sum`
- `ProbabilityTheory.measure_ge_le_exp_mul_mgf`
- `ProbabilityTheory.measure_le_le_exp_mul_mgf`

Primary file: `Mathlib/Probability/Moments/SubGaussian.lean`.

Pinned Mathlib provides Hamming/Lipschitz interfaces, natural filtrations, conditional expectations and martingales, conditional sub-Gaussian predicates, sum composition, and generic Chernoff-MGF bounds. It lacks a coordinatewise bounded-variation API, McDiarmid's inequality, the tailored Doob decomposition and increment bound, a bounded conditional Hoeffding lemma, vector Hoeffding, and centered or noncentered Bernstein/Bennett/subexponential concentration. Supporting files include InformationTheory/Hamming.lean, Probability/Martingale/Basic.lean, Probability/Process/Filtration.lean, and Probability/Moments/Basic.lean.
