---
kind: roadmap
status: mapped
---

# Deterministic convex optimization lower bounds

Oracle lower bounds for deterministic first-order optimization of Lipschitz, smooth, and strongly convex objectives.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Smooth convex gradient-descent rates](../smooth-convex-gradient-descent-rates/README.md)
- [Nesterov acceleration and momentum methods](../nesterov-acceleration-and-momentum-methods/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)

## Candidate contents

- Deterministic first-order oracle model
- Linear-span restriction on iterates
- Adversarial chain objective
- Support-growth lemma for oracle iterates
- Nonsmooth convex one-over-square-root-iteration lower bound
- Smooth convex one-over-iteration-squared lower bound
- Strongly convex exponential lower bound
- Dimension and iteration restrictions
- Matching accelerated-gradient dependence

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Section 15.2.1, printed pages 441-443

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: convexity, strong convexity, differentiability, Lipschitz maps, finite-dimensional spans, and spectral linear algebra exist, but searches for first-order oracle, oracle complexity/lower bound, resisting oracle, adversarial or zero-chain objective, support-growth lemma, Nesterov lower bound, and iteration lower bound found no relevant API. Materially uncovered members: Deterministic first-order oracle model; Linear-span restriction on iterates; Adversarial chain objective; Support-growth lemma for oracle iterates; Nonsmooth convex one-over-square-root-iteration lower bound; Smooth convex one-over-iteration-squared lower bound; Strongly convex exponential lower bound; Dimension and iteration restrictions; Matching accelerated-gradient dependence.
