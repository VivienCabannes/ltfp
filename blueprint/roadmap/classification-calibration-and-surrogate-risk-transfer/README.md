---
kind: roadmap
status: mapped
---

# Classification calibration and surrogate-risk transfer

Qualitative and quantitative criteria that transfer excess convex-surrogate risk into excess zero-one risk.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Conditional Phi-risk
- Conditional zero-one risk
- Classification calibration
- Fisher consistency
- Differentiability-at-zero calibration criterion
- Conditional excess zero-one formula
- Calibration-function inequality
- Square-loss square-root transfer
- Smooth-surrogate square-root transfer
- Hinge-loss identity transfer
- Fenchel-conjugate calibration exercise (Exercise 4.1)
- General convex calibration transform exercise (Exercise 4.2)
- Low-noise linear calibration exercise (Exercise 4.3)
- Surrogate-dependent optimal score functions
- Logistic Gaussian discriminant exercise (Exercise 4.4)
- Multicategory discriminant extension exercise (Exercise 4.4)

## Sources

- `sources/ltfp_book.pdf` — Chapter 4, Sections 4.1.3-4.1.4, printed pages 76-83

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Searches using the node title, description, and every provisional-member phrase found no member-level declaration. Direct coverage: none. Assembly-only ingredients: generic probability, convexity, calculus, matrix, metric, or finite-sum prerequisites named by this node exist elsewhere in Mathlib, but they do not implement any listed member. Materially uncovered members: Conditional Phi-risk; Conditional zero-one risk; Classification calibration; Fisher consistency; Differentiability-at-zero calibration criterion; Conditional excess zero-one formula; Calibration-function inequality; Square-loss square-root transfer; Smooth-surrogate square-root transfer; Hinge-loss identity transfer; Fenchel-conjugate calibration exercise; General convex calibration transform exercise; Low-noise linear calibration exercise; Surrogate-dependent optimal score functions; Logistic Gaussian discriminant exercise; Multicategory discriminant extension exercise.
