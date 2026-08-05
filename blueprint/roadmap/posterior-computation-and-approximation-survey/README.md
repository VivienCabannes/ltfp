---
kind: roadmap
status: mapped
---

# Posterior computation and approximation survey

The book's brief survey of exact and approximate posterior-computation strategies; it states method templates rather than convergence or approximation theorems.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Bayesian posterior updating and prediction](../bayesian-posterior-updating-and-prediction/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Conjugate-prior families (survey)
- Laplace approximation around a posterior mode (survey)
- Posterior sampling and Markov-chain Monte Carlo (survey)
- Langevin sampling link (survey)
- Variational posterior approximation (survey)

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.3.1, printed pages 421-422

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib searches found no unified conjugate-prior, Laplace-posterior-approximation, MCMC, Langevin posterior-sampling, or variational-inference API. The source itself only surveys these methods and supplies no convergence, mixing, or approximation-error theorem to formalize here.
