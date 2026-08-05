---
kind: roadmap
status: mapped
---

# Structured losses and score decoding

General structured-output prediction, structure-encoding losses, vector score functions, decoding maps, and population calibration criteria.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Loss risk and Bayes decision theory](../loss-risk-and-bayes-decision-theory/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Convex analysis and normed-space geometry](../convex-analysis-and-normed-space-geometry/README.md)
- [Classification calibration and surrogate-risk transfer](../classification-calibration-and-surrogate-risk-transfer/README.md)
- [Fourier analysis and Sobolev approximation](../fourier-analysis-and-sobolev-approximation/README.md)

## Candidate contents

- General structured output space
- Structured loss matrix
- Multicategory zero-one loss as a structure-encoding loss
- Multilabel, ranking, ordinal, and robust-regression examples
- Structure-encoding loss factorization
- Output feature maps and bilinear losses
- Vector-valued score function
- Loss-aware decoding map
- Conditional structured risk
- Fisher consistency of score and decoding pairs
- Structured calibration function
- Comparison inequalities for surrogate excess risk

## Sources

- `sources/ltfp_book.pdf` — Chapter 13, Sections 13.2-13.3, printed pages 387-393

## Mathlib assessment

Legacy assessment: `missing`.

Decision-theory foundations may be reusable, but the structured encoding and decoding interfaces are project-local.
