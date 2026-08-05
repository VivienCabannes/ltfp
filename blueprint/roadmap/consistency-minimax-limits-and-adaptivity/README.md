---
kind: roadmap
status: mapped
---

# Consistency, minimax limits, and adaptivity

Criteria for learning over classes of distributions, impossibility without assumptions, and adaptive statistical rates.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Supervised learning setup and evaluation](../supervised-learning-setup-and-evaluation/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Learning rules, capacity, and risk decomposition](../learning-rules-capacity-and-risk-decomposition/README.md)

## Candidate contents

- Sampled dataset law
- Expected-error consistency
- Probably approximately correct guarantee and consistency
- Universal consistency
- Uniform consistency
- Minimax risk
- Upper-bound and lower-bound principles
- Asymptotic and nonasymptotic analysis
- Fixed-sample no-free-lunch theorem
- Arbitrary-slow-convergence theorem
- Lipschitz curse rate
- Smooth-target rate
- Latent-projection rate
- Manifold-dimension adaptivity

## Sources

- `sources/ltfp_book.pdf` — Chapter 2, Sections 2.4-2.6, printed pages 36-40

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.minimaxRisk`
- `ProbabilityTheory.iSup_bayesRisk_le_minimaxRisk`

Primary file: `Mathlib/Probability/Decision/Risk/Defs.lean`.

Pinned Mathlib has a generic kernel-estimation minimax risk and the lower bound by the supremum of Bayes risks. Searches found no learning-theoretic expected/PAC/universal/uniform consistency definitions, sampled-dataset learning asymptotics, no-free-lunch or arbitrary-slow-convergence theorem, or the smoothness/latent/manifold adaptive-rate results. The minimax interface can be reused, but nearly all source-specific content is project-local.
