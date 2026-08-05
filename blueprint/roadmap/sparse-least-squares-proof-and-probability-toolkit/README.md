---
kind: roadmap
status: mapped
---

# Sparse least-squares proof and probability toolkit

Constrained least-squares comparison and Gaussian maximum estimates used throughout sparse model selection.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Fixed-design ordinary least-squares statistics](../fixed-design-ordinary-least-squares-statistics/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)
- [Maxima and smooth-sum expectation bounds](../maxima-and-smooth-sum-expectation-bounds/README.md)
- [Finite-dimensional linear algebra and spectral theory](../finite-dimensional-linear-algebra-and-spectral-theory/README.md)

## Candidate contents

- Sparse fixed-design regression setup
- Constrained least-squares basic inequality
- Supremum comparison inequality
- Ordinary least-squares projection consequence
- Gaussian squared-norm moment-generating function
- Exponential maximum inequality
- Gaussian projection maximum bound
- Subset-count bound
- Chi-squared concentration (Exercise 8.1)

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Sections 8.1-8.1.2, printed pages 221-225

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Nat.choose_le_pow_div`
- `Nat.choose_le_pow`

Primary file: `Mathlib/Data/Nat/Choose/Bounds.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Directly covered: Subset-count bound. Nat.choose_le_pow_div proves the standard binomial-coefficient bound by a power divided by a factorial, and Nat.choose_le_pow gives the coarser power bound. Assembly-only ingredients: Mathlib/Probability/Moments/SubGaussian.lean supplies scalar sub-Gaussian MGF and tail APIs, and the inner-product-space library supplies orthogonal projections; neither yields the listed vector Gaussian squared-norm, projection-maximum, or chi-squared statements. Materially uncovered members: Sparse fixed-design regression setup; Constrained least-squares basic inequality; Supremum comparison inequality; Ordinary least-squares projection consequence; Gaussian squared-norm moment-generating function; Exponential maximum inequality; Gaussian projection maximum bound; Chi-squared concentration (Exercise 8.1).
