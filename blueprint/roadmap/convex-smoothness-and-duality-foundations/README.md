---
kind: roadmap
status: mapped
---

# Convex smoothness and duality foundations

Convexity, strong convexity, smoothness, conjugacy, Fenchel-Young inequalities, co-coercivity, and gradient domination.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)
- [Differential and integral calculus](../differential-and-integral-calculus/README.md)

## Candidate contents

- Differentiable convex function
- Jensen inequality
- Strict Jensen equality exercise (Exercise 5.3)
- Convexity closure properties
- Stationary-point global optimality
- Stationary-point identification exercise (Exercise 5.4)
- Quadratic-shift characterization exercise (Exercise 5.5)
- Uniqueness of strongly convex minimizer exercise (Exercise 5.6)
- Strong gradient monotonicity exercise (Exercise 5.7)
- Lojasiewicz gradient-domination lemma
- Smoothness
- Lipschitz-gradient equivalence
- Condition number
- Descent-direction angle exercise (Exercise 5.8)
- Fenchel conjugate
- Smooth-conjugate strong-convexity exercise (Exercise 5.10)
- Fenchel-Young inequality exercise (Exercise 5.11)
- Fenchel-Young residual bound exercise (Exercise 5.11)
- Co-coercivity

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Sections 5.2.2-5.2.4, printed pages 116-125

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ConvexOn`
- `StrongConvexOn`

Primary file: `Mathlib/Analysis/Convex/Strong.lean`.

Convexity and strong convexity are verified; conjugacy, subgradients, smoothness, and co-coercivity need detailed checking.
