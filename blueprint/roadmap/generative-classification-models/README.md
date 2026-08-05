---
kind: roadmap
status: mapped
---

# Generative classification models

Generative multicategory models and their discriminative decision rules, including linear and quadratic discriminant analysis and naive Bayes.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Likelihood and prior modeling foundations](../likelihood-and-prior-modeling-foundations/README.md)
- [Multicategory convex surrogates](../multicategory-convex-surrogates/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Class-prior and class-conditional factorization
- Bayes classifier from a generative model
- Gaussian class-conditionals with shared covariance
- Linear discriminant analysis score
- Equivalence of LDA posterior scores and softmax regression
- Maximum-likelihood LDA parameters (Exercise 14.12)
- Class-specific covariance model
- Quadratic discriminant analysis (Exercise 14.13)
- Naive-Bayes conditional-independence model
- Naive-Bayes likelihood and classifier
- Generative versus discriminative population criteria
- Maximum-likelihood parameter estimation

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.2 and Exercises 14.12-14.13, printed pages 417-420

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.Measure.compProd`
- `ProbabilityTheory.posterior`
- `ProbabilityTheory.compProd_posterior_eq_map_swap`
- `ProbabilityTheory.multivariateGaussian`
- `ProbabilityTheory.iIndepFun`

Primary file: `Mathlib/Probability/Kernel/Composition/MeasureCompProd.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: ProbabilityTheory.Measure.compProd constructs a joint law from a class-prior measure and class-conditional kernel; posterior and compProd_posterior_eq_map_swap provide the generic reverse conditioning; multivariateGaussian supplies Gaussian class-conditional measures; iIndepFun supplies the independence predicate needed to state a naive-Bayes factorization. Supporting files are Mathlib/Probability/Kernel/Posterior.lean, Mathlib/Probability/Distributions/Gaussian/Multivariate.lean, and Mathlib/Probability/Independence/Basic.lean. No classification-model, maximum-likelihood, softmax, LDA, QDA, or naive-Bayes theorem was found. Materially uncovered members: Bayes classifier from a generative model; Gaussian class-conditionals with shared covariance as a class-indexed model; Linear discriminant analysis score; Equivalence of LDA posterior scores and softmax regression; Maximum-likelihood LDA parameters (Exercise 14.12); Class-specific covariance model; Quadratic discriminant analysis (Exercise 14.13); Naive-Bayes conditional-independence model beyond the generic predicate; Naive-Bayes likelihood and classifier; Generative versus discriminative population criteria; Maximum-likelihood parameter estimation.
