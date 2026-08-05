---
kind: roadmap
status: mapped
---

# Bayesian regression lower bounds

Bayes-risk reductions yielding minimax lower bounds for dense and sparse Gaussian regression models.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Consistency, minimax limits, and adaptivity](../consistency-minimax-limits-and-adaptivity/README.md)
- [Bayesian minimax lower bound for fixed design](../bayesian-minimax-lower-bound-for-fixed-design/README.md)
- [Posterior mean and posterior mode](../posterior-mean-and-posterior-mode/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Combinatorial sparse model selection](../combinatorial-sparse-model-selection/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Supremum risk lower-bounded by Bayes risk
- Rademacher-prior dense regression lower bound
- Posterior-variance expression for Bayes risk
- Gaussian-tail testing lower bound
- Block sparse prior construction
- Sparse regression Bayes lower rate
- Comparison of Bayesian and Fano lower-bound methods

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Section 15.1.6, printed pages 438-441

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.minimaxRisk`
- `ProbabilityTheory.bayesRisk`
- `ProbabilityTheory.bayesRisk_le_minimaxRisk`
- `ProbabilityTheory.iSup_bayesRisk_le_minimaxRisk`
- `ProbabilityTheory.multivariateGaussian`

Primary file: `Mathlib/Probability/Decision/Risk/Basic.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: ProbabilityTheory.bayesRisk_le_minimaxRisk and iSup_bayesRisk_le_minimaxRisk formalize the generic supremum-risk/Bayes-risk reduction, with minimaxRisk and bayesRisk providing the two risk notions; multivariateGaussian supplies the Gaussian-prior substrate. No regression-specific prior, conjugate posterior variance, Gaussian testing calculation, block-sparse Bayes construction, or quantitative regression lower rate was found. Materially uncovered members: Rademacher-prior dense regression lower bound; Posterior-variance expression for Bayes risk; Gaussian-tail testing lower bound; Block sparse prior construction; Sparse regression Bayes lower rate; Comparison of Bayesian and Fano lower-bound methods.
