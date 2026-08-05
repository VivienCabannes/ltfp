---
kind: roadmap
status: mapped
---

# Multicategory convex surrogates

Convex score-based surrogate losses for multicategory classification, their calibration properties, and their optimization constants.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Classification calibration and surrogate-risk transfer](../classification-calibration-and-surrogate-risk-transfer/README.md)
- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)

## Candidate contents

- Multicategory score vectors and argmax decoding
- One-versus-all convex surrogates
- Sum-over-competitors convex surrogates
- Softmax cross-entropy surrogate
- Multicategory hinge and square surrogates
- Fisher consistency of multicategory surrogates
- Calibration functions for multicategory scores
- Majority-class Fisher consistency of the multicategory hinge (Exercise 13.1)
- One-versus-all surrogate analysis (Exercise 13.2)
- Pairwise surrogate analysis (Exercise 13.3)

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Section 13.1.1 and Exercises 13.1-13.3, printed pages 380-383

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: List.argmax and List.le_of_mem_argmax implement a finite-list argmax, and generic convexity and Bayes-decision primitives exist, but Mathlib has no multicategory score-vector/decoder or surrogate-loss API. Searches for multiclass/multicategory, one-versus-all, pairwise surrogate, softmax/cross-entropy, Fisher consistency, calibration function, and hinge/square-loss terminology found no relevant declarations. Materially uncovered members: Multicategory score vectors and argmax decoding; One-versus-all convex surrogates; Sum-over-competitors convex surrogates; Softmax cross-entropy surrogate; Multicategory hinge and square surrogates; Fisher consistency of multicategory surrogates; Calibration functions for multicategory scores; Majority-class Fisher consistency of the multicategory hinge (Exercise 13.1); One-versus-all surrogate analysis (Exercise 13.2); Pairwise surrogate analysis (Exercise 13.3).
