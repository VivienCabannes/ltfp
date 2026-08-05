---
kind: roadmap
status: mapped
---

# Likelihood and prior modeling foundations

Parameterized joint and conditional probability models, iid likelihoods, maximum-likelihood estimation, and prior distributions used by the book's statistical examples.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Learning rules, capacity, and risk decomposition](../learning-rules-capacity-and-risk-decomposition/README.md)

## Candidate contents

- Parameterized joint probability model
- Parameterized conditional probability model
- Likelihood of an observed sample
- Conditional likelihood
- Iid product likelihood
- Maximum-likelihood estimator
- Prior distribution and prior density

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.1 opening, printed pages 409-410
- `sources/ltfp_book.pdf` — Chapter 14, Section 14.3 opening, printed pages 420-421

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.HasLaw`
- `ProbabilityTheory.iIndepFun`
- `MeasureTheory.Measure.rnDeriv`

Primary file: `Mathlib/MeasureTheory/Measure/Decomposition/Lebesgue.lean`.

Pinned Mathlib provides laws, independence, and Radon-Nikodym derivatives from which dominated iid models can be built. No generic parameterized likelihood, conditional-likelihood, or maximum-likelihood-estimator API was found, so those interfaces remain project-local.
