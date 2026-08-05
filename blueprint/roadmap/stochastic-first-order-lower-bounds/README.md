---
kind: roadmap
status: mapped
---

# Stochastic first-order lower bounds

Information-theoretic lower bounds for stochastic-gradient oracles with unbiased bounded gradients.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Entropy, data processing, and Fano inequalities](../entropy-data-processing-and-fano-inequalities/README.md)
- [Relative entropy and Gibbs variational principles](../relative-entropy-and-gibbs-variational-principles/README.md)
- [Minimax reduction and packing](../minimax-reduction-and-packing/README.md)
- [Stochastic gradient descent and generalization](../stochastic-gradient-descent-and-generalization/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)

## Candidate contents

- Stochastic first-order oracle model
- Unbiased bounded stochastic gradients
- Hypercube-indexed convex objective family
- Separation lemma for near-minimizers (Lemma 15.3)
- Bernoulli coordinate oracle construction
- Transcript as a multiple-hypothesis testing experiment
- Mutual-information bound per oracle query
- Adaptive transcript information bound
- Fano lower bound for stochastic optimization
- One-over-square-root-query minimax lower rate
- Matching dependence on gradient bound and domain diameter
- Quadratic stochastic-gradient lower bound (Exercise 15.5)

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Section 15.3, Lemma 15.3, and Exercise 15.5, printed pages 447-449

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: ProbabilityTheory.bernoulliMeasure and integral_bernoulliMeasure provide Bernoulli laws and expectations; KL divergence, generic minimax risk, convexity, and finite-dimensional algebra exist elsewhere. Searches found no stochastic first-order oracle, unbiased-gradient oracle protocol, adaptive transcript, per-query mutual-information theorem, Fano optimization reduction, or stochastic-gradient lower-rate theorem. Materially uncovered members: Stochastic first-order oracle model; Unbiased bounded stochastic gradients; Hypercube-indexed convex objective family; Separation lemma for near-minimizers (Lemma 15.3); Bernoulli coordinate oracle construction; Transcript as a multiple-hypothesis testing experiment; Mutual-information bound per oracle query; Adaptive transcript information bound; Fano lower bound for stochastic optimization; One-over-square-root-query minimax lower rate; Matching dependence on gradient bound and domain diameter; Quadratic stochastic-gradient lower bound (Exercise 15.5).
