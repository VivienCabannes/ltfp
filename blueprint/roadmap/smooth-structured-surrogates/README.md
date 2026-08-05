---
kind: roadmap
status: mapped
---

# Smooth structured surrogates

Quadratic and smooth structured surrogates, their calibrated decoding rules, and their reduction to vector-valued regression.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Structured losses and score decoding](../structured-losses-and-score-decoding/README.md)
- [Ordinary least-squares formulation and geometry](../ordinary-least-squares-formulation-and-geometry/README.md)
- [Classification calibration and surrogate-risk transfer](../classification-calibration-and-surrogate-risk-transfer/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [RKHS foundations and representer principles](../rkhs-foundations-and-representer-principles/README.md)
- [Local-averaging estimator constructions](../local-averaging-estimator-constructions/README.md)
- [Kernel ridge covariance theory](../kernel-ridge-covariance-theory/README.md)
- [Gaussian zeroth-order optimization and smoothing](../gaussian-zeroth-order-optimization-and-smoothing/README.md)

## Candidate contents

- Quadratic structured surrogate
- Conditional surrogate minimizer
- Quadratic-surrogate Fisher consistency
- Square-root calibration inequality
- Observation-linear vector-valued estimators
- Local-averaging vector-valued estimator
- Decoding from conditional mean embeddings
- Kernelized vector-valued estimator
- General smooth convex structured surrogate
- Fenchel-dual score representation
- Smooth-surrogate calibration bound
- Softmax calibration function (Exercise 13.6)
- Reduction to binary calibration problems (Exercise 13.7)
- Perturb-and-MAP stochastic smoothing

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Section 13.4 and Exercises 13.6-13.7, printed pages 393-398

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: Mathlib has RKHS kernels, least-squares, integration, Gaussian measures, and generic convexity/calculus, but searches found no structured surrogate, conditional-mean embedding decoder, vector-valued regression reduction, structured calibration, Fenchel score representation, or perturb-and-MAP smoothing API. Materially uncovered members: Quadratic structured surrogate; Conditional surrogate minimizer; Quadratic-surrogate Fisher consistency; Square-root calibration inequality; Observation-linear vector-valued estimators; Local-averaging vector-valued estimator; Decoding from conditional mean embeddings; Kernelized vector-valued estimator; General smooth convex structured surrogate; Fenchel-dual score representation; Smooth-surrogate calibration bound; Softmax calibration function (Exercise 13.6); Reduction to binary calibration problems (Exercise 13.7); Perturb-and-MAP stochastic smoothing.
