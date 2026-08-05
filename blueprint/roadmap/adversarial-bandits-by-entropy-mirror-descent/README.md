---
kind: roadmap
status: mapped
---

# Adversarial bandits by entropy mirror descent

Hedge handles full feedback, while an importance-weighted estimator and entropy mirror descent yield the Exp3 bandit algorithm and regret bound.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Mirror descent geometry](../mirror-descent-geometry/README.md)
- [Stochastic multiarmed bandits](../stochastic-multiarmed-bandits/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Adversarial-bandit regret
- Deterministic-policy impossibility
- Hedge algorithm and regret
- Importance-weighted reward estimator
- Simplex entropy mirror bound
- Exp3 algorithm
- Exp3 regret bound

## Sources

- `sources/ltfp_book.pdf` — Chapter 11, Section 11.3.4, printed pages 339-341

## Mathlib assessment

Legacy assessment: `missing`.

Pinned-checkout searches found no adversarial-bandit regret, deterministic-policy lower bound, Hedge, importance-weighted reward estimator, Exp3, or associated regret theorem. Simplex and scalar entropy primitives exist, but none of the seven bandit or multiplicative-update members is directly present.
