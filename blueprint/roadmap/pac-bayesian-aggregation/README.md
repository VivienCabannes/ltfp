---
kind: roadmap
status: mapped
---

# PAC-Bayesian aggregation

PAC-Bayesian risk bounds for randomized and averaged predictors, with KL regularization and Gibbs-posterior aggregation.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Relative entropy and Gibbs variational principles](../relative-entropy-and-gibbs-variational-principles/README.md)
- [Combinatorial sparse model selection](../combinatorial-sparse-model-selection/README.md)

## Candidate contents

- Prior and data-dependent posterior over predictors
- Integrated expected and empirical risks
- Randomized Gibbs predictor
- Posterior-mean predictor
- Exponentially weighted Gibbs posterior
- Bounded-loss exponential-moment inequality
- PAC-Bayesian expected-risk bound
- PAC-Bayesian high-probability bound
- KL complexity penalty
- Temperature optimization
- Jensen transfer to posterior means
- Sparse-regression PAC-Bayes specialization

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.4, printed pages 423-426

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `MeasureTheory.Measure.tilted`
- `MeasureTheory.isProbabilityMeasure_tilted`
- `InformationTheory.klDiv`
- `InformationTheory.klDiv_eq_zero_iff`
- `ProbabilityTheory.mgf_le_of_mem_Icc_of_integral_eq_zero`
- `ProbabilityTheory.hasSubgaussianMGF_of_mem_Icc_of_integral_eq_zero`

Primary file: `Mathlib/MeasureTheory/Measure/Tilted.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: MeasureTheory.Measure.tilted is exactly a normalized exponential tilt and can instantiate the exponentially weighted Gibbs posterior after supplying the empirical-risk exponent; isProbabilityMeasure_tilted proves normalization under integrability. InformationTheory.klDiv supplies the KL term, while the two SubGaussian declarations prove the centered bounded-variable exponential-moment/Hoeffding ingredient. Supporting files are Mathlib/InformationTheory/KullbackLeibler/Basic.lean and Mathlib/Probability/Moments/SubGaussian.lean. No PAC-Bayesian learning-bound API was found. The required Donsker-Varadhan theorem is owned by the dependency Relative entropy and Gibbs variational principles rather than duplicated in this cluster. Materially uncovered members: Prior and data-dependent posterior over predictors as a learning interface; Integrated expected and empirical risks; Randomized Gibbs predictor; Posterior-mean predictor; PAC-Bayesian expected-risk bound; PAC-Bayesian high-probability bound; KL complexity penalty as part of either bound; Temperature optimization; Jensen transfer to posterior means; Sparse-regression PAC-Bayes specialization.
