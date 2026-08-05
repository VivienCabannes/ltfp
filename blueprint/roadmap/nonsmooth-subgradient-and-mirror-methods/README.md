---
kind: roadmap
status: mapped
---

# Nonsmooth subgradient and mirror methods

Subgradient, projection, averaging, doubling, Bregman, and mirror-descent methods for convex Lipschitz objectives.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Gradient descent on quadratic objectives](../gradient-descent-on-quadratic-objectives/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Linear and regularized predictor generalization](../linear-and-regularized-predictor-generalization/README.md)

## Candidate contents

- Lipschitz-continuous objective
- Bounded-gradient equivalence exercise (Exercise 5.18)
- Subdifferential
- Subgradient method
- Absolute-value and hinge subdifferentials exercise (Exercise 5.19)
- Subgradient convergence theorem
- Normalized subgradient exercise (Exercise 5.20)
- Projection contractivity exercise (Exercise 5.21)
- Projected subgradient convergence exercise (Exercise 5.21)
- Bregman divergence (Exercise 5.22)
- Mirror-descent update exercise (Exercise 5.22)
- Entropy mirror map and multiplicative update exercise (Exercise 5.22)
- Averaged projected-subgradient exercise (Exercise 5.23)
- Fixed-horizon subgradient bound
- Doubling-trick exercise (Exercise 5.24)
- Logistic and support-vector constants exercise (Exercise 5.25)
- Optimization-generalization iteration comparison

## Sources

- `sources/ltfp_book.pdf` — Chapter 5, Section 5.3, printed pages 130-134

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `LipschitzWith`
- `lipschitzWith_of_nnnorm_fderiv_le`
- `norm_fderiv_le_of_lipschitz`
- `Submodule.lipschitzWith_orthogonalProjectionOnto`

Primary file: `Mathlib/Topology/EMetricSpace/Lipschitz.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: Lipschitz-continuous objective; Bounded-gradient equivalence exercise. Assembly ingredients and limits: LipschitzWith is exact, and the fderiv lemmas give the differentiable bounded-gradient equivalence under their hypotheses. Submodule.lipschitzWith_orthogonalProjectionOnto proves contractivity only for projection onto a closed subspace, not an arbitrary closed convex set. No subdifferential, subgradient algorithm, Bregman divergence, mirror-descent, or convergence-rate API was found. Supporting files are Mathlib/Analysis/Calculus/MeanValue.lean, Mathlib/Analysis/Calculus/FDeriv/Basic.lean, and Mathlib/Analysis/InnerProductSpace/Projection/Basic.lean. Materially uncovered members: Subdifferential; Subgradient method; Absolute-value and hinge subdifferentials exercise; Subgradient convergence theorem; Normalized subgradient exercise; Projection contractivity exercise; Projected subgradient convergence exercise; Bregman divergence; Mirror-descent update exercise; Entropy mirror map and multiplicative update exercise; Averaged projected-subgradient exercise; Fixed-horizon subgradient bound; Doubling-trick exercise; Logistic and support-vector constants exercise; Optimization-generalization iteration comparison.
