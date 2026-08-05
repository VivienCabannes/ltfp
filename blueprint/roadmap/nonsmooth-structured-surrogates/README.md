---
kind: roadmap
status: mapped
---

# Nonsmooth structured surrogates

Structured max-margin and max-min surrogates, their decoding rules, convex programs, and calibration guarantees.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Structured losses and score decoding](../structured-losses-and-score-decoding/README.md)
- [Margin surrogates and support-vector geometry](../margin-surrogates-and-support-vector-geometry/README.md)
- [Nonsmooth subgradient and mirror methods](../nonsmooth-subgradient-and-mirror-methods/README.md)
- [Convex smoothness and duality foundations](../convex-smoothness-and-duality-foundations/README.md)
- [Multicategory convex surrogates](../multicategory-convex-surrogates/README.md)

## Candidate contents

- Structured hinge loss
- Loss-augmented inference
- Structured support-vector-machine objective
- Subgradients of structured hinge losses
- Structured margin constraints
- Max-min structured surrogate
- Max-min conditional optimization problem
- Max-min decoding rule
- Fisher consistency and calibration of max-min surrogates
- Binary max-min specialization (Exercise 13.8)
- Multicategory max-min formulation (Exercise 13.9)

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Section 13.5 and Exercises 13.8-13.9, printed pages 398-402

## Mathlib assessment

Legacy assessment: `missing`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct coverage: none. Assembly-only ingredients: supremum/infimum, generic convexity, finite argmax, and linear-algebra primitives can express pieces of the definitions, but searches for structured hinge, loss-augmented inference, structured SVM, structured margin, and max-min surrogate/calibration found no relevant API. Materially uncovered members: Structured hinge loss; Loss-augmented inference; Structured support-vector-machine objective; Subgradients of structured hinge losses; Structured margin constraints; Max-min structured surrogate; Max-min conditional optimization problem; Max-min decoding rule; Fisher consistency and calibration of max-min surrogates; Binary max-min specialization (Exercise 13.8); Multicategory max-min formulation (Exercise 13.9).
