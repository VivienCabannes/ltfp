---
kind: roadmap
status: mapped
---

# Lasso geometry and optimization

Sparsity-inducing l1 geometry, variational identities, optimality conditions, and algorithms for regularized least squares.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Proximal, projected, and composite gradient methods](../proximal-projected-and-composite-gradient-methods/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)

## Candidate contents

- Lasso objective
- l1 norm as a convex relaxation of l0
- Soft-thresholding formula
- Proximal soft-thresholding
- Coordinate descent
- Coordinate update (Exercise 8.5)
- Eta trick
- Reweighted l2 minimization
- Directional and KKT optimality conditions
- Homotopy and piecewise-affine regularization path
- Zero Lasso solution (Exercise 8.6)

## Sources

- `sources/ltfp_book.pdf` — Chapter 8, Section 8.3.1, printed pages 231-234

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: generic convex, proximal, positive-part, and subgradient APIs provide background only; Mathlib/Analysis/Calculus/LagrangeMultipliers.lean explicitly leaves KKT formalization as a TODO. Searches for Lasso, soft thresholding, coordinate descent, reweighted l2, KKT conditions, homotopy, and regularization paths found no member-level implementation. Materially uncovered members: Lasso objective; l1 norm as a convex relaxation of l0; Soft-thresholding formula; Proximal soft-thresholding; Coordinate descent; Coordinate update (Exercise 8.5); Eta trick; Reweighted l2 minimization; Directional and KKT optimality conditions; Homotopy and piecewise-affine regularization path; Zero Lasso solution (Exercise 8.6).
